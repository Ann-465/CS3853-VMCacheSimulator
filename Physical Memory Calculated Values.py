import math

def physical_pages(memory):
    memory *= 1024
    pages = memory / 4
    return int(pages)
    
def pages_system(pages, percent):
    percent /= 100
    system = pages * percent
    return int(system)

def page_table_entry(memory, page_size):
    physical_address_bits = math.log2(memory*1024)
    page_offset_bits = math.log2(page_size)
    physical_frame_bits = physical_address_bits - page_offset_bits + 1
    return int(physical_frame_bits)

def ram_page_table(cache, files, page_table_entry):
    cache *= 1024
    total_entries = cache * files
    total_space = total_entries * page_table_entry
    ram = total_space / 8
    return int(ram)
