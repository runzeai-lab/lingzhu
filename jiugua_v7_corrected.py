#!/usr/bin/env python3
"""
九卦理论 · 素数间隙探索系统 V7.0 (修正版)

使用正确的"和"态定义：
  "和" = |gap[i] - gap[i-1]| / gap[i-1] <= 0.3

基于润泽博士的验证结果，重新探索素数序列的三进制结构。

作者：灵助 AI
日期：2026-06-23
"""

from math import sqrt, log
import numpy as np
from collections import Counter, defaultdict
import json
from datetime import datetime

def sieve_of_eratosthenes(n):
    """生成小于等于n的所有素数"""
    sieve = bytearray([True]) * (n + 1)
    sieve[0:2] = 0, 0
    for i in range(2, int(sqrt(n)) + 1):
        if sieve[i]:
            sieve[i*i::i] = bytearray(len(range(i*i, n+1, i)))
    return [i for i, is_prime in enumerate(sieve) if is_prime]

def gap_to_ternary_correct(gap, prev_gap):
    """
    正确的三进制编码：使用相对误差
    
    这是润泽博士验证有效的定义
    """
    if prev_gap is None or prev_gap == 0:
        return 0  # 第一个素数，返回"和"
    
    rel_change = abs(gap - prev_gap) / prev_gap
    
    if rel_change <= 0.3:
        return 0   # 和（近似平衡）
    elif gap > prev_gap:
        return +1  # 阳（发散）
    else:
        return -1  # 阴（收敛）

def analyze_ternary_sequence_correct(primes):
    """使用正确的'和'态定义分析三进制序列"""
    # 计算间隙序列
    gaps = []
    for i, p in enumerate(primes):
        if i == 0:
            gap = 0
        else:
            gap = p - primes[i-1]
        gaps.append(gap)
    
    # 三进制编码
    ternary_seq = []
    for i in range(1, len(gaps)):
        val = gap_to_ternary_correct(gaps[i], gaps[i-1])
        ternary_seq.append(val)
    
    # 统计频率
    freq = Counter(ternary_seq)
    total = len(ternary_seq)
    
    yin_pct = freq.get(-1, 0) / total * 100
    he_pct = freq.get(0, 0) / total * 100
    yang_pct = freq.get(1, 0) / total * 100
    
    # 分析三元组
    trigrams = []
    for i in range(len(ternary_seq) - 2):
        trigram = tuple(ternary_seq[i:i+3])
        trigrams.append(trigram)
    
    trigram_freq = Counter(trigrams)
    
    # 阴阳交替模式
    alternating_count = 0
    for trigram, count in trigram_freq.items():
        if (trigram[0] == +1 and trigram[1] == -1 and trigram[2] == +1) or \
           (trigram[0] == -1 and trigram[1] == +1 and trigram[2] == -1):
            alternating_count += count
    
    alternating_pct = alternating_count / len(trigrams) * 100
    
    return {
        'total': total,
        'yin_pct': yin_pct,
        'he_pct': he_pct,
        'yang_pct': yang_pct,
        'trigram_freq': trigram_freq,
        'alternating_pct': alternating_pct,
        'ternary_seq': ternary_seq
    }

def map_to_jiugua_space(primes, ternary_seq):
    """将三进制序列映射到九卦空间（简化版）"""
    # 简化映射：使用三进制序列的前9个值作为卦象维度
    # 注意：这需要更复杂的设计
    
    indices = []
    for i in range(len(ternary_seq)):
        # 取当前位置及前8个位置的三进制值（如果可用）
        dims = []
        for j in range(9):
            idx = i - j
            if idx >= 0:
                dims.append(ternary_seq[idx])
            else:
                dims.append(0)  # 边界填充
        
        # 转换为卦象索引
        index = 0
        for j, val in enumerate(dims):
            digit = val + 1  # -1->0, 0->1, +1->2
            index += digit * (3 ** j)
        
        indices.append(index)
    
    return indices

def main():
    print("="*80)
    print("九卦理论 · 素数间隙探索系统 V7.0 (修正版)")
    print("="*80)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 参数设置
    N = 100000  # 可以调整到1000000
    
    print(f"\n探索参数:")
    print(f"  - 素数数量: {N}")
    print(f"  - '和'态定义: |gap[i]-gap[i-1]|/gap[i-1] <= 0.3")
    print(f"  - 期望'和'态频率: ~18.7%")
    
    # 生成素数
    print(f"\n生成素数...")
    start_time = time.time()
    if N <= 100000:
        limit = 2000000
    else:
        limit = 20000000
    
    primes = sieve_of_eratosthenes(limit)
    primes = primes[:N]
    print(f"  完成，耗时: {time.time()-start_time:.2f}秒")
    print(f"  最大素数: {primes[-1]}")
    
    # 分析三进制序列（使用正确定义）
    print(f"\n分析三进制序列（正确定义）...")
    result = analyze_ternary_sequence_correct(primes)
    
    print(f"\n{'='*80}")
    print("三进制序列分析结果（修正后）")
    print(f"{'='*80}")
    print(f"序列长度: {result['total']}")
    print(f"\n三进制值频率:")
    print(f"  阴 (-1): {result['yin_pct']:.2f}%")
    print(f"  和 (0):  {result['he_pct']:.2f}%  ← 应该是~18.7%")
    print(f"  阳 (+1): {result['yang_pct']:.2f}%")
    
    print(f"\n阴阳交替模式频率: {result['alternating_pct']:.2f}%")
    print(f"  (期望: ~43.9%)")
    
    print(f"\n前10个高频三元组:")
    for rank, (trigram, count) in enumerate(result['trigram_freq'].most_common(10), 1):
        pct = count / len(result['ternary_seq']) * 100
        print(f"  {rank}. {trigram}: {count} ({pct:.2f}%)")
    
    # 映射到九卦空间
    print(f"\n映射到九卦空间...")
    indices = map_to_jiugua_space(primes, result['ternary_seq'])
    
    # 分析卦象分布
    freq = Counter(indices)
    most_common = freq.most_common(20)
    
    print(f"\n前20个最频繁卦象:")
    print(f"{'排名':<4} {'卦象索引':<8} {'频率':<8} {'百分比':<10}")
    print("-" * 40)
    
    for rank, (hex_idx, count) in enumerate(most_common, 1):
        pct = count / len(indices) * 100
        print(f"{rank:<4} {hex_idx:<8} {count:<8} {pct:<10.4f}%")
    
    top4_pct = sum(count for _, count in most_common[:4]) / len(indices) * 100
    print(f"\nTop-4集中度: {top4_pct:.2f}%")
    
    # 保存结果
    output = {
        'timestamp': datetime.now().isoformat(),
        'version': 'V7.0 (修正和态定义)',
        'N': N,
        'he_definition': '|gap[i]-gap[i-1]|/gap[i-1] <= 0.3',
        'results': {
            'yin_pct': result['yin_pct'],
            'he_pct': result['he_pct'],
            'yang_pct': result['yang_pct'],
            'alternating_pct': result['alternating_pct'],
            'top4_pct': top4_pct
        }
    }
    
    output_file = f"jiugua_v7_corrected_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    # 简化输出（不保存完整序列）
    output_save = output.copy()
    output_save['results']['trigram_top10'] = dict(result['trigram_freq'].most_common(10))
    
    with open(output_file, 'w') as f:
        json.dump(output_save, f, indent=2)
    
    print(f"\n结果已保存到: {output_file}")
    print(f"\n{'='*80}")
    print("探索完成")
    print(f"{'='*80}")
    print(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    import time
    main()
