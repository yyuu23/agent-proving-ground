from agent_proving_ground._util.registry import registry_unqualified_name


def task_display_name(task_name: str) -> str:
    if task_name.startswith("hf/"):
        return task_name
    else:
        return registry_unqualified_name(task_name)
