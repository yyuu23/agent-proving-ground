from test_helpers.utils import identity_solver

from agent_proving_ground import Task, eval
from agent_proving_ground._util.constants import MODEL_NONE


def test_no_model():
    log = eval(Task(solver=identity_solver()), model=None)[0]
    assert log.status == "success"
    assert log.eval.model == MODEL_NONE
