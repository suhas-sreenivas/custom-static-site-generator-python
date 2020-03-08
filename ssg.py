from markdown2 import markdown
from jinja2 import Environment, PackageLoader
from bs4 import BeautifulSoup
from pathlib import Path
import toml
import shutil

def generate_page(template_env, template_path, markdown_file_path, dest):
    template = template_env.get_template(template_path)

    with open(markdown_file_path) as markdown_file:
        html = markdown(markdown_file.read())

    with open(dest, 'w') as index_file:
        index_file.write(
            template.render(
                article=html
            )
        )
    
    return html

if __name__ == "__main__":
    config = toml.load('config.toml')
    site_gen_path = config['site_gen_path']
    print(site_gen_path)

    p = Path(site_gen_path + 'blog')
    p.mkdir(parents=True, exist_ok=True)

    shutil.copy('templates/styles.css', site_gen_path)
    template_env = Environment(loader=PackageLoader('ssg', 'templates'))
    
    _ = generate_page(template_env, 'main.html', 'content/about_me.md', site_gen_path + 'index.html')
    
    posts_info = {}
    post_files = Path('content/blog_posts')
    for post_file in post_files.iterdir():
        html = generate_page(template_env, 'main.html', post_file, site_gen_path + 'blog/' + post_file.stem + '.html')
        soup = BeautifulSoup(html, 'html.parser')
        posts_info[soup.h1.string] = post_file.stem + '.html'


    post_list_template = template_env.get_template('blog_index.html')
    with open(site_gen_path + 'blog/index.html', 'w') as blog_index_file:
        blog_index_file.write(
            post_list_template.render(
                posts_info = posts_info
            )
        )