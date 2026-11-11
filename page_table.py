class PageTable:
    PAGE_SIZE = 4096
    MAX_ENTRIES = 524288

    def __init__(self):
        self.entries = {}

    def lookup(self, virtual_page):
        return self.entries.get(virtual_page)

    def map_page(self, virtual_page, physical_page):
        if not isinstance(virtual_page, int) or not 0 <= virtual_page < self.MAX_ENTRIES:
            raise ValueError("Invalid virtual page number")

        if not isinstance(physical_page, int) or physical_page < 0:
            raise ValueError("Invalid physical page number")

        self.entries[virtual_page] = physical_page

    def unmap_page(self, virtual_page):
        return self.entries.pop(virtual_page, None)

    def used_entries(self):
        return len(self.entries)

    def clear(self):
        self.entries.clear()

    def get_page_number(self, virtual_address):
        if not isinstance(virtual_address, int) or not 0 <= virtual_address < 0x80000000:
            raise ValueError("Invalid virtual address")

        return virtual_address // self.PAGE_SIZE

    def usage_percentage(self):
        return (self.used_entries() / self.MAX_ENTRIES) * 100

    def wasted_bytes(self, bits_per_entry):
        unused_entries = self.MAX_ENTRIES - self.used_entries()
        wasted_bits = unused_entries * bits_per_entry
        return wasted_bits // 8