from enum import Enum
from htmlnode import LeafNode
import re
class TextType(Enum):
	NORMAL = "normal"
	BOLD = "bold"
	ITALIC = "italic"
	CODE = "code"
	LINK = "link"
	IMAGE = "image"

class TextNode():
	def __init__(self, text, text_type, url=None):
		self.text = text
		self.text_type = text_type
		self.url = url	

	def __eq__(self, other):
		if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
			return True
	
	def __repr__(self):
		return f"TextNode({self.text}, {self.text_type}, {self.url})"

def text_node_to_html_node(text_node):
	if text_node.text_type == TextType.NORMAL:
		return LeafNode(None, text_node.text)
	if text_node.text_type == TextType.BOLD:
		return LeafNode("b", text_node.text)
	if text_node.text_type == TextType.ITALIC:
		return LeafNode("i", text_node.text)
	if text_node.text_type == TextType.CODE:
		return LeafNode("code", text_node.text)
	if text_node.text_type == TextType.LINK:
		return LeafNode("a", text_node.text, props={"href":text_node.url})
	if text_node.text_type == TextType.IMAGE:
		return LeafNode("img", "", props={"src":text_node.url, "alt":text_node.text})
	raise ValueError(f"invalid text type: {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
	new_nodes = []
	for node in old_nodes:
		if node.text_type != TextType.NORMAL:
			new_nodes.append(node)
			continue
		split_node = []
		sections = node.text.split(delimiter)
		if len(sections) % 2 == 0:
			raise ValueError("invalid markdown, formatted section not closed")
		for n in range (len(sections)):
			if sections[n] == "":
				continue
			if n % 2 == 0:
				split_node.append(TextNode(sections[n], TextType.NORMAL))
			else:
				split_node.append(TextNode(sections[n], text_type))
		new_nodes.extend(split_node)
	return new_nodes

def extract_markdown_images(text):
	matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
	return matches

def extract_markdown_links(text):
	matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
	return matches

def split_nodes_image(old_nodes):
	new_nodes = []
	for node in old_nodes:
		if node.text_type != TextType.NORMAL:
			new_nodes.append(node)
			continue
		original_text = node.text
		images = extract_markdown_images(original_text)
		if len(images) == 0:
			new_nodes.append(node)
			continue
		for image in images:
			sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
			if len(sections) != 2:
				raise ValueError("invalide markdown, image section not closed")
			if sections[0] != "":
				new_nodes.append(TextNode(sections[0], TextType.NORMAL))
			new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
			original_text = sections[1]
		if original_text != "":
			new_nodes.append(TextNode(original_text, TextType.NORMAL))
	return new_nodes



def split_nodes_link(old_nodes):
	new_nodes = []
	for node in old_nodes:
		if node.text_type != TextType.NORMAL:
			new_nodes.append(node)
			continue
		original_text = node.text
		links = extract_markdown_links(original_text)
		if len(links) == 0:
			new_nodes.append(node)
			continue
		for link in links:
			sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
			if len(sections) != 2:
				raise ValueError("invalid markdown, link section not closed")
			if sections[0] != "":
				new_nodes.append(TextNode(sections[0], TextType.NORMAL))
			new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
			original_text = sections[1]
		if original_text != "":
			new_nodes.append(TextNode(original_text, TextType.NORMAL))
	return new_nodes


def text_to_textnodes(text):
	text_node = [TextNode(text, TextType.NORMAL)]
	nodes = split_nodes_delimiter(text_node, "**", TextType.BOLD)
	nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
	nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
	nodes = split_nodes_link(nodes)
	nodes = split_nodes_image(nodes)
	return nodes
