from pathlib import Path
from typing import Union, Dict, Any, List, Tuple
from dataclasses import dataclass
import pkgutil
import importlib
import inspect
import shutil

import markdown
import markdown.extensions.wikilinks
import md2html_links

import builder.templates
import builder.extensions


@dataclass
class NetworkLink:
    network: str
    link: str
    text: str


@dataclass
class Footer:
    description: str
    links: List[NetworkLink]


@dataclass
class Global:
    title: str
    base_url: str
    links_in_header: List[Tuple[str, str]]
    footer: Footer = None


def build_site(
    input_folder: Union[Path, str],
    output_folder: Union[Path, str],
    global_setup: Global,
) -> None:
    if isinstance(input_folder, str):
        input_folder = Path(input_folder)
    if isinstance(output_folder, str):
        output_folder = Path(output_folder)

    output_folder.mkdir(exist_ok=True, parents=True)

    markdown_converter = markdown.Markdown(
        extensions=[
            "codehilite",
            "footnotes",
            "extra",
            "toc",
            "meta",
            "admonition",
            "sane_lists",
            markdown.extensions.wikilinks.WikiLinkExtension(
                base_url=f"{global_setup.base_url}",
                end_url=".html",
            ),
            md2html_links.CustomLinkExtension(),
            "markdown_katex",
            "caption",
            "image_captions",
            "table_captions",
            builder.extensions.ClickableImageExtension(),
            "smarty",
        ],
        extension_configs={"toc": {"toc_depth": 3, "baselevel": 2}},
    )

    for file in input_folder.iterdir():
        if file.is_dir():
            build_site(file, output_folder / file.stem, global_setup)
        elif file.is_file():
            if file.suffix == ".md":
                print(f"Building {file}")
                _build_file(
                    markdown_converter,
                    file,
                    output_folder / (file.stem + ".html"),
                    global_setup,
                )
            else:
                print(f"Copying {file}")
                shutil.copy(file.absolute(), output_folder / file.name)


def _get_template(template_name: str) -> builder.templates.Template:
    for module in pkgutil.iter_modules(path=["builder/templates/"]):
        template_module = importlib.import_module(f"builder.templates.{module.name}")
        for element in dir(template_module):
            element = getattr(template_module, element)
            if (
                inspect.isclass(element)
                and element.__module__ == template_module.__name__
            ):
                if element.name == template_name:
                    return element()
    print(
        f"Could not find a template named {template_name}. Default layout will be used."
    )
    return None


def _build_file(
    markdown_converter: markdown.Markdown,
    input_file: Path,
    output_file: Path,
    global_setup: Global,
) -> None:
    html = ""
    with open(input_file, "r", encoding="UTF-8") as file:
        html = markdown_converter.convert(file.read())
    metadata: Dict[str, Any] = markdown_converter.Meta  # pylint: disable=E1101

    template: builder.templates.Template = _get_template(
        metadata.get("layout", ["default"])[0]
    )
    if template is None:
        template = _get_template("default")

    output = template.build_document(
        html, metadata, global_setup, markdown_converter.toc
    )

    with open(output_file, "w", encoding="UTF-8") as file:
        file.write(output)
