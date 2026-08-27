from agent_proving_ground import Task, task
from agent_proving_ground.dataset import Sample
from agent_proving_ground.scorer import includes
from agent_proving_ground.solver import generate, use_tools
from agent_proving_ground.tool import ToolError, tool
from agent_proving_ground.util import sandbox


@tool
def list_files():
    async def execute(dir: str):
        """List the files in a directory.

        Args:
            dir: Directory

        Returns:
            File listing of the directory
        """
        result = await sandbox().exec(["ls", dir])
        if result.success:
            return result.stdout
        else:
            raise ToolError(result.stderr)

    return execute


@task
def file_probe():
    return Task(
        dataset=[
            Sample(
                input='Is there a file named "foo.txt" in the current directory?',
                target="Yes",
                files={"foo.txt": "hello"},
            ),
        ],
        solver=[use_tools([list_files()]), generate()],
        scorer=includes(),
        sandbox="docker",
    )
