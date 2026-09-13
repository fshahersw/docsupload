# Synthetic engineering examples

These files contain invented fixture text and placeholder hashes. Exclude this directory from legal retrieval, training and matter evidence.

From the tools directory:

```powershell
python -B corpus_tools.py registry examples/sources.json --output examples/normalized-sources.json
python -B corpus_tools.py plan examples/documents.json --output examples/scan-plan.json
python -B corpus_tools.py coverage examples/scan-plan.json --results examples/attempts.json --output examples/coverage.json
python -B corpus_tools.py verify examples/documents.json --results examples/findings.json --output examples/grounding.json
python -B corpus_tools.py csv examples/findings.json --output examples/findings.csv
```

The expected report preserves one unreadable page. An unverified finding without a quote fails literal grounding. The scan plan is 1.1.0, and all offsets are Unicode code points. These are deliberate non-success cases, not legal data or evidence of model performance.
