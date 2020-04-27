import os
import shutil
import sublime

from LSP.plugin.core.handlers import LanguageHandler
from LSP.plugin.core.settings import ClientConfig, read_client_config
from LSP.plugin.core.typing import Dict, List
from lsp_utils import ServerNpmResource

PACKAGE_NAME = 'LSP-yaml'
SETTINGS_FILENAME = 'LSP-yaml.sublime-settings'
SERVER_DIRECTORY = 'yaml-language-server-resources'
SERVER_BINARY_PATH = os.path.join(SERVER_DIRECTORY, 'node_modules', 'yaml-language-server',
                                  'bin', 'yaml-language-server')

server = ServerNpmResource(PACKAGE_NAME, SERVER_DIRECTORY, SERVER_BINARY_PATH)


def plugin_loaded():
    server.setup()


def plugin_unloaded():
    server.cleanup()


def is_node_installed():
    return shutil.which('node') is not None


class LspYamlPlugin(LanguageHandler):
    def __init__(self) -> None:
        self._default_schemas = []  # type: List[Dict]

    @property
    def name(self) -> str:
        return PACKAGE_NAME.lower()

    @property
    def config(self) -> ClientConfig:
        # Calling setup() also here as this might run before `plugin_loaded`.
        # Will be a no-op if already ran.
        # See https://github.com/sublimelsp/LSP/issues/899
        server.setup()

        configuration = self.migrate_and_read_configuration()

        default_configuration = {
            'enabled': True,
            'command': ['node', server.binary_path, '--stdio'],
        }

        default_configuration.update(configuration)

        return read_client_config(self.name, default_configuration)

    def migrate_and_read_configuration(self) -> dict:
        settings = {}
        loaded_settings = sublime.load_settings(SETTINGS_FILENAME)

        if loaded_settings:
            # No migration needed (yet)

            # Read configuration keys
            for key in ['languages', 'settings']:
                settings[key] = loaded_settings.get(key)

        return settings

    def on_start(self, window) -> bool:
        if not is_node_installed():
            sublime.status_message('Please install Node.js for the YAML Language Server to work.')
            return False
        return server.ready
