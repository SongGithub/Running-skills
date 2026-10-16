#!/usr/bin/env python3
"""Publish a Strava run via the local adapter, with mandatory pre-publish hook."""
import argparse
import json
import pathlib
import sys
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from pre_publish_hook import GateError, load_policy, review_fields, validate_copy, validate_review


def publish(activity_id, title, description, workspace):
    # Local adapter provides token refresh and read access. It is never committed here.
    sys.path.insert(0, str(workspace))
    from strava_mcp_server import API, _ctx, access_token, api_get

    current = api_get(f"/activities/{activity_id}")
    if current.get("type") != "Run" and current.get("sport_type") != "Run":
        raise GateError("refusing to update a non-run activity")
    payload = urlencode({"name": title, "description": description}).encode("utf-8")
    req = Request(
        f"{API}/activities/{activity_id}",
        data=payload,
        headers={"Authorization": "Bearer " + access_token(),
                 "Content-Type": "application/x-www-form-urlencoded"},
        method="PUT",
    )
    with urlopen(req, context=_ctx(), timeout=40) as response:
        json.loads(response.read())
    saved = api_get(f"/activities/{activity_id}")
    if saved.get("name") != title or saved.get("description") != description:
        raise GateError("Strava readback does not match published copy")
    return saved


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--activity-id", type=int, required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--description-file", type=pathlib.Path, required=True)
    parser.add_argument("--policy", type=pathlib.Path, required=True)
    parser.add_argument("--workspace", type=pathlib.Path, required=True,
                        help="Local directory containing strava_mcp_server.py")
    parser.add_argument("--review-file", type=pathlib.Path)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.activity_id <= 0:
            raise GateError("activity id must be positive")
        title = args.title.strip()
        description = args.description_file.read_text(encoding="utf-8").strip()
        policy, policy_digest = load_policy(args.policy)
        errors = validate_copy(policy, title, description)
        if errors:
            raise GateError("; ".join(errors))
        if args.apply:
            if not args.review_file:
                raise GateError("--apply requires --review-file")
            validate_review(args.review_file, policy_digest, title, description)
            publish(args.activity_id, title, description, args.workspace)
            print(f"PUBLISHED AND VERIFIED: activity {args.activity_id}")
        else:
            print("PASS: local policy preflight; no network call")
            print(json.dumps(review_fields(policy_digest, title, description), indent=2))
        return 0
    except (GateError, OSError, ValueError) as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
