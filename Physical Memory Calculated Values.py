def physical_pages(memory):
    memory *= 1024
    pages = memory / 4
    return pages
    
def pages_system(pages, percent):
    percent /= 100
    system = pages * percent
    return system

def page_table_entry():
    entry = 0
    return entry

def ram_page_table():
    ram = 0
    return ram