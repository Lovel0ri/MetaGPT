#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
from pathlib import Path

import typer

from metagpt.const import CONFIG_ROOT

# 创建 Typer 应用实例，用于命令行交互
app = typer.Typer(add_completion=False, pretty_exceptions_show_locals=False)


def generate_repo(
        idea,
        investment=3.0,
        n_round=5,
        code_review=True,
        run_tests=False,
        implement=True,
        project_name="",
        inc=False,
        project_path="",
        reqa_file="",
        max_auto_summarize_code=0,
        recover_path=None,
):
    """
    运行项目启动逻辑。可直接从脚本或其他 Python 调用。

    参数:
        idea (str): 项目创意，例如 'Create a 2048 game.'
        investment (float): 投资金额（美元）。
        n_round (int): 模拟运行的轮数。
        code_review (bool): 是否启用代码评审。
        run_tests (bool): 是否启用测试 QA。
        implement (bool): 是否启用代码实现。
        project_name (str): 项目名称，如 'game_2048'。
        inc (bool): 增量模式，配合已有仓库使用。
        project_path (str): 旧版本项目目录路径。
        reqa_file (str): 质量保证代码来源文件名。
        max_auto_summarize_code (int): 自动调用 'SummarizeCode' 的最大次数，-1 为无限制。
        recover_path (str): 从已序列化存储恢复项目的路径。

    返回:
        str: 最终的 project_path 配置。
    """
    # 延迟导入以避免循环依赖
    from metagpt.config2 import config
    from metagpt.context import Context
    from metagpt.roles import (
        Architect,
        DataAnalyst,
        Engineer,
        Engineer2,
        QaEngineer,
        ProductManager,
        TeamLeader,
        Searcher,
        ProjectManager
    )
    from metagpt.team import Team

    # 根据 CLI 或脚本参数更新配置
    config.update_via_cli(project_path, project_name, inc, reqa_file, max_auto_summarize_code)
    # 创建上下文对象
    ctx = Context(config=config)

    if not recover_path:
        # 创建 AI 公司团队
        company = Team(context=ctx)
        company.hire([
            TeamLeader(),      # 团队负责人
            ProductManager(),  # 产品经理
            Architect(),       # 架构师
            Engineer2(),       # 高级工程师
            Engineer(),  # 工程师，负责业务逻辑实现
            # QaEngineer(),
            # Searcher(),       # 信息检索与调研
            # 如果需要可以追加其他角色，如 ProjectManager
            # DataAnalyst(),     # 数据分析师
            ProjectManager()
        ])

        # 若需实现或代码评审，可酌情添加 Engineer
        if implement or code_review:
            company.hire([Engineer(n_borg=5, use_code_review=code_review)])
        # 若启用测试，则添加 QA 工程师并强制最少轮数
        if run_tests:
            company.hire([QaEngineer()])
            if n_round < 8:
                n_round = 8
    else:
        # 恢复已有团队实例
        stg_path = Path(recover_path)
        if not stg_path.exists() or not str(stg_path).endswith("team"):
            raise FileNotFoundError(f"{recover_path} 不存在或路径末尾不是 'team'")

        company = Team.deserialize(stg_path=stg_path, context=ctx)
        idea = company.idea  # 恢复创意

    # 投资运作，启动模拟
    company.invest(investment)
    asyncio.run(company.run(n_round=n_round, idea=idea))

    # 返回项目路径参数
    return ctx.kwargs.get("project_path")


@app.command("", help="Start a new project.")
def startup(
        idea: str = typer.Argument(None, help="你的创新创意，例如 'Create a 2048 game.'"),
        investment: float = typer.Option(default=3.0, help="投资金额（美元）。"),
        n_round: int = typer.Option(default=5, help="模拟运行轮数。"),
        code_review: bool = typer.Option(default=True, help="是否启用代码评审。"),
        run_tests: bool = typer.Option(default=False, help="是否启用测试 QA。"),
        implement: bool = typer.Option(default=True, help="是否启用代码实现。"),
        project_name: str = typer.Option(default="", help="项目名称，如 'game_2048'。"),
        inc: bool = typer.Option(default=False, help="增量模式，配合已有仓库使用。"),
        project_path: str = typer.Option(
            default="",
            help="旧版本项目目录路径，用于增量更新。",
        ),
        reqa_file: str = typer.Option(
            default="", help="质量保证代码来源文件名。"
        ),
        max_auto_summarize_code: int = typer.Option(
            default=0,
            help="自动调用 'SummarizeCode' 的最大次数，-1 为无限制。",
        ),
        recover_path: str = typer.Option(default=None, help="从已序列化存储恢复项目的路径。"),
        init_config: bool = typer.Option(default=False, help="初始化配置文件。"),
):
    """
    命令行入口函数：启动一个新项目或初始化配置。
    """
    # 如果要求初始化配置，则复制示例配置到目标路径
    if init_config:
        copy_config_to()
        return

    # 检查必填参数
    if idea is None:
        typer.echo("缺少参数 'IDEA'。运行 'metagpt --help' 获取更多信息。")
        raise typer.Exit()

    # 调用核心生成逻辑
    return generate_repo(
        idea,
        investment,
        n_round,
        code_review,
        run_tests,
        implement,
        project_name,
        inc,
        project_path,
        reqa_file,
        max_auto_summarize_code,
        recover_path,
    )

# 默认配置示例内容
DEFAULT_CONFIG = """# Full Example: https://github.com/geekan/MetaGPT/blob/main/config/config2.example.yaml
# Reflected Code: https://github.com/geekan/MetaGPT/blob/main/metagpt/config2.py
# Config Docs: https://docs.deepwisdom.ai/main/en/guide/get_started/configuration.html
llm:
  api_type: "openai"  # 或 azure / ollama / groq 等
  model: "gpt-4-turbo"  # 或 gpt-3.5-turbo
  base_url: "https://api.openai.com/v1"  # API 基础 URL
  api_key: "YOUR_API_KEY"
"""


def copy_config_to():
    """
    将默认配置写入 CONFIG_ROOT/config2.yaml，若已存在则备份。
    """
    target_path = CONFIG_ROOT / "config2.yaml"

    # 创建父目录（如不存在）
    target_path.parent.mkdir(parents=True, exist_ok=True)

    # 若已有配置文件，则重命名为 .bak
    if target_path.exists():
        backup_path = target_path.with_suffix(".bak")
        target_path.rename(backup_path)
        print(f"已备份旧配置文件到 {backup_path}")

    # 写入默认配置
    target_path.write_text(DEFAULT_CONFIG, encoding="utf-8")
    print(f"配置文件已初始化至 {target_path}")


if __name__ == "__main__":
    # 入口执行
    app()