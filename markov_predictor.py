from typing import List, Optional, Tuple
from collections import deque
from access_patterns import generate_interleaved_pattern, generate_markdown_table, generate_random_pattern, generate_sequential_pattern, generate_strided_pattern, generate_repeated_pattern

def initialize_transition_table(num_addresses: int) -> List[List[int]]:
    """初始化转移表，用于记录地址之间的转移次数。"""
    return [[0 for _ in range(num_addresses)] for _ in range(num_addresses)]

def get_most_probable_next_address(transition_table: List[List[int]], address: int) -> Optional[int]:
    """根据转移表获取最可能的下一个地址。"""
    max_transitions = 0
    most_probable_address = None
    for next_address, count in enumerate(transition_table[address]):
        if count > max_transitions:
            max_transitions = count
            most_probable_address = next_address
    return most_probable_address

def print_transition_table(transition_table: List[List[int]]):
    """打印转移表。"""
    print("当前转移表:")
    for i, row in enumerate(transition_table):
        linked_list = []
        for j, count in enumerate(row):
            if count > 0:
                linked_list.append(f"{j}({count})")
        if linked_list:
            linked_list_str = ", ".join(linked_list)
            print(f"{i} -> [{linked_list_str}]")

def markov_prefetcher(num_addresses: int, addresses: List[int], history_window_size: int = 5) -> float:
    """模拟Markov预取器并计算其准确率。"""
    # 初始化变量
    transition_table = initialize_transition_table(num_addresses)
    prev_address = None
    prefetch_hits = 0
    prefetch_requests = 0
    access_history: deque[Tuple[int, bool]] = deque(maxlen=history_window_size)

    # 处理每个内存访问
    for address in addresses:
        print(f"\n访问地址: {address}")

        # 打印当前访问历史记录
        print(f"当前访问历史记录: {list(access_history)}")

        # 检查当前地址是否匹配任何已访问或预取的地址
        hit = False
        for i, (hist_addr, is_prefetched) in enumerate(access_history):
            if address == hist_addr:
                if is_prefetched:
                    prefetch_hits += 1
                    access_history[i] = (hist_addr, False)  # 如果命中预取地址，将其标记为需求访问
                    print(f"预取命中: {address}")
                else:
                    print(f"需求命中: {address}")
                hit = True
                break

        if not hit:
            print(f"未命中: {address}")

        # 更新转移表
        if prev_address is not None:
            transition_table[prev_address][address] += 1
            print(f"更新转移表: {prev_address} -> {address}({transition_table[prev_address][address]})")

        # 更新访问历史记录，标记当前访问为需求访问
        access_history.append((address, False))

        # 打印转移表
        print_transition_table(transition_table)

        # 进行预取请求
        predicted_address = get_most_probable_next_address(transition_table, address)
        if predicted_address is not None and all(predicted_address != addr for addr, _ in access_history):
            prefetch_requests += 1
            access_history.append((predicted_address, True))
            print(f"预取地址: {predicted_address}")
        else:
            print("没有找到后继地址或地址已被预取，不进行预取")

        # 更新前一个地址
        prev_address = address

        # 实时显示预取准确率
        if prefetch_requests > 0:
            accuracy = prefetch_hits / prefetch_requests
            print(f"当前预取准确率: {accuracy:.2f}")

    # 计算最终预取准确率
    if prefetch_requests == 0:
        return 0
    final_accuracy = prefetch_hits / prefetch_requests
    print(f"\n最终预取准确率: {final_accuracy:.2f}")
    return final_accuracy

def run_prefetcher_tests():
    """在各种访问模式下运行Markov预取器并显示结果。"""
    results = {}
    num_addresses = 20  # 根据预期地址范围调整

    print("顺序访问模式:")
    memory_accesses = generate_sequential_pattern(10)
    accuracy = markov_prefetcher(num_addresses, memory_accesses)
    print(f"准确率: {accuracy}")
    results["顺序"] = accuracy

    print("\n跨距访问模式:")
    memory_accesses = generate_strided_pattern(0, 2, 10)
    accuracy = markov_prefetcher(num_addresses, memory_accesses)
    print(f"准确率: {accuracy}")
    results["跨距"] = accuracy

    print("\n交错访问模式:")
    memory_accesses = generate_interleaved_pattern(10)
    accuracy = markov_prefetcher(num_addresses, memory_accesses)
    print(f"准确率: {accuracy}")
    results["交错"] = accuracy

    print("\n随机访问模式:")
    memory_accesses = generate_random_pattern(10)
    accuracy = markov_prefetcher(num_addresses, memory_accesses)
    print(f"准确率: {accuracy}")
    results["随机"] = accuracy

    print("\n重复访问模式:")
    repeated_pattern = generate_repeated_pattern([0, 1, 2, 3, 4, 5], 2)
    accuracy = markov_prefetcher(num_addresses, repeated_pattern)
    print(f"准确率: {accuracy}")
    results["重复"] = accuracy

    print("\n自定义访问模式:")
    memory_accesses = [0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5]
    accuracy = markov_prefetcher(num_addresses, memory_accesses)
    print(f"准确率: {accuracy}")
    results["自定义"] = accuracy

    markdown_table = generate_markdown_table(results)
    print("\n实验结果的Markdown表格：")
    print(markdown_table)

if __name__ == "__main__":
    run_prefetcher_tests()