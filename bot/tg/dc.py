from dataclasses import dataclass, field
from typing import List, Optional
from dataclasses_json import Undefined, dataclass_json, config, CatchAll

@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class ChatObj:
    id: int
    unknown_things: CatchAll


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class FromObj:
    id: int
    unknown_things: CatchAll

@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class MessageObj:
    from_: FromObj = field(metadata=config(field_name="from"))
    chat: ChatObj
    text: str
    unknown_things: CatchAll


@dataclass
class UpdateObj:
    update_id: int
    message: Optional[MessageObj] = None
    edited_message: Optional[MessageObj] = None


@dataclass_json
@dataclass
class GetUpdatesResponse:
    ok: bool
    result: List[UpdateObj]


@dataclass_json
@dataclass
class SendMessageResponse:
    ok: bool
    result: MessageObj