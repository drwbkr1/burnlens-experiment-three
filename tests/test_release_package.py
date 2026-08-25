from __future__ import annotations

import hashlib
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.build_release_package import ARCHIVE_NAME, PACKAGE_NAME, build
from scripts.verify_release_package import verify

TEMP_ROOT = ROOT / ".test-tmp"
TEMP_ROOT.mkdir(exist_ok=True)


class ReleasePackageTests(unittest.TestCase):
    def test_two_builds_are_exact_and_standalone_verifier_passes(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as temporary:
            root = Path(temporary)
            first = build(root / "first")
            second = build(root / "second")
            self.assertEqual(first["archive_sha256"], second["archive_sha256"])
            self.assertEqual(
                hashlib.sha256((root / "first" / ARCHIVE_NAME).read_bytes()).hexdigest(),
                hashlib.sha256((root / "second" / ARCHIVE_NAME).read_bytes()).hexdigest(),
            )
            receipt = verify(root / "first" / PACKAGE_NAME)
            self.assertEqual("PASS", receipt["status"])
            self.assertEqual("FAIL", receipt["comparative_status"])

    def test_verifier_rejects_result_tampering(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as temporary:
            root = Path(temporary)
            build(root)
            result = root / PACKAGE_NAME / "evidence/evaluation-record.json"
            result.write_bytes(result.read_bytes().replace(b'"comparative_status": "FAIL"', b'"comparative_status": "PASS"'))
            with self.assertRaises(ValueError):
                verify(root / PACKAGE_NAME)


if __name__ == "__main__":
    unittest.main()
