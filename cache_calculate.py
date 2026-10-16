import math

def numBlocks(size, block_size):
    # Calculate the number of blocks needed
    num_blocks = size *1024 // block_size
    return num_blocks

def tagsize(phys_mem, block_size, index_bits):
    # Calculate the number of bits needed for the tag
    physical_address_bits = math.log2(phys_mem * 1024 * 1024)
    block_offset_bits = math.log2(block_size)
    tag_bits = physical_address_bits - block_offset_bits - index_bits
    return tag_bits

def numRows(num_blocks, associativity):
    # Calculate the number of rows in the cache
    num_rows = num_blocks // associativity
    return num_rows

def indexsize(num_rows):
    # Calculate the number of bits needed for the index
    index_bits = math.log2(num_rows)
    return index_bits

def overheadsize(num_blocks, tag_bits):
    # Calculate the overhead size of the cache
    overhead_bits = num_blocks * (tag_bits + 1) / 8 # +1 for valid bit
    return overhead_bits

def implement_mem_size(cache_size, overhead_bits):
    # Calculate the total memory size needed for the cache
    total_mem_size = cache_size * 1024 + overhead_bits
    # convert to KB
    total_mem_size /= 1024
    return total_mem_size

def cost(total_mem_size):
    # Calculate the cost of the cache based on the physical memory and block size
    total_cost = total_mem_size * 0.07
    return total_cost