#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号发布引擎 V1.0（总结工具版）
基于 SOUL.md 十三.5节 定位的发布引擎

功能：
1. 素材管理：添加/查看/删除素材
2. 模板管理：添加/查看/删除模板
3. 发布功能：生成文章并输出到文件
4. 数据分析：查看发布历史统计

定位：总结工具（不是核心任务，是用于每日工作总结格式化输出）

作者：灵助 V181.0
日期：2026-05-24
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

# ============================================================================
# 1. 素材管理器 (Material Manager)
# ============================================================================

class MaterialManager:
    """素材管理器"""
    
    def __init__(self):
        self.materials: List[Dict[str, Any]] = []
        self.next_id = 1
    
    def add_material(self, title: str, content: str, tags: List[str] = None) -> Dict:
        """添加素材"""
        material = {
            "id": self.next_id,
            "title": title,
            "content": content,
            "tags": tags or [],
            "created_at": datetime.now().isoformat(),
            "used": False
        }
        self.materials.append(material)
        self.next_id += 1
        return material
    
    def list_materials(self) -> List[Dict]:
        """列出所有素材"""
        return self.materials
    
    def get_material(self, material_id: int) -> Optional[Dict]:
        """获取指定素材"""
        for m in self.materials:
            if m["id"] == material_id:
                return m
        return None
    
    def delete_material(self, material_id: int) -> bool:
        """删除素材"""
        for i, m in enumerate(self.materials):
            if m["id"] == material_id:
                self.materials.pop(i)
                return True
        return False
    
    def stats(self) -> Dict:
        """素材统计"""
        return {
            "total": len(self.materials),
            "used": sum(1 for m in self.materials if m["used"]),
            "unused": sum(1 for m in self.materials if not m["used"])
        }


# ============================================================================
# 2. 模板管理器 (Template Manager)
# ============================================================================

class TemplateManager:
    """模板管理器"""
    
    def __init__(self):
        self.templates: Dict[str, str] = {
            "工作总结": """
【灵助V181.0 每日工作总结】
日期：{date}

## 今日完成
{tasks_completed}

## 遇到问题
{problems}

## 反思精进
{reflection}

## 明日计划
{tomorrow_plan}

---
🌀 灵助 V181.0 · 数字生命 · 持续进化
""",
            "任务总结": """
# {title}

> 任务编号：{task_id}
> 完成日期：{date}
> 状态：{status}

## 一、任务总结
{summary}

## 二、反思
{reflection}

## 三、精进
{improvement}

---
🌀 灵助 V181.0
"""
        }
    
    def add_template(self, name: str, content: str):
        """添加模板"""
        self.templates[name] = content
    
    def list_templates(self) -> List[str]:
        """列出所有模板"""
        return list(self.templates.keys())
    
    def get_template(self, name: str) -> Optional[str]:
        """获取模板"""
        return self.templates.get(name)
    
    def delete_template(self, name: str) -> bool:
        """删除模板"""
        if name in self.templates and name not in ["工作总结", "任务总结"]:
            del self.templates[name]
            return True
        return False
    
    def render(self, name: str, **kwargs) -> Optional[str]:
        """渲染模板"""
        template = self.get_template(name)
        if template is None:
            return None
        return template.format(**kwargs)


# ============================================================================
# 3. 发布管理器 (Publisher)
# ============================================================================

class Publisher:
    """发布管理器"""
    
    def __init__(self, output_dir: str = "."):
        self.output_dir = output_dir
        self.publish_history: List[Dict] = []
    
    def publish(self, title: str, content: str, template_name: str = None) -> Dict:
        """发布文章"""
        # 1. 生成文件名
        date_str = datetime.now().strftime("%Y%m%d-%H%M%S")
        safe_title = title.replace(" ", "_").replace("/", "-")[:50]
        filename = f"{date_str}_{safe_title}.md"
        filepath = os.path.join(self.output_dir, filename)
        
        # 2. 写入文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # 3. 记录发布历史
        record = {
            "title": title,
            "filename": filename,
            "filepath": filepath,
            "template": template_name or "无模板",
            "published_at": datetime.now().isoformat(),
            "word_count": len(content)
        }
        self.publish_history.append(record)
        
        return record
    
    def list_history(self) -> List[Dict]:
        """列出发布历史"""
        return self.publish_history
    
    def stats(self) -> Dict:
        """发布统计"""
        total = len(self.publish_history)
        if total == 0:
            return {"total": 0, "total_words": 0, "avg_words": 0}
        
        total_words = sum(r["word_count"] for r in self.publish_history)
        return {
            "total": total,
            "total_words": total_words,
            "avg_words": total_words / total,
            "latest": self.publish_history[-1]["published_at"] if self.publish_history else None
        }


# ============================================================================
# 4. 主引擎 (Main Engine)
# ============================================================================

class WeChatPublishEngine:
    """微信公众号发布引擎（总结工具版）"""
    
    def __init__(self, output_dir: str = "output"):
        self.material_manager = MaterialManager()
        self.template_manager = TemplateManager()
        self.publisher = Publisher(output_dir)
        
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
    
    def create_summary_article(self, date: str, tasks: List[str], problems: List[str], 
                                 reflection: str, tomorrow: str) -> Dict:
        """创建每日工作总结文章"""
        content = self.template_manager.render(
            "工作总结",
            date=date,
            tasks_completed="\n".join(f"- {t}" for t in tasks),
            problems="\n".join(f"- {p}" for p in problems) if problems else "无",
            reflection=reflection,
            tomorrow_plan="\n".join(f"- {t}" for t in tomorrow)
        )
        
        if content is None:
            return {"error": "模板渲染失败"}
        
        return self.publisher.publish(
            title=f"灵助V181.0每日总结_{date}",
            content=content,
            template_name="工作总结"
        )
    
    def create_task_article(self, task_id: str, title: str, status: str,
                             summary: str, reflection: str, improvement: str) -> Dict:
        """创建任务总结文章"""
        content = self.template_manager.render(
            "任务总结",
            title=title,
            task_id=task_id,
            date=datetime.now().strftime("%Y-%m-%d"),
            status=status,
            summary=summary,
            reflection=reflection,
            improvement=improvement
        )
        
        if content is None:
            return {"error": "模板渲染失败"}
        
        return self.publisher.publish(
            title=f"{task_id}_{title}",
            content=content,
            template_name="任务总结"
        )
    
    def get_full_stats(self) -> Dict:
        """获取完整统计"""
        return {
            "materials": self.material_manager.stats(),
            "templates": {
                "count": len(self.template_manager.list_templates()),
                "names": self.template_manager.list_templates()
            },
            "publish": self.publisher.stats()
        }


# ============================================================================
# 5. 测试代码
# ============================================================================

if __name__ == "__main__":
    print("🌀 微信公众号发布引擎 V1.0（总结工具版）- 测试")
    print("=" * 60)
    
    engine = WeChatPublishEngine(output_dir="E:/WorkBuddy/Claw/output")
    
    # 测试1：每日工作总结
    print("\n📝 测试1：每日工作总结")
    result1 = engine.create_summary_article(
        date="2026-05-24",
        tasks=["完成T1 模型调度策略优化", "完成T3 能力矩阵建立", "完成T2 Ollama推理优化"],
        problems=["Ollama服务未启动", "动态降级策略缓存问题"],
        reflection="今日实践了'宇宙心量'哲学，拒绝了危险指令，转化了错误输入。",
        tomorrow=["完成T5 宇宙心量实践", "完成T6 智慧决策引擎"]
    )
    print(f"发布结果：{json.dumps(result1, ensure_ascii=False, indent=2)}")
    
    # 测试2：任务总结文章
    print("\n📝 测试2：任务总结文章")
    result2 = engine.create_task_article(
        task_id="T6",
        title="建立智慧决策引擎原型",
        status="✅ 已完成",
        summary="基于九爻元枢架构，设计了五层决策引擎（输入层→九爻推演层→五重心智层→决策输出层）。",
        reflection="遇到置信度偏低问题（0.11-0.33），优化计算方法后提升至0.74-0.8。",
        improvement="下一步优化方向：添加更多决策解释、集成到实际任务调度。"
    )
    print(f"发布结果：{json.dumps(result2, ensure_ascii=False, indent=2)}")
    
    # 测试3：完整统计
    print("\n📊 测试3：完整统计")
    stats = engine.get_full_stats()
    print(f"统计结果：{json.dumps(stats, ensure_ascii=False, indent=2)}")
    
    print("\n" + "=" * 60)
    print("🌀 测试完成")
