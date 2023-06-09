from typing import List
from access_patterns import generate_interleaved_pattern, generate_markdown_table, generate_random_pattern, generate_sequential_pattern, generate_strided_pattern


class StridePrefetcher:
    def __init__(self):
        self.prev_address: int = None
        self.stride: int = None
        self.prefetch_hits = 0
        self.prefetch_requests = 0

    def access(self, address: int):
        if self.prev_address is not None:
            current_stride = address - self.prev_address
            if self.stride is not None:
                prefetch_address = address + self.stride
                self.prefetch(prefetch_address)

            self.stride = current_stride

        self.prev_address = address

    def prefetch(self, prefetch_address: int):
        self.prefetch_requests += 1
        print(f"Prefetching address: {prefetch_address}")

    def report_prefetch_hit(self):
        self.prefetch_hits += 1

    def get_accuracy(self) -> float:
        if self.prefetch_requests == 0:
            return 0
        return self.prefetch_hits / self.prefetch_requests
    
def simulate_memory_accesses(prefetcher: StridePrefetcher, addresses: List[int]):
    for i, address in enumerate(addresses):
        print(f"Accessing address: {address}")
        prefetcher.access(address)

        if prefetcher.stride is not None and i + 1 < len(addresses) and prefetcher.prev_address + prefetcher.stride == addresses[i + 1]:
            prefetcher.report_prefetch_hit()
    
if __name__ == "__main__":
    results = {}

    print("Sequential access pattern:")
    prefetcher = StridePrefetcher()
    memory_accesses = generate_sequential_pattern(10)
    simulate_memory_accesses(prefetcher, memory_accesses)
    accuracy = prefetcher.get_accuracy()
    print(f"Accuracy: {accuracy}")
    results["Sequential"] = accuracy

    print("\nStrided access pattern:")
    prefetcher = StridePrefetcher()
    memory_accesses = generate_strided_pattern(0, 2, 10)
    simulate_memory_accesses(prefetcher, memory_accesses)
    accuracy = prefetcher.get_accuracy()
    print(f"Accuracy: {accuracy}")
    results["Strided"] = accuracy

    print("\nInterleaved access pattern:")
    prefetcher = StridePrefetcher()
    memory_accesses = generate_interleaved_pattern(10)
    simulate_memory_accesses(prefetcher, memory_accesses)
    accuracy = prefetcher.get_accuracy()
    print(f"Accuracy: {accuracy}")
    results["Interleaved"] = accuracy

    print("\nRandom access pattern:")
    prefetcher = StridePrefetcher()
    memory_accesses = generate_random_pattern(10)
    simulate_memory_accesses(prefetcher, memory_accesses)
    accuracy = prefetcher.get_accuracy()
    print(f"Accuracy: {accuracy}")
    results["Random"] = accuracy

    markdown_table = generate_markdown_table(results)
    print("\n实验结果的Markdown表格：")
    print(markdown_table)