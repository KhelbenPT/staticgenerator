from enum import Enum
from textnode import *
from htmlnode import *
class BlockType(Enum):
	PARAGRAPH = "paragraph"
	HEADING = "heading"
	CODE = "code"
	QUOTE = "quote"
	UNORDERED_LIST = "unordered_list"
	ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
	blocks = markdown.split("\n\n")
	striped_blocks = []
	for block in blocks:
		if len(block) == 0:
			continue
		striped_blocks.append(block.strip())

	return striped_blocks

def block_to_block_type(block):
	if block.startswith(("#", "##", "###", "####", "#####", "######")):
		return BlockType.HEADING
	if block.startswith("```") and block.endswith("```"):
		return BlockType.CODE
	splited= block.splitlines()
	if all(split.startswith(">") for split in splited):
		return BlockType.QUOTE
	if all(split.startswith("- ") for split in splited):
		return BlockType.UNORDERED_LIST
	if all(split.startswith(("1. ","2. ","3. ","4. ","5. ","6. ","7. ","8. ","9. ","0. ")) for split in splited):
		order = [int(split[0]) for split in splited]
		if order == list(range(order[0], order[-1] +1)):
			return BlockType.ORDERED_LIST
	return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
	blocks = markdown_to_blocks(markdown)
	nodes = []
	for block in blocks:
		if len(block) > 0:
			block_type = block_to_block_type((block))
			if block_type == BlockType.PARAGRAPH:
				lines = block.splitlines()
				paragraph = ""
				for line in lines:
					paragraph = paragraph + line.strip() + " "
				nodes.append(text_to_children(paragraph.rstrip(), "p"))
			if block_type == BlockType.HEADING:
				heading = block.split()[0].count("#")
				nodes.append(text_to_children((block.strip("# ")), f"h{heading}"))
			if block_type == BlockType.QUOTE:
				lines = block.splitlines()
				quote = ""
				for line in lines:
					if len(line) > 0:
						quote = quote + line.strip(">").strip() + "\n"
				nodes.append(text_to_children(quote, "blockquote"))
			if block_type == BlockType.CODE:
				lines = block.strip("```").splitlines()
				code_lines = ""
				for line in lines:
					if len(line) > 0:
						code_lines = code_lines + line.strip() + "\n"
				code_lines = code_lines.rstrip("\n")
				children = ParentNode("pre", [LeafNode("code", code_lines)])
				nodes.append(children)
			if block_type == BlockType.UNORDERED_LIST:
				lines = block.splitlines()
				children = []
				for line in lines:
					children.append(text_to_children(line.strip("-").strip(), "li"))
				nodes.append(ParentNode("ul", children))
			if block_type == BlockType.ORDERED_LIST:
				lines = block.splitlines()
				children = []
				for line in lines:
					children.append(text_to_children(line[3:],  "li"))
				nodes.append(ParentNode("ol", children))

	return ParentNode("div", nodes)

def text_to_children(text, tag):
	nodes = text_to_textnodes(text)
	children =(ParentNode(tag, [text_node_to_html_node(n) for n in nodes]))
	return children

def extract_title(markdown):
	blocks = markdown.split("\n\n")
	if blocks[0].startswith("#"):
		return blocks[0].strip("# ")
	else:
		raise Exception("Markdown must start with heading 1")

