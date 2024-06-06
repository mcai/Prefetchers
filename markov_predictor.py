from typing import List
from access_patterns import generate_interleaved_pattern, generate_markdown_table, generate_random_pattern, generate_sequential_pattern, generate_strided_pattern

# 马尔可夫预取器类
class MarkovPrefetcher:
    def __init__(self, num_addresses: int):
        self.num_addresses = num_addresses
        # 初始化转移表，记录地址之间的转移次数
        self.transition_table = [[0 for _ in range(num_addresses)] for _ in range(num_addresses)]
        self.prev_address = None
        self.prefetch_hits = 0
        self.prefetch_requests = 0

    # 处理内存访问
    def access(self, address: int):
        if self.prev_address is not None:
            # 更新转移表
            self.transition_table[self.prev_address][address] += 1

        if sum(self.transition_table[address]) > 0:
            # 获取最可能的下一个地址进行预取
            prefetch_address = self.get_most_probable_next_address(address)
            self.prefetch(prefetch_address)

        self.prev_address = address

    # 获取最可能的下一个地址
    def get_most_probable_next_address(self, address: int) -> int:
        max_transitions = -1
        most_probable_address = None
        for next_address, count in enumerate(self.transition_table[address]):
            if count > max_transitions:
                max_transitions = count
                most_probable_address = next_address
        return most_probable_address

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
def simulate_memory_accesses(prefetcher: MarkovPrefetcher, addresses: List[int]):
    for address in addresses:
        print(f"访问地址: {address}")
        prefetcher.access(address)

        if prefetcher.prev_address is not None:
            prefetch_address = prefetcher.get_most_probable_next_address(prefetcher.prev_address)
            if prefetch_address == address:
                prefetcher.report_prefetch_hit()

if __name__ == "__main__":
    results = {}
    num_addresses = 20  # 根据预期的最大地址范围调整

    print("顺序访问模式:")
    prefetcher = MarkovPrefetcher(num_addresses)
    memory_accesses = generate_sequential_pattern(10)
    simulate_memory_accesses(prefetcher, memory_accesses)
    accuracy = prefetcher.get_accuracy()
    print(f"准确率: {accuracy}")
    results["顺序"] = accuracy

    print("\n跨距访问模式:")
    prefetcher = MarkovPrefetcher(num_addresses)
    memory_accesses = generate_strided_pattern(0, 2, 10)
    simulate_memory_accesses(prefetcher, memory_accesses)
    accuracy = prefetcher.get_accuracy()
    print(f"准确率: {accuracy}")
    results["跨距"] = accuracy

    print("\n交错访问模式:")
    prefetcher = MarkovPrefetcher(num_addresses)
    memory_accesses = generate_interleaved_pattern(10)
    simulate_memory_accesses(prefetcher, memory_accesses)
    accuracy = prefetcher.get_accuracy()
    print(f"准确率: {accuracy}")
    results["交错"] = accuracy

    print("\n随机访问模式:")
    prefetcher = MarkovPrefetcher(num_addresses)
    memory_accesses = generate_random_pattern(10)
    simulate_memory_accesses(prefetcher, memory_accesses)
    accuracy = prefetcher.get_accuracy()
    print(f"准确率: {accuracy}")
    results["随机"] = accuracy

    markdown_table = generate_markdown_table(results)
    print("\n实验结果的Markdown表格：")
    print(markdown_table)