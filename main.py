import argparse
import os
from contextlib import redirect_stdout

from cache_calculate import (
    numBlocks, tagsize, numRows, indexsize,
    overheadsize, implement_mem_size, cost
)

from PhysicalMemoryCalculatedValues import (
    physical_pages, pages_system,
    page_table_entry, ram_page_table
)

from output import (
    print_header,
    print_input_parameters,
    print_cache_calculated_values,
    print_physical_memory_values,
    print_virtual_memory_simulation_results,
    print_virtual_pages_mapped,
    print_page_table_usage_per_process
)

import page_table
from pages_available import (
    physical_pages_used_by_system,
    pages_available_to_user
)

from page_table import PageTable

from virtual_memo import PhysicalMemoryManager

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

def main():
    args = parse_arguments()

    cache_size = args.s
    block_size = args.b
    associativity = args.a
    replacement_policy = args.r.upper()
    physical_memory = args.p
    time_slice = args.n
    system_percent = args.u
    trace_files = args.f

    # Validate inputs
    if cache_size not in [2**i for i in range(3, 14)]:
        raise ValueError("Invalid cache size")

    if block_size not in [8, 16, 32, 64]:
        raise ValueError("Invalid block size")

    if associativity not in [1, 2, 4, 8, 16]:
        raise ValueError("Invalid associativity")

    if replacement_policy not in ["RR", "RND"]:
        raise ValueError("Invalid replacement policy")

    if physical_memory not in [128, 256, 512, 1024, 2048, 4096]:
        raise ValueError("Invalid physical memory")

    if not 0 <= system_percent <= 100:
        raise ValueError("Invalid system memory percentage")

    if time_slice != -1 and time_slice < 1:
        raise ValueError("Invalid time slice")

    if not 1 <= len(trace_files) <= 3:
        raise ValueError("Must provide 1 to 3 trace files")

    # Cache calculations
    total_blocks = numBlocks(cache_size, block_size)
    total_rows = numRows(total_blocks, associativity)
    index_bits = int(indexsize(total_rows))
    tag_bits = int(tagsize(
        physical_memory, block_size, index_bits
    ))

    overhead_bytes = int(overheadsize(
        total_blocks, tag_bits
    ))

    implementation_bytes = implement_mem_size(
        cache_size, overhead_bytes
    )

    total_cost = cost(implementation_bytes)

    # Physical memory calculations
    num_physical_pages = physical_pages(physical_memory)

    num_system_pages = pages_system(
        num_physical_pages, system_percent
    )

    pte_bits = page_table_entry(physical_memory, 4096)

    page_table_bytes = ram_page_table(
        cache_size, len(trace_files), pte_bits
    )
    
    pages_used_by_system = physical_pages_used_by_system(num_physical_pages, system_percent)
    
    pages_available_user = pages_available_to_user(num_physical_pages, num_system_pages)
    
    page_tables = [PageTable() for _ in trace_files]
    
    memory_manager = PhysicalMemoryManager(num_physical_pages, num_system_pages, 
                                           pages_available_user)
    page_table_hits = 0
    
    virtual_pages_mapped = 0
    
    for process_id, trace_file in enumerate(trace_files):
        
        page_table = page_tables[process_id]
        
        with open(trace_file, "r") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
            
        for i in range(0, len(lines), 2):
            if i + 1 >= len(lines):
                break
            
            eip_parts = lines[i].split()
            mem_parts = lines[i + 1].split()
            
            if len(eip_parts) < 3 or len(mem_parts) < 6:
                continue
            
            address = []
            
            address.append(int(eip_parts[2], 16))
            
            if mem_parts[2] != "--------":
                address.append(int(mem_parts[1], 16))
            
            if mem_parts[5] != "--------":
                address.append(int(mem_parts[4], 16))
                
            for addr in address:
                virtual_page = page_table.get_page_number(addr)
                
                physical_page = page_table.lookup(virtual_page)
                
                if physical_page is not None:
                    page_table_hits += 1
                else:
                    physical_page, old_page = memory_manager.allocate_page(process_id, virtual_page)
                    
                    if old_page is not None:
                        old_process_id, old_virtual_page = old_page
                        old_process_table = page_tables[old_process_id]
                        old_process_table.unmap_page(old_virtual_page)
                        
                    page_table.map_page(virtual_page, physical_page)
                    
                    virtual_pages_mapped += 1
                    
                    
                        
                        

    # Print results
    with open("output.txt", "w") as f:
        with redirect_stdout(f):
            print_header(2, trace_files)
            policy_name = (
                    "Round Robin" if replacement_policy == "RR"
                    else "Random"
                )
            
            print_input_parameters(
                    cache_size, block_size, associativity,
                    policy_name, physical_memory,
                    system_percent, time_slice
                )
            
            print_cache_calculated_values(
                    total_blocks, tag_bits, index_bits,
                    total_rows, overhead_bytes,
                    implementation_bytes, total_cost
                )
            
            print_physical_memory_values(
                    num_physical_pages, num_system_pages,
                    pte_bits, page_table_bytes
                )
            
            print_virtual_memory_simulation_results(pages_used_by_system, 
                                                    pages_available_user)
            
            print_virtual_pages_mapped(virtual_pages_mapped, page_table_hits,
                                       memory_manager.pages_from_free, memory_manager.page_faults)
            
            for num, trace_file in enumerate(trace_files):
                page_table = page_tables[num]
                used_page = page_table.used_entries()
                percent_used = page_table.usage_percentage()
                page_wasted = page_table.wasted_bytes(pte_bits)
                print_page_table_usage_per_process(num, trace_file, used_page, 
                                                   percent_used, page_wasted)


    
#     instruction_length = []
#     value_addresses = []
# #Parsing through each trace file and placed inside instruction_length and value_addresses lists
#     for trace_file in trace_files:
#         print(f"Processing trace file: {trace_file}")
#         with open(trace_file, "r") as f:
#             trace_data = f.readlines()
#         for i, line in enumerate(trace_data):
#             if i % 3 == 0:
#                 components = line.strip().split()
#                 instruction_length.append(int(components[1][1:3]))
#                 value_addresses.append(components[2])
#             elif i % 3 == 1:
#                 components = line.strip().split()
#                 if components[2] != "--------":
#                     instruction_length.append(int(4))
#                     value_addresses.append(components[1])
#                 if components[5] != "--------":
#                     instruction_length.append(int(4))
#                     value_addresses.append(components[4])


if __name__ == "__main__":
    main()
