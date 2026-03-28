from dataclasses import dataclass
from typing import Literal

# Tool middleware (wrap_tool_call): logging + retry
TOOL_CALL_MAX_RETRIES = 3
TOOL_CALL_RETRY_DELAY_SECONDS = 1.0


@dataclass
class AgentName:
    PLAN_AGENT = "plan_agent"
    EXECUTE_AGENT = "execute_agent"
    REVIEW_AGENT = "review_agent"


CategoryNameJAPANESE = Literal[
    "背表紙・表紙",
    "目次・インデックス",
    "備品引渡リスト",
    "工事完了報告書",
    "工事工程表",
    "竣工図面・施工図面",
    "試験成績書・検査表",
    "自主検査表",
    "機器構成表・一覧",
    "PCS・パワコン",
    "モジュール",
    "監視装置・通信機器",
    "納入機器仕様書",
    "取扱・操作説明書",
    "行政手続き書類",
    "電力手続き書類・回答",
    "保証書",
    "工事写真・写真帳",
    "強度計算書類",
    "その他・マニフェスト",
]