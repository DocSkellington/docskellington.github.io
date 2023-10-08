import pathlib
import builder
import cvbuilder
import cvbuilder.contexts.latex
import cvbuilder.contexts.html # Temporary workaround for a bug in the library
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
from cvbuilder.modules.text import LinkModule, TextModule

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

cv_builder.add_context(MarkdownContext("sources/academic/index.md", "Academic CV"))

cv_builder.add_module("logos", LogosModule())
cv_builder.add_module("summary", SummaryModule())
cv_builder.add_module("jobs", JobModule())
cv_builder.add_module("awards", AwardModule())
cv_builder.add_module(None, LinkModule("Publications", "My list of publications is given on a ", "publications.md", "specific page", ".", level=1))
cv_builder.add_module("projects", ProjectModule())
cv_builder.add_module(None, LinkModule("Talks and events", "The list of attended events and given talks is given on a ", "talks.md", "specific page", ".", level=1))
cv_builder.add_module(None, LinkModule("Teaching duties and supervision", "The list of my attending duties and supervised projects can be consulted on a ", "teaching.md", "specific page", ".", level=1))
cv_builder.add_module("languages", LanguageModule())
cv_builder.add_module(None, TextModule("Miscellaneous", "During the academic year 2016-2017, I won the 454th place (out of 5558) in University CodeSprint, and my team won the 43d place in the Benelux Algorithm Programming Contest (BAPC).", level=1))
cv_builder.add_module("contact", ContactModule())

cv_builder.build("resume/resume.json")

cv_builder = cvbuilder.Builder()
cv_builder.add_context(MarkdownContext("sources/academic/talks.md", "Given talks and attended events"))

cv_builder.add_module("talks", TalkModule())
cv_builder.add_module("events", EventModule())

cv_builder.build("resume/talks_events.json")

cv_builder = cvbuilder.Builder()
cv_builder.add_context(MarkdownContext("sources/academic/publications.md", "Publications"))

cv_builder.add_module("publications", PublicationModule())

cv_builder.build("resume/publications.json")

cv_builder = cvbuilder.Builder()
cv_builder.add_context(MarkdownContext("sources/academic/teaching.md", "Teaching duties and supervision"))

cv_builder.add_module("teaching", TeachModule())
cv_builder.add_module("supervision", SupervisionModule())

cv_builder.build("resume/teaching.json")

# Markdown -> HTML
input_folder = pathlib.Path("sources/")
output_folder = pathlib.Path("output/")
global_setup = builder.Global(
    title="Gaëtan Staquet",
    base_url="file:///home/gaetan/GitHub/Perso/docskellington.github.io/output/",
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
