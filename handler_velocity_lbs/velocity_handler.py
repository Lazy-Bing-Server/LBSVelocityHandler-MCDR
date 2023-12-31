from parse import parse
import typing
import re
import json
from mcdreforged.handler.impl.velocity_handler import VelocityHandler
from mcdreforged.api.rtext import RTextBase
from mcdreforged.api.types import ServerInformation, Info, ServerInterface

if typing.TYPE_CHECKING:
    from mcdreforged.handler.abstract_server_handler import InfoSource
    from handler_velocity_lbs import Main


MessageText = typing.Union[str, RTextBase]
si = ServerInterface.si()


class LBSVelocityInfo(Info):
    def __init__(self, source: "InfoSource", raw_content: str):
        super().__init__(source, raw_content)
        self.subserver = None


class LBSVelocityHandler(VelocityHandler):
    __inst: typing.Optional["Main"] = None

    def get_name(self) -> str:
        return "lbs_velocity_handler"

    @classmethod
    def set_inst(cls, inst: "Main"):
        cls.__inst = inst
    
    @staticmethod
    def clean_console_color_code(text):
        return re.sub(r'\033\[(\d+(;\d+)?)?m', '', text)

    @classmethod
    def _get_server_stdout_raw_result(cls, text: str) -> LBSVelocityInfo:
        info = super()._get_server_stdout_raw_result(text)
        result = LBSVelocityInfo(info.source, info.raw_content)
        result.content = cls.clean_console_color_code(info.raw_content)
        return result

    def get_send_message_command(self, target: str, message: MessageText, server_information: ServerInformation) -> typing.Optional[str]:
        return "alertraw {} {}".format(target, self.format_message(message))

    @classmethod
    def format_message(cls, message: MessageText) -> str:
        if isinstance(message, RTextBase):
            return message.to_json_str()
        else:
            return json.dumps(str(message))

    def get_broadcast_message_command(self, message: MessageText, server_information: ServerInformation) -> typing.Optional[str]:
        return self.get_send_message_command("@a", message, server_information)

    @classmethod
    def _verify_player_name(cls, name: str):
        return re.fullmatch(r'\w+', name) is not None
    
    @classmethod
    def get_player_message_parsing_formatter(cls) -> typing.List[str]:
        return [
            '[{server}] <{name}> {message}'
        ]

    @classmethod
    def process_player_message(cls, text: str):
        config = cls.__inst.get_config()
        args = list(text.split(' ', 1))
        if args[0] in config.ignore_prefixes:
            return None
        redirect_map = config.redirect_prefixes_map
        if args[0] in redirect_map.keys():
            args[0] = redirect_map.get(args[0])
        return ' '.join(args)
    
    def parse_server_stdout(self, text: str) -> Info:
        result: LBSVelocityInfo = super().parse_server_stdout(text)
        for formatter in self.get_player_message_parsing_formatter():
            parsed = parse(formatter, result.content)
            if parsed is not None and self._verify_player_name(parsed['name']):
                text = self.process_player_message(parsed['message'])
                if text is not None:
                    result.player, result.content, result.subserver = parsed['name'], text, parsed.named.get('server')
                    break
        return result
