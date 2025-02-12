from litellm.proxy._types import UserAPIKeyAuth
from fastapi import Request

async def user_api_key_auth(request: Request, api_key: str) -> UserAPIKeyAuth: 
    # try: 
    #     modified_master_key = "sk-my-master-key"
    #     if api_key == modified_master_key:
    #         return UserAPIKeyAuth(api_key=api_key)
    #     raise Exception
    # except: 
    #     raise Exception
    return UserAPIKeyAuth(api_key=api_key)