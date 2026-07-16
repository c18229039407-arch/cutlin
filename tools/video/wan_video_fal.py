"""Wan 2.2 (Alibaba, open weights) video generation via fal.ai's hosted API.

The budget workhorse of the cloud tier: the same Wan family as the local
`wan_video` tool, but running on fal's GPUs — no local VRAM required.
"""

from __future__ import annotations

import os
import time
from typing import Any

from tools.base_tool import (
    BaseTool,
    Determinism,
    ExecutionMode,
    ResourceProfile,
    RetryPolicy,
    ToolResult,
    ToolRuntime,
    ToolStability,
    ToolStatus,
    ToolTier,
)


class WanVideoFal(BaseTool):
    name = "wan_video_fal"
    version = "0.1.0"
    tier = ToolTier.GENERATE
    capability = "video_generation"
    provider = "wan"
    stability = ToolStability.EXPERIMENTAL
    execution_mode = ExecutionMode.SYNC
    determinism = Determinism.STOCHASTIC
    runtime = ToolRuntime.API

    dependencies = []
    install_instructions = (
        "Set FAL_KEY to your fal.ai API key.\n"
        "  Get one at https://fal.ai/dashboard/keys"
    )
    agent_skills = ["ai-video-gen"]

    capabilities = ["text_to_video", "image_to_video"]
    supports = {
        "text_to_video": True,
        "image_to_video": True,
        "native_audio": False,
        "cinematic_quality": False,
    }
    best_for = [
        "budget-tier motion clips when no local GPU is available",
        "high-volume iteration before committing to a premium model",
        "open-weights family consistency with the local wan_video tool",
    ]
    not_good_for = ["dialogue/native audio", "4K hero shots"]
    fallback_tools = ["wan_video", "kling_video", "minimax_video"]

    input_schema = {
        "type": "object",
        "properties": {
            "prompt": {"type": "string"},
            "operation": {
                "type": "string",
                "enum": ["text_to_video", "image_to_video"],
                "default": "text_to_video",
            },
            "model_variant": {
                "type": "string",
                "enum": ["v2.2-a14b"],
                "default": "v2.2-a14b",
                "description": "Wan variant hosted on fal.",
            },
            "image_url": {"type": "string", "description": "Reference image URL (or data URI) for image_to_video"},
            "extra_params": {
                "type": "object",
                "description": "Advanced: extra payload fields passed straight to the fal endpoint.",
            },
            "output_path": {"type": "string", "default": "wan_fal_output.mp4"},
        },
        "required": ["prompt"],
    }
    output_schema = {"type": "object"}

    resource_profile = ResourceProfile(network_required=True)
    retry_policy = RetryPolicy(max_retries=2, retryable_errors=["rate_limit", "timeout"])
    idempotency_key_fields = ["prompt", "model_variant", "operation"]
    side_effects = ["writes video file to output_path", "calls fal.ai API"]
    user_visible_verification = ["Watch generated clip for motion coherence"]

    def _get_api_key(self) -> str | None:
        return os.environ.get("FAL_KEY") or os.environ.get("FAL_AI_API_KEY")

    def get_status(self) -> ToolStatus:
        return ToolStatus.AVAILABLE if self._get_api_key() else ToolStatus.UNAVAILABLE

    def estimate_cost(self, inputs: dict[str, Any]) -> float:
        # fal lists Wan 2.2 A14B around $0.10/second; default clips run ~5s.
        return 0.50

    def estimate_runtime(self, inputs: dict[str, Any]) -> float:
        return 120.0

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        api_key = self._get_api_key()
        if not api_key:
            return ToolResult(success=False, error="FAL_KEY not set. " + self.install_instructions)

        start = time.time()
        operation = inputs.get("operation", "text_to_video")
        variant = inputs.get("model_variant", "v2.2-a14b")
        model_path = f"wan/{variant}/{operation.replace('_', '-')}"

        payload: dict[str, Any] = {"prompt": inputs["prompt"]}
        if operation == "image_to_video" and inputs.get("image_url"):
            payload["image_url"] = inputs["image_url"]
        payload.update(inputs.get("extra_params") or {})

        from tools.video._shared import probe_output, run_fal_queue_job

        output_path = inputs.get("output_path", "wan_fal_output.mp4")
        ok, info = run_fal_queue_job(model_path, payload, api_key, output_path)
        if not ok:
            return ToolResult(success=False, error=f"Wan (fal) generation failed: {info}")

        from pathlib import Path
        probed = probe_output(Path(info["path"]))
        return ToolResult(
            success=True,
            data={
                "provider": "wan",
                "channel": "fal",
                "model": f"fal-ai/{model_path}",
                "prompt": inputs["prompt"],
                "operation": operation,
                "output": info["path"],
                "output_path": info["path"],
                "format": "mp4",
                **probed,
            },
            artifacts=[info["path"]],
            cost_usd=self.estimate_cost(inputs),
            duration_seconds=round(time.time() - start, 2),
            model=f"fal-ai/{model_path}",
        )
