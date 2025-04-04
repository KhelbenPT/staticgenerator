import shutil

from textnode import *
from markdown_blocks import *
import os

public_path = "public/"
static_path = "static/"
content_path = "content/"
template_path = "template.html"
test_public = "..\\public"
test_static = "..\\static"


def main():
	write_files()
	contents = os.listdir(public_path)
	generate_page_recursive(content_path, template_path, public_path)

def write_files():
	if not os.path.exists(public_path):
		shutil.copytree(static_path, public_path)
	else:
		if os.path.exists(static_path):
			shutil.rmtree(public_path)
			shutil.copytree(static_path, public_path)
		else:
			raise Exception("Static directory doesn't exists")

def generate_page(from_path, template_path, to_path):
	print(f"Generating webpage from {from_path} to {to_path} using {template_path}")
	with open(from_path + "index.md") as file:
		contents = file.read()
	with open(template_path) as temp:
		template = temp.read()
	title = extract_title(contents)
	md = markdown_to_html_node(contents)
	html = md.to_html()
	webpage = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
	with open(to_path + "index.html", "w") as file:
		file.write(webpage)

def generate_page_recursive(from_path, template_path, to_path):
	for item in os.listdir(from_path):
		if item == "index.md":
			print(f"Generating webpage from {from_path} to {to_path} using {template_path}")
			with open(from_path + "index.md") as file:
				contents = file.read()
			with open(template_path) as temp:
				template = temp.read()
			title = extract_title(contents)
			md = markdown_to_html_node(contents)
			html = md.to_html()
			webpage = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
			with open(to_path + "index.html", "w") as file:
				file.write(webpage)
		else:
			if not os.path.isdir(to_path+item+"/"):
				os.mkdir(to_path+item+"/")
			generate_page_recursive(from_path+item+"/", template_path, to_path+item+"/")


main()
