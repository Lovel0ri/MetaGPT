#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py - 直接调用 MetaGPT 的 generate_repo 函数，无需 CLI，支持所有配置参数。
将此文件放在项目根目录（与 metagpt 包同级），修改下方配置即可一键启动项目。
"""
import os
from pathlib import Path
from metagpt.software_company import generate_repo

def main():
    # ======== 配置参数开始 ========
    # 自定义工作目录（workspace）路径
    workspace_dir = os.getenv("MGX_WORKSPACE", "./舆情监测")  # 可根据需要自定义路径
    Path(workspace_dir).mkdir(parents=True, exist_ok=True)  # 确保目录存在

    params = {
        # 项目核心创意（必填）
        "idea": """
开发一个舆情监测平台，使用python+django实现，能够实时抓取和分析社交媒体、新闻网站等数据，提供舆情趋势分析、热点事件预警等功能。主要抓取海外信息

        """,
        "investment": float(os.getenv("MGX_INVESTMENT", 1.0)),# 投资金额（美元）
        "n_round": int(os.getenv("MGX_N_ROUND", 10)), # 模拟轮数
        "code_review": "True",# 是否启用代码审查
        "run_tests": "True",# 是否启用 QA 测试
        "implement":  "True",# 是否启用实现逻辑
        "project_name":  "Dashu-舆情-1.0",# 项目名称，用于区分多个项目
        "inc": "False",# 增量模式
        "project_path": "/Volumes/extra1tb/extra-coding/MetaGPT/舆情监测",  # 使用指定的 workspace 文件夹
        "reqa_file": os.getenv("MGX_REQA_FILE", ""),# QA 源文件路径
        "max_auto_summarize_code": 1,# 最大自动代码总结次数 (-1 表示无限)
        "recover_path": os.getenv("MGX_RECOVER_PATH", ""),# 从已有 team 状态恢复
    }
    # ======== 配置参数结束 ========

    # 调用 generate_repo 启动项目生成流程
    project_dir = generate_repo(**params)
    print(f"项目已生成/恢复于: {project_dir}")

if __name__ == "__main__":
    print("启动大鼠软件公司1号")
    main()
