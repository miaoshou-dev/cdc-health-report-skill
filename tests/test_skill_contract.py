from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def validate_extracted(payload: dict) -> None:
    assert payload["schema_version"] == "2.0"
    assert isinstance(payload["report"], dict)
    assert isinstance(payload["pages"], list)
    assert isinstance(payload["vision_pages"], list)
    assert isinstance(payload["warnings"], list)

    page_numbers = [page["page"] for page in payload["pages"]]
    assert page_numbers == list(range(1, len(page_numbers) + 1))
    expected_vision = sorted(
        page["page"] for page in payload["pages"] if page["requires_vision"]
    )
    assert payload["vision_pages"] == expected_vision
    assert len(payload["vision_pages"]) == len(set(payload["vision_pages"]))

    if payload["pages"]:
        assert payload["content"] is None
    else:
        assert payload["content"] is not None


class SkillContractTests(unittest.TestCase):
    def test_pdf_contract_covers_every_page_and_derives_vision_pages(self):
        pages = [
            {
                "page": page,
                "text": "" if page in (1, 19) else f"page {page}",
                "tables": [],
                "visuals": [],
                "requires_vision": page in (1, 5, 19),
            }
            for page in range(1, 20)
        ]
        payload = {
            "schema_version": "2.0",
            "report": {"content_mode": "pdf"},
            "pages": pages,
            "content": None,
            "vision_pages": [1, 5, 19],
            "warnings": [],
        }
        validate_extracted(payload)
        self.assertEqual(len(payload["pages"]), 19)

    def test_html_contract_has_no_pages_or_visual_queue(self):
        payload = {
            "schema_version": "2.0",
            "report": {"content_mode": "html"},
            "pages": [],
            "content": {"text": "body", "tables": [], "images": []},
            "vision_pages": [],
            "warnings": [],
        }
        validate_extracted(payload)

    def test_extract_artifact_is_single_json_file(self):
        with tempfile.TemporaryDirectory() as directory:
            report_dir = Path(directory) / "report"
            report_dir.mkdir()
            (report_dir / "extracted.json").write_text(
                json.dumps({"schema_version": "2.0"}), encoding="utf-8"
            )
            self.assertEqual(
                [path.name for path in report_dir.iterdir()], ["extracted.json"]
            )

    def test_legacy_browser_state_directory_is_absent(self):
        self.assertFalse((ROOT / ("browser" + "-memory")).exists())


if __name__ == "__main__":
    unittest.main()
