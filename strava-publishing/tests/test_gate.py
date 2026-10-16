import json
import pathlib
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
import types

MODULE = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MODULE))
from pre_publish_hook import GateError, load_policy, review_fields, validate_copy, validate_review
from publish import publish


class GateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.dir = pathlib.Path(self.tmp.name)
        self.policy_path = self.dir / "policy.json"
        self.policy_path.write_text(json.dumps({
            "version": 1,
            "title": {"required": True, "max_length": 100,
                      "forbidden_patterns": [r"\bprivate[ -]?term\b"]},
            "description": {"required": True, "ending": "Done.",
                            "guidance": "A short factual story"},
        }))
        self.description = self.dir / "description.txt"
        self.description.write_text("A short run story.\n\nDone.")
        self.title = "Morning Run"
        self.policy, self.hash = load_policy(self.policy_path)

    def receipt(self, **changes):
        data = review_fields(self.hash, self.title, self.description.read_text().strip())
        data.update({"approved": True, "english_story": True, "factual_fit": True,
                     "no_unwanted_metrics": True, "no_private_details": True})
        data.update(changes)
        path = self.dir / "review.json"
        path.write_text(json.dumps(data))
        return path

    def cli(self, title=None, apply=False, review=None):
        cmd = [sys.executable, str(MODULE / "publish.py"), "--activity-id", "123",
               "--title", title or self.title, "--description-file", str(self.description),
               "--policy", str(self.policy_path), "--workspace", str(self.dir)]
        if apply:
            cmd.append("--apply")
        if review:
            cmd.extend(["--review-file", str(review)])
        return subprocess.run(cmd, capture_output=True, text=True)

    def test_preflight_passes_without_adapter(self):
        self.assertEqual(0, self.cli().returncode)

    def test_configured_title_rule_blocks(self):
        self.assertIn("locally forbidden", self.cli(title="Private term jog").stderr)

    def test_apply_needs_review_before_adapter(self):
        self.assertIn("requires --review-file", self.cli(apply=True).stderr)

    def test_stale_review_blocks(self):
        review = self.receipt()
        self.assertIn("stale", self.cli(title="Another Run", apply=True, review=review).stderr)
        self.policy_path.write_text(self.policy_path.read_text() + " ")
        self.assertIn("stale", self.cli(apply=True, review=review).stderr)

    def test_negative_review_blocks(self):
        review = self.receipt(no_private_details=False)
        with self.assertRaises(GateError):
            validate_review(review, self.hash, self.title, self.description.read_text().strip())

    def test_missing_or_malformed_policy_blocks(self):
        self.policy_path.unlink()
        self.assertNotEqual(0, self.cli().returncode)
        self.policy_path.write_text("{}")
        self.assertNotEqual(0, self.cli().returncode)

    def test_non_run_is_not_mutated(self):
        adapter = types.SimpleNamespace(
            API="https://example.invalid", _ctx=lambda: None,
            access_token=lambda: "not-a-real-token",
            api_get=lambda path: {"type": "Ride"},
        )
        with mock.patch.dict(sys.modules, {"strava_mcp_server": adapter}):
            with mock.patch("publish.urlopen") as send:
                with self.assertRaises(GateError):
                    publish(123, self.title, "A story", self.dir)
                send.assert_not_called()

    def test_write_requires_exact_readback(self):
        calls = iter([{"type": "Run"}, {"name": "different", "description": "A story"}])
        adapter = types.SimpleNamespace(
            API="https://example.invalid", _ctx=lambda: None,
            access_token=lambda: "not-a-real-token",
            api_get=lambda path: next(calls),
        )
        response = mock.MagicMock()
        response.__enter__.return_value.read.return_value = b"{}"
        with mock.patch.dict(sys.modules, {"strava_mcp_server": adapter}):
            with mock.patch("publish.urlopen", return_value=response) as send:
                with self.assertRaises(GateError):
                    publish(123, self.title, "A story", self.dir)
                send.assert_called_once()

    def test_description_suffix_blocks(self):
        self.assertTrue(any("required ending" in x for x in validate_copy(self.policy, self.title, "A story")))


if __name__ == "__main__":
    unittest.main()
