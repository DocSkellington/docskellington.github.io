import builder.templates
from typing import Any, Dict


class DefaultTemplate(builder.templates.Template):
    name = "default"

    def __init__(self) -> None:
        super().__init__()
        self.css_files = [
            "resources/style.css",
            "resources/code.css",
            "https://cdn.jsdelivr.net/gh/iconoir-icons/iconoir@main/css/iconoir.css",
        ]
        self.script_files = []

    def build_document(
        self,
        body: str,
        metadata: Dict[str, Any],
        global_setup: builder.Global,
        toc: str,
    ) -> str:
        title = ""
        title_html = ""
        if "title" in metadata:
            title = metadata["title"][0]
            title_html = f'<h1 class="page-title">{title}</h1>'

        head = self._head(title, global_setup)
        header = self._header(metadata, global_setup)
        footer = self._footer(metadata, global_setup)

        return f"<html>{head}{header}{toc}<main>{title_html}{body}</main>{footer}</html>"

    def _header(self, metadata: Dict[str, Any], global_setup: builder.Global) -> str:
        header = "<header>"
        header += f"<div><a href='{builder.templates.add_base_url(global_setup.base_url, '''index.html''')}' class='title'>{global_setup.title}</a></div>"
        header += "<nav>"
        for link in global_setup.links_in_header:
            header += f"<div class='link'><a href='{builder.templates.add_base_url(global_setup.base_url, link[1])}'>{link[0]}</a></div>"
        header += "</nav>"
        header += "</header>"

        return header

    def _footer(self, metadata: Dict[str, Any], global_setup: builder.Global) -> str:
        footer = "<footer>"
        if global_setup.footer is not None:
            footer += f"<p class='left'>{global_setup.footer.description}</p>"
            footer += "<address class='right'>"
            for network_link in global_setup.footer.links:
                footer += f'<div class="network {network_link.network}">'
                footer += self._build_network_link(
                    network_link.network, network_link.link, network_link.text
                )
                footer += "</div>"
            footer += "</address>"
        footer += "</footer>"
        return footer
