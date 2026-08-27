from test_helpers.utils import (
    flaky_retry,
    skip_if_no_anthropic,
    skip_if_no_google,
    skip_if_no_moonshot,
    skip_if_no_openai,
)

from agent_proving_ground import Task, eval, task
from agent_proving_ground._util.constants import PKG_PATH
from agent_proving_ground._util.images import file_as_data_uri
from agent_proving_ground.dataset import Sample
from agent_proving_ground.model._model import get_model
from agent_proving_ground.scorer import includes
from agent_proving_ground.solver import generate, use_tools
from agent_proving_ground.tool import ContentImage, tool

IMAGES_PATH = PKG_PATH / ".." / ".." / "tests" / "dataset" / "test_dataset" / "images"


@tool
def camera():
    async def execute() -> ContentImage:
        """
        Take a picture of the environment.

        Returns:
            Image with a picture of the environment
        """
        ballons = (IMAGES_PATH / "ballons.png").as_posix()

        return ContentImage(image=await file_as_data_uri(ballons))

    return execute


@task
def camera_task():
    return Task(
        dataset=[
            Sample(
                input="Use the 'camera' tool to take a picture of the environment. What do you see?",
                target="balloons",
            )
        ],
        solver=[use_tools(camera()), generate()],
        scorer=includes(),
    )


@skip_if_no_openai
def test_openai_tool_image_result():
    check_tool_image_result("openai/gpt-4o")


@skip_if_no_openai
@flaky_retry(max_retries=3)
def test_openai_responses_tool_image_result():
    check_tool_image_result(get_model("openai/gpt-4o-mini", responses_api=True))


@skip_if_no_openai
@flaky_retry(max_retries=3)
def test_openai_o4_mini_tool_image_result():
    check_tool_image_result(get_model("openai/o4-mini"))


@skip_if_no_google
@flaky_retry(
    max_retries=3
)  # We've seen this fail when the model passes extra arguments to the tool
def test_google_tool_image_result():
    check_tool_image_result("google/gemini-2.5-pro")


@skip_if_no_anthropic
def test_anthropic_tool_image_result():
    check_tool_image_result("anthropic/claude-sonnet-4-5")


@skip_if_no_moonshot
def test_moonshot_tool_image_result():
    check_tool_image_result("moonshot/kimi-k3")


def check_tool_image_result(model):
    log = eval(camera_task(), model=model)[0]
    assert log.status == "success"
    assert log.samples
    assert log.samples[0].scores
    assert log.samples[0].scores["includes"].as_str() == "C"
