"""
Translate from OpenAI's `/v1/chat/completions` to VLLM's `/v1/chat/completions`
"""

from typing import List, Optional, Tuple

from litellm.secret_managers.main import get_secret_str
from litellm.types.llms.openai import AllMessageValues

from ....utils import _remove_additional_properties, _remove_strict_from_schema
from ...openai.chat.gpt_transformation import OpenAIGPTConfig
from ..panzhi_auth import create_header


class PanzhiChatConfig(OpenAIGPTConfig):
    def map_openai_params(
        self,
        non_default_params: dict,
        optional_params: dict,
        model: str,
        drop_params: bool,
    ) -> dict:
        print("non_default_params", non_default_params)
        print("optional_params", optional_params)
        _tools = non_default_params.pop("tools", None)
        if _tools is not None:
            # remove 'additionalProperties' from tools
            _tools = _remove_additional_properties(_tools)
            # remove 'strict' from tools
            _tools = _remove_strict_from_schema(_tools)
        if _tools is not None:
            non_default_params["tools"] = _tools
        return super().map_openai_params(
            non_default_params, optional_params, model, drop_params
        )

    def _get_openai_compatible_provider_info(
        self, api_base: Optional[str], api_key: Optional[str]
    ) -> Tuple[Optional[str], Optional[str]]:
        api_base = api_base or get_secret_str("HOSTED_VLLM_API_BASE")  # type: ignore
        dynamic_api_key = (
            api_key or get_secret_str("HOSTED_VLLM_API_KEY") or "fake-api-key"
        )  # vllm does not require an api key
        return api_base, dynamic_api_key

    def transform_request(
        self,
        model: str,
        messages: List[AllMessageValues],
        optional_params: dict,
        litellm_params: dict,
        headers: dict,
    ) -> dict:
        """
        Transform the overall request to be sent to the API.

        Returns:
            dict: The transformed request. Sent as the body of the API call.
        """
        # print("optional_params", optional_params)
        # print("litellm_params", litellm_params)
        # print("headers", headers)
        extra_body = optional_params.get("extra_body", {})

        # 获取并删除字段
        appid = extra_body.pop("panzhi_app_id", "")
        appkey = extra_body.pop("panzhi_app_key", "")
        # print("appid:", appid, "appKey:", appkey, "optional_params:", optional_params)
        auth_headers = create_header(appid=appid, appKey=appkey)
        optional_params.update({"extra_headers": auth_headers})
        messages = self._transform_messages(messages=messages, model=model)
        return {
            "model": model,
            "messages": messages,
            **optional_params,
        }
