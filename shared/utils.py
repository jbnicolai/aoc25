import os
import urllib.request
import urllib.error
import re

SESSION_COOKIE = "session=53616c7465645f5f62e962be88ebb2bfff374106913565bf3636fc07b3ebdd6b507fa223990c304900962a7013dda4b6980403fc55d348d1148f17925f0be61b"

def read_input(day: int, year: int = 2025, file_name: str = "input.txt") -> str:
    """Reads input file for Day X, fetching from web if needed."""
    day_str = f"day{day:02d}"

    # Determine potential paths (root-relative or day-dir-relative)
    paths = [os.path.join(day_str, file_name)]
    if os.path.basename(os.getcwd()) == day_str:
        paths.append(file_name)

    # Check if file exists locally
    for path in paths:
        if os.path.exists(path):
            return open(path, "r").read().strip()

    # If not found and it's the standard input, fetch it
    if file_name == "input.txt":
        print(f"Fetching input for day {day}...")
        url = f"https://adventofcode.com/{year}/day/{day}/input"
        req = urllib.request.Request(url)
        req.add_header("Cookie", SESSION_COOKIE)
        req.add_header("User-Agent", "github.com/google-deepmind/antigravity via python-urllib")

        try:
            with urllib.request.urlopen(req) as response:
                content = response.read().decode("utf-8").strip()
        except urllib.error.URLError as e:
            raise RuntimeError(f"Failed to fetch input: {e}")

        # Save to the first valid path (prefer root-relative)
        save_path = paths[-1] if len(paths) > 1 else paths[0]

        # Ensure dir exists if saving to day_str/input.txt
        if os.path.dirname(save_path):
            os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with open(save_path, "w") as f:
            f.write(content)
        print(f"Saved input to {save_path}")
        return content

    raise FileNotFoundError(f"Input file '{file_name}' not found for day {day}")

def parse_lines(content: str) -> list[str]:
    return content.splitlines()

def parse_ints(content: str) -> list[int]:
    return [int(line) for line in content.splitlines() if line.strip()]

def parse_pts(v):
    """Extracts tuples of all integers from each line."""
    return [tuple(extract_ints(l)) for l in v.strip().splitlines() if l.strip()]

def extract_ints(content: str) -> list[int]:
    """Extracts all integers (including negative) from a string."""
    return [int(x) for x in re.findall(r'-?\d+', content)]

def parse_range_list(content: str) -> list[tuple[int, int]]:
    """
    Parses a string of comma-separated ranges (e.g., "1-2,5-10")
    into a list of (start, end) tuples.
    """
    ranges = []
    # Handle single line input, stripping newlines
    content = content.replace('\n', '').strip()
    if not content:
        return []

    for part in content.split(','):
        start_str, end_str = part.split('-')
        ranges.append((int(start_str), int(end_str)))
    return ranges

DIRECTIONS_4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
DIRECTIONS_8 = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1)
]

def in_bounds(r: int, c: int, rows: int, cols: int) -> bool:
    """Checks if (r, c) is within grid bounds [0, rows) x [0, cols)."""
    return 0 <= r < rows and 0 <= c < cols

def parse_grid(content: str) -> list[list[str]]:
    """Parses input into a 2D grid (list of lists of characters)."""
    return [list(line) for line in content.splitlines() if line.strip()]

def get_neighbors(r: int, c: int, rows: int, cols: int, diag: bool = False) -> list[tuple[int, int]]:
    """Returns valid neighbor coordinates in a grid."""
    from shared.utils import DIRECTIONS_4, DIRECTIONS_8
    dirs = DIRECTIONS_8 if diag else DIRECTIONS_4
    neighbors = []
    for dr, dc in dirs:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbors.append((nr, nc))
    return neighbors

class UnionFind:
    """Standard Disjoint Set Union (DSU) implementation."""
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n
        self.num_components = n

    def find(self, i: int) -> int:
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i: int, j: int) -> bool:
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            # Union by size
            if self.size[root_i] < self.size[root_j]:
                root_i, root_j = root_j, root_i
            self.parent[root_j] = root_i
            self.size[root_i] += self.size[root_j]
            self.num_components -= 1
            return True
        return False

def parse_graph_adj(content: str) -> dict[str, list[str]]:
    """
    Parses graph adjacency list from string: 'node: neighbor1 neighbor...'.
    Returns a dict mapping node -> list of neighbors.
    """
    from collections import defaultdict
    graph = defaultdict(list)
    for line in content.splitlines():
        if not line.strip():
            continue
        parts = line.split(':')
        node = parts[0].strip()
        if len(parts) > 1 and parts[1].strip():
            neighbors = parts[1].strip().split()
            graph[node].extend(neighbors)
    return graph

def merge_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Sorts and merges overlapping or adjacent ranges."""
    if not ranges: return []
    ranges.sort(key=lambda x: x[0])
    merged = []
    current_start, current_end = ranges[0]
    for i in range(1, len(ranges)):
        next_start, next_end = ranges[i]
        if next_start <= current_end + 1:
            current_end = max(current_end, next_end)
        else:
            merged.append((current_start, current_end))
            current_start, current_end = next_start, next_end
    merged.append((current_start, current_end))
    return merged
