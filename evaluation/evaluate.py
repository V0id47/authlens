"""Evaluate labeled scenarios by host; metrics are behavioral, not field accuracy."""

import json
from collections import Counter
from pathlib import Path

from authlens.config import Settings
from authlens.engine import detect
from authlens.ingest import ingest

ROOT = Path(__file__).resolve().parents[1]


def main():
    labels = json.loads((ROOT / "evaluation/labels.json").read_text(encoding="utf-8"))
    dataset = ingest(ROOT / "evaluation/events.jsonl", Settings())
    findings = detect(dataset.events, Settings())
    actual = {}
    for finding in findings:
        actual.setdefault(finding.host, set()).add(finding.rule_id)
    counts = Counter()
    rows = []
    for scenario in labels["scenarios"]:
        expected = set(scenario["expected_rules"])
        observed = actual.get(scenario["host"], set())
        for rule in {"AL-001", "AL-002", "AL-003"}:
            pair = (rule in expected, rule in observed)
            counts[
                (
                    "tp"
                    if pair == (True, True)
                    else "fn"
                    if pair == (True, False)
                    else "fp"
                    if pair == (False, True)
                    else "tn"
                )
            ] += 1
        rows.append(
            {
                "host": scenario["host"],
                "expected": sorted(expected),
                "observed": sorted(observed),
                "match": expected == observed,
            }
        )
    tp, fp, fn = counts["tp"], counts["fp"], counts["fn"]
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    print(
        json.dumps(
            {
                "scenarios": rows,
                "counts": dict(counts),
                "precision": precision,
                "recall": recall,
                "f1": f1,
            },
            indent=2,
            sort_keys=True,
        )
    )
    if not all(row["match"] for row in rows):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
