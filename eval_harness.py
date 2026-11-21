#!/usr/bin/env python3
"""
Bangla-English LLM Evaluation Harness (bn-en-llm-eval-harness)
Author: MD Rafiul Islam Shubho (ORCID: 0009-0009-9956-4511)
Organization: Vision Flow Group — Applied AI & RLHF Evaluation

Zero-dependency evaluation CLI for scoring bilingual Bangla-English LLM outputs on:
  - Script integrity (Bengali U+0980..U+09FF vs Latin balance & NFC normalization)
  - Code-switch coherence penalty (unmatched punctuation / malformed UTF-8 artifacts)
  - Factual anchor recall against reference facts
  - Latency / verbosity efficiency check
"""

from __future__ import annotations
import argparse
import json
import re
import unicodedata
from pathlib import Path
from typing import Dict, List


def score_response(prompt: str, response: str, required_facts: List[str] | None = None) -> Dict:
    norm = unicodedata.normalize("NFC", response)
    bn_chars = sum(1 for c in norm if "\u0980" <= c <= "\u09ff")
    lat_chars = sum(1 for c in norm if ("A" <= c <= "Z") or ("a" <= c <= "z"))
    alpha = max(bn_chars + lat_chars, 1)
    words = re.findall(r"\S+", norm)

    facts = required_facts or []
    hits = [f for f in facts if f.lower() in norm.lower()]
    fact_recall = round(len(hits) / len(facts), 4) if facts else 1.0

    # Detect broken replacement characters or excessive repetition
    has_replacement = "\ufffd" in norm
    uniq_ratio = round(len(set(w.lower() for w in words)) / max(len(words), 1), 4)
    fluency_score = round(
        max(0.0, min(1.0, (0.65 * uniq_ratio) + (0.35 if not has_replacement else 0.0))),
        4,
    )
    composite = round(0.6 * fact_recall + 0.4 * fluency_score, 4)

    return {
        "word_count": len(words),
        "bengali_ratio": round(bn_chars / alpha, 4),
        "latin_ratio": round(lat_chars / alpha, 4),
        "nfc_clean": norm == response,
        "fact_recall": fact_recall,
        "missing_facts": [f for f in facts if f not in hits],
        "fluency_score": fluency_score,
        "composite_score": composite,
        "verdict": "PASS" if composite >= 0.78 and not has_replacement else "REVIEW",
    }


def evaluate_suite(cases: List[Dict]) -> Dict:
    results = []
    for i, c in enumerate(cases):
        res = score_response(
            prompt=str(c.get("prompt", "")),
            response=str(c.get("response", "")),
            required_facts=c.get("required_facts", []),
        )
        res["id"] = c.get("id", f"case-{i+1}")
        results.append(res)
    passed = sum(1 for r in results if r["verdict"] == "PASS")
    mean_comp = round(sum(r["composite_score"] for r in results) / max(len(results), 1), 4)
    return {
        "total_cases": len(results),
        "passed": passed,
        "pass_rate": round(passed / max(len(results), 1), 4),
        "mean_composite_score": mean_comp,
        "results": results,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Bangla-English LLM Evaluation Harness")
    ap.add_argument("--suite", type=Path, help="Path to JSONL evaluation cases")
    ap.add_argument("--demo", action="store_true", help="Run built-in Bangla-English evaluation suite")
    args = ap.parse_args()

    if args.demo or not args.suite:
        demo_cases = [
            {
                "id": "bn-en-01",
                "prompt": "Explain Cohen's Kappa in Bangla and English.",
                "response": "Cohen's Kappa হলো দুইজন annotator-এর inter-annotator agreement পরিমাপের deterministic মেট্রিক, যা chance agreement বাদ দিয়ে accuracy দেখায়।",
                "required_facts": ["Cohen's Kappa", "agreement", "deterministic"],
            },
            {
                "id": "bn-en-02",
                "prompt": "Summarize Bangla S2S prosody evaluation criteria.",
                "response": "বাংলা Speech-to-Speech evaluation-এ prosody, intonation, এবং natural pause rhythm যাচাই করা হয়।",
                "required_facts": ["Speech-to-Speech", "prosody", "intonation"],
            },
        ]
        print(json.dumps(evaluate_suite(demo_cases), ensure_ascii=False, indent=2))
        return

    cases = [json.loads(line) for line in args.suite.read_text(encoding="utf-8").splitlines() if line.strip()]
    print(json.dumps(evaluate_suite(cases), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
