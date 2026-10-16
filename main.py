import argparse
import os

def parse_arguments():
    parser = argparse.ArgumentParser(description='VM Cache Simulator')
    parser.add_argument('-s', type=int, required=True, help='Cache size in bytes(8KB to 8MB)')
    parser.add_argument('-b', type=int, required=True, help='Block size in bytes(8,16, 32, 64)')
    parser.add_argument('-a', type=int, required=True, help='Associativity (direct-mapped, 2-way, 4-way, 8-way, 16-way)')
    parser.add_argument('-r', type=str, required=True, help='Replacement policy (Round Robin, Random)')
    parser.add_argument('-p', type=int, required=True, help='Physical memory size in bytes(128MB to 4096MB)')
    parser.add_argument('-n', type=int, required=True, help='Instruction count (1 to -1)')
    parser.add_argument('-u', type=int, required=True, help='Percentage of used memory (0 to 100)')

    parser.add_argument('-f', action="append", required=True, help='Trace files(s)')
    return parser.parse_args()

args = parse_arguments()
chache_size = args.s
block_size = args.b
associativity = args.a
replacement_policy = args.r
physical_memory_size = args.p
instruction_count = args.n
percentage_used_memory = args.u
trace_files = args.f