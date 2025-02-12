"""
Calling logic for Databricks embeddings
"""

from typing import Optional

from litellm.utils import EmbeddingResponse

from ...openai_like.embedding.handler import OpenAILikeEmbeddingHandler
from ..panzhi_auth import create_header


class PanzhiEmbeddingHandler(OpenAILikeEmbeddingHandler):
    def embedding(
        self,
        model: str,
        input: list,
        timeout: float,
        logging_obj,
        api_key: Optional[str],
        api_base: Optional[str],
        optional_params: dict,
        model_response: Optional[EmbeddingResponse] = None,
        client=None,
        aembedding=None,
        custom_endpoint: Optional[bool] = None,
        headers: Optional[dict] = None,
    ) -> EmbeddingResponse:
        # api_base, headers = self.databricks_validate_environment(
        #     api_base=api_base,
        #     api_key=api_key,
        #     endpoint_type="embeddings",
        #     custom_endpoint=custom_endpoint,
        #     headers=headers,
        # )
        # print("optional_params", optional_params)

        # 获取并删除字段
        appid = optional_params.pop("panzhi_app_id", "")
        appkey = optional_params.pop("panzhi_app_key", "")
        # print("appid:", appid, "appKey:", appkey, "optional_params:", optional_params)
        auth_headers = create_header(appid=appid, appKey=appkey)
        headers = headers if headers else {}
        headers.update(auth_headers)
        # api_base = api_base if api_base else "https://api.panzhi.ai"
        # api_base += "/embeddings"
        return super().embedding(
            model=model,
            input=input,
            timeout=timeout,
            logging_obj=logging_obj,
            api_key=api_key,
            api_base=api_base,
            optional_params=optional_params,
            model_response=model_response,
            client=client,
            aembedding=aembedding,
            custom_endpoint=False,
            headers=headers,
        )
