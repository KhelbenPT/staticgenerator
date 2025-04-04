
import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
	def test_eq(self):
		node = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is a text node", TextType.BOLD)
		self.assertEqual(node, node2)

	def test_not_eq(self):
		node = TextNode("this is a text node", TextType.BOLD)
		node2 = TextNode("this is a test node", TextType.BOLD)
		self.assertNotEqual(node, node2)
	def test_not_eq2(self):
		node = TextNode("this is a text node", TextType.BOLD)
		node2 = TextNode("this is a text node", TextType.ITALIC)
		self.assertNotEqual(node, node2)
	def test_not_eq3(self):
		node = TextNode("this is a text node", TextType.BOLD)
		node2 = TextNode("this is a test node", TextType.BOLD, url="http:\\localhost")
		self.assertNotEqual(node, node2)

	def test_text_to_html(self):
		text = TextNode("teste so texto", TextType.NORMAL)
		leaf = text_node_to_html_node(text)
		expected = "teste so texto"
		self.assertEqual(leaf.to_html(), expected)
	def test_text_to_html2(self):
		text = TextNode("teste so texto", TextType.BOLD)
		leaf = text_node_to_html_node(text)
		expected = "<b>teste so texto</b>"
		self.assertEqual(leaf.to_html(), expected)
	def test_text_to_html3(self):
		text = TextNode("teste so texto", TextType.ITALIC)
		leaf = text_node_to_html_node(text)
		expected = "<i>teste so texto</i>"
		self.assertEqual(leaf.to_html(), expected)
	def test_text_to_html4(self):
		text = TextNode("teste so texto", TextType.CODE)
		leaf = text_node_to_html_node(text)
		expected = "<code>teste so texto</code>"
		self.assertEqual(leaf.to_html(), expected)
	def test_text_to_html4(self):
		text = TextNode("teste so texto", TextType.LINK, url="http://www.google.com")
		leaf = text_node_to_html_node(text)
		expected = "<a href=http://www.google.com>teste so texto</a>"
		self.assertEqual(leaf.to_html(), expected)
	def test_split_node(self):
		nodes = [TextNode("isto e um **bold** test", TextType.NORMAL)]
		splited = split_nodes_delimiter(nodes, "**", TextType.BOLD)
		expected = "[TextNode(isto e um , TextType.NORMAL, None), TextNode(bold, TextType.BOLD, None), TextNode( test, TextType.NORMAL, None)]"

		if splited == expected:
			return True


	def test_split_node2(self):
		nodes = [TextNode("isto e um **bold** test", TextType.NORMAL), TextNode("isto e um *italic* test", TextType.NORMAL)]
		splited = split_nodes_delimiter(nodes, "**", TextType.BOLD)
		splited2 = split_nodes_delimiter(splited, "*", TextType.ITALIC)

	def test_extract_markdown_images(self):
		matches = extract_markdown_images(
        	"This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
		self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

	def test_split_image(self):
		node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.NORMAL,
        )
		new_nodes = split_nodes_image([node])
		self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

	def test_split_image_single(self):
		node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.NORMAL,
        )
		new_nodes = split_nodes_image([node])
		self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

	def test_split_images(self):
		node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
		new_nodes = split_nodes_image([node])
		self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

	def test_split_links(self):
		node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.NORMAL,
        )
		new_nodes = split_nodes_link([node])
		self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.NORMAL),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.NORMAL),
            ],
            new_nodes,
        )

	def test_text_to_textnodes(self):
		text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
		nodes = text_to_textnodes(text)
		print(nodes)


if __name__ == "__main__":
	unittest.main()
