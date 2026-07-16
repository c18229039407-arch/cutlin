"""PixVerse video generation via fal.ai's hosted API.

Social-content oriented generator with stylized motion — a mid-budget
option between the draft tier (LTX/Wan) and the premium tier (Kling/Veo).
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


class PixverseVideo(BaseTool):
    name = "pixverse_video"
    version = "0.1.0"
    tier = ToolTier.GENERATE
    capability = "video_generation"
    provider = "pixverse"
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
        "stylized social-media clips with lively motion",
        "anime / illustration-flavored image-to-video",
        "mid-budget shots between draft and premium tiers",
    ]
    not_good_for = ["photoreal cinematic hero shots", "native dialogue audio"]
    fallback_tools = ["kling_video", "minimax_video", "wan_video_fal"]

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
                "enum": ["v4.5", "v5"],
                "default": "v4.5",
                "description": "PixVerse version on fal.",
            },
            "image_url": {"type": "string", "description": "Reference image URL (or data URI) for image_to_video"},
            "extra_params": {
                "type": "object",
                "description": "Advanced: extra payload fields passed straight to the fal endpoint.",
            },
            "output_path": {"type": "string", "default": "pixverse_output.mp4"},
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
        # PixVerse sits in the low-mid band on fal; a default 5s clip lands around $0.15-0.35.
        return 0.30

    def estimate_runtime(self, inputs: dict[str, Any]) -> float:
        return 120.0

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        api_key = self._get_api_key()
        if not api_key:
            return ToolResult(success=False, error="FAL_KEY not set. " + self.install_instructions)

        start = time.time()
        operation = inputs.get("operation", "text_to_video")
        variant = inputs.get("model_variant", "v4.5")  # v5 endpoint intermittently 500s on fal (2026-07)
        model_path = f"pixverse/{variant}/{operation.replace('_', '-')}"

        payload: dict[str, Any] = {"prompt": inputs["prompt"]}
        if operation == "image_to_video" and inputs.get("image_url"):
            payload["image_url"] = inputs["image_url"]
        payload.update(inputs.get("extra_params") or {})

        from tools.video._shared import probe_output, run_fal_queue_job

        output_path = inputs.get("output_path", "wan_fal_output.mp4")
        ok, info = run_fal_queue_job(model_path, payload, api_key, output_path)
        if not ok:
            return ToolResult(success=False, error=f"PixVerse generation failed: {info}")

        from pathlib import Path
        probed = probe_output(Path(info["path"]))
        return ToolResult(
            success=True,
            data={
                "provider": "pixverse",
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
