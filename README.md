# Advent of Code 2025

[![AoC](https://img.shields.io/badge/Advent%20of%20Code-2025-blue.svg)](https://adventofcode.com/2025)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

Clean, performant, and hyper-optimized Python solutions for Advent of Code 2025.

## Performance Summary

All solutions are verified to pass against both example and real inputs. The project primary focus is on sub-second parallel execution and minimal source lines of code (SLOC).

| Day | Part | SLOC | Test Time | Real Time | Result |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Total** | | **~600** | **<1s** | **~2.5s** | ✅ All Passed |

## Usage

Execution is strictly enforced via the central `runner.py` script. Single-day execution is supported via explicit arguments.

### Run All Solutions
```bash
python3 runner.py -p
```

### Run a Specific Day
```bash
python3 runner.py 12 -p
```

## Project Structure

- `dayXX/`: Daily solution directories.
  - `part1.py`: Part 1 solver.
  - `part2.py`: Part 2 solver.
  - `input.txt`: Puzzle input.
  - `puzzleX.md`: Puzzle descriptions.
- `shared/`: Centralized utilities.
- `runner.py`: The only entry point for execution.
- `results.json`: Validated results for verification.

## Architecture

- **Standard Library Only**: No external dependencies.
- **Pure Python**: Highly optimized algorithmic approaches.
- **Parallelized**: Uses `ProcessPoolExecutor` for maximum performance.
- **Dense Logic**: Aggressively compressed SLOC while maintaining legibility.
