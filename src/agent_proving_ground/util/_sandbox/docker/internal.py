from agent_proving_ground._util.constants import PKG_PATH
from agent_proving_ground._util.error import PrerequisiteError
from agent_proving_ground.util._display import display_type
from agent_proving_ground.util._subprocess import subprocess

APG_WEB_BROWSER_IMAGE_DOCKERHUB_DEPRECATED = "aisiuk/inspect-web-browser-tool"

APG_WEB_BROWSER_IMAGE_DEPRECATED = "inspect_web_browser"
APG_COMPUTER_IMAGE = "inspect-computer-tool"

INTERNAL_IMAGES = {
    APG_WEB_BROWSER_IMAGE_DEPRECATED: PKG_PATH
    / "tool"
    / "_tools"
    / "_web_browser"
    / "_resources",
    APG_COMPUTER_IMAGE: PKG_PATH / "tool" / "beta" / "_computer" / "_resources",
}


async def is_internal_image_built(image: str) -> bool:
    result = await subprocess(
        ["docker", "images", "--filter", f"reference={image}", "--format", "json"]
    )
    return len(result.stdout.strip()) > 0


async def build_internal_image(image: str) -> None:
    args = [
        "docker",
        "build",
        "--tag",
        image,
        "--progress",
        "plain" if display_type() == "plain" else "auto",
    ]
    if display_type() == "none":
        args.append("--quiet")
    result = await subprocess(
        args + [INTERNAL_IMAGES[image].as_posix()],
        capture_output=False,
    )
    if not result.success:
        raise PrerequisiteError(f"Unexpected error building Docker image '{image}'")


def is_internal_image(image: str) -> bool:
    return any([image == internal for internal in INTERNAL_IMAGES.keys()])
