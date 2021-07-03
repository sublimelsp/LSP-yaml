from LSP.plugin.core.typing import Callable
from lsp_utils import NpmClientHandler
import functools
import os
import sublime
import urllib.parse
import urllib.request


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

    def on_open_uri_async(self, uri: str, callback: Callable[[str, str, str], None]) -> bool:
        if not uri.startswith("json-schema:"):
            return False

        def run_blocking() -> None:
            title = urllib.parse.urldefrag(uri).url
            try:
                # TODO: Make async!
                parsed = urllib.parse.urlparse(uri)
                http_url = urllib.parse.unquote(parsed.fragment)
                with urllib.request.urlopen(http_url) as f:
                    content = f.read().decode('utf-8').replace("\r", "")
                syntax = sublime.find_syntax_for_file(urllib.parse.urlparse(http_url).path).path
            except Exception as ex:
                content = "Error: {}".format(ex)
                syntax = "Packages/Text/Plain text.tmLanguage"
            sublime.set_timeout_async(functools.partial(callback, title, content, syntax))

        sublime.set_timeout_async(run_blocking)
        return True
