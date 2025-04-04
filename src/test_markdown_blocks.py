import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node, extract_title


class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_type_paragrap(self):
        block = ("isto e um teste"
                 "com falso `code block`"
                 "> e falsa lista"
                 "para ver se detecta paragrafo")
        blocktype = block_to_block_type(block)
        self.assertEqual(blocktype,BlockType.PARAGRAPH)
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "### heading3"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = ">isto\n>e um\n>quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- lista\n- nao\n- ordenada"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "- falsa lista\nnao\n- ordenada"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "1. lista\n2. ordenada"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "1. lista\n3. ordenada"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        #print(html)
        self.assertEqual(
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
            html

        )

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        #print(html)
        self.assertEqual(
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>", html,
        )
    def test_all(self):
        md = ("""# heading1 test

isto é um teste de **markdown**
isto é um __paragrafo__
com `teste de inline` 


``` teste
de
codigo``` 


>teste
>de
>quotes


- teste
- de 
- lista
- nao
- organizada

1. e por
2. ultimo
3. de lista
4. organizada
""")
        node = markdown_to_html_node(md)
        html = node.to_html()
        print (html)

    def test_extract_title(self):
        md = ("""# heading1 test

isto é um teste de **markdown**
isto é um __paragrafo__
com `teste de inline` 


``` teste
de
codigo``` 


>teste
>de
>quotes


- teste
- de 
- lista
- nao
- organizada

1. e por
2. ultimo
3. de lista
4. organizada
""")
        title = extract_title(md)
        print(title)
if __name__ == "__main__":
    unittest.main()