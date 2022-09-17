import panflute

def markdown_links_to_html(elem, doc):
    if isinstance(elem, panflute.Link) and elem.url.endswith(".md"):
        elem.url = elem.url[:-3] + ".html"
        return elem

if __name__ == "__main__":
    panflute.run_filter(markdown_links_to_html)