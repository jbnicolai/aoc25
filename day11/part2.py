from day11.part1 import count_paths
from shared.utils import parse_graph_adj

def solve(v):
    g = parse_graph_adj(v)
    return (count_paths(g,'svr','dac',{})*count_paths(g,'dac','fft',{})*count_paths(g,'fft','out',{}) +
            count_paths(g,'svr','fft',{})*count_paths(g,'fft','dac',{})*count_paths(g,'dac','out',{}))
