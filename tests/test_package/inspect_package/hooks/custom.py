from agent_proving_ground.hooks import Hooks, RunStart


class CustomHooks(Hooks):
    async def on_run_start(self, event: RunStart) -> None:
        global run_ids
        run_ids.append(event.run_id)


run_ids: list[str] = []
