import math

def physical_pages(memory):
    memory *= 1024
    pages = memory / 4
    return pages
    
def pages_system(pages, percent):
    percent /= 100
    system = pages * percent
    return system

def page_table_entry(memory, page_size):
    physical_address_bits = math.log2(memory*1024)
    page_offset_bits = math.log2(page_size)
    physical_frame_bits = physical_address_bits - page_offset_bits + 1
    return physical_frame_bits

def ram_page_table():
    ram = 0
    return ram
