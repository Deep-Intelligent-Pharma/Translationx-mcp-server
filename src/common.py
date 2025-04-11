from enum import Enum

class ProjectFileStatusEnum(int, Enum):
    """
    项目文件状态
    """
    PARSE_IN = 14  # 解析中
    PARSE_FAIL = 15  # 解析失败
    NOT_ANALYSIS = 1  # 未分析
    ANALYSIS_IN = 5  # 分析中
    ANALYSIS_FAIL = 6  # 分析失败
    ANALYSIS_DONE = 7  # 已分析
    TRANSLATING = 2  # 翻译中
    TRANSLATION_FAILED = 3  # 翻译失败
    TRANSLATED = 4  # 已翻译
    POLISH_IN = 8  # 润色中
    POLISH_FAIL = 9  # 润色失败
    POLISH_DONE = 10  # 已润色