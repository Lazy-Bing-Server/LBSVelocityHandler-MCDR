from mcdreforged.api.all import Serializable, PluginServerInterface
from mcdreforged.api.command import *
import typing


PLUGIN_METADATA = {
    "id": 'lbs_velocity_handler_config_manager',
    'version': '0.1.0'
}


class Config(Serializable):
    redirect_map: typing.Dict[str, str] = {}
    ignore_words: typing.List[str] = []


config: Config

def get_redirect_map():
    return config.redirect_map


def get_ignore_words():
    return config.ignore_words


def on_load(server: PluginServerInterface, prev):
    global config
    config = server.load_config_simple(target_class=Config)
    server.register_command(
        Literal("!!lvhcm").then(
            Literal('reload').requires(lambda src: src.has_permission(4)).runs(
                lambda: server.reload_plugin(PLUGIN_METADATA['id'])
            )
        )
    )
