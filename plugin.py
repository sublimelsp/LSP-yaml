from __future__ import annotations

from pathlib import Path
from typing import final
from urllib.parse import unquote, urldefrag, urlparse
from urllib.request import urlopen

import sublime
from LSP.plugin import LspPlugin, OnPreStartContext, Promise, uri_handler
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
    def handle_json_schema_uri(self, uri: DocumentUri, flags: sublime.NewFileFlags) -> Promise[sublime.Sheet | None]:
        if not (session := self.weaksession()):
            return Promise.resolve(None)
        title = urldefrag(uri).url
        syntax = "Packages/Text/Plain text.tmLanguage"
        try:
            parsed = urlparse(uri)
            http_url = unquote(parsed.fragment)
            with urlopen(http_url) as f:
                content = f.read().decode("utf-8").replace("\r", "")
            if syntax_obj := sublime.find_syntax_for_file(urlparse(http_url).path):
                syntax = syntax_obj.path
        except Exception as ex:
            content = f"Error: {ex}"
        return session.open_scratch_buffer(title, content, syntax, uri, None, flags) \
            .then(lambda view: view.sheet() if view else None)
