from __future__ import annotations

import asyncio
from pathlib import Path
from typing import final
from urllib.parse import unquote, urlparse
from urllib.request import urlopen

import sublime
from LSP.plugin import LspPlugin, OnPreStartContext, uri_handler
from LSP.protocol import DocumentUri
from lsp_utils import NodeManager
from sublime_lib import ResourcePath
from typing_extensions import override


def plugin_loaded() -> None:
    LspYamlPlugin.register()


def plugin_unloaded() -> None:
    LspYamlPlugin.unregister()


@final
class LspYamlPlugin(LspPlugin):

    @classmethod
    @override
    def on_pre_start_async(cls, context: OnPreStartContext) -> None:
        package_name = cls.plugin_storage_path.name
        NodeManager.on_pre_start_async(
            context,
            cls.plugin_storage_path,
            ResourcePath('Packages', package_name, 'language-server'),
            Path('node_modules', 'yaml-language-server', 'bin', 'yaml-language-server'),
            node_version_requirement='>=18',
        )

    @uri_handler('json-schema')
    async def handle_json_schema_uri(self, uri: DocumentUri, flags: sublime.NewFileFlags) -> sublime.Sheet | None:
        if not (session := self.weaksession()):
            return None
        parsed = urlparse(uri)
        http_url = unquote(parsed.fragment)
        try:
            content, syntax = await asyncio.get_running_loop().run_in_executor(
                None, _blocking_get_content_and_syntax, http_url
            )
        except Exception as ex:
            content = f"Error: {ex}"
            syntax = _DEFAULT_SYNTAX
        return (await session.open_scratch_buffer(http_url, content, syntax, flags)).sheet()


_DEFAULT_SYNTAX = "Packages/Text/Plain text.tmLanguage"


# TODO: Make async!
def _blocking_get_content_and_syntax(http_url: str) -> tuple[str, str]:
    syntax = _DEFAULT_SYNTAX
    with urlopen(http_url) as f:
        content = f.read().decode("utf-8").replace("\r", "")
    if syntax_obj := sublime.find_syntax_for_file(urlparse(http_url).path):
        syntax = syntax_obj.path
    return content, syntax
