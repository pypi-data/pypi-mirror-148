import re
import mkdocs
from mkdocs.config import config_options


class Plugin(mkdocs.plugins.BasePlugin):
    config_scheme = (
        ("mark", config_options.Type(str, default="type:video-tag"))
    )

    def on_page_content(self, html, page, config, files):
        # Separate tags by strings to simplify the use of regex
        content = html
        content = re.sub(r'>\s*<', '>\n<', content)

        tags = self.find_marked_tags(content)

        for tag in tags:
            src = self.get_tag_src(tag)
            if src is None:
                continue
            repl_tag = self.create_repl_tag(src)
            esc_tag = re.sub(r'\/', "\\\\/", tag)
            html = re.sub(esc_tag, repl_tag, html)

        return html


    def get_tag_src(self, tag):
        '''
        Get value of the src attribute

        return: str
        '''

        result = re.search(
            r'src=\"[^\s]*\"',
            tag
        )

        return result[0][5:-1] if result is not None else None


    def create_repl_tag(self, src):
        '''
        Сreate a replacement tag with the specified source and style.

        return: str
        '''

        return "<video controls>"\
            "<source "\
            "src=\"{}\" "\
            "type=\"video/mp4\">"\
            "</source>"\
            "</video>".format(src)


    def find_marked_tags(self, content):
        '''
        Find image tag with marked alternative name

        return: list
        '''

        mark = self.config["mark"]

        return re.findall(
            r'<img alt="' + mark + '" src="[^\s]*"\s*\/>',
            content
        )
