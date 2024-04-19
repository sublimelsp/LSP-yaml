from __future__ import annotations

import functools
import os
import urllib.parse
import urllib.request
from collections.abc import Callable

import sublime
from lsp_utils import NpmClientHandler


def plugin_loaded() -> None:
    LspYamlPlugin.setup()


def plugin_unloaded() -> None:
    LspYamlPlugin.cleanup()


class LspYamlPlugin(NpmClientHandler):
    package_name = __package__
    server_directory = "language-server"
    server_binary_path = os.path.join(
        server_directory,
        "node_modules",
        "yaml-language-server",
        "bin",
        "yaml-language-server",
    )

    def on_open_uri_async(self, uri: str, callback: Callable[[str, str, str], None]) -> bool:
        def run_blocking() -> None:
            title = urllib.parse.urldefrag(uri).url
            try:
                # TODO: Make async!
                parsed = urllib.parse.urlparse(uri)
                http_url = urllib.parse.unquote(parsed.fragment)
                with urllib.request.urlopen(http_url) as f:
                    content = f.read().decode("utf-8").replace("\r", "")
                if syntax_obj := sublime.find_syntax_for_file(urllib.parse.urlparse(http_url).path):
                    syntax = syntax_obj.path
            except Exception as ex:
                content = f"Error: {ex}"
                syntax = "Packages/Text/Plain text.tmLanguage"
            sublime.set_timeout_async(functools.partial(callback, title, content, syntax))

        if not uri.startswith("json-schema:"):
            return False

        sublime.set_timeout_async(run_blocking)
        return True
