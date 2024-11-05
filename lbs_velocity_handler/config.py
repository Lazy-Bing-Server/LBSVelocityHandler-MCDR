import os.path
import shutil
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
        psi = ServerInterface.psi()
        new_data_folder = psi.get_data_folder()
        old_data_folder = os.path.join('config', 'handler_velocity_lbs')
        if not os.path.isdir(new_data_folder) and os.path.isdir(old_data_folder):
            shutil.copytree(old_data_folder, new_data_folder)
        return ServerInterface.psi().load_config_simple(target_class=cls)
