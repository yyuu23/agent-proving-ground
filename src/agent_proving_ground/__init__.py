# ruff: noqa: F401 F403 F405

from importlib.metadata import version as importlib_version

from agent_proving_ground._eval.eval import eval, eval_async, eval_retry, eval_retry_async
from agent_proving_ground._eval.evalset import eval_set
from agent_proving_ground._eval.list import list_tasks
from agent_proving_ground._eval.registry import task, task_source
from agent_proving_ground._eval.score import score, score_async
from agent_proving_ground._eval.task import (
    Epochs,
    SampleSource,
    Task,
    TaskInfo,
    TaskSource,
    task_with,
)
from agent_proving_ground._eval.task.enqueue import enqueue_task
from agent_proving_ground._eval.task.sample_source import enqueue_sample
from agent_proving_ground._eval.task.scan import ScannerConfig, Scanners
from agent_proving_ground._eval.task.tasks import Tasks
from agent_proving_ground._util.constants import PKG_NAME
from agent_proving_ground._view.view import view
from agent_proving_ground.agent._human.agent import human_cli
from agent_proving_ground.log._metric import recompute_metrics
from agent_proving_ground.log._score import edit_score
from agent_proving_ground.solver._human_agent import human_agent

__version__ = importlib_version(PKG_NAME)


__all__ = [
    "__version__",
    "eval",
    "eval_async",
    "eval_retry",
    "eval_retry_async",
    "eval_set",
    "list_tasks",
    "score",
    "score_async",
    "edit_score",
    "recompute_metrics",
    "Epochs",
    "Scanners",
    "ScannerConfig",
    "SampleSource",
    "Task",
    "Tasks",
    "TaskInfo",
    "TaskSource",
    "task",
    "task_source",
    "task_with",
    "enqueue_sample",
    "enqueue_task",
    "view",
]
