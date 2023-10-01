import xml.etree.ElementTree as etree
import markdown.treeprocessors


class ClickableImageProcessor(markdown.treeprocessors.Treeprocessor):
    def run(self, root: etree.Element):
        # Since the processor changes every 'img' into 'a/img',
        # we do not want to perform the process if we already have 'a/img'
        for img_parent in root.findall(".//*[img]"):
            if img_parent.tag != "a":
                for img in img_parent.findall("./img"):
                    attrib = img.attrib
                    tail = img.tail
                    src = attrib.get("src")

                    img.clear()
                    img.tag = "a"
                    img.set("href", src)
                    etree.SubElement(img, "img", attrib=attrib)
                    img.tail = tail


class ClickableImageExtension(markdown.Extension):
    def extendMarkdown(self, md):
        md.treeprocessors.register(
            ClickableImageProcessor(md), "clickableimageprocessor", 7
        )
