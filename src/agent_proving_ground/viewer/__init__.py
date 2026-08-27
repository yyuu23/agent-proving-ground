"""Public viewer-configuration surface.

Typed Pydantic classes that a `Task` author passes via the `viewer=` argument
(see `Task.viewer`) to control how the AgentProvingGround log viewer renders scanner
output in the sidebar.
"""

from agent_proving_ground._util.deprecation import relocated_module_attribute
from agent_proving_ground.viewer._config import (
    MetadataField,
    SampleScoreView,
    SampleScoreViewSort,
    ScannerResultField,
    ScannerResultView,
    ScoreColorScale,
    TaskSamplesColumn,
    TaskSamplesColumnId,
    TaskSamplesSort,
    TaskSamplesView,
    ViewerConfig,
)

__all__ = [
    "MetadataField",
    "SampleScoreView",
    "SampleScoreViewSort",
    "ScannerResultField",
    "ScannerResultView",
    "ScoreColorScale",
    "TaskSamplesColumn",
    "TaskSamplesColumnId",
    "TaskSamplesSort",
    "TaskSamplesView",
    "ViewerConfig",
]


_RENAMED_IN = "0.3.218"
_REMOVED_IN = "0.4"

for old, new in [
    ("SamplesView", "TaskSamplesView"),
    ("SamplesColumn", "TaskSamplesColumn"),
    ("SamplesSort", "TaskSamplesSort"),
]:
    relocated_module_attribute(
        old,
        f"agent_proving_ground.viewer._config.{new}",
        _RENAMED_IN,
        _REMOVED_IN,
        f"'{old}' has been renamed to '{new}'. Please update your import.",
    )
