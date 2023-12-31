from typing import List, Dict

from mcdreforged.api.all import Serializable, ServerInterface


class Config(Serializable):
    command_prefix: str = '!!hvl'
    admin_permission: int = 4
    replace_prefixes_map: Dict[str, str] = {
        "!!MCDR": "!!VMCDR",
        "!!VMCDR": "!!MCDR"
    }
    ignore_prefixes: List[str] = []
    player_chat_log_format: List[str] = [
        '[{server}] <{name}> {message}'
    ]

    @classmethod
    def load(cls):
        return ServerInterface.psi().load_config_simple(target_class=cls)
