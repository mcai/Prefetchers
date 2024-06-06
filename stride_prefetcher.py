from typing import List
from access_patterns import generate_interleaved_pattern, generate_markdown_table, generate_random_pattern, generate_sequential_pattern, generate_strided_pattern

# 跨距预取器类
class StridePrefetcher:
    def __init__(self):
        self.prev_address: int = None
        self.stride: int = None
        self.prefetch_hits = 0
        self.prefetch_requests = 0

    # 处理内存访问
    def access(self, address: int):
        if self.prev_address is not None:
            current_stride = address - self.prev_address
            if self.stride is not None:
                prefetch_address = address + self.stride
                self.prefetch(prefetch_address)

            self.stride = current_stride

        self.prev_address = address

    # 预取地址
    def prefetch(self, prefetch_address: int):
        self.prefetch_requests += 1
        print(f"预取地址: {prefetch_address}")

    # 记录预取命中
    def report_prefetch_hit(self):
        self.prefetch_hits += 1

    # 获取预取准确率
    def get_accuracy(self) -> float:
        if self.prefetch_requests == 0:
            return 0
        return self.prefetch_hits / self.prefetch_requests

# 模拟内存访问
def simulate_memory_accesses(prefetcher: StridePrefetcher, addresses: List[int]):
    for i, address in enumerate(addresses):
        print(f"访问地址: {address}")
        prefetcher.access(address)

        if prefetcher.stride is not None and i + 1 < len(addresses) and prefetcher.prev_address + prefetcher.stride == addresses[i + 1]:
            prefetcher.report_prefetch_hit()

if __name__ == "__main__":
    results = {}

    print("顺序访问模式:")
    prefetcher = StridePrefetcher()
    memory_accesses = generate_sequential_pattern(10)
    simulate_memory_accesses(prefetcher, memory_accesses)
    accuracy = prefetcher.get_accuracy()
    print(f"准确率: {accuracy}")
    results["顺序"] = accuracy

    print("\n跨距访问模式:")
    prefetcher = StridePrefetcher()
    memory_accesses = generate_strided_pattern(0, 2, 10)
    simulate_memory_accesses(prefetcher, memory_accesses)
    accuracy = prefetcher.get_accuracy()
    print(f"准确率: {accuracy}")
    results["跨距"] = accuracy

    print("\n交错访问模式:")
    prefetcher = StridePrefetcher()
    memory_accesses = generate_interleaved_pattern(10)
    simulate_memory_accesses(prefetcher, memory_accesses)
    accuracy = prefetcher.get_accuracy()
    print(f"准确率: {accuracy}")
    results["交错"] = accuracy

    print("\n随机访问模式:")
    prefetcher = StridePrefetcher()
    memory_accesses = generate_random_pattern(10)
    simulate_memory_accesses(prefetcher, memory_accesses)
    accuracy = prefetcher.get_accuracy()
    print(f"准确率: {accuracy}")
    results["随机"] = accuracy

    markdown_table = generate_markdown_table(results)
    print("\n实验结果的Markdown表格：")
    print(markdown_table)