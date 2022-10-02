from typing import List
import pathlib
import shutil

import pypandoc


def remove_dir(directory: pathlib.Path):
    if not directory.exists():
        return
    for child in directory.iterdir():
        if child.is_file():
            child.unlink()
        else:
            remove_dir(child)
    directory.rmdir()


def generate_page(input_file: pathlib.Path, output_file: pathlib.Path, navigation_file: pathlib.Path, css_files: List[pathlib.Path], depth: int):
    extra_args = [
        "--standalone",
        "--toc",
        "--variable=toc-title:Table of contents"
    ]
    for css_file in css_files:
        extra_args.append("--css")
        extra_args.append(("../" * depth) + str(css_file))

    if navigation_file is None:
        pypandoc.convert_file(
            str(input_file),
            "html5",
            outputfile=str(output_file),
            filters=["links_to_html.py"],
            extra_args=extra_args
        )
    else:
        extra_args.append("--include-before-body")
        extra_args.append(str(navigation_file))
        pypandoc.convert_file(
            str(input_file),
            "html5",
            outputfile=str(output_file),
            filters=["links_to_html.py"],
            extra_args=extra_args
        )


def generate_site():
    input_path = pathlib.Path("sources")
    output_path = pathlib.Path("docs")
    remove_dir(output_path)
    output_path.mkdir(exist_ok=True)

    css_files = []
    for file in input_path.iterdir():
        if file.is_file() and file.suffix == ".css":
            shutil.copy(file.absolute(), output_path / file.name)
            css_files.append(file.name)

    input_file = input_path / "index.md"
    output_file = output_path / "index.html"
    generate_page(input_file, output_file, None, css_files, 0)

    iterate_over_directory(input_path / "en", output_path / "en", input_path / "navigation.html", css_files, 1)
    iterate_over_directory(input_path / "fr", output_path / "fr", input_path / "navigation.html", css_files, 1)


def iterate_over_directory(input_path: pathlib.Path, output_path: pathlib.Path, navigation_file: pathlib.Path, css_files: List[pathlib.Path], depth: int):
    output_path.mkdir(exist_ok=True)
    for filename in input_path.iterdir():
        if filename.is_dir():
            iterate_over_directory(filename, output_path / filename.name, navigation_file, css_files, depth+1)
        elif filename.is_file():
            if filename.suffix == ".md":
                input_file = str(filename.absolute())
                output_file = str(output_path / filename.with_suffix(".html").name)
                generate_page(input_file, output_file, navigation_file, css_files, depth)
            elif filename.suffix == ".png":
                shutil.copy(filename.absolute(), output_path / filename.name)


if __name__ == "__main__":
    generate_site()