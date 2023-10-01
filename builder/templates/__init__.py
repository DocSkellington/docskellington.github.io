import abc
import urllib
from typing import Dict, Any, List
from dataclasses import dataclass, field


@dataclass
class JavaScript:
    src: str
    id: str = ""
    other: List[str] = field(default_factory=list)


def add_base_url(base_url: str, link: str) -> str:
    try:
        url = urllib.parse.urlparse(link)
        if url.scheme == "":
            if base_url[-1] == "/":
                return base_url + link
            return base_url + "/" + link
        return link
    except ValueError:
        return None


class Template(abc.ABC):
    def __init__(self) -> None:
        self.css_files: List[str] = []
        self.script_files: List[JavaScript] = []

    def _head(self, title: str, global_setup: "builder.Global") -> str:
        head = f"""
<head>
<meta charset="utf-8" />
<title>{title} -- {global_setup.title}</title>
    """
        for css in self.css_files:
            url = add_base_url(global_setup.base_url, css)
            if url is None:
                print(f"Invalid CSS path {css}")
            else:
                head += f'<link rel="stylesheet" href="{url}"/>\n'

        for script in self.script_files:
            url = add_base_url(global_setup.base_url, script.src)
            if url is None:
                print(f"Invalid script path {script}")
            else:
                id = f'id="{script.id}"' if script.id != "" else ""
                other = " ".join(script.other)
                head += (
                    f'<script type="text/javascript" {id} {other} src="{url}"></script>'
                )

        head += "</head>"
        return head

    def build_document(
        self,
        body: str,
        metadata: Dict[str, Any],
        global_setup: "builder.Global",
        toc: str,
    ) -> str:
        raise NotImplementedError(
            "Each template must implement the method build_document"
        )

    def _build_network_link(self, network: str, link: str, text: str) -> str:
        network = network.lower()
        if network == "github":
            icon = "iconoir-github"
        elif network == "orcid":
            return (
                '<img class="contact-icon orcid" src="https://info.orcid.org/wp-content/uploads/2019/11/orcid_16x16.png" alt=""/>'
                + f'<a class="orcid-link" href="{link}">{text}</a>'
            )
        else:
            return f'<a href="{link}">{text}</a>'

        return (
            f'<i class="contact-icon {icon}"></i>'
            + f'<a class="{network}-link" href="{link}">{text}</a>'
        )
