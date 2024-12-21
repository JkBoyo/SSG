from constants import Block_Type
#from textnode import TextNode
from conversion import markdown_to_html_node, markdown_to_blocks, block_to_block_type
import shutil
import os


def main():
    static_to_public()
    generate_page("./content/index.md", "./template.html", "./public/index.html")

def static_to_public(static_path = "/home/heffstech/workspace/SSG/static/", public_path = "/home/heffstech/workspace/SSG/public/"):
    if os.path.exists(public_path):
        shutil.rmtree(public_path)
        os.mkdir(public_path)
    static_objs = os.listdir(static_path)
    for obj in static_objs:
        obj_path = os.path.join(static_path, obj)
        if not os.path.isfile(obj_path):
            new_public_dir = os.path.join(public_path, obj)
            os.mkdir(new_public_dir)
            static_to_public(obj_path, new_public_dir)
        else:
            public_obj_path = os.path.join(public_path, obj)
            shutil.copy(obj_path, public_obj_path)

def extract_title(markdown):
    for block in markdown_to_blocks(markdown):
       if block_to_block_type(block) == Block_Type.heading and block.count('#') == 1:
            return block.strip('# ')
    raise Exception("No Title in markdown.")

def generate_page(from_path, template_path, dest_path):
    print(f"Generateing page {from_path} to {dest_path} using {template_path}")
    markdown_file = open(from_path, 'r')
    markdown_string = markdown_file.read()
    template_file = open(template_path,'r')
    template_string = template_file.read()
    markdown_file.close()
    template_file.close()
    html_nodes = markdown_to_html_node(markdown_string)
    html_string = html_nodes.to_html()
    title = extract_title(markdown_string)
    final_html = template_string.replace('{{ Title }}', title).replace('{{ Content }}', html_string)
    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    html_file = open(dest_path, 'w')
    html_file.write(final_html)
    html_file.close()

main()
