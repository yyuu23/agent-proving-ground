from agent_proving_ground import Task, eval
from agent_proving_ground._util.environ import environ_var


def test_log_filename():
    with environ_var("APG_EVAL_LOG_FILE_PATTERN", "{task}_{model}_{id}"):
        log = eval(Task(), model="mockllm/model")[0]
        assert "mockllm-model" in log.location


def test_log_filename_no_plus_sign():
    log = eval(Task(), model="mockllm/model")[0]
    filename = log.location.split("/")[-1]
    assert "+" not in filename, f"Filename contains '+': {filename}"
