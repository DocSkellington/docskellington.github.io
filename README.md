title: Test based on README

[TOC]

# Building a website from Markdown files

This tool adds commands to easily define styles and classes in the HTML output.

* List test
* Multiple lines

End of list

    Some code block


## GFM specific

| foo | bar |
| --- | --- |
| baz | bim |

TODO list
- [ ] foo
- [x] bar

## Footnote

This is a test for a foonote.[^1]

[^1]: The corresponding footnote.

## Codehilite
```python
def test(a):
  return a + 2

print(test(2))
```

### How to define styles for code

Run ```pygmentize -S default -f html -a .highlight > test.css```
to obtain default style.
See [CodeHilite's documentation](https://python-markdown.github.io/extensions/code_hilite/) for more information.

## Attributes

Test
{: .test }

## Metadata

Metadata exist!

## Admonition

!!! note "Test for note"
    This is the first paragraph of the note.

    This is the second paragraph.

Out of the note.

## Wikilinks

[[sub page]]
