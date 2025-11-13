import json
import requests
from pyquery import PyQuery as pq


class DomTools:
    def __init__(self, html: str):
        # 检查是否为 HTTP/HTTPS 链接
        if html.startswith(('http://', 'https://')):
            response = requests.get(html)
            response.raise_for_status()
            # 尝试检测响应的编码
            response.encoding = response.apparent_encoding or 'utf-8'
            html_content = response.text
            self.doc = pq(html_content)
        else:
            self.doc = pq(html)

    def get_text(self, dateSelector: str, descSelector: str = None, versionSelector: str = None) -> str:
        date_html = str(self.doc(dateSelector).html() or '')
        if descSelector is not None:
            desc_html = str(self.doc(descSelector).html() or '')
            version_html = str(self.doc(versionSelector).html() or '') if versionSelector is not None else ''
            result = {
                "date": date_html,
                "desc": desc_html,
                "version": version_html
            }
        else:
            result = {
                "date": date_html
            }
        return json.dumps(result, ensure_ascii=False)

if __name__ == '__main__':
    html = 'https://docs.jiguang.cn/jpush/jpush_changelog/updates_iOS'
    dom = DomTools(html)
    print(dom.get_text('h1'))
    print(dom.get_text('h1', 'p'))
    print(dom.get_text('h1', 'p', 'h2'))