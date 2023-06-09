import collections
from typing import Dict, List

class MarkovNode:
    def __init__(self, address: int):
        self.address = address
        self.transitions = collections.defaultdict(int)
        self.total_transitions = 0

    def add_transition(self, next_address: int):
        self.transitions[next_address] += 1
        self.total_transitions += 1

    def get_most_probable_next_address(self) -> int:
        if not self.transitions:
            return None
        return max(self.transitions, key=self.transitions.get)

class MarkovPrefetcher:
    def __init__(self):
        self.markov_table: Dict[int, MarkovNode] = {}
        self.prev_address: int = None
        self.prefetch_hits = 0
        self.prefetch_requests = 0

    def access(self, address: int):
        if address not in self.markov_table:
            self.markov_table[address] = MarkovNode(address)

        if self.prev_address is not None:
            self.markov_table[self.prev_address].add_transition(address)

        if self.markov_table[address].total_transitions > 0:
            node = self.markov_table[address]
            prefetch_address = node.get_most_probable_next_address()
            self.prefetch(prefetch_address)

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

def simulate_memory_accesses(prefetcher: MarkovPrefetcher, addresses: List[int]):
    for address in addresses:
        print(f"Accessing address: {address}")
        prefetcher.access(address)

        if prefetcher.prev_address is not None:
            prefetch_address = prefetcher.markov_table[prefetcher.prev_address].get_most_probable_next_address()
            if prefetch_address == address:
                prefetcher.report_prefetch_hit()

def generate_sequential_pattern(length: int) -> List[int]:
    return list(range(length))

def generate_strided_pattern(start: int, stride: int, length: int) -> List[int]:
    return [start + i * stride for i in range(length)]

def generate_interleaved_pattern(length: int) -> List[int]:
    return [i for j in range(length // 2) for i in (2 * j, 2 * j + 1)]

def generate_random_pattern(length: int) -> List[int]:
    import random
    return [random.randint(0, length - 1) for _ in range(length)]

def generate_markdown_table(results: Dict[str, float]) -> str:
    header = "| 访问模式 | 预测准确性 |\n| -------- | ---------- |\n"
    rows = [f"| {key} | {value} |" for key, value in results.items()]
    return header + "\n".join(rows)

if __name__ == "__main__":
    results = {}

    print("Sequential access pattern:")
    prefetcher = MarkovPrefetcher()
    memory_accesses = generate_sequential_pattern(10)
    simulate_memory_accesses(prefetcher, memory_accesses)
    accuracy = prefetcher.get_accuracy()
    print(f"Accuracy: {accuracy}")
    results["Sequential"] = accuracy

    print("\nStrided access pattern:")
    prefetcher = MarkovPrefetcher()
    memory_accesses = generate_strided_pattern(0, 2, 10)
    simulate_memory_accesses(prefetcher, memory_accesses)
    accuracy = prefetcher.get_accuracy()
    print(f"Accuracy: {accuracy}")
    results["Strided"] = accuracy

    print("\nInterleaved access pattern:")
    prefetcher = MarkovPrefetcher()
    memory_accesses = generate_interleaved_pattern(10)
    simulate_memory_accesses(prefetcher, memory_accesses)
    accuracy = prefetcher.get_accuracy()
    print(f"Accuracy: {accuracy}")
    results["Interleaved"] = accuracy

    print("\nRandom access pattern:")
    prefetcher = MarkovPrefetcher()
    memory_accesses = generate_random_pattern(10)
    simulate_memory_accesses(prefetcher, memory_accesses)
    accuracy = prefetcher.get_accuracy()
    print(f"Accuracy: {accuracy}")
    results["Random"] = accuracy

    markdown_table = generate_markdown_table(results)
    print("\n实验结果的Markdown表格：")
    print(markdown_table)