# Advent of Code 2025

[![AoC](https://img.shields.io/badge/Advent%20of%20Code-2025-blue.svg)](https://adventofcode.com/2025)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

Python solutions for Advent of Code 2025.

## Performance

The project focuses on parallel execution and low Source Lines of Code (SLOC).

- **Total SLOC**: 409 lines
- **Parallel Runtime**: ~2.4 seconds (Combined)
- **Status**: All 23 parts verified against test and real inputs.

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
- **Interface**: Consolidated `solve(v)` signature across all days.
