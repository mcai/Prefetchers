import collections
from typing import Dict, List, Tuple

class MarkovNode:
    def __init__(self, address: int):
        self.address = address
        self.transitions = collections.defaultdict(int)
        self.total_transitions = 0

    def add_transition(self, next_address: int):
        self.transitions[next_address] += 1
        self.total_transitions += 1

    def get_most_probable_next_address(self) -> int:
        return max(self.transitions, key=self.transitions.get)

class MarkovPrefetcher:
    def __init__(self):
        self.markov_table: Dict[int, MarkovNode] = {}
        self.prev_address: int = None

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
        print(f"Prefetching address: {prefetch_address}")

def simulate_memory_accesses(prefetcher: MarkovPrefetcher, addresses: List[int]):
    for address in addresses:
        print(f"Accessing address: {address}")
        prefetcher.access(address)

def generate_sequential_pattern(length: int) -> List[int]:
    return list(range(length))

def generate_strided_pattern(start: int, stride: int, length: int) -> List[int]:
    return [start + i * stride for i in range(length)]

def generate_interleaved_pattern(length: int) -> List[int]:
    return [i for j in range(length // 2) for i in (2 * j, 2 * j + 1)]

def generate_random_pattern(length: int) -> List[int]:
    import random
    return [random.randint(0, length - 1) for _ in range(length)]

if __name__ == "__main__":
    prefetcher = MarkovPrefetcher()

    print("Sequential access pattern:")
    memory_accesses = generate_sequential_pattern(10)
    simulate_memory_accesses(prefetcher, memory_accesses)

    print("\nStrided access pattern:")
    memory_accesses = generate_strided_pattern(0, 2, 10)
    simulate_memory_accesses(prefetcher, memory_accesses)

    print("\nInterleaved access pattern:")
    memory_accesses = generate_interleaved_pattern(10)
    simulate_memory_accesses(prefetcher, memory_accesses)

    print("\nRandom access pattern:")
    memory_accesses = generate_random_pattern(10)
    simulate_memory_accesses(prefetcher, memory_accesses)