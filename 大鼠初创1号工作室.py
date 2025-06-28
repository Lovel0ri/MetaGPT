import asyncio
from metagpt.roles import (
    TeamLeader,
    Engineer2,
    Architect,
    Engineer,
    ProductManager,
    ProjectManager,
    DataAnalyst,
    QaEngineer
)
from metagpt.team import Team


async def startup(idea: str):
    company = Team()
    company.hire(
        [
            TeamLeader(),  # 任务计划、分配与跟进
            ProductManager(),  # 撰写 PRD、用户故事
            Architect(),  # 设计系统架构
            ProjectManager(),  # 拆解任务并指派执行
            Engineer(),  # 编写业务逻辑代码
            Engineer2(),  # 具备编辑、部署、复查能力的高级工程角色
            # QaEngineer(),  # 编写测试案例并执行 QA
            # Searcher(),  # 信息检索与调研
            # DataAnalyst(),  # 数据分析与报告
            # Sales(),  # 客户交流与需求反馈
        ]
    )
    company.invest(investment=1.0)
    company.run_project(idea=idea)

    await company.run(n_round=10)


if __name__ == "__main__":
    asyncio.run(startup(idea="""
 
 使用python和django完成一个bi看板，实现电商数据管理。不用接入第三方存储库，主要是本地上传excel文件，支持可视化看板
    """))

