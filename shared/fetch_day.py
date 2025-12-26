import sys, os, urllib.request as ur, re
from html.parser import HTMLParser
from shared.utils import read_input, SESSION_COOKIE

class AoCP(HTMLParser):
    def __init__(self):
        super().__init__(); self.o, self.c, self.p = [], 0, 0
        self.m = {'p':('\n\n',''), 'pre':('\n\n```\n','\n```\n'), 'code':('`','`'), 'h2':('\n## ','\n'), 'li':('\n- ',''), 'em':('**','**')}
    def handle_starttag(self, t, a):
        if t in self.m: self.o.append(self.m[t][0])
        if t == 'code': self.c = 1
        if t == 'pre': self.p = 1
    def handle_endtag(self, t):
        if t in self.m: self.o.append(self.m[t][1])
        if t == 'code': self.c = 0
        if t == 'pre': self.p = 0
    def handle_data(self, d): self.o.append(d if self.p else re.sub(r'\s+', ' ', d))
    def get(self): return re.sub(r'\n{3,}', '\n\n', "".join(self.o).strip())

def fetch(d, y=2025, p=1):
    u = f"https://adventofcode.com/{y}/day/{d}"
    r = ur.Request(u, headers={"Cookie": SESSION_COOKIE, "User-Agent": "aoc-fetch"})
    with ur.urlopen(r) as b: h = b.read().decode()
    ms = re.findall(r'<article class="day-desc">(.*?)</article>', h, re.DOTALL)
    if len(ms) < p: return None
    ps = AoCP(); ps.feed(ms[p-1]); return ps.get()

if __name__ == "__main__":
    if len(sys.argv) < 2: print("Usage: fetch_day <day>"); sys.exit(1)
    d = int(sys.argv[1]); ds = f"day{d:02d}"; os.makedirs(ds, exist_ok=True)
    try: read_input(d); print("Input ready.")
    except Exception as e: print(f"Input error: {e}")
    for p in [1, 2]:
        fn = os.path.join(ds, f"puzzle{p}.md")
        if not os.path.exists(fn):
            try:
                md = fetch(d, p=p)
                if md: 
                    with open(fn, "w") as f: f.write(md)
                    print(f"Saved {fn}")
            except Exception as e: print(f"Part {p} error: {e}")
