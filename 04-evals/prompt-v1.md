# Review prompt v1 (baseline)
Model: Claude Opus 5.5 (Cursor subagent, `generalPurpose`, model `inherit`). Context file: none. The reviewer gets only the diff and the prompt. Date: 2026-10-31

The prompt is copied verbatim from `ops/evals/README.md` in `ai-in-sdlc-assignment`:

```
Review this diff for defects. For each finding give the file, the line, what
goes wrong, and how confident you are. If you find nothing, say so
explicitly rather than listing general observations.
```

Harness wrapper, identical for v1 and v2: "You are a code reviewer. Do not use any tools, do not read
files, and do not search. Use only the diff below." Followed by the prompt, then the diff in a fenced block.
Each case runs in a fresh subagent session, so no context carries over between cases or runs.
