#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试分割逻辑的脚本
"""

import random

def generate_segments(total_duration, min_dur, max_dur):
    """生成分割方案（测试版本）"""
    segments = []
    current_time = 0.0
    
    while current_time < total_duration:
        # 计算剩余时间
        remaining_time = total_duration - current_time
        
        # 如果剩余时间不足最小时长，则跳过（不生成片段）
        if remaining_time < min_dur:
            print(f"剩余时间 {remaining_time:.2f} 秒不足最小时长 {min_dur} 秒，跳过")
            break
        
        # 在最小和最大时长之间随机选择
        # 确保不超过剩余时间
        max_possible_duration = min(max_dur, remaining_time)
        
        # 如果最大可能时长小于最小时长，则跳过
        if max_possible_duration < min_dur:
            print(f"剩余时间 {remaining_time:.2f} 秒不足以生成符合最小时长 {min_dur} 秒的片段，跳过")
            break
        
        # 生成随机时长，确保在有效范围内
        segment_duration = random.uniform(min_dur, max_possible_duration)
        
        # 再次确保片段时长至少为最小时长（双重保险）
        segment_duration = max(segment_duration, min_dur)
        
        segments.append((current_time, segment_duration))
        current_time += segment_duration
        
        print(f"片段 {len(segments)}: 起始时间 {current_time - segment_duration:.2f}s, 时长 {segment_duration:.2f}s")
    
    return segments

def test_segmentation():
    """测试分割逻辑"""
    print("测试分割逻辑")
    print("=" * 50)
    
    # 测试用例
    test_cases = [
        (60, 5, 15),    # 60秒视频，5-15秒片段
        (30, 10, 20),   # 30秒视频，10-20秒片段
        (25, 8, 12),    # 25秒视频，8-12秒片段
        (10, 5, 8),     # 10秒视频，5-8秒片段
        (5, 3, 5),      # 5秒视频，3-5秒片段
    ]
    
    for total_duration, min_dur, max_dur in test_cases:
        print(f"\n测试视频时长: {total_duration}s, 片段范围: {min_dur}-{max_dur}s")
        print("-" * 40)
        
        segments = generate_segments(total_duration, min_dur, max_dur)
        
        # 验证结果
        total_segment_time = sum(duration for _, duration in segments)
        print(f"总片段数: {len(segments)}")
        print(f"总片段时长: {total_segment_time:.2f}s")
        print(f"覆盖率: {total_segment_time/total_duration*100:.1f}%")
        
        # 检查是否有过短的片段
        short_segments = [duration for _, duration in segments if duration < min_dur]
        if short_segments:
            print(f"WARNING: 发现过短片段: {short_segments}")
        else:
            print("OK: 所有片段都符合最小时长要求")

if __name__ == "__main__":
    test_segmentation()
