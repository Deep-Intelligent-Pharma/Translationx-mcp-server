import uuid
from pydantic import Field

from server import mcp, host, headers
from utils import send_request


@mcp.tool(description="记忆库列表")
async def get_memory_lib_list(
        size: int = Field(10, description="每页数量"),
        page: int = Field(1, description="页数"),
        name: str = Field('', description="记忆库名称"),
):
    """
    Name:
        记忆库列表
    Description:
        记忆库列表
    Args:
        size: 每页数量
        page: 页数
        name: 记忆库名称
    """
    url = f"{host}/api/master_lib/memory/list"
    headers["x-request-id"] = f"mcp-{str(uuid.uuid4())}"
    data = {
        "size": size,
        "page": page,
        "name": name
    }
    return await send_request("POST", url, headers, None, data)


@mcp.tool(description="术语库列表")
async def get_term_lib_list(
        size: int = Field(10, description="每页数量"),
        page: int = Field(1, description="页数"),
        name: str = Field('', description="术语库名称"),
):
    """
    Name:
        术语库列表
    Description:
        术语库列表
    Args:
        size: 每页数量
        page: 页数
        name: 术语库名称
    """
    url = f"{host}/api/master_lib/term/list"
    headers["x-request-id"] = f"mcp-{str(uuid.uuid4())}"
    data = {
        "size": size,
        "page": page,
        "name": name
    }
    return await send_request("POST", url, headers, None, data=data)


@mcp.tool(description="创建记忆库")
async def create_memory_lib(
        name: str = Field(..., description="记忆库名称"),
        source_language: str = Field(...,
                                     description="源语言code {'世界语': 'eo', '中文(简体)': 'zh-cn', '丹麦语': 'da', '乌克兰语': 'uk', '乌兹别克语（拉丁）': 'uz', '乌尔都语': 'ur', '亚美尼亚语': 'hy', '伊博语': 'ig', '俄语': 'ru', '保加利亚语': 'bg', '信德语': 'sd', '修纳语': 'sn', '僧伽罗语': 'si', '克罗地亚语': 'hr', '克里奥语': 'kri', '冰岛语': 'is', '加利西亚语': 'gl', '加泰罗尼亚语': 'ca', '匈牙利语': 'hu', '南非荷兰语': 'af', '卡纳达语': 'kn', '卢森堡语': 'lb', '印地语': 'hi', '印度尼西亚语': 'id', '古吉拉特语': 'gu', '吉尔吉斯语（西里尔）': 'ky', '哈萨克语': 'kk', '土耳其语': 'tr', '塔吉克语': 'tg', '塞尔维亚语（拉丁）': 'sr-Latn', '塞尔维亚语（西里尔）': 'sr-Cyrl', '塞索托语': 'st', '夏威夷语': 'haw', '奥迪亚语': 'or', '威尔士语': 'cy', '孟加拉语': 'bn', '宿务语': 'ceb', '尼扬贾语': 'nya', '尼泊尔语': 'ne', '巴斯克语': 'eu', '巴西葡萄牙语': 'pt', '巽他语': 'su', '希伯来语': 'he', '希腊语': 'el', '库尔德语（中部）': 'ku', '库尔德语（北部）': 'kmr', '弗里西亚语': 'fy', '德语': 'de', '意大利语': 'it', '意第绪语': 'yi', '拉丁语': 'la', '拉脱维亚语': 'lv', '挪威语': 'nb', '捷克语': 'cs', '斯洛伐克语': 'sk', '斯洛文尼亚语': 'sl', '斯瓦希里语（拉丁）': 'sw', '旁遮普语': 'pa', '日文': 'ja', '普什图语': 'ps', '曼尼普尔语（美替隆语）': 'mni-Mtei', '未选择': '', '格鲁吉亚语': 'ka', '毛利语': 'mi', '法语': 'fr', '波兰语': 'pl', '波斯尼亚语（拉丁）': 'bs', '波斯语': 'fa', '泰卢固语': 'te', '泰米尔语': 'ta', '泰语': 'th', '海地克里奥尔语': 'ht', '爪哇语': 'jv', '爱尔兰语': 'ga', '爱沙尼亚语': 'et', '瑞典语': 'sv', '白俄罗斯语': 'be', '白苗语（拉丁）': 'mww', '祖鲁语': 'zu', '科萨语': 'xh', '科西嘉语': 'co', '立陶宛语': 'lt', '索马里语（阿拉伯）': 'so', '约鲁巴语': 'yo', '维吾尔语（阿拉伯）': 'ug', '缅甸语': 'my', '罗马尼亚语': 'ro', '老挝语': 'lo', '芬兰语': 'fi', '苏格兰盖尔语': 'gd', '英文': 'en', '荷兰语': 'nl', '菲律宾语': 'fil', '萨摩亚语（拉丁）': 'sm', '葡萄牙葡萄牙语': 'pt-pt', '蒙古语（传统）': 'mn-Mong', '蒙古语（西里尔）': 'mn-Cyrl', '西班牙语': 'es', '豪萨语': 'ha', '越南语': 'vi', '迪维希语': 'dv', '阿塞拜疆语（拉丁）': 'az', '阿姆哈拉语': 'am', '阿尔巴尼亚语': 'sq', '阿拉伯语': 'ar', '阿萨姆语': 'as', '韩语': 'ko', '马其顿语': 'mk', '马拉地语': 'mr', '马拉雅拉姆语': 'ml', '马来语（拉丁）': 'ms', '马耳他语': 'mt', '马达加斯加语': 'mg'}"),
        target_language: str = Field(...,
                                     description="目标语言code {'世界语': 'eo', '中文(简体)': 'zh-cn', '丹麦语': 'da', '乌克兰语': 'uk', '乌兹别克语（拉丁）': 'uz', '乌尔都语': 'ur', '亚美尼亚语': 'hy', '伊博语': 'ig', '俄语': 'ru', '保加利亚语': 'bg', '信德语': 'sd', '修纳语': 'sn', '僧伽罗语': 'si', '克罗地亚语': 'hr', '克里奥语': 'kri', '冰岛语': 'is', '加利西亚语': 'gl', '加泰罗尼亚语': 'ca', '匈牙利语': 'hu', '南非荷兰语': 'af', '卡纳达语': 'kn', '卢森堡语': 'lb', '印地语': 'hi', '印度尼西亚语': 'id', '古吉拉特语': 'gu', '吉尔吉斯语（西里尔）': 'ky', '哈萨克语': 'kk', '土耳其语': 'tr', '塔吉克语': 'tg', '塞尔维亚语（拉丁）': 'sr-Latn', '塞尔维亚语（西里尔）': 'sr-Cyrl', '塞索托语': 'st', '夏威夷语': 'haw', '奥迪亚语': 'or', '威尔士语': 'cy', '孟加拉语': 'bn', '宿务语': 'ceb', '尼扬贾语': 'nya', '尼泊尔语': 'ne', '巴斯克语': 'eu', '巴西葡萄牙语': 'pt', '巽他语': 'su', '希伯来语': 'he', '希腊语': 'el', '库尔德语（中部）': 'ku', '库尔德语（北部）': 'kmr', '弗里西亚语': 'fy', '德语': 'de', '意大利语': 'it', '意第绪语': 'yi', '拉丁语': 'la', '拉脱维亚语': 'lv', '挪威语': 'nb', '捷克语': 'cs', '斯洛伐克语': 'sk', '斯洛文尼亚语': 'sl', '斯瓦希里语（拉丁）': 'sw', '旁遮普语': 'pa', '日文': 'ja', '普什图语': 'ps', '曼尼普尔语（美替隆语）': 'mni-Mtei', '未选择': '', '格鲁吉亚语': 'ka', '毛利语': 'mi', '法语': 'fr', '波兰语': 'pl', '波斯尼亚语（拉丁）': 'bs', '波斯语': 'fa', '泰卢固语': 'te', '泰米尔语': 'ta', '泰语': 'th', '海地克里奥尔语': 'ht', '爪哇语': 'jv', '爱尔兰语': 'ga', '爱沙尼亚语': 'et', '瑞典语': 'sv', '白俄罗斯语': 'be', '白苗语（拉丁）': 'mww', '祖鲁语': 'zu', '科萨语': 'xh', '科西嘉语': 'co', '立陶宛语': 'lt', '索马里语（阿拉伯）': 'so', '约鲁巴语': 'yo', '维吾尔语（阿拉伯）': 'ug', '缅甸语': 'my', '罗马尼亚语': 'ro', '老挝语': 'lo', '芬兰语': 'fi', '苏格兰盖尔语': 'gd', '英文': 'en', '荷兰语': 'nl', '菲律宾语': 'fil', '萨摩亚语（拉丁）': 'sm', '葡萄牙葡萄牙语': 'pt-pt', '蒙古语（传统）': 'mn-Mong', '蒙古语（西里尔）': 'mn-Cyrl', '西班牙语': 'es', '豪萨语': 'ha', '越南语': 'vi', '迪维希语': 'dv', '阿塞拜疆语（拉丁）': 'az', '阿姆哈拉语': 'am', '阿尔巴尼亚语': 'sq', '阿拉伯语': 'ar', '阿萨姆语': 'as', '韩语': 'ko', '马其顿语': 'mk', '马拉地语': 'mr', '马拉雅拉姆语': 'ml', '马来语（拉丁）': 'ms', '马耳他语': 'mt', '马达加斯加语': 'mg'}"),

):
    url = f"{host}/api/master_lib/memory/add"
    headers["x-request-id"] = f"mcp-{str(uuid.uuid4())}"
    data = {
        "name": name,
        "source_language": source_language,
        "target_language": target_language
    }
    return await send_request("POST", url, headers, None, data=data)


@mcp.tool(description="添加记忆库条目")
async def add_memory_lib_entry(
        lib_id: str = Field(..., description="记忆库ID"),
        source_text: str = Field(..., description="源语言文本"),
        target_text: str = Field(..., description="目标语言文本"),
):
    url = f"{host}/api/master_lib/memory/add_entry"
    headers["x-request-id"] = f"mcp-{str(uuid.uuid4())}"
    data = {
        "lib_id": lib_id,
        "source_text": source_text,
        "target_text": target_text
    }
    return await send_request("POST", url, headers, None, data=data)
