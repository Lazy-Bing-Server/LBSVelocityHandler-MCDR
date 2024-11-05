import typing
import threading

from mcdreforged.api.all import PluginServerInterface, CommandSource
from mcdreforged.api.rtext import *
from mcdreforged.api.command import *

from lbs_velocity_handler.config import Config
from lbs_velocity_handler.velocity_handler import LBSVelocityHandler


__all__ = [
    "handler"
]


handler = LBSVelocityHandler()


class Main:
    def __init__(self):
        self.psi = PluginServerInterface.psi()
        self.config_read_lock = threading.RLock()
        with self.config_read_lock:
            self.__config = self.load_config()
        LBSVelocityHandler.set_inst(self)

    def load_config(self):
        with self.config_read_lock:
            return Config.load()

    def get_config(self):
        with self.config_read_lock:
            return self.__config

    def tr(self, translation_key: str, *args, _lbs_tr_prefix: typing.Optional[str] = None, **kwargs):
        if _lbs_tr_prefix is None:
            _lbs_tr_prefix = f"{self.psi.get_self_metadata().id}."
        return self.psi.rtr(f'{_lbs_tr_prefix}{translation_key}', *args, **kwargs)

    def reload_self(self, source: CommandSource):
        self.__config = self.load_config()
        source.reply(self.tr('reload.reloaded'))

    def plugin_credits(self, source: CommandSource):
        source.reply(RTextList(
            f'§7---- §b§l{self.psi.get_self_metadata().name}§r §7----\n',
            self.tr('credits.version'), f'§3§l{str(self.psi.get_self_metadata().version)}§r\n',
            self.tr(
                'credits.reload', pre=self.get_config().command_prefix
            ).c(
                RAction.run_command, f'{self.get_config().command_prefix} reload'
            ).h(
                self.tr('credits.reload_h')
            )
        ))

    def on_load(self, server: PluginServerInterface, prev_module):
        server.register_server_handler(handler)
        server.register_command(
            Literal(self.get_config().command_prefix).runs(self.plugin_credits).then(
                Literal('reload').requires(
                    lambda src: src.has_permission(self.get_config().admin_permission)
                ).runs(self.reload_self)
            )
        )
        server.register_help_message(self.get_config().command_prefix, self.tr('help.mcdr'))


__main = Main()


def on_load(server: PluginServerInterface, prev_module):
    __main.on_load(server, prev_module)
