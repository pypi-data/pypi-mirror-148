from dataclasses import dataclass
from typing import Optional

from apis.base_event import BaseEvent
from utilss.hash_util import string_fingerprint


@dataclass
class UserIdentifier(BaseEvent):
    organization_id: str
    email: str
    auth_token: Optional[dict]

    def hash_key(self):
        return string_fingerprint(f'{self.organization_id}-{self.email}')
