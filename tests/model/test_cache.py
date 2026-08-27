from datetime import datetime, timezone
from pathlib import Path

import pytest
from test_helpers.utils import run_example

from agent_proving_ground import Task, eval
from agent_proving_ground.dataset import Sample
from agent_proving_ground.event._model import ModelEvent
from agent_proving_ground.log import EvalSample
from agent_proving_ground.solver import generate


def test_cache_examples():
    logs = run_example("cache.py", model="mockllm/model")
    assert all(log.status == "success" for log in logs)


def test_cache(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    # The miss-then-hit assertion below requires a cache no other test can
    # touch: under pytest-xdist a concurrent worker (e.g. test_cache_examples
    # exercising expiry policies) can evict entries from the shared cache dir
    # between the two evals.
    monkeypatch.setenv("APG_CACHE_DIR", str(tmp_path))

    # helper to check for cache hit
    def sample_cache_hit(sample: EvalSample) -> bool:
        return (
            sum(
                1
                for event in sample.events
                if (isinstance(event, ModelEvent) and event.cache == "read")
            )
            > 0
        )

    timestamp = str(datetime.now(timezone.utc))

    def check_eval_with_cache(cache_hit: bool):
        log = eval(
            Task(
                dataset=[Sample(input=f"What is the timestamp: {timestamp}")],
                solver=[generate(cache=True)],
            ),
            model="mockllm/model",
        )[0]
        assert log.samples
        assert sample_cache_hit(log.samples[0]) == cache_hit

    # first eval should miss the cache and the second should hit it
    check_eval_with_cache(False)
    check_eval_with_cache(True)
