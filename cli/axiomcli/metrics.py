"""Read-only evidence metadata checks; never an execution or release certification."""
import hashlib
import json
import math
import os
from pathlib import Path
import re
import stat
from datetime import datetime, timezone

MAX_INPUT = 1_048_576
MAX_EVIDENCE = 16_777_216
MAX_TASKS = 256
MAX_OBSERVATIONS = 4096
LIMITATION = "File digests support declared observations; execution, deployment and release are not independently verified."


class Invalid(ValueError):
    pass


def _read(root, relative, limit):
    """Walk with no-follow descriptors so symlink swaps cannot escape containment."""
    if not isinstance(relative, str) or not relative or len(relative) > 4096:
        raise Invalid("invalid_path")
    parts = relative.split('/')
    if Path(relative).is_absolute() or any(p in ('', '.', '..') for p in parts) or '\\' in relative:
        raise Invalid("invalid_path")
    if not all(hasattr(os, name) for name in ('O_DIRECTORY', 'O_NOFOLLOW')) or os.open not in os.supports_dir_fd:
        raise Invalid("secure_file_access_unavailable")
    absolute = Path(root).resolve()
    fd = os.open(absolute.anchor, os.O_RDONLY | os.O_DIRECTORY)
    try:
        for component in (*absolute.parts[1:], *parts[:-1]):
            child = os.open(component, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = child
        leaf = os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=fd)
        try:
            info = os.fstat(leaf)
            if not stat.S_ISREG(info.st_mode) or info.st_size > limit:
                raise Invalid("not_regular_or_too_large")
            data = bytearray()
            while len(data) <= limit:
                block = os.read(leaf, min(65536, limit + 1 - len(data)))
                if not block:
                    return bytes(data)
                data.extend(block)
            raise Invalid("too_large")
        finally:
            os.close(leaf)
    finally:
        os.close(fd)


def _keys(value, expected):
    if not isinstance(value, dict) or set(value) != set(expected):
        raise Invalid("invalid_fields")


def _text(value):
    if not isinstance(value, str) or not value.strip() or len(value) > 2048:
        raise Invalid("invalid_text")


def _date(value, now):
    if not isinstance(value, str) or len(value) > 64:
        raise Invalid("invalid_timestamp")
    try:
        date = datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError:
        raise Invalid("invalid_timestamp") from None
    if date.tzinfo is None or date.utcoffset() is None or date > now:
        raise Invalid("invalid_or_future_timestamp")
    return date


def _unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise Invalid("duplicate_json_key")
        result[key] = value
    return result


def report(target: Path, now: datetime = None, stale_hours: float = 24) -> dict:
    """Inspect optional progress.json. Free-form declarations and evidence bytes stay private."""
    now = now or datetime.now(timezone.utc)
    if not isinstance(now, datetime) or now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("now must be timezone-aware")
    if isinstance(stale_hours, bool) or not isinstance(stale_hours, (float, int)) or not math.isfinite(stale_hours) or stale_hours <= 0:
        raise ValueError("stale_hours must be finite and positive")
    result = {"status": "unavailable", "tasks": [], "limitation": LIMITATION}
    try:
        raw = _read(target, 'sdd/progress.json', MAX_INPUT)
    except FileNotFoundError:
        return result
    except (OSError, Invalid):
        return dict(result, status="invalid", error="unsafe_or_unreadable_input")
    try:
        document = json.loads(raw, object_pairs_hook=_unique)
        _keys(document, ('version', 'tasks'))
        if type(document['version']) is not int or document['version'] != 1:
            raise Invalid("unsupported_version")
        tasks = document['tasks']
        if not isinstance(tasks, list) or len(tasks) > MAX_TASKS:
            raise Invalid("invalid_tasks")
        seen_ids = set()
        total = 0
        for task in tasks:
            _keys(task, ('id', 'owner', 'next_action', 'blocker', 'required_mode', 'observations'))
            for key in ('id', 'owner', 'next_action'):
                _text(task[key])
            if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,79}', task['id']) or task['id'] in seen_ids:
                raise Invalid("invalid_or_duplicate_id")
            seen_ids.add(task['id'])
            if task['blocker'] is not None:
                _text(task['blocker'])
            if task['required_mode'] not in ('real', 'simulated') or not isinstance(task['observations'], list):
                raise Invalid("invalid_task")
            total += len(task['observations'])
            if total > MAX_OBSERVATIONS:
                raise Invalid("too_many_observations")
            item = {"id": task['id'], "state": "no_evidence", "blocked": task['blocker'] is not None,
                    "required_mode": task['required_mode'], "age_hours": None, "stale": None}
            previous = None
            first_seen = {}
            try:
                for observation in task['observations']:
                    _keys(observation, ('at', 'path', 'sha256', 'mode', 'passed', 'failed', 'skipped'))
                    at = _date(observation['at'], now)
                    if previous is not None and at < previous:
                        raise Invalid("nonchronological_observations")
                    previous = at
                    digest = observation['sha256']
                    if not isinstance(digest, str) or not re.fullmatch('[a-f0-9]{64}', digest):
                        raise Invalid("invalid_digest")
                    if observation['mode'] not in ('real', 'simulated'):
                        raise Invalid("invalid_mode")
                    counts = tuple(observation[k] for k in ('passed', 'failed', 'skipped'))
                    if any(type(n) is not int or not 0 <= n <= 1_000_000_000 for n in counts):
                        raise Invalid("invalid_counts")
                    if hashlib.sha256(_read(target, observation['path'], MAX_EVIDENCE)).hexdigest() != digest:
                        raise Invalid("digest_mismatch")
                    fingerprint = (digest, observation['mode'], *counts)
                    first_seen.setdefault(fingerprint, at)
                    item.update(age_hours=(now - first_seen[fingerprint]).total_seconds() / 3600,
                                mode=observation['mode'], passed=counts[0], failed=counts[1], skipped=counts[2])
                    item['stale'] = item['age_hours'] >= stale_hours
                    item['state'] = ('incomplete_checks' if counts[1] or counts[2] or not counts[0]
                                     else 'real_evidence_required' if task['required_mode'] == 'real' and observation['mode'] != 'real'
                                     else 'declared_checks_supported')
            except (Invalid, OSError) as exc:
                item = {"id": task['id'], "state": "invalid_evidence", "blocked": task['blocker'] is not None,
                        "age_hours": None, "stale": None,
                        "error": str(exc) if isinstance(exc, Invalid) else "unsafe_or_unreadable_evidence"}
            result['tasks'].append(item)
        result['status'] = 'available'
    except (Invalid, ValueError, TypeError, RecursionError):
        return {"status": "invalid", "tasks": [], "error": "invalid_progress_document", "limitation": LIMITATION}
    return result
