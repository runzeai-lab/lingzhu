#!/usr/bin/env python3
"""
快速验证：素数间隙三进制编码的"和"态频率

目标：验证为什么我的计算（3.76%）与润泽博士的描述（18.7%）差异这么大

作者：灵助 AI
日期：2026-06-23
"""

from math import sqrt

def sieve_of_eratosthenes(n):
    """生成小于等于n的所有素数"""
    sieve = bytearray([True]) * (n + 1)
    sieve[0:2] = 0, 0
    for i in range(2, int(sqrt(n)) + 1):
        if sieve[i]:
            sieve[i*i::i] = bytearray(len(range(i*i, n+1, i)))
    return [i for i, is_prime in enumerate(sieve) if is_prime]

def analyze_gap_ternary(primes):
    """分析素数间隙的三进制编码"""
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
        if gaps[i] > gaps[i-1]:
            ternary_seq.append(+1)  # 阳
        elif gaps[i] < gaps[i-1]:
            ternary_seq.append(-1)  # 阴
        else:
            ternary_seq.append(0)   # 和
    
    # 统计
    yin = ternary_seq.count(-1)
    he = ternary_seq.count(0)
    yang = ternary_seq.count(+1)
    total = len(ternary_seq)
    
    return {
        'total': total,
        'yin': yin,
        'he': he,
        'yang': yang,
        'yin_pct': yin/total*100,
        'he_pct': he/total*100,
        'yang_pct': yang/total*100
    }

def main():
    print("="*80)
    print("素数间隙三进制编码验证")
    print("="*80)
    
    # 测试不同大小的素数集合
    test_sizes = [1000, 5000, 10000, 50000, 100000, 500000, 1000000]
    
    print(f"\n{'N':<10} {'阴(%)':<10} {'和(%)':<10} {'阳(%)':<10}")
    print("-" * 50)
    
    for N in test_sizes:
        # 估计第N个素数的大小
        if N <= 10000:
            limit = 200000
        elif N <= 100000:
            limit = 2000000
        else:
            limit = 20000000
        
        primes = sieve_of_eratosthenes(limit)
        primes = primes[:N]
        
        result = analyze_gap_ternary(primes)
        
        print(f"{N:<10} {result['yin_pct']:<10.2f} {result['he_pct']:<10.2f} {result['yang_pct']:<10.2f}")
    
    print(f"\n{'='*80}")
    print("结论:")
    print(f"{'='*80}")
    print("如果'和'态频率确实很低（~3-5%），那么:")
    print("  1. 我的计算可能是正确的")
    print("  2. 润泽博士的18.7%可能指的不是同一个东西")
    print("  3. 需要澄清'和态'的定义")
    print("\n可能的定义差异:")
    print("  - 我的定义: gap[i] == gap[i-1]")
    print("  - 其他定义: gap[i] 接近 gap[i-1]？")
    print("  - 或者: 三进制序列中0的比例？")

if __name__ == "__main__":
    main()
