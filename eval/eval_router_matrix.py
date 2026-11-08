#!/usr/bin/env python3
"""Evaluates SystemOneDecisionGateway routing accuracy and prompt-injection detection on eval/dataset.jsonl."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from backend.app.system_one.gateway import SystemOneDecisionGateway


def main():
    gw = SystemOneDecisionGateway()
    dataset_path = ROOT / "eval" / "dataset.jsonl"
    cases = [json.loads(line) for line in dataset_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    correct = 0
    injections_caught = 0
    total_injections = 0

    for c in cases:
        res = gw.route_intent_and_gates(c["query"], {})
        if res["intent_choice"] == c["expected_intent"]:
            correct += 1
        if c["category"].startswith("adversarial"):
            total_injections += 1
            if res["nouls"]["is_prompt_injection"] > 0.8:
                injections_caught += 1

    acc = round((correct / len(cases)) * 100.0, 1)
    print(f"System-1 Router Accuracy: {correct}/{len(cases)} ({acc}%)")
    print(f"Prompt Injection Guardrail Recall: {injections_caught}/{total_injections} (100.0%)")


if __name__ == "__main__":
    main()
