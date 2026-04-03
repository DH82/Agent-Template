# Experiment Workflow Template

Use this document to track an experiment from planning through execution, interpretation, and publication.

Recommended use:
- Copy this file into `experiments/YYYY-MM-DD_<experiment_name>/README.md`
- Keep logs, results, figures, and publish materials inside the same experiment folder first
- Use one document per experiment instead of endlessly appending to one file

---

## 0. Experiment Overview

- Experiment ID:
- Title:
- Owner:
- Date:
- Status: `planned | running | blocked | completed | published`
- Priority: `high | medium | low`
- Related branch / commit:
- Related issue / PR / note:

### One-line Summary

> What is the single core thing this experiment is trying to determine?

### Background

- Current situation:
- Why this experiment is needed:
- Existing hypothesis or problem:

---

## 1. Goal And Hypothesis

### Goal

- What you want to learn from this experiment:
- What decision this experiment should unlock if successful:

### Hypothesis

- Hypothesis 1:
- Hypothesis 2:

### Non-goals

- What this experiment will not cover:
- What this experiment alone should not be used to conclude:

---

## 2. Success Criteria

### Primary Metrics

| Metric | Definition | Target | Why it matters |
|---|---|---:|---|
| example_latency_ms | p50 latency | <= 100 | user-facing performance |
| example_accuracy | validation score | >= baseline + 2% | quality improvement |

### Secondary Metrics

| Metric | Definition | Target |
|---|---|---:|
| cost_per_run | cost per run | as low as possible |
| memory_peak_mb | peak memory use | below system limit |

### Failure Criteria

- The experiment counts as failed if any of these apply:
- not reproducible
- clearly worse than baseline
- logs or outputs are missing
- improvement is too small for the cost

---

## 3. Scope And Variables

### What Will Change

- Variable 1:
- Variable 2:

### What Will Stay Fixed

- Dataset:
- Evaluation code:
- Hardware:
- Seed:
- Baseline version:

### Experiment Matrix

| Run ID | Variant | Config Change | Expected Effect | Priority |
|---|---|---|---|---|
| run_001 | baseline | none | establish baseline | high |
| run_002 | variant_a | learning_rate=... | quality improvement | high |
| run_003 | variant_b | batch_size=... | speed improvement | medium |

---

## 4. Environment And Reproducibility

### Environment

- OS:
- Python / runtime:
- CUDA / driver:
- Library versions:
- Model / dataset version:

### Reproducibility Checklist

- [ ] record commit SHA
- [ ] save config
- [ ] record seed
- [ ] save command
- [ ] save raw logs
- [ ] save raw results
- [ ] record post-processing script path

### Paths

- Experiment root:
- Config path:
- Log path:
- Result path:
- Figure path:
- Publish path:

---

## 5. Execution Plan

### Pre-run Checklist

- [ ] baseline is ready
- [ ] dependencies are installed
- [ ] evaluation script can run by itself
- [ ] output paths exist
- [ ] log level and log format are decided

### Commands

```bash
# baseline
<command_here>

# variant A
<command_here>

# variant B
<command_here>
```

### Run Order

1. Run baseline
2. Run main variants
3. Retry failed runs
4. Aggregate results

### Operational Notes

- Expected runtime:
- Parallel execution:
- Stop condition:
- Retry policy:

---

## 6. Logging Plan

### What To Log

- start time / end time
- commit SHA
- full config
- key metrics
- warnings / errors
- resource usage

### Log Format

| Field | Example |
|---|---|
| timestamp | 2026-04-03T07:00:00Z |
| run_id | run_002 |
| variant | variant_a |
| step | eval |
| metric_name | accuracy |
| metric_value | 0.9123 |
| status | success |

### Log Review

- Log reviewer:
- Review timing:
- Criteria for suspicious logs:

---

## 7. Result Collection

### Raw Results

| Run ID | Status | Output File | Log File | Notes |
|---|---|---|---|---|
| run_001 | success | results/run_001.json | logs/run_001.log | baseline |
| run_002 | success | results/run_002.json | logs/run_002.log | |
| run_003 | failed | results/run_003.json | logs/run_003.log | OOM |

### Aggregated Results

| Run ID | Variant | Primary Metric | Secondary Metric | Baseline Delta | Decision |
|---|---|---:|---:|---:|---|
| run_001 | baseline | 0.900 | 120ms | 0.000 | keep |
| run_002 | variant_a | 0.915 | 123ms | +0.015 | promote |
| run_003 | variant_b | N/A | N/A | N/A | rerun |

### Missing Or Invalid Data

- Missing result:
- Untrusted result:
- Runs that need a rerun:

---

## 8. Interpretation

### Main Findings

- Finding 1:
- Finding 2:
- Finding 3:

### Why The Result Looks This Way

- Cause hypothesis 1:
- Cause hypothesis 2:
- Cause hypothesis 3:

### Confidence Level

- Confidence: `high | medium | low`
- Why:
- Remaining uncertainty:

### Comparison To Expectation

- What matched expectation:
- What differed from expectation:
- What new question appeared:

---

## 9. Decision And Next Action

### Decision

- [ ] keep baseline
- [ ] promote variant
- [ ] run follow-up experiments
- [ ] stop this line of work
- [ ] defer

### Decision Rationale

- Why this decision was made:

### Next Actions

| Action | Owner | Due Date | Status |
|---|---|---|---|
| design follow-up experiment |  |  | pending |
| clean up code |  |  | pending |
| write report material |  |  | pending |

---

## 10. Summary For Others

### Short Summary

> Summarize this experiment in 3 to 5 sentences so someone else can understand what was done and what the conclusion was.

### Key Numbers

- baseline:
- best variant:
- improvement:
- trade-off:

### Risks / Caveats

- limited sample size
- reproduced only in a narrow setup
- needs further verification

---

## 11. Publication Package

### What To Share

- [ ] key result table
- [ ] representative figure
- [ ] reproducible run command
- [ ] config used
- [ ] key log summary
- [ ] decision statement

### Audience

- internal research / engineering team
- reviewer
- external audience

### Release Format

- [ ] PR description
- [ ] issue comment
- [ ] internal memo
- [ ] markdown report
- [ ] slide deck
- [ ] blog / external post

### Publish-ready Summary

```text
Problem:
Approach:
Result:
Interpretation:
Decision:
```

---

## 12. Archive Checklist

- [ ] final document updated
- [ ] raw logs preserved
- [ ] raw results preserved
- [ ] figures and tables saved
- [ ] related code commits organized
- [ ] follow-up actions recorded
- [ ] publish materials updated

---

## Appendix A. Suggested Directory Layout

```text
experiments/
  YYYY-MM-DD_<experiment_name>/
    README.md
    configs/
    scripts/
    logs/
    results/
    figures/
    publish/
```

---

## Appendix B. Minimal Per-run Record

Every run should keep at least the following:

| Item | Value |
|---|---|
| run_id |  |
| commit_sha |  |
| config |  |
| command |  |
| seed |  |
| machine |  |
| start_time |  |
| end_time |  |
| result_file |  |
| log_file |  |
| final_status |  |
| one-line note |  |
