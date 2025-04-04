

class HTMLNode():
	def __init__(self, tag = None, value = None, children = None, props = None):
		self.tag = tag
		self.value = value
		self.children = children
		self.props = props
	
	def to_html(self):
		raise NotImplementedError()

	def props_to_html(self):
		prop_string = ""
		for prop in self.props:
			prop_string += " " + prop + "=" + self.props[prop]
		return prop_string

	def __repr__(self):
		return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

	def __eq__(self, other):
		if self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props:
			return True
class LeafNode(HTMLNode):
	def __init__(self, tag, value, props=None):
		super().__init__(self, tag, value, props = props)
		self.tag = tag
		self.value = value
		self.props = props

	def to_html(self):
		if self.value == None:
			raise ValueError
		if self.tag == None:
			return self.value
		if self.props == None:
			return f"<{self.tag}>{self.value}</{self.tag}>"
		else:
			return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
	def __init__(self, tag, children, props = None):
		super().__init__(self, tag, children, props=props)
		self.tag = tag
		self.children = children
		self.props = props

	def to_html(self):
		if self.tag == None:
			raise ValueError
		if self.children == None:
			raise ValueError("no children present")
		string = f"<{self.tag}>"
		for leaf in self.children:
			string =string + leaf.to_html()
		string = string + f"</{self.tag}>"
		return string

