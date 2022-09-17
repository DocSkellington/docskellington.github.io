import pathlib

import pypandoc


def remove_dir(directory: pathlib.Path):
    for child in directory.iterdir():
        if child.is_file():
            child.unlink()
        else:
            remove_dir(child)
    directory.rmdir()


def generate_page(input_file: pathlib.Path, output_file: pathlib.Path, navigation_file: pathlib.Path):
    if navigation_file is None:
        pypandoc.convert_file(
            str(input_file),
            "html5",
            outputfile=str(output_file),
            filters=["links_to_html.py"],
            extra_args=["--standalone"]
        )
    else:
        pypandoc.convert_file(
            str(input_file),
            "html5",
            outputfile=str(output_file),
            filters=["links_to_html.py"],
            extra_args=["--standalone", "--include-before-body", str(navigation_file)]
        )


def generate_site():
    input_path = pathlib.Path("sources")
    output_path = pathlib.Path("site")
    remove_dir(output_path)
    output_path.mkdir(exist_ok=True)

    input_file = input_path / "index.md"
    output_file = output_path / "index.html"
    generate_page(input_file, output_file, None)

    iterate_over_directory(input_path / "en", output_path / "en", input_path / "en" / "navigation.html")
    iterate_over_directory(input_path / "fr", output_path / "fr", input_path / "fr" / "navigation.html")


def iterate_over_directory(input_path: pathlib.Path, output_path: pathlib.Path, navigation_file: pathlib.Path):
    output_path.mkdir(exist_ok=True)
    for filename in input_path.iterdir():
        if filename.is_dir():
            iterate_over_directory(filename, output_path / filename.name, navigation_file)
        elif filename.is_file():
            if filename.suffix == ".md":
                input_file = str(filename.absolute())
                output_file = str(output_path / filename.with_suffix(".html").name)
                generate_page(input_file, output_file, navigation_file)


if __name__ == "__main__":
    generate_site()