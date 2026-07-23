from __future__ import annotations

import argparse
import hashlib
import importlib.util
import io
import tempfile
import unittest
from unittest import mock
from email.message import Message
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/download_official_document.py"
SPEC = importlib.util.spec_from_file_location("download_official_document", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class FakeResponse(io.BytesIO):
    def __init__(self, body: bytes, url: str, content_type: str = "application/pdf") -> None:
        super().__init__(body)
        self._url = url
        self.status = 200
        self.headers = Message()
        self.headers["Content-Type"] = content_type

    def geturl(self) -> str:
        return self._url

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        self.close()


class FakeOpener:
    def __init__(self, body: bytes, final_url: str) -> None:
        self.body = body
        self.final_url = final_url
        self.requests = []

    def open(self, request, timeout):
        self.requests.append((request, timeout))
        return FakeResponse(self.body, self.final_url)


def args(output_dir: Path) -> argparse.Namespace:
    return argparse.Namespace(
        url="https://www.chinacdc.cn/jksj/jksj04_14249/202607/P1.pdf",
        referer="https://www.chinacdc.cn/jksj/jksj04_14249/202607/t1_1.html",
        allowed_path_prefix="/jksj/jksj04_14249/",
        output_dir=output_dir,
        report_type="influenza_weekly",
        year=2026,
        week=28,
        month=None,
        issue=917,
        timeout=12.0,
        max_bytes=1024 * 1024,
        user_agent=MODULE.DEFAULT_USER_AGENT,
    )


class DownloaderTests(unittest.TestCase):
    def test_download_validates_and_reuses_identical_pdf(self):
        body = b"%PDF-1.7\nfixture\n%%EOF\n"
        with tempfile.TemporaryDirectory() as directory:
            output_dir = Path(directory)
            opener = FakeOpener(body, args(output_dir).url)
            first = MODULE.download(args(output_dir), opener=opener)
            second = MODULE.download(args(output_dir), opener=opener)
            digest = hashlib.sha256(body).hexdigest()
            self.assertEqual(first["sha256"], digest)
            self.assertEqual(first["transport"], "verified_http_download")
            self.assertEqual(Path(first["path"]).name, f"influenza_weekly_2026_W28_917_{digest[:8]}.pdf")
            self.assertFalse(first["reused"])
            self.assertTrue(second["reused"])
            self.assertEqual(len(list(output_dir.glob("*.pdf"))), 1)
            request, timeout = opener.requests[0]
            self.assertEqual(timeout, 12.0)
            self.assertEqual(request.get_header("Referer"), args(output_dir).referer)
            self.assertIn("Chrome/", request.get_header("User-agent"))

    def test_collision_gets_numeric_suffix(self):
        with tempfile.TemporaryDirectory() as directory:
            output_dir = Path(directory)
            body = b"%PDF-1.7\nnew\n%%EOF\n"
            digest = hashlib.sha256(body).hexdigest()
            expected = output_dir / f"influenza_weekly_2026_W28_917_{digest[:8]}.pdf"
            expected.write_bytes(b"different")
            result = MODULE.download(args(output_dir), opener=FakeOpener(body, args(output_dir).url))
            self.assertTrue(Path(result["path"]).name.endswith("_2.pdf"))

    def test_rejects_non_pdf_signature_and_out_of_scope_url(self):
        with tempfile.TemporaryDirectory() as directory:
            output_dir = Path(directory)
            with self.assertRaisesRegex(MODULE.DownloadError, "PDF signature"):
                MODULE.download(args(output_dir), opener=FakeOpener(b"<html>no</html>", args(output_dir).url))
            bad = args(output_dir)
            bad.url = "https://example.com/file.pdf"
            with self.assertRaisesRegex(MODULE.DownloadError, "official China CDC host"):
                MODULE.download(bad, opener=FakeOpener(b"%PDF-1.7", bad.url))

    def test_direct_opener_disables_environment_proxies(self):
        with mock.patch.object(MODULE.urllib.request, "getproxies", side_effect=AssertionError("environment proxy consulted")):
            opener = MODULE.build_direct_opener("/jksj/jksj04_14249/")
        self.assertIsInstance(opener, MODULE.urllib.request.OpenerDirector)

    def test_redirect_handler_rejects_cross_origin(self):
        handler = MODULE.ScopedRedirectHandler("/jksj/jksj04_14249/")
        with self.assertRaisesRegex(MODULE.DownloadError, "official China CDC host"):
            handler.redirect_request(None, None, 302, "Found", {}, "https://example.com/file.pdf")


if __name__ == "__main__":
    unittest.main()
