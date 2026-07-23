from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "skills/find-china-cdc-health-report/scripts/fetch_report.py"
)
SPEC = importlib.util.spec_from_file_location("fetch_report", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


def query(report_type: str, action: str = "extract") -> dict:
    return {
        "report_type": report_type,
        "latest": True,
        "year": None,
        "week": None,
        "month": None,
        "issue": None,
        "action": action,
    }


def report(report_type: str, content_mode: str) -> dict:
    weekly = report_type in {"influenza_weekly", "respiratory_weekly"}
    issue = 917 if report_type == "influenza_weekly" else None
    period = {"year": 2026, "week": 28 if weekly else None, "month": None if weekly else 6}
    if weekly:
        identifier = f"{report_type}-2026-W28-I{issue if issue is not None else 'NA'}"
    else:
        identifier = f"{report_type}-2026-M06-INA"
    has_detail = content_mode != "pdf"
    has_document = content_mode != "html"
    return {
        "report_id": identifier,
        "report_type": report_type,
        "title": f"fixture {report_type}",
        "reporting_period": period,
        "issue_number": issue,
        "publish_date": "2026-07-16",
        "content_mode": content_mode,
        "detail_url": "https://www.chinacdc.cn/detail.html" if has_detail else None,
        "document_url": "https://www.chinacdc.cn/report.pdf" if has_document else None,
        "source_page_url": "https://www.chinacdc.cn/index.html",
    }


def valid_html_payload(report_value: dict, detail: dict) -> dict:
    return {
        "schema_version": "2.0",
        "report": report_value,
        "pages": [],
        "content": {"text": detail["text"], "tables": [], "images": []},
        "vision_pages": [],
        "warnings": [],
    }


def valid_pdf_payload(report_value: dict, _path: Path) -> dict:
    return {
        "schema_version": "2.0",
        "report": report_value,
        "pages": [
            {
                "page": 1,
                "text": "fixture",
                "tables": [],
                "visuals": [],
                "requires_vision": False,
            }
        ],
        "content": None,
        "vision_pages": [],
        "warnings": [],
    }


class FetchReportPipelineTests(unittest.TestCase):
    def test_html_extract_skips_downloader_and_writes_one_artifact(self):
        current = report("covid_monthly", "html")
        detail = {"text": "verified HTML body"}

        def fail_downloader(*_args):
            raise AssertionError("HTML extraction must not invoke the PDF downloader")

        with tempfile.TemporaryDirectory() as directory:
            result = MODULE.run_pipeline(
                query("covid_monthly"),
                artifact_root=Path(directory),
                locator=lambda _query: (current, detail),
                downloader=fail_downloader,
                html_extract=valid_html_payload,
            )
            artifact = Path(result["artifact"])
            self.assertTrue(artifact.is_file())
            self.assertEqual([path.name for path in artifact.parent.iterdir()], ["extracted.json"])
            payload = json.loads(artifact.read_text(encoding="utf-8"))
            self.assertEqual(payload["content"]["text"], "verified HTML body")

    def test_html_with_pdf_extract_uses_temporary_download_and_cleans_it(self):
        current = report("influenza_weekly", "html_with_pdf")
        temporary_directories: list[Path] = []

        def fake_downloader(_report, _adapter, output_dir):
            temporary_directories.append(output_dir)
            pdf = output_dir / "verified.pdf"
            pdf.write_bytes(b"%PDF-1.7\nfixture")
            return {"path": str(pdf), "reused": False}

        def fake_pdf_extract(report_value, pdf_path):
            self.assertTrue(pdf_path.is_file())
            return valid_pdf_payload(report_value, pdf_path)

        with tempfile.TemporaryDirectory() as directory:
            result = MODULE.run_pipeline(
                query("influenza_weekly"),
                artifact_root=Path(directory),
                locator=lambda _query: (current, {"text": "detail"}),
                downloader=fake_downloader,
                pdf_extract=fake_pdf_extract,
            )
            self.assertTrue(Path(result["artifact"]).is_file())
            self.assertEqual(len(temporary_directories), 1)
            self.assertFalse(temporary_directories[0].exists())

    def test_direct_pdf_extract_does_not_require_detail_content(self):
        current = report("global_infectious_risk_monthly", "pdf")

        def fake_downloader(report_value, _adapter, output_dir):
            self.assertIsNone(report_value["detail_url"])
            pdf = output_dir / "verified.pdf"
            pdf.write_bytes(b"%PDF-1.7\nfixture")
            return {"path": str(pdf), "reused": False}

        with tempfile.TemporaryDirectory() as directory:
            result = MODULE.run_pipeline(
                query("global_infectious_risk_monthly"),
                artifact_root=Path(directory),
                locator=lambda _query: (current, None),
                downloader=fake_downloader,
                pdf_extract=valid_pdf_payload,
            )
            payload = json.loads(Path(result["artifact"]).read_text(encoding="utf-8"))
            self.assertEqual(payload["report"]["content_mode"], "pdf")
            self.assertIsNone(payload["report"]["detail_url"])

    def test_valid_cached_extract_skips_downloader_and_extractor(self):
        current = report("influenza_weekly", "html_with_pdf")

        with tempfile.TemporaryDirectory() as directory:
            artifact = Path(directory) / current["report_id"] / "extracted.json"
            MODULE.atomic_write_json(artifact, valid_pdf_payload(current, Path("unused")))

            def fail(*_args):
                raise AssertionError("cache hit must skip downstream processing")

            result = MODULE.run_pipeline(
                query("influenza_weekly"),
                artifact_root=Path(directory),
                locator=lambda _query: (current, {"text": "detail"}),
                downloader=fail,
                pdf_extract=fail,
            )
            self.assertTrue(result["cache_hit"])
            self.assertEqual(Path(result["artifact"]).resolve(), artifact.resolve())

    def test_download_is_rejected_for_html_only_report(self):
        current = report("respiratory_weekly", "html")
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(MODULE.PipelineError, "has no PDF"):
                MODULE.run_pipeline(
                    query("respiratory_weekly", action="download"),
                    artifact_root=Path(directory),
                    locator=lambda _query: (current, {"text": "detail"}),
                )


class FetchReportQueryTests(unittest.TestCase):
    def test_list_parser_separates_date_appended_to_link_text(self):
        page = {
            "url": "https://www.chinacdc.cn/jksj/jksj04_14249/",
            "links": [
                {
                    "text": "2026年第28周第917期中国流感监测周报 2026-07-16",
                    "href": (
                        "https://www.chinacdc.cn/jksj/jksj04_14249/"
                        "202607/t20260715_1838199.html"
                    ),
                    "context": "",
                }
            ],
        }
        records = MODULE.parse_records(page, MODULE.ADAPTERS["influenza_weekly"])
        self.assertEqual(records[0]["title"], "2026年第28周第917期中国流感监测周报")
        self.assertEqual(records[0]["publish_date"], "2026-07-16")

    def test_latest_conflicts_with_explicit_period(self):
        value = query("influenza_weekly", action="locate")
        value["year"] = 2026
        with self.assertRaisesRegex(MODULE.PipelineError, "latest cannot"):
            MODULE.validate_query(value, MODULE.ADAPTERS["influenza_weekly"])

    def test_latest_influenza_prefers_highest_issue(self):
        records = [
            {"year": 2026, "week": 29, "month": None, "issue": 917, "publish_date": "2026-07-20"},
            {"year": 2026, "week": 28, "month": None, "issue": 918, "publish_date": "2026-07-19"},
        ]
        chosen = MODULE.choose_record(records, query("influenza_weekly"), MODULE.ADAPTERS["influenza_weekly"])
        self.assertEqual(chosen["issue"], 918)


if __name__ == "__main__":
    unittest.main()
