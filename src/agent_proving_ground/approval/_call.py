import inspect
from logging import getLogger

from agent_proving_ground._util.logger import warn_once
from agent_proving_ground._util.registry import registry_log_name
from agent_proving_ground.event._approval import ApprovalEvent
from agent_proving_ground.model._chat_message import ChatMessage
from agent_proving_ground.tool._tool_call import ToolCall, ToolCallView

from ._approval import Approval
from ._approver import Approver

logger = getLogger(__name__)


async def call_approver(
    approver: Approver,
    message: str,
    call: ToolCall,
    view: ToolCallView,
    history: list[ChatMessage],
) -> Approval:
    # run approver (if the approval is still using state then
    # provide that but issue a warning)
    signature = inspect.signature(approver)
    if "state" in signature.parameters.keys():
        from agent_proving_ground.solver._task_state import sample_state

        warn_once(
            logger, "Approver 'state' parameter is deprecated (use 'history' instead)"
        )
        approval = await approver(message, call, view, sample_state())  # type: ignore[arg-type]
    else:
        approval = await approver(message, call, view, history)

    # record
    record_approval(registry_log_name(approver), message, call, view, approval)

    # return approval
    return approval


def record_approval(
    approver_name: str,
    message: str,
    call: ToolCall,
    view: ToolCallView | None,
    approval: Approval,
) -> None:
    from agent_proving_ground.log._transcript import transcript

    transcript()._event(
        ApprovalEvent(
            message=message,
            call=call,
            view=view,
            approver=approver_name,
            decision=approval.decision,
            modified=approval.modified,
            explanation=approval.explanation,
            metadata=approval.metadata,
        )
    )
