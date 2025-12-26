# Advent of Code 2025

[![AoC](https://img.shields.io/badge/Advent%20of%20Code-2025-blue.svg)](https://adventofcode.com/2025)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

Python solutions for Advent of Code 2025.

## Performance

The project focuses on fast and parallel execution, running all solutions in under 3 seconds.

- **Total SLOC**: 409 lines
- **Parallel Runtime**: ~2.5 seconds (Combined)
- **Status**: All 23 parts verified against test and real inputs.

### Execution Results

| Day | Part | SLOC | Test Time | Real Time | Result |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Day 1 | 1 | 6 | 0.0000s | 0.0011s | ✅ [REDACTED] |
| Day 1 | 2 | 11 | 0.0000s | 0.0028s | ✅ [REDACTED] |
| Day 2 | 1 | 9 | 0.0314s | 0.0502s | ✅ [REDACTED] |
| Day 2 | 2 | 16 | 0.0631s | 0.0896s | ✅ [REDACTED] |
| Day 3 | 1 | 15 | 0.0000s | 0.0016s | ✅ [REDACTED] |
| Day 3 | 2 | 2 | 0.0001s | 0.0029s | ✅ [REDACTED] |
| Day 4 | 1 | 4 | 0.0001s | 0.0354s | ✅ [REDACTED] |
| Day 4 | 2 | 18 | 0.0002s | 0.0521s | ✅ [REDACTED] |
| Day 5 | 1 | 6 | 0.0001s | 0.0035s | ✅ [REDACTED] |
| Day 5 | 2 | 4 | 0.0000s | 0.0002s | ✅ [REDACTED] |
| Day 6 | 1 | 17 | 0.0001s | 0.0037s | ✅ [REDACTED] |
| Day 6 | 2 | 2 | 0.0001s | 0.0059s | ✅ [REDACTED] |
| Day 7 | 1 | 12 | 0.0000s | 0.0010s | ✅ [REDACTED] |
| Day 7 | 2 | 12 | 0.0000s | 0.0017s | ✅ [REDACTED] |
| Day 8 | 1 | 10 | 0.0002s | 0.5083s | ✅ [REDACTED] |
| Day 8 | 2 | 9 | 0.0002s | 0.5046s | ✅ [REDACTED] |
| Day 9 | 1 | 7 | 0.0001s | 0.0446s | ✅ [REDACTED] |
| Day 9 | 2 | 42 | 0.0001s | 0.2201s | ✅ [REDACTED] |
| Day 10 | 1 | 39 | 0.0002s | 0.0081s | ✅ [REDACTED] |
| Day 10 | 2 | 61 | 0.0009s | 0.7327s | ✅ [REDACTED] |
| Day 11 | 1 | 6 | 0.0001s | 0.0010s | ✅ [REDACTED] |
| Day 11 | 2 | 6 | 0.0000s | 0.0024s | ✅ [REDACTED] |
| Day 12 | 1 | 95 | 0.7363s | 0.2483s | ✅ [REDACTED] |
| **Total** | | **409** | **0.8333s** | **2.5220s** | |

## Usage

Solutions are executed via the `runner.py` script.

### Run All Solutions
```bash
python3 runner.py -p
```

### Run a Specific Day
```bash
python3 runner.py 12 -p
```

### Scaffold a New Day
The `shared/fetch_day.py` utility automates the creation of daily directories, downloads puzzle inputs, and converts puzzle descriptions to Markdown.

```bash
python3 -m shared.fetch_day 13
```

This will:
1. Create `day13/` directory.
2. Download `input.txt` (requires a valid `SESSION_COOKIE` in `shared/utils.py`).
3. Fetch and convert the puzzle description to `day13/puzzle1.md`.
4. Fetch Part 2 description as `day13/puzzle2.md` once Part 1 is unlocked.

## Project Structure

- `dayXX/`: Daily solution directories.
  - `part1.py`, `part2.py`: Solvers.
  - `example_input.txt`: Data for verification.
- `shared/`: Utilities and input fetching logic.
- `runner.py`: Execution entry point.
- `results.json`: Solution values for regression testing.

## Implementation Details

- **Dependencies**: Python standard library only.
- **Concurrency**: `ProcessPoolExecutor` for multi-core scaling.
