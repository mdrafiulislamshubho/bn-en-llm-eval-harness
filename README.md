# Bangla-English LLM Evaluation Harness

Lightweight, zero-dependency Python evaluation harness for scoring bilingual Bangla-English LLM responses on script integrity, Unicode NFC normalization, factual anchor recall, and code-switch fluency.

**Author:** [MD Rafiul Islam Shubho](https://orcid.org/0009-0009-9956-4511) — Co-Founder, Managing Director & Applied AI / RLHF Evaluator, [Vision Flow Group](https://visionflowgroup.com/)

## Key Metrics

- **Bengali / Latin Script Ratio** (`U+0980–U+09FF` vs ASCII Latin) + strict **Unicode NFC** validation.
- **Required Fact Recall** against golden factual anchors per prompt.
- **Code-Switch Fluency & Replacement-Char Guard** (`U+FFFD` detection + lexical diversity).
- **Composite Verdict Gate** (`PASS` vs `REVIEW` threshold at `0.78`).

## Usage

```bash
# Run built-in Bangla-English evaluation demo
python3 eval_harness.py --demo

# Evaluate a custom JSONL suite
python3 eval_harness.py --suite cases.jsonl
```

## Companion Projects & Verification

- **ORCID:** [0009-0009-9956-4511](https://orcid.org/0009-0009-9956-4511)
- **Crunchbase:** [MD Rafiul Islam Shubho](https://www.crunchbase.com/person/md-rafiul-islam-shubho)
- **DEV.to:** [Deterministic Bilingual RLHF Rubric Calibration](https://dev.to/mdrafiulislamshubho/deterministic-bilingual-rlhf-rubric-calibration-and-bangla-speech-to-speech-evaluation-1l4f)
- **RLHF Rubric Calibration Kit:** [rlhf-rubric-calibration-kit](https://github.com/mdrafiulislamshubho/rlhf-rubric-calibration-kit)
- **Bangla S2S Prosody Bench:** [bangla-s2s-prosody-bench](https://github.com/mdrafiulislamshubho/bangla-s2s-prosody-bench)
- **Organization:** [Vision Flow Group](https://visionflowgroup.com/md-rafiul-islam-shubho/)
