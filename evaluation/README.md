# Controlled evaluation corpus

This corpus is intentionally separate from `examples/` and from any future tuning fixtures. AuthLens has no machine-learning training step; thresholds remain the documented defaults. No rule was tuned against these cases. The files are synthetic, use documentation IPs and are suitable for repeatable regression/evaluation only.

`events.jsonl` contains valid normalized JSONL. Each scenario uses a distinct host so scenarios cannot correlate with one another. `labels.json` defines the expected behavioral indicator IDs, whether the scenario is benign or suspicious in the exercise narrative, and the reason for the label. `evaluate.py` compares rule IDs per host and prints TP/FP/TN/FN, precision, recall and F1 over scenario-rule pairs.

The metrics answer: “Did the implementation emit the expected behavioral indicator for this controlled case?” They do not answer: “Will AuthLens identify real attacks?” Benign scenarios that intentionally match a rule are retained to expose false-positive context; they are not counted as malicious positives. Do not change detector thresholds based only on this evaluation set. Add a new labeled case and document the expected semantics first.

Run:

```console
python evaluation/evaluate.py
```

The evaluator uses the real parser and detector, not a copied predicate. A clean run should produce stable counts and no unmatched scenario. It does not replace the independent randomized oracle in `tests/unit/test_engine.py`.
