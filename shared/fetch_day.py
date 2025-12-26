import sys
import os
import urllib.request
import urllib.error
import re
from html.parser import HTMLParser
from shared.utils import read_input, SESSION_COOKIE

class AoCHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.output = []
        self.in_code = False
        self.in_pre = False

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.output.append('\n\n')
        elif tag == 'pre':
            self.in_pre = True
            self.output.append('\n\n```\n')
        elif tag == 'code':
            self.in_code = True
            if not self.in_pre:
                self.output.append('`')
        elif tag == 'h2':
            self.output.append('\n## ')
        elif tag == 'li':
            self.output.append('\n- ')
        elif tag == 'em':
            self.output.append('**')

    def handle_endtag(self, tag):
        if tag == 'pre':
            self.in_pre = False
            self.output.append('\n```\n')
        elif tag == 'code':
            self.in_code = False
            if not self.in_pre:
                self.output.append('`')
        elif tag == 'h2':
            self.output.append('\n')
        elif tag == 'em':
            self.output.append('**')

    def handle_data(self, data):
        if self.in_pre:
            self.output.append(data)
        else:
            # Collapse whitespace (newlines -> space) for normal text
            data = re.sub(r'\s+', ' ', data)
            self.output.append(data)

    def get_markdown(self):
        text = "".join(self.output).strip()
        # Ensure max 2 newlines (one blank line) between blocks
        return re.sub(r'\n{3,}', '\n\n', text)

def fetch_puzzle(day: int, year: int = 2025, part: int = 1) -> str:
    """Fetches puzzle description (markdown) for Day X, Part Y."""
    url = f"https://adventofcode.com/{year}/day/{day}"
    req = urllib.request.Request(url)
    req.add_header("Cookie", SESSION_COOKIE)
    req.add_header("User-Agent", "github.com/google-deepmind/antigravity via python-urllib")

    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        raise RuntimeError(f"Failed to fetch puzzle: {e}")

    # Find all <article class="day-desc">...</article>
    matches = re.findall(r'<article class="day-desc">(.*?)</article>', html, re.DOTALL)

    if len(matches) < part:
        raise ValueError(f"Part {part} not found. Is Part 1 complete?")

    puzzle_html = matches[part - 1]

    parser = AoCHTMLParser()
    parser.feed(puzzle_html)
    return parser.get_markdown()

def main():
    if len(sys.argv) != 2:
        print("Usage: python -m shared.fetch_day <day>")
        sys.exit(1)

    day = int(sys.argv[1])
    day_str = f"day{day:02d}"

    # Ensure directory exists
    os.makedirs(day_str, exist_ok=True)

    # 1. Fetch Input (handled by read_input)
    print(f"Checking input for Day {day}...")
    try:
        # read_input will fetch and save if not present
        read_input(day)
        print("Input ready.")
    except Exception as e:
        print(f"Error fetching input: {e}")

    # 2. Fetch Puzzle Part 1
    p1_file = os.path.join(day_str, "puzzle1.md")
    if not os.path.exists(p1_file):
        print(f"Fetching puzzle Part 1 for Day {day}...")
        try:
            markdown = fetch_puzzle(day, part=1)
            with open(p1_file, "w") as f:
                f.write(markdown)
            print(f"Saved {p1_file}")
        except Exception as e:
            print(f"Error fetching puzzle part 1: {e}")
    else:
        print(f"{p1_file} already exists.")

    # 3. Fetch Puzzle Part 2
    p2_file = os.path.join(day_str, "puzzle2.md")
    if not os.path.exists(p2_file):
        print(f"Fetching puzzle Part 2 for Day {day}...")
        try:
            markdown = fetch_puzzle(day, part=2)
            with open(p2_file, "w") as f:
                f.write(markdown)
            print(f"Saved {p2_file}")
        except Exception as e:
            # It's expected to fail if Part 1 isn't done or Part 2 doesn't exist yet
            print(f"Could not fetch puzzle part 2 (maybe not unlocked yet?): {e}")
    else:
        print(f"{p2_file} already exists.")

if __name__ == "__main__":
    main()
