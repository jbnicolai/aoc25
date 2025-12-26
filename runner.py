import importlib
import os
import sys
import time
import json
import argparse
from concurrent.futures import ProcessPoolExecutor
from shared.utils import read_input

def get_all_results():
    """Loads validated results from results.json if it exists."""
    path = "results.json"
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}

def run_part(day_part_data):
    """Worker function to run a single part solution."""
    day, part, expectations = day_part_data
    day_str = f"day{day:02d}"
    module_name = f"{day_str}.part{part}"

    result_entry = {
        "day": day,
        "part": part,
        "test_time": 0.0,
        "real_time": 0.0,
        "sloc": 0,
        "solution": "N/A",
        "status": "Skipped"
    }

    try:
        module = importlib.import_module(module_name)
        # Get source lines of code (SLOC)
        src_path = os.path.join(day_str, f"part{part}.py")
        if os.path.exists(src_path):
            with open(src_path, "r") as f:
                result_entry["sloc"] = len([l for l in f if l.strip()])
    except ImportError:
        return result_entry

    print(f"Executing {day_str}, part {part}")

    # Test
    expected_test = expectations.get("test") if expectations else None
    if expected_test is None:
        expected_test = getattr(module, 'TEST_RESULT', None)

    if expected_test is not None:
        try:
            example_file = f"example_input_part{part}.txt"
            if not os.path.exists(os.path.join(day_str, example_file)):
                example_file = "example_input.txt"

            example_data = read_input(day, file_name=example_file)
            test_kwargs = getattr(module, 'TEST_KWARGS', {})

            start_time = time.perf_counter()
            test_result = module.solve(example_data, **test_kwargs)
            end_time = time.perf_counter()
            result_entry["test_time"] = end_time - start_time

            if str(test_result) != str(expected_test):
                print(f"  Test: Failed {day_str} P{part} ({result_entry['test_time']:.4f}s)")
                print(f"    Expected: {expected_test}, Got: {test_result}")
        except Exception as e:
            print(f"  Test: Error {day_str} P{part} ({e})")

    # Real Solution
    try:
        real_data = read_input(day)
        real_kwargs = getattr(module, 'REAL_KWARGS', {})

        start_time = time.perf_counter()
        solution = module.solve(real_data, **real_kwargs)
        end_time = time.perf_counter()

        result_entry["real_time"] = end_time - start_time
        result_entry["solution"] = str(solution)

        expected_real = expectations.get("real") if expectations else None
        if expected_real is None:
            expected_real = getattr(module, 'REAL_RESULT', None)

        if expected_real is not None:
            if str(solution) == str(expected_real):
                 result_entry["status"] = "Passed"
            else:
                 print(f"  Result: Failed {day_str} P{part}. Expected: {expected_real}, Got: {solution}")
                 result_entry["status"] = "Failed"
        else:
             result_entry["status"] = "Unknown"

    except Exception as e:
        print(f"  Solution: Error {day_str} P{part} ({e})")
        result_entry["status"] = "Error"
        result_entry["solution"] = str(e)

    return result_entry

def print_summary(results):
    print("\n" + "=" * 90)
    print(f"{'Day':<6} | {'Part':<5} | {'SLOC':<6} | {'Test Time':<12} | {'Real Time':<12} | {'Result':<10}")
    print("-" * 90)

    total_test_time = 0.0
    total_real_time = 0.0
    total_sloc = 0

    for res in sorted(results, key=lambda x: (x['day'], x['part'])):
        day = f"Day {res['day']}"
        part = str(res['part'])
        sloc = f"{res['sloc']}"
        test_t = f"{res['test_time']:.4f}s"
        real_t = f"{res['real_time']:.4f}s"

        total_test_time += res['test_time']
        total_real_time += res['real_time']
        total_sloc += res['sloc']

        status_icon = "❓"
        if res['status'] == "Passed": status_icon = "✅"
        elif res['status'] == "Failed": status_icon = "❌"
        elif res['status'] == "Error": status_icon = "⚠️"
        elif res['status'] == "Missing": status_icon = "❌"

        result_str = f"{status_icon} {res['solution']}"
        print(f"{day:<6} | {part:<5} | {sloc:<6} | {test_t:<12} | {real_t:<12} | {result_str:<10}")

    print("-" * 90)
    avg_sloc = total_sloc / len(results) if results else 0
    print(f"{'TOTAL':<6} | {'':<5} | {total_sloc:<6} | {total_test_time:<12.4f}s | {total_real_time:<12.4f}s | Avg SLOC: {avg_sloc:.1f}")
    print("=" * 90)

def main():
    parser = argparse.ArgumentParser(description="Advent of Code Runner")
    parser.add_argument('days', metavar='N', type=int, nargs='*', help='days to run')
    parser.add_argument('-p', '--parallel', action='store_true', help='run solutions in parallel')
    args = parser.parse_args()

    all_expectations = get_all_results()
    days = args.days if args.days else range(1, 26)

    tasks = []
    for day in days:
        if not os.path.exists(f"day{day:02d}"): continue
        day_expectations = all_expectations.get(str(day), {})
        for part in [1, 2]:
            tasks.append((day, part, day_expectations.get(str(part), {})))

    all_results = []
    if args.parallel:
        with ProcessPoolExecutor() as executor:
            all_results = list(executor.map(run_part, tasks))
    else:
        for t in tasks:
            all_results.append(run_part(t))
            print("-" * 20)

    all_results = [r for r in all_results if r['status'] != "Skipped"]
    if all_results:
        print_summary(all_results)
    else:
        print("No solutions found.")

if __name__ == "__main__":
    main()
