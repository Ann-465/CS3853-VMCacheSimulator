def print_input_parameters(cache_size, block_size, associativity,
                           replacement_policy, physical_memory,
                           system_percent, time_slice):

    print("***** Cache Input Parameters *****")
    print()

    print(f"{'Cache Size:':<40}{cache_size} KB")
    print(f"{'Block Size:':<40}{block_size} bytes")
    print(f"{'Associativity:':<40}{associativity}")
    print(f"{'Replacement Policy:':<40}{replacement_policy}")
    print(f"{'Physical Memory:':<40}{physical_memory} MB")
    print(f"{'Percent Memory Used by System:':<40}{system_percent:.1f}%")
    print(f"{'Instructions / Time Slice:':<40}{time_slice}")


def print_cache_calculated_values(total_blocks, tag_size, index_size,
                                  total_rows, overhead_size,
                                  implementation_bytes, cost):

    print()
    print("***** Cache Calculated Values *****")
    print()

    print(f"{'Total # Blocks:':<40}{total_blocks}")
    print(f"{'Tag Size:':<40}{tag_size} bits")
    print(f"{'Index Size:':<40}{index_size} bits")
    print(f"{'Total # Rows:':<40}{total_rows}")
    print(f"{'Overhead Size:':<40}{overhead_size} bytes")
    print(f"{'Implementation Memory Size:':<40}{implementation_bytes / 1024:.2f} KB ({implementation_bytes} bytes)")
    print(f"{'Cost:':<40}${cost:.2f} @ $0.07 per KB")



def print_physical_memory_values(physical_pages, system_pages,
                                 pte_size, page_table_ram):

    print()
    print("***** Physical Memory Calculated Values *****")
    print()

    print(f"{'Number of Physical Pages:':<40}{physical_pages}")
    print(f"{'Number of Pages for System:':<40}{system_pages}")
    print(f"{'Size of Page Table Entry:':<40}{pte_size} bits")
    print(f"{'Total RAM for Page Table(s):':<40}{page_table_ram} bytes")


def print_header(team_number, trace_file):

    print(f"Cache Simulator - CS 3853 - Team #{team_number}")
    print()
    print("Trace File(s):")
    for trace_file in trace_file:
        print(trace_file)
    print()
    
def print_virtual_memory_simulation_results(physical_pages_used, pages_available):
    print()
    print("***** VIRTUAL MEMORY SIMULATION RESULTS *****")
    print()
    
    print(f"{'Physical Pages Used By SYSTEM:':<40}{physical_pages_used}")
    print(f"{'Pages Available to User:':<40}{pages_available}")
    print()
    
def print_virtual_pages_mapped(virtual_pages_mapped, page_table_hits, 
                                pages_from_free, total_page_faults):
    print(f"{'Virtual Pages Mapped:':<40}{virtual_pages_mapped}")
    print("\t------------------------------")
    print(f"{'\tPage Table Hits:':<37}{page_table_hits}")
    print()
    print(f"{'\tPages from Free:':<37}{pages_from_free}")
    print()
    print(f"{'\tTotal Page Faults:':<37}{total_page_faults}")
    print()
    print("Page Table Usage Per Process:")
    print("------------------------------")
    
def print_page_table_usage_per_process(num, file,used_page, percent_used, page_wasted):
    print(f"[{num}] {file}:")
    print(f"\tUsed Page Table Entries: {used_page} ( {percent_used}%)")
    print(f"\tPage Table Wasted: {page_wasted} bytes")
    print()
    

import sys

def save_output(filename):
    original_stdout = sys.stdout

    with open(filename, "w") as file:

        class DualOutput:
            def write(self, text):
                original_stdout.write(text)
                file.write(text)

            def flush(self):
                original_stdout.flush()
                file.flush()

        sys.stdout = DualOutput()

        try:
            print_header("2", "A-9_new_trunk.trc")
            print_input_parameters(512, 16, 4, "Round Robin", 1024, 75, 100)
            print_cache_calculated_values(32768, 13, 13, 8192, 57344, 581632, 39.76)
            print_physical_memory_values(262144, 196608, 19, 3735552)

        finally:
            sys.stdout = original_stdout

    
if __name__ == "__main__":
    save_output("Team_2_Milestone1_TEST.txt")
