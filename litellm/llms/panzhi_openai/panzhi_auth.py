import logging
import math
import base64
import json
import hashlib

import logging
import os
from logging import handlers
import sys
import uuid
import time
sys.path.append(os.getcwd())


TDEV = 0  # 测试机器与北京时间的偏差（慢多少毫秒）
API_PATH = "/v1/chat/completions"


# 适配推理网关协议的头部构造方法
def create_header(appid:str = "", appKey:str = ""):
    """
    Generates the header for an 磐智 API request.

    Args:
        appid (str, optional): The application ID. Defaults to APPID.
        appKey (str, optional): The application key. Defaults to APPKey.

    Returns:
        dict: The header for the API request, containing the following keys:
            - "X-Server-Param" (str): The base64-encoded JSON string of the server parameters.
            - "X-CurTime" (str): The current time in Unix timestamp format.
            - "X-CheckSum" (str): The MD5 hash of the concatenated strings of the application key, current time, and server parameters.
            - 'Content-Type' (str): The content type of the request, set to 'application/json'.
    """
    # appid = APPID
    # appKey = APPKey
    # print("appid:",appid,"appKey:",appKey)
    # uuid = "52a7bb1fc08841ad9efc76d8ae1ef07b"
    if appid == "" or appKey == "":
        return {}
    uuid_str = str(uuid.uuid4())

    appName = API_PATH.split('/')[1]
    for i in range(24 - len(appName)):
        appName += "0"
    capabilityname = appName
    # print(len(capabilityname))
    csid = appid + capabilityname + uuid_str
    tmp_xServerParam = {
        "appid": appid,
        "csid": csid
    }
    # print(tmp_xServerParam)
    xCurTime = str(int(math.floor(time.time())) + TDEV)
    # print(xCurTime)
    xServerParam = str(base64.b64encode(json.dumps(
        tmp_xServerParam).encode('utf-8')), encoding="utf8")
    # xServerParam = str(base64.b64encode(json.dumps(tmp_xServerParam).encode('utf-8')))

    # turn to bytes
    xCheckSum = hashlib.md5(
        bytes(appKey + xCurTime + xServerParam, encoding="utf8")).hexdigest()
    # xCheckSum = hashlib.md5(bytes(appKey + xCurTime + xServerParam)).hexdigest()

    header = {
        # "appKey": appKey,
        "X-Server-Param": xServerParam,
        "X-CurTime": xCurTime,
        "X-CheckSum": xCheckSum,
        'Content-Type': 'application/json'
    }
    # print(header)

    return header