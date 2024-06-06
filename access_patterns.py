from typing import Dict, List

# 生成顺序访问模式
def generate_sequential_pattern(length: int) -> List[int]:
    return list(range(length))

# 生成跨距访问模式
def generate_strided_pattern(start: int, stride: int, length: int) -> List[int]:
    return [start + i * stride for i in range(length)]

# 生成交错访问模式
def generate_interleaved_pattern(length: int) -> List[int]:
    return [i for j in range(length // 2) for i in (2 * j, 2 * j + 1)]

# 生成随机访问模式
def generate_random_pattern(length: int) -> List[int]:
    import random
    return [random.randint(0, length - 1) for _ in range(length)]

# 生成Markdown表格
def generate_markdown_table(results: Dict[str, float]) -> str:
    header = "| 访问模式 | 预测准确性 |\n| -------- | ---------- |\n"
    rows = [f"| {key} | {value} |" for key, value in results.items()]
    return header + "\n".join(rows)