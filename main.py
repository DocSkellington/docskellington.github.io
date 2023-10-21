import pathlib
import builder
import cvbuilder
import cvbuilder.contexts.latex
import cvbuilder.contexts.html  # Temporary workaround for a bug in the library
from cvbuilder.contexts.markdown import MarkdownContext
from cvbuilder.modules.contact import ContactModule
from cvbuilder.modules.logos import LogosModule
from cvbuilder.modules.award import AwardModule
from cvbuilder.modules.event import EventModule
from cvbuilder.modules.job import JobModule
from cvbuilder.modules.language import LanguageModule
from cvbuilder.modules.project import ProjectModule
from cvbuilder.modules.publication import PublicationModule
from cvbuilder.modules.summary import SummaryModule
from cvbuilder.modules.supervision import SupervisionModule
from cvbuilder.modules.talk import TalkModule
from cvbuilder.modules.teach import TeachModule
from cvbuilder.modules.text import TextModule


def remove_dir(directory: pathlib.Path):
    if not directory.exists():
        return
    for child in directory.iterdir():
        if child.is_file():
            child.unlink()
        else:
            remove_dir(child)
    directory.rmdir()


# From resume.json
cv_builder = cvbuilder.Builder()

index = MarkdownContext("sources/academic/index.md", "Academic CV")
cv_builder.add_context(index)

index.add_module("logos", LogosModule())
index.add_module("summary", SummaryModule())
index.add_module("jobs", JobModule())
index.add_module("awards", AwardModule())
index.add_module(
    None,
    TextModule(
        "Publications",
        text="Please consult the [specific page](publications.md).",
        level=1,
    ),
)
index.add_module("projects", ProjectModule())
index.add_module(
    None,
    TextModule(
        "Talks and events",
        text="Please consult the [specific page](talks.md).",
        level=1,
    ),
)
index.add_module(
    None,
    TextModule(
        "Teaching duties and supervision",
        text="Please consult the [specific page](teaching.md).",
        level=1,
    ),
)
index.add_module("languages", LanguageModule())
index.add_module(
    None,
    TextModule(
        "Miscellaneous",
        "During the academic year 2016-2017, I won the 454th place (out of 5558) in University CodeSprint, and my team won the 43d place in the Benelux Algorithm Programming Contest (BAPC).",
        level=1,
    ),
)
index.add_module("contact", ContactModule())

talks = MarkdownContext("sources/academic/talks.md", "Given talks and attended events")
cv_builder.add_context(talks)

talks.add_module("talks", TalkModule())
talks.add_module("events", EventModule())

publications = MarkdownContext("sources/academic/publications.md", "Publications")
cv_builder.add_context(publications)

publications.add_module("publications", PublicationModule())

teaching = MarkdownContext(
    "sources/academic/teaching.md", "Teaching duties and supervision"
)
cv_builder.add_context(teaching)

teaching.add_module("teaching", TeachModule())
teaching.add_module("supervision", SupervisionModule())

cv_builder.build(
    [
        "resume/resume.json",
        "resume/jobs.json",
        "resume/publications.json",
        "resume/talks_events.json",
        "resume/teaching.json",
    ]
)

# Markdown -> HTML
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
