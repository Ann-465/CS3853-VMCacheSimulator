from collections import deque

class PhysicalMemoryManager:
    #Figure out the available physical pages
    def __init__(self, physical_pages, pages_for_system, user_pages):
        self.total_pages = physical_pages
        self.system_pages = pages_for_system
        self.user_pages = user_pages

        # a list of unsused physical pages available for allocation
        self.free_pages = deque(range(self.system_pages, self.total_pages))

        # a dictionary mapping allocated physical pages to their owners (process_id, virtual_page)
        self.allocated = {}
        # a queue to track the order of allocated pages for replacement
        self.replacement_queue = deque()

        self.pages_from_free = 0 # times when a virtual page is mapped to a physical page not currently in used
        self.page_faults = 0 # times when no physical page is available and must be swapped with one in used

#Allocate physical pages
    def allocate_page(self, process_id, virtual_page):
        if self.free_pages: # if there are free pages available, allocate physical page from the list of free pages
            physical_page = self.free_pages.popleft()

            self.allocated[physical_page] = (process_id, virtual_page)

            self.replacement_queue.append(physical_page)
            self.pages_from_free += 1

            return physical_page, None
        
        # Inside allocate_page(), after the free-page check
        return self.round_robin(process_id, virtual_page) # if the physical memo is full, use Round robin replacement

    def round_robin (self, new_process_id, new_virtual_page): #replacement policy, 
        # it selects the next position in a circular order whenever a replacement is necessary.
        physical_page = self.replacement_queue.popleft()

        old_page = self.allocated[physical_page] #get the old page that is being replaced

        self.page_faults += 1 

        self.allocated[physical_page] = (new_process_id, new_virtual_page)

        self.replacement_queue.append(physical_page)

        return physical_page, old_page
    
    def release_page(self, process_id):
        released = []

        # find all physical pages allocated to the given process_id and release them
        for physical_page, id in list(self.allocated.items()):
            if id[0] == process_id:
                released.append(physical_page)
                del self.allocated[physical_page]

        #remve the released pages from the replacement queue
        released_set = set(released)
        self.replacement_queue = deque(page for page in self.replacement_queue if page not in released_set)

        #return them to self.free_pages
        self.free_pages.extend(released)
        return released

    def get_page_from_free(self):
        return self.pages_from_free

    def get_page_faults(self):
        return self.page_faults