import markdown
import markdown.extensions.wikilinks

text: str = ""
with open("README.md", "r", encoding="utf-8") as f:
    text = f.read()

md = markdown.Markdown(
    output_format="html",
    extensions=[
        "codehilite",
        "footnotes",
        "extra",
        "toc",
        "meta",
        "admonition",
        "sane_lists",
        markdown.extensions.wikilinks.WikiLinkExtension(base_url="file:///home/gaetan/GitHub/Perso/docskellington.github.io/", end_url=".html")
    ],
)
body = md.convert(text)
metadata = md.Meta  # pylint: disable=E1101

output = f"""<!doctype html>
<html lang="en-US">
  <head>
    <meta charset="utf-8" />
    <title>{metadata["title"][0]}</title>
    <link rel="stylesheet" href="test.css" />
  </head>
  <body>
    {body}
  </body>
</html>
"""

with open("output.html", "w", encoding="utf-8") as f:
    f.write(output)
