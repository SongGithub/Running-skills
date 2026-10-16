"""Fail-closed local pre-publish gate. No network calls or credentials."""
import hashlib
import json
import pathlib
import re


class GateError(ValueError):
    pass


def digest(value):
    return hashlib.sha256(value).hexdigest()


def load_policy(path):
    raw = pathlib.Path(path).read_bytes()
    policy = json.loads(raw)
    if policy.get("version") != 1:
        raise GateError("unsupported or missing policy version")
    title = policy.get("title")
    description = policy.get("description")
    if not isinstance(title, dict) or not isinstance(description, dict):
        raise GateError("title and description policy sections are required")
    if not isinstance(title.get("max_length"), int) or title["max_length"] < 1:
        raise GateError("invalid title max_length")
    if not isinstance(title.get("forbidden_patterns"), list):
        raise GateError("title forbidden_patterns must be a list")
    for pattern in title["forbidden_patterns"]:
        if not isinstance(pattern, str):
            raise GateError("forbidden pattern must be a string")
        try:
            re.compile(pattern)
        except re.error as exc:
            raise GateError("invalid forbidden pattern") from exc
    if not isinstance(description.get("ending"), str):
        raise GateError("description ending must be a string")
    return policy, digest(raw)


def validate_copy(policy, title, description):
    errors = []
    if policy["title"].get("required") and not title.strip():
        errors.append("title is empty")
    if len(title) > policy["title"]["max_length"]:
        errors.append("title exceeds max_length")
    for pattern in policy["title"]["forbidden_patterns"]:
        if re.search(pattern, title, flags=re.IGNORECASE):
            errors.append("title matches a locally forbidden pattern")
            break
    if policy["description"].get("required") and not description.strip():
        errors.append("description is empty")
    ending = policy["description"]["ending"]
    if ending and not description.rstrip().endswith(ending):
        errors.append("description does not have the required ending")
    return errors


def review_fields(policy_digest, title, description):
    return {
        "policy_sha256": policy_digest,
        "title_sha256": digest(title.encode("utf-8")),
        "description_sha256": digest(description.encode("utf-8")),
    }


def validate_review(path, policy_digest, title, description):
    try:
        review = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise GateError("review receipt is missing or invalid") from exc
    if any(review.get(k) != v for k, v in review_fields(policy_digest, title, description).items()):
        raise GateError("review receipt is stale for this policy or copy")
    required = ("english_story", "factual_fit", "no_unwanted_metrics", "no_private_details")
    if review.get("approved") is not True or any(review.get(k) is not True for k in required):
        raise GateError("semantic review was not approved")
    return review
