"""
Translate from OpenAI's `/v1/chat/completions` to VLLM's `/v1/chat/completions`
"""

from typing import List, Optional, Tuple

# from litellm.secret_managers.main import get_secret_str
from litellm.types.llms.openai import AllEmbeddingInputValues, AllMessageValues

# from ....utils import _remove_additional_properties, _remove_strict_from_schema
# from ...openai.chat.gpt_transformation import OpenAIGPTConfig
from litellm.llms.base_llm.embedding.transformation import BaseEmbeddingConfig
from ..panzhi_auth import create_header


class PanzhiEmbeddingConfig(BaseEmbeddingConfig):

    def transform_embedding_request(
        self,
        model: str,
        input: AllEmbeddingInputValues,
        optional_params: dict,
        headers: dict,
    ) -> dict:
        extra_body = optional_params.get("extra_body", {})

        # 获取并删除字段
        appid = extra_body.pop("panzhi_app_id", "")
        appkey = extra_body.pop("panzhi_app_key", "")
        auth_headers = create_header(appid=appid, appKey=appkey)
        optional_params.update({"extra_headers": auth_headers})
        return {
            "model": model,
            "input": input,
            **optional_params,
        }
