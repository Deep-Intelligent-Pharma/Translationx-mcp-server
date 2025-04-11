import contextvars
import os
from contextlib import asynccontextmanager
from typing import Union

import anyio
import httpx
import uvicorn
from pydantic import Field, BaseModel
from mcp.server.fastmcp import FastMCP
from utils import send_request
import uuid

from server import mcp, host, headers


@mcp.tool(description="获取文件列表")
async def file_list(
        keyword: str = Field("", description="文件名查询"),
        page: int = Field(1, description="页数"),
        size: int = Field(10, description="每页数量")
):
    """
    Name:
        文件列表信息
    Description:
        根据用户提供的文件名称，获取文件的信息
    Args:
        keyword: 用于查询文件的关键字
        page: 页数
        size: 每页的数量
    """
    url = f"{host}/api/trans/file_list"
    headers["x-request-id"] = f"mcp-{str(uuid.uuid4())}"
    data = {
        "page": page,
        "size": size,
        "keyword": keyword
    }
    return await send_request("POST", url, headers, None, data)


@mcp.tool(description="提交文件翻译")
async def submit_translation(
        file_ids: list,
        source_language: str,
        target_language: str,
        master_memory_libs: list[dict[str, Union[int, float]]] = None,
        master_term_lib_ids: list[int] = None,
):
    """
    Name:
        提交文件翻译
    Description:
        根据输入的参数提交翻译请求
        传入需要提交翻译的文件id列表，源文件的语种和目标语种
        语种对应的语种code为 {'世界语': 'eo', '中文(简体)': 'zh-cn', '丹麦语': 'da', '乌克兰语': 'uk', '乌兹别克语（拉丁）': 'uz', '乌尔都语': 'ur', '亚美尼亚语': 'hy', '伊博语': 'ig', '俄语': 'ru', '保加利亚语': 'bg', '信德语': 'sd', '修纳语': 'sn', '僧伽罗语': 'si', '克罗地亚语': 'hr', '克里奥语': 'kri', '冰岛语': 'is', '加利西亚语': 'gl', '加泰罗尼亚语': 'ca', '匈牙利语': 'hu', '南非荷兰语': 'af', '卡纳达语': 'kn', '卢森堡语': 'lb', '印地语': 'hi', '印度尼西亚语': 'id', '古吉拉特语': 'gu', '吉尔吉斯语（西里尔）': 'ky', '哈萨克语': 'kk', '土耳其语': 'tr', '塔吉克语': 'tg', '塞尔维亚语（拉丁）': 'sr-Latn', '塞尔维亚语（西里尔）': 'sr-Cyrl', '塞索托语': 'st', '夏威夷语': 'haw', '奥迪亚语': 'or', '威尔士语': 'cy', '孟加拉语': 'bn', '宿务语': 'ceb', '尼扬贾语': 'nya', '尼泊尔语': 'ne', '巴斯克语': 'eu', '巴西葡萄牙语': 'pt', '巽他语': 'su', '希伯来语': 'he', '希腊语': 'el', '库尔德语（中部）': 'ku', '库尔德语（北部）': 'kmr', '弗里西亚语': 'fy', '德语': 'de', '意大利语': 'it', '意第绪语': 'yi', '拉丁语': 'la', '拉脱维亚语': 'lv', '挪威语': 'nb', '捷克语': 'cs', '斯洛伐克语': 'sk', '斯洛文尼亚语': 'sl', '斯瓦希里语（拉丁）': 'sw', '旁遮普语': 'pa', '日文': 'ja', '普什图语': 'ps', '曼尼普尔语（美替隆语）': 'mni-Mtei', '未选择': '', '格鲁吉亚语': 'ka', '毛利语': 'mi', '法语': 'fr', '波兰语': 'pl', '波斯尼亚语（拉丁）': 'bs', '波斯语': 'fa', '泰卢固语': 'te', '泰米尔语': 'ta', '泰语': 'th', '海地克里奥尔语': 'ht', '爪哇语': 'jv', '爱尔兰语': 'ga', '爱沙尼亚语': 'et', '瑞典语': 'sv', '白俄罗斯语': 'be', '白苗语（拉丁）': 'mww', '祖鲁语': 'zu', '科萨语': 'xh', '科西嘉语': 'co', '立陶宛语': 'lt', '索马里语（阿拉伯）': 'so', '约鲁巴语': 'yo', '维吾尔语（阿拉伯）': 'ug', '缅甸语': 'my', '罗马尼亚语': 'ro', '老挝语': 'lo', '芬兰语': 'fi', '苏格兰盖尔语': 'gd', '英文': 'en', '荷兰语': 'nl', '菲律宾语': 'fil', '萨摩亚语（拉丁）': 'sm', '葡萄牙葡萄牙语': 'pt-pt', '蒙古语（传统）': 'mn-Mong', '蒙古语（西里尔）': 'mn-Cyrl', '西班牙语': 'es', '豪萨语': 'ha', '越南语': 'vi', '迪维希语': 'dv', '阿塞拜疆语（拉丁）': 'az', '阿姆哈拉语': 'am', '阿尔巴尼亚语': 'sq', '阿拉伯语': 'ar', '阿萨姆语': 'as', '韩语': 'ko', '马其顿语': 'mk', '马拉地语': 'mr', '马拉雅拉姆语': 'ml', '马来语（拉丁）': 'ms', '马耳他语': 'mt', '马达加斯加语': 'mg'}
        可以选择要使用的术语库和记忆库
        记忆库的格式为 {"memory_lib_id": 123, "threshold": 0.8}, memory_lib_id为记忆库ID，threshold为阈值
        术语库的格式为 [123, 456, 789], 123为术语库ID
    Args:
        file_ids: 文件ID列表
        source_language: 源语言code {'世界语': 'eo', '中文(简体)': 'zh-cn', '丹麦语': 'da', '乌克兰语': 'uk', '乌兹别克语（拉丁）': 'uz', '乌尔都语': 'ur', '亚美尼亚语': 'hy', '伊博语': 'ig', '俄语': 'ru', '保加利亚语': 'bg', '信德语': 'sd', '修纳语': 'sn', '僧伽罗语': 'si', '克罗地亚语': 'hr', '克里奥语': 'kri', '冰岛语': 'is', '加利西亚语': 'gl', '加泰罗尼亚语': 'ca', '匈牙利语': 'hu', '南非荷兰语': 'af', '卡纳达语': 'kn', '卢森堡语': 'lb', '印地语': 'hi', '印度尼西亚语': 'id', '古吉拉特语': 'gu', '吉尔吉斯语（西里尔）': 'ky', '哈萨克语': 'kk', '土耳其语': 'tr', '塔吉克语': 'tg', '塞尔维亚语（拉丁）': 'sr-Latn', '塞尔维亚语（西里尔）': 'sr-Cyrl', '塞索托语': 'st', '夏威夷语': 'haw', '奥迪亚语': 'or', '威尔士语': 'cy', '孟加拉语': 'bn', '宿务语': 'ceb', '尼扬贾语': 'nya', '尼泊尔语': 'ne', '巴斯克语': 'eu', '巴西葡萄牙语': 'pt', '巽他语': 'su', '希伯来语': 'he', '希腊语': 'el', '库尔德语（中部）': 'ku', '库尔德语（北部）': 'kmr', '弗里西亚语': 'fy', '德语': 'de', '意大利语': 'it', '意第绪语': 'yi', '拉丁语': 'la', '拉脱维亚语': 'lv', '挪威语': 'nb', '捷克语': 'cs', '斯洛伐克语': 'sk', '斯洛文尼亚语': 'sl', '斯瓦希里语（拉丁）': 'sw', '旁遮普语': 'pa', '日文': 'ja', '普什图语': 'ps', '曼尼普尔语（美替隆语）': 'mni-Mtei', '未选择': '', '格鲁吉亚语': 'ka', '毛利语': 'mi', '法语': 'fr', '波兰语': 'pl', '波斯尼亚语（拉丁）': 'bs', '波斯语': 'fa', '泰卢固语': 'te', '泰米尔语': 'ta', '泰语': 'th', '海地克里奥尔语': 'ht', '爪哇语': 'jv', '爱尔兰语': 'ga', '爱沙尼亚语': 'et', '瑞典语': 'sv', '白俄罗斯语': 'be', '白苗语（拉丁）': 'mww', '祖鲁语': 'zu', '科萨语': 'xh', '科西嘉语': 'co', '立陶宛语': 'lt', '索马里语（阿拉伯）': 'so', '约鲁巴语': 'yo', '维吾尔语（阿拉伯）': 'ug', '缅甸语': 'my', '罗马尼亚语': 'ro', '老挝语': 'lo', '芬兰语': 'fi', '苏格兰盖尔语': 'gd', '英文': 'en', '荷兰语': 'nl', '菲律宾语': 'fil', '萨摩亚语（拉丁）': 'sm', '葡萄牙葡萄牙语': 'pt-pt', '蒙古语（传统）': 'mn-Mong', '蒙古语（西里尔）': 'mn-Cyrl', '西班牙语': 'es', '豪萨语': 'ha', '越南语': 'vi', '迪维希语': 'dv', '阿塞拜疆语（拉丁）': 'az', '阿姆哈拉语': 'am', '阿尔巴尼亚语': 'sq', '阿拉伯语': 'ar', '阿萨姆语': 'as', '韩语': 'ko', '马其顿语': 'mk', '马拉地语': 'mr', '马拉雅拉姆语': 'ml', '马来语（拉丁）': 'ms', '马耳他语': 'mt', '马达加斯加语': 'mg'}
        target_language: 目标语言code {'世界语': 'eo', '中文(简体)': 'zh-cn', '丹麦语': 'da', '乌克兰语': 'uk', '乌兹别克语（拉丁）': 'uz', '乌尔都语': 'ur', '亚美尼亚语': 'hy', '伊博语': 'ig', '俄语': 'ru', '保加利亚语': 'bg', '信德语': 'sd', '修纳语': 'sn', '僧伽罗语': 'si', '克罗地亚语': 'hr', '克里奥语': 'kri', '冰岛语': 'is', '加利西亚语': 'gl', '加泰罗尼亚语': 'ca', '匈牙利语': 'hu', '南非荷兰语': 'af', '卡纳达语': 'kn', '卢森堡语': 'lb', '印地语': 'hi', '印度尼西亚语': 'id', '古吉拉特语': 'gu', '吉尔吉斯语（西里尔）': 'ky', '哈萨克语': 'kk', '土耳其语': 'tr', '塔吉克语': 'tg', '塞尔维亚语（拉丁）': 'sr-Latn', '塞尔维亚语（西里尔）': 'sr-Cyrl', '塞索托语': 'st', '夏威夷语': 'haw', '奥迪亚语': 'or', '威尔士语': 'cy', '孟加拉语': 'bn', '宿务语': 'ceb', '尼扬贾语': 'nya', '尼泊尔语': 'ne', '巴斯克语': 'eu', '巴西葡萄牙语': 'pt', '巽他语': 'su', '希伯来语': 'he', '希腊语': 'el', '库尔德语（中部）': 'ku', '库尔德语（北部）': 'kmr', '弗里西亚语': 'fy', '德语': 'de', '意大利语': 'it', '意第绪语': 'yi', '拉丁语': 'la', '拉脱维亚语': 'lv', '挪威语': 'nb', '捷克语': 'cs', '斯洛伐克语': 'sk', '斯洛文尼亚语': 'sl', '斯瓦希里语（拉丁）': 'sw', '旁遮普语': 'pa', '日文': 'ja', '普什图语': 'ps', '曼尼普尔语（美替隆语）': 'mni-Mtei', '未选择': '', '格鲁吉亚语': 'ka', '毛利语': 'mi', '法语': 'fr', '波兰语': 'pl', '波斯尼亚语（拉丁）': 'bs', '波斯语': 'fa', '泰卢固语': 'te', '泰米尔语': 'ta', '泰语': 'th', '海地克里奥尔语': 'ht', '爪哇语': 'jv', '爱尔兰语': 'ga', '爱沙尼亚语': 'et', '瑞典语': 'sv', '白俄罗斯语': 'be', '白苗语（拉丁）': 'mww', '祖鲁语': 'zu', '科萨语': 'xh', '科西嘉语': 'co', '立陶宛语': 'lt', '索马里语（阿拉伯）': 'so', '约鲁巴语': 'yo', '维吾尔语（阿拉伯）': 'ug', '缅甸语': 'my', '罗马尼亚语': 'ro', '老挝语': 'lo', '芬兰语': 'fi', '苏格兰盖尔语': 'gd', '英文': 'en', '荷兰语': 'nl', '菲律宾语': 'fil', '萨摩亚语（拉丁）': 'sm', '葡萄牙葡萄牙语': 'pt-pt', '蒙古语（传统）': 'mn-Mong', '蒙古语（西里尔）': 'mn-Cyrl', '西班牙语': 'es', '豪萨语': 'ha', '越南语': 'vi', '迪维希语': 'dv', '阿塞拜疆语（拉丁）': 'az', '阿姆哈拉语': 'am', '阿尔巴尼亚语': 'sq', '阿拉伯语': 'ar', '阿萨姆语': 'as', '韩语': 'ko', '马其顿语': 'mk', '马拉地语': 'mr', '马拉雅拉姆语': 'ml', '马来语（拉丁）': 'ms', '马耳他语': 'mt', '马达加斯加语': 'mg'}
        master_memory_libs: 记忆库列表 eg: {"memory_lib_id": 123, "threshold": 0.8}
        master_term_lib_ids: 术语库ID列表
    """
    source_language = "zh-cn" if source_language == "zh" else source_language
    target_language = "zh-cn" if target_language == "zh" else target_language
    url = f"{host}/api/trans/file_trans"
    headers["x-request-id"] = f"mcp-{str(uuid.uuid4())}"
    data = {
        "file_ids": file_ids,
        "source_language": source_language,
        "target_language": target_language,
        # TODO: 后续注释掉gpt_model
        "gpt_model": 6,
        "master_memory_libs": master_memory_libs or [],
        "master_term_lib_ids": master_term_lib_ids or []
    }
    return await send_request("POST", url, headers, None, data)
