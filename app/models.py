from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class WarningModel(BaseModel):
    _id: str
    guild_id: int
    user_id: int
    moderator_id: int
    reason: str
    timestamp: datetime

class GuildConfigModel(BaseModel):
    _id: int
    mod_log_channel: Optional[int]

class ModLogEntry(BaseModel):
    guild_id: int
    action: str
    moderator_id: int
    target_id: Optional[int]
    reason: str
    timestamp: datetime
