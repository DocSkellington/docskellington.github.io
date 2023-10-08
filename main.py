import pathlib
import builder


def remove_dir(directory: pathlib.Path):
    if not directory.exists():
        return
    for child in directory.iterdir():
        if child.is_file():
            child.unlink()
        else:
            remove_dir(child)
    directory.rmdir()


input_folder = pathlib.Path("sources/")
output_folder = pathlib.Path("output/")
global_setup = builder.Global(
    title="Gaëtan Staquet",
    base_url="https://docskellington.github.io/",
    links_in_header=[
        ("Home page", "index.html"),
        ("Academic CV", "academic/index.html"),
        ("Non-academic part (English)", "nonacademic/en/index.html"),
        ("Non-academic part (French)", "nonacademic/fr/index.html"),
    ],
    footer=builder.Footer(
        "Website of Gaëtan Staquet, PhD Student in Computer Science.",
        [
            builder.Link(
                "Github", "https://github.com/DocSkellington", "DocSkellington"
            ),
            builder.Link(
                "Orcid", "https://orcid.org/0000-0001-5795-3265", "0000-0001-5795-3265"
            ),
        ],
    ),
)

builder.templates.category_to_icon.add_iconoir("Github", "iconoir-github")
builder.templates.category_to_icon.add_icon(
    "orcid",
    lambda: '<img class="icon orcid" src="https://info.orcid.org/wp-content/uploads/2019/11/orcid_16x16.png" alt=""/>',
)

remove_dir(output_folder)

builder.build_site(input_folder, output_folder, global_setup)
