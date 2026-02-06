import os
import subprocess
from typing import Optional

from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()
CLIP_TOKEN = os.environ.get("CLIP_TOKEN", "")


def run_cmd(
    cmd: list[str], input_text: Optional[str] = None, fire_and_forget: bool = False
) -> str:
    if fire_and_forget:
        p = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            text=True,
        )
        if input_text and p.stdin:
            p.stdin.write(input_text)
            p.stdin.close()
        return ""
    else:
        p = subprocess.run(
            cmd,
            input=input_text,
            capture_output=True,
            text=True,
            timeout=5,
        )

        if p.returncode != 0:
            raise RuntimeError(p.stderr.strip() or "command failed")

        return p.stdout


def is_wayland() -> bool:
    return bool(os.environ.get("WAYLAND_DISPLAY"))


def set_clipboard(text: str) -> None:
    if is_wayland():
        run_cmd(["wl-copy"], input_text=text, fire_and_forget=True)
    else:
        run_cmd(["xclip", "-selection", "clipboard"], input_text=text)


def get_clipboard() -> str:
    if is_wayland():
        return run_cmd(["wl-paste", "--no-newline"])
    else:
        return run_cmd(["xclip", "-selection", "clipboard", "-o"])


def require_auth(auth: Optional[str]) -> None:
    if not CLIP_TOKEN:
        return
    if not auth or auth != f"Bearer {CLIP_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")
