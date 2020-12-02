import os
from lsp_utils import NpmClientHandler


def plugin_loaded():
    LspYamlPlugin.setup()


def plugin_unloaded():
    LspYamlPlugin.cleanup()


class LspYamlPlugin(NpmClientHandler):
    package_name = __package__
    server_directory = 'language-server'
    server_binary_path = os.path.join(
        server_directory, 'node_modules', 'yaml-language-server', 'bin', 'yaml-language-server'
    )
