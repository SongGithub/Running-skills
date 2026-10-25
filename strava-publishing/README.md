# Strava publishing gate

This package is the guarded activity-title/description writer. It contains no personal policy or credentials. Keep both outside this public repo.

1. Initialise this repository with Spec Kit (`specify init --here --integration codex --integration-options='--skills'`); the generated `.specify/` and `.agents/skills/speckit-*` files are included. Feature requirements live in `specs/`.
2. Create a private JSON policy from `policy.example.json.template` outside this repository, e.g. under your agent workspace. Fill in local title patterns, sign-off and editorial guidance. The template is not a live policy.
3. Draft the activity title and an English story in a local description file. Read the private policy and review exact copy for factual fit, undesired metrics and private details.
4. Run the CLI without `--apply` to preflight and obtain the three SHA-256 fields. Create a local review JSON with those fields plus `approved`, `english_story`, `factual_fit`, `no_unwanted_metrics`, and `no_private_details` all set to `true` only after the semantic review. Never commit the review JSON.
5. Run the same CLI with `--apply --review-file <local-review.json>`. The pre-publish hook rechecks policy and receipt before importing the local Strava adapter or making a request. Any changed title, description or policy invalidates the receipt.

```sh
python3 strava-publishing/publish.py --activity-id 123 --title 'Morning Run' \
  --description-file /path/to/local-description.txt \
  --policy /path/to/local-policy.json --workspace /path/to/local-running-workspace
```

The local workspace must contain `strava_mcp_server.py` and its own `strava_config.json`; neither belongs in this repo. The publisher uses that adapter to refresh credentials, reject non-run activities and verify the saved values. The receipt is an attestation of agent review, not cryptographic proof that the review was thoughtful. Agents must not bypass this writer with direct REST, browser or ad-hoc scripts.

Run offline tests: `python3 -m unittest discover -s strava-publishing/tests`.

Install these two source files into the local running workspace with `strava-publishing/install-local.sh /absolute/path/to/workspace`. The installer never copies or modifies the private policy. The local runbook should specify the absolute private policy path and require a fresh review receipt for each proposed copy.
