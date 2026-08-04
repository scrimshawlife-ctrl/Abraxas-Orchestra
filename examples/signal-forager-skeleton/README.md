# Signal Forager Skeleton Example

See [EXAMPLE.md](EXAMPLE.md) for the full walkthrough.

Regenerate the dual-named package stubs:

```bash
./regenerate.sh
# or from repo root:
python3 scripts/orchestra.py do structure \
  -f tree-of-life \
  -o alchemical-stages \
  -c "intent,intake,constraint,adversarial,synthesis,store,output" \
  --out examples/signal-forager-skeleton
```

This keeps the example reproducible from the live CLI rather than freezing generated stubs in git.
