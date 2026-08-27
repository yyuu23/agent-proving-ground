"""Textual TUI client for ``apg acp``.

Phase 1 — attach plumbing only. See
``design/acp/agent-acp-tui.md`` for the full phasing.
"""

from .app import ApgAcpApp, run_tui

__all__ = ["ApgAcpApp", "run_tui"]
