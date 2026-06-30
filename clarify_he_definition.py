#!/usr/bin/env python3
"""
严格澄清"和"态定义

目标：理解为什么我的计算（3.76%）与润泽博士的描述（18.7%）有差异

定义测试：
1. 严格相等：gap[i] == gap[i-1]
2. 软相等：|gap[i] - gap[i-1]| <= threshold
3. 相对相等：|gap[i] - gap[i-1]| / gap[i-1] <= rel_threshold
4. 三进制序列中的0比例（可能润泽博士指的是这个？）

作者：灵助 AI
日期：2026-06-23
"""

from math import sqrt
import numpy as np

def sieve_of_eratosthenes(n):
    """生成小于等于n的所有素数"""
    sieve = bytearray([True]) * (n + 1)
    sieve[0:2] = 0, 0
    for i in range(2, int(sqrt(n)) + 1):
        if sieve[i]:
            sieve[i*i::i] = bytearray(len(range(i*i, n+1, i)))
    return [i for i, is_prime in enumerate(sieve) if is_prime]

def test_he_definitions(primes):
    """测试不同的'和'态定义"""
    # 计算间隙序列
    gaps = []
    for i, p in enumerate(primes):
        if i == 0:
            gap = 0
        else:
            gap = p - primes[i-1]
        gaps.append(gap)
    
    # 定义1：严格相等
    he_strict = 0
    for i in range(1, len(gaps)):
        if gaps[i] == gaps[i-1]:
            he_strict += 1
    
    # 定义2：软相等（绝对误差）
    he_soft_abs = {}
    for threshold in [0, 1, 2, 4, 6, 8, 10]:
        count = 0
        for i in range(1, len(gaps)):
            if abs(gaps[i] - gaps[i-1]) <= threshold:
                count += 1
        he_soft_abs[threshold] = count / (len(gaps) - 1) * 100
    
    # 定义3：软相等（相对误差）
    he_soft_rel = {}
    for rel_threshold in [0.0, 0.1, 0.2, 0.3, 0.5, 0.8, 1.0]:
        count = 0
        for i in range(1, len(gaps)):
            if gaps[i-1] == 0:
                continue
            if abs(gaps[i] - gaps[i-1]) / gaps[i-1] <= rel_threshold:
                count += 1
        he_soft_rel[rel_threshold] = count / (len(gaps) - 1) * 100
    
    # 定义4：三进制序列中0的比例
    ternary_seq = []
    for i in range(1, len(gaps)):
        if gaps[i] > gaps[i-1]:
            ternary_seq.append(+1)
        elif gaps[i] < gaps[i-1]:
            ternary_seq.append(-1)
        else:
            ternary_seq.append(0)
    
    he_ternary = ternary_seq.count(0) / len(ternary_seq) * 100
    
    return {
        'strict': he_strict / (len(gaps) - 1) * 100,
        'soft_abs': he_soft_abs,
        'soft_rel': he_soft_rel,
        'ternary': he_ternary
    }

def main():
    print("="*80)
    print("'和'态定义严格测试")
    print("="*80)
    
    # 测试不同大小的素数集合
    test_sizes = [10000, 50000, 100000, 500000]
    
    for N in test_sizes:
        # 估计第N个素数的大小
        if N <= 100000:
            limit = 2000000
        else:
            limit = 10000000
        
        primes = sieve_of_eratosthenes(limit)
        primes = primes[:N]
        
        print(f"\n{'='*80}")
        print(f"N = {N}")
        print(f"{'='*80}")
        
        results = test_he_definitions(primes)
        
        print(f"\n定义1 - 严格相等 (gap[i] == gap[i-1]):")
        print(f"  '和'态频率: {results['strict']:.2f}%")
        
        print(f"\n定义2 - 软相等（绝对误差）:")
        for threshold, pct in results['soft_abs'].items():
            print(f"  |gap[i] - gap[i-1]| <= {threshold}: {pct:.2f}%")
        
        print(f"\n定义3 - 软相等（相对误差）:")
        for rel_threshold, pct in results['soft_rel'].items():
            print(f"  |gap[i] - gap[i-1]|/gap[i-1] <= {rel_threshold}: {pct:.2f}%")
        
        print(f"\n定义4 - 三进制序列中0的比例:")
        print(f"  '和'态频率: {results['ternary']:.2f}%")
    
    print(f"\n{'='*80}")
    print("结论分析")
    print(f"{'='*80}")
    print("如果润泽博士的18.7%对应某个定义，那么:")
    print("  1. 检查定义2中是否有threshold使频率接近18.7%")
    print("  2. 检查定义3中是否有rel_threshold使频率接近18.7%")
    print("  3. 如果都没有，可能需要检查原始计算方法")
    print("\n我的猜测:")
    print("  - 定义1（严格相等）：~3-5%")
    print("  - 定义2（绝对误差threshold=2-4）：可能接近18.7%？")
    print("  - 定义3（相对误差）：需要计算")
    print("  - 定义4（三进制序列）：同定义1")

if __name__ == "__main__":
    main()
