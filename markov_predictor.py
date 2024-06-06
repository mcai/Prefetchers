# markov_predictor.py

from typing import List, Optional, Tuple
from collections import deque
import random

# 生成顺序访问模式
def generate_sequential_pattern(length: int) -> List[int]:
    """生成长度为length的顺序访问模式。
    Args:
        length (int): 模式的长度。
    Returns:
        List[int]: 顺序访问模式。
    """
    return list(range(length))

# 生成跨距访问模式
def generate_strided_pattern(start: int, stride: int, length: int) -> List[int]:
    """生成跨距访问模式，从start开始，每次跨越stride，直到长度为length。
    Args:
        start (int): 起始地址。
        stride (int): 跨距。
        length (int): 模式的长度。
    Returns:
        List[int]: 跨距访问模式。
    """
    return [start + i * stride for i in range(length)]

# 生成交错访问模式
def generate_interleaved_pattern(length: int) -> List[int]:
    """生成交错访问模式，交替访问相邻地址。
    Args:
        length (int): 模式的长度。
    Returns:
        List[int]: 交错访问模式。
    """
    return [i for j in range(length // 2) for i in (2 * j, 2 * j + 1)]

# 生成随机访问模式
def generate_random_pattern(length: int) -> List[int]:
    """生成随机访问模式，在给定长度范围内随机生成访问地址。
    Args:
        length (int): 模式的长度。
    Returns:
        List[int]: 随机访问模式。
    """
    return [random.randint(0, length - 1) for _ in range(length)]

# 生成重复访问模式
def generate_repeated_pattern(pattern: List[int], repetitions: int) -> List[int]:
    """生成重复访问模式，将基本模式重复给定次数。
    Args:
        pattern (List[int]): 基本模式。
        repetitions (int): 重复次数。
    Returns:
        List[int]: 重复访问模式。
    """
    return pattern * repetitions

def initialize_transition_table(num_addresses: int) -> List[List[int]]:
    """初始化转移表，用于记录地址之间的转移次数。
    Args:
        num_addresses (int): 地址的数量。
    Returns:
        List[List[int]]: 初始化的转移表。
    """
    return [[0 for _ in range(num_addresses)] for _ in range(num_addresses)]

def get_most_probable_next_address(transition_table: List[List[int]], address: int) -> Optional[int]:
    """根据转移表获取最可能的下一个地址。
    Args:
        transition_table (List[List[int]]): 转移表。
        address (int): 当前地址。
    Returns:
        Optional[int]: 最可能的下一个地址，如果没有找到则返回None。
    """
    max_transitions = 0
    most_probable_address = None
    for next_address, count in enumerate(transition_table[address]):
        if count > max_transitions:
            max_transitions = count
            most_probable_address = next_address
    return most_probable_address

def markov_prefetcher(num_addresses: int, addresses: List[int], history_window_size: int = 5) -> float:
    """模拟Markov预取器并计算其准确率。
    Args:
        num_addresses (int): 地址空间的大小。
        addresses (List[int]): 内存访问地址序列。
        history_window_size (int): 访问历史记录的窗口大小。
    Returns:
        float: 预取器的准确率。
    """
    # 初始化变量
    transition_table = initialize_transition_table(num_addresses)  # 初始化转移表
    prev_address = None  # 用于存储前一个访问的地址
    prefetch_hits = 0  # 预取命中次数
    prefetch_requests = 0  # 预取请求次数
    access_history: deque[Tuple[int, str]] = deque(maxlen=history_window_size)  # 访问历史记录，存储最近的访问地址和访问类型（预取或非预取）

    # 处理每个内存访问
    for address in addresses:
        sentence = f"访问历史: {list(access_history)}, 访问地址: {address}"

        # 检查当前地址是否匹配任何已访问或预取的地址
        hit = False
        for i, (hist_addr, access_type) in enumerate(access_history):
            if address == hist_addr:
                if access_type == "预取":
                    prefetch_hits += 1  # 预取命中次数增加
                    access_history[i] = (hist_addr, "非预取")  # 如果命中预取地址，将其标记为非预取访问
                    sentence += f", 预取命中"
                else:
                    sentence += f", 非预取命中"
                hit = True
                break

        if not hit:
            sentence += f", 未命中"

        # 更新转移表
        if prev_address is not None:
            transition_table[prev_address][address] += 1  # 增加转移次数
            sentence += f", 更新转移表: {prev_address} -> {address}({transition_table[prev_address][address]})"

        # 更新访问历史记录，标记当前访问为非预取访问
        # 如果地址已经存在于访问历史记录中，将其删除并重新添加到队列尾部
        access_history = deque([(addr, atype) for addr, atype in access_history if addr != address], maxlen=history_window_size)
        access_history.append((address, "非预取"))

        # 打印转移表
        transition_table_summary = ", ".join([f"{i} -> [{', '.join(f'{j}({count})' for j, count in enumerate(row) if count > 0)}]" for i, row in enumerate(transition_table) if any(count > 0 for count in row)])
        sentence += f", 当前转移表: {transition_table_summary}"

        # 进行预取请求
        predicted_address = get_most_probable_next_address(transition_table, address)
        if predicted_address is not None:
            if predicted_address not in [addr for addr, _ in access_history]:
                prefetch_requests += 1  # 预取请求次数增加
                access_history.append((predicted_address, "预取"))
                sentence += f", 预取地址: {predicted_address}"
            else:
                sentence += ", 不进行预取(地址已存在)"
        else:
            sentence += ", 不进行预取(没有找到后继地址)"

        # 更新前一个地址
        prev_address = address

        # 打印总结语句
        print(sentence)

    # 计算最终预取准确率
    if prefetch_requests == 0:
        return 0
    final_accuracy = prefetch_hits / prefetch_requests  # 计算预取准确率
    print(f"\n准确率: {final_accuracy:.2f}")
    return final_accuracy

def run_prefetcher_tests():
    """在各种访问模式下运行Markov预取器并显示结果。"""
    results = {}
    num_addresses = 20  # 根据预期地址范围调整

    print("顺序访问模式:")
    memory_accesses = generate_sequential_pattern(10)
    accuracy = markov_prefetcher(num_addresses, memory_accesses)
    results["顺序"] = accuracy

    print("\n跨距访问模式:")
    memory_accesses = generate_strided_pattern(0, 2, 10)
    accuracy = markov_prefetcher(num_addresses, memory_accesses)
    results["跨距"] = accuracy

    print("\n交错访问模式:")
    memory_accesses = generate_interleaved_pattern(10)
    accuracy = markov_prefetcher(num_addresses, memory_accesses)
    results["交错"] = accuracy

    print("\n随机访问模式:")
    memory_accesses = generate_random_pattern(10)
    accuracy = markov_prefetcher(num_addresses, memory_accesses)
    results["随机"] = accuracy

    print("\n重复访问模式:")
    memory_accesses = generate_repeated_pattern([0, 1, 2, 3, 4, 5], 2)
    accuracy = markov_prefetcher(num_addresses, memory_accesses)
    results["重复"] = accuracy

    print("\n自定义访问模式:")
    memory_accesses = [0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5]
    accuracy = markov_prefetcher(num_addresses, memory_accesses)
    results["自定义"] = accuracy

    # 总结结果
    print("\n实验结果总结：")
    for pattern, accuracy in results.items():
        print(f"{pattern}访问模式的预测准确率为: {accuracy:.2f}")

if __name__ == "__main__":
    run_prefetcher_tests()