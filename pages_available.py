def physical_pages_used_by_system(physical_pages, physical_mem_used):
    return physical_pages * (physical_mem_used / 100)

def pages_available_to_user(physical_pages, pages_for_system):
    return physical_pages - pages_for_system