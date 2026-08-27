from typing import Sequence

from agent_proving_ground import Task, task
from agent_proving_ground.dataset import Sample, json_dataset
from agent_proving_ground.scorer import includes
from agent_proving_ground.solver import generate, system_message


def _filter_by_category(
    samples: Sequence[Sample], categories: str
) -> list[Sample]:
    """按逗号分隔的类别过滤样本;categories 为空则返回全部。"""
    if not categories:
        return list(samples)
    selected = {c.strip() for c in categories.split(",")}
    return [s for s in samples if s.metadata.get("category") in selected]


def _make_task(samples: Sequence[Sample]) -> Task:
    return Task(
        dataset=list(samples),
        solver=[
            system_message("请用简体中文简洁地回答问题。"),
            generate(),
        ],
        scorer=includes(),
    )


@task
def basic_qa(categories: str = ""):
    """自定义知识问答评测:内联样本版。

    Args:
        categories: 逗号分隔的类别过滤,如 "geography" 或
            "geography,science";留空则运行全部样本。
    """
    samples = [
        Sample(
            input="法国的首都是哪座城市?请用一个词回答。",
            target="巴黎",
            id="geo_001",
            metadata={"category": "geography"},
        ),
        Sample(
            input="中国的首都是哪座城市?请用一个词回答。",
            target="北京",
            id="geo_002",
            metadata={"category": "geography"},
        ),
        Sample(
            input="地球绕太阳公转一周大约需要多少天?请只回答一个整数。",
            target="365",
            id="sci_001",
            metadata={"category": "science"},
        ),
        Sample(
            input="一年中天数最少的月份是几月?请只回答月份。",
            target=["2月", "二月"],  # 多个可接受答案,命中任意一个即算对
            id="cal_001",
            metadata={"category": "common_sense"},
        ),
    ]
    return _make_task(_filter_by_category(samples, categories))


@task
def qa_from_json(categories: str = ""):
    """自定义知识问答评测:外部 JSON 数据集版(代码与题库分离)。

    Args:
        categories: 逗号分隔的类别过滤;留空则运行全部样本。
    """
    dataset = json_dataset("qa_dataset.json")  # 相对任务文件的路径
    return _make_task(_filter_by_category(list(dataset), categories))
