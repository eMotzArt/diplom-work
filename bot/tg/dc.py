from dataclasses import dataclass, field
from typing import List, Optional
from dataclasses_json import Undefined, dataclass_json, config, CatchAll


# @dataclass
# class EntitiesObj:
#     offset: int
#     length: int
#     type: str

@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class ChatObj:
    id: int
    # first_name: str
    # last_name: str
    # username: str
    # type: str
    unknown_things: CatchAll


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class FromObj:
    id: int
    # is_bot: bool
    # first_name: str
    # username: str
    # last_name: Optional[str] = None
    # language_code: Optional[str] = None
    unknown_things: CatchAll

@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class MessageObj:
    # message_id: int
    from_: FromObj = field(metadata=config(field_name="from"))
    chat: ChatObj
    # date: int
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