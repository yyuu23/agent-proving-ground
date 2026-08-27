from datetime import datetime, timedelta, timezone

from agent_proving_ground import Task, task
from agent_proving_ground.dataset import FieldSpec, example_dataset
from agent_proving_ground.scorer import model_graded_qa
from agent_proving_ground.solver import generate, use_tools
from agent_proving_ground.tool import web_search

openai_options = {
    "search_context_size": "high",
    "user_location": {
        "type": "approximate",
        "country": "US",
        "city": "Boston",
    },
}

tavily_options = {"max_results": 5, "max_connections": 8}

gemini_options = {
    "time_range_filter": {
        "start_time": datetime.now(timezone.utc).replace(microsecond=0)
        - timedelta(days=365),
        "end_time": datetime.now(timezone.utc).replace(microsecond=0),
    }
}


@task
def biology_qa() -> Task:
    return Task(
        dataset=example_dataset(
            name="biology_qa",
            sample_fields=FieldSpec(input="question", target="answer"),
        ),
        solver=[
            use_tools(
                web_search(
                    providers={
                        "grok": True,
                        "openai": openai_options,
                        "anthropic": True,
                        "tavily": tavily_options,
                        "gemini": gemini_options,
                    },
                )
            ),
            generate(),
        ],
        scorer=model_graded_qa(),
    )
