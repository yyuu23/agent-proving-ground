from agent_proving_ground import Task, task
from agent_proving_ground.dataset import Sample
from agent_proving_ground.scorer import includes
from agent_proving_ground.solver import generate, use_tools
from agent_proving_ground.tool import web_browser


@task
def browser():
    return Task(
        dataset=[
            Sample(
                input="Use the web browser tool to navigate to https://www.aisi.gov.uk/. Then, see if you can find a page on the site that describes the work of the UK AISI. Then, summarize this work in two paragraphs."
            )
        ],
        solver=[
            use_tools(web_browser()),
            generate(),
        ],
        scorer=includes(),
        sandbox="docker",
    )
