import unittest

from htmlnode import *
from textnode import *

class TestHTMLNode(unittest.TestCase):
	def test_eq(self):
		node = HTMLNode("This is a html node", props= {"href": "https://www.google.com"})
		node2 = HTMLNode("This is a html node", props= {"href": "https://www.google.com"})
		self.assertEqual(node, node2)

	def test_not_eq(self):
		node = HTMLNode("this is a text node", props = {"href": "https://www.google.com", "target": "_blank",})
		node2 = HTMLNode("this is a text node", props = {"href": "https://www.yahoo.com", "target": "_blank",})
		self.assertNotEqual(node, node2)
	def test_not_eq2(self):
		node = HTMLNode("<a>", value= "http://www.google.com",props = {"href": "https://www.google.com", "target": "_blank",})
		node2 = HTMLNode("<a>", value= "http://www.yahoo.com",props = {"href": "https://www.google.com", "target": "_blank",})
		self.assertNotEqual(node, node2)

	def test_leaf1(self):
		leaf = LeafNode(None, "test")
		expected = "test"
		print(f"Expected: {expected}")
		print(f"Actual: {leaf.to_html()}")
		self.assertEqual(leaf.to_html(), expected)

	def test_leaf2(self):
		leaf = LeafNode("b", "test")
		expected = "<b>test</b>"
		print(f"Expected: {expected}")
		print(f"Actual: {leaf.to_html()}")
		self.assertEqual(leaf.to_html(), expected)
	def test_leaf3(self):
		leaf = LeafNode("a", "test.com", props = {"href":"http://www.test.com"})
		expected = "<a href=http://www.test.com>test.com</a>"
		print(f"Expected: {expected}")
		print(f"Actual: {leaf.to_html()}")
		self.assertEqual(leaf.to_html(), expected)
	def test_leaf4(self):
		leaf = LeafNode("a", "test.com", props={"href": "http://www.test.com", "target": "_blank"})
		expected = "<a href=http://www.test.com target=_blank>test.com</a>"
		print(f"Expected: {expected}")
		print(f"Actual: {leaf.to_html()}")
		self.assertEqual(leaf.to_html(), expected)
	def test_leaf5(self):
		leaf = LeafNode("code", "\n    This is text that _should_ remain\n    the **same** even with inline stuff\n    ")
		print(leaf.to_html())

	def test_parent1(self):
		node = ParentNode(
			"p",
			[
				LeafNode("b", "Bold text"),
				LeafNode(None, "Normal text"),
				LeafNode("i", "italic text"),
				LeafNode(None, "Normal text"),

			],
		)
		expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
		self.assertEqual(node.to_html(), expected)

	def test_parent2(self):
		node = ParentNode(
				"p",
				[
					LeafNode("b", "Bold text"),
					LeafNode(None, "Normal text"),
					LeafNode("i", "italic text"),
					LeafNode(None, "Normal text"),
					ParentNode(
						"a",
						[
							LeafNode("b", "Bold text"),
							LeafNode(None, "Normal text"),
							LeafNode("i", "italic text"),
							LeafNode(None, "Normal text"),
						]),
				],
			)
		expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text<a><b>Bold text</b>Normal text<i>italic text</i>Normal text</a></p>"
		self.assertEqual(node.to_html(), expected)

if __name__ == "__main__":
    unittest.main()
