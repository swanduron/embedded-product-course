#!/usr/bin/env python3
"""Build a local offline HTML reader from the authoritative Markdown lesson source.

The old v0.1 HTML was an entirely hand-authored prototype. This script keeps
its navigation and OLED interactivity, and replaces lesson 1.1 from Markdown.
"""
from pathlib import Path
import re
import sys

try:
    from bs4 import BeautifulSoup
    import mistune
except ImportError:
    print('Missing build dependencies. Run: python3 -m pip install -r requirements-build.txt', file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
MD_PATH = ROOT / 'chapters' / 'ch01-lesson01.md'
TEMPLATE = ROOT / 'site' / 'template.html'
TARGET = ROOT / 'index.html'
VERSION = 'v0.2.0-preview'

md = MD_PATH.read_text(encoding='utf-8')
html = mistune.create_markdown(plugins=['table', 'strikethrough'])(md)
soup = BeautifulSoup(TEMPLATE.read_text(encoding='utf-8'), 'html.parser')
section = soup.find('section', id='lesson')
if section is None:
    sys.exit('Template is missing section#lesson')
section.clear()

label = soup.new_tag('span', attrs={'class': 'tag'})
label.string = '教材正文 · 第 1 章 / 第 1.1 节'
section.append(label)
content = BeautifulSoup(html, 'html.parser')
article = soup.new_tag('article', attrs={'class': 'textbook-article'})

# Adjust heading hierarchy for the surrounding HTML page.
headings = content.find_all(re.compile(r'^h[1-6]$'))
toc = []
for i, head in enumerate(headings):
    level = int(head.name[1:])
    head.name = f'h{min(level + 1, 6)}'
    head['id'] = f'lesson-heading-{i + 1}'
    if level == 2:
        toc.append((head['id'], head.get_text(' ', strip=True)))
for child in list(content.contents):
    article.append(child.extract())

if toc:
    toc_div = soup.new_tag('details', attrs={'class': 'lesson-toc'})
    summ = soup.new_tag('summary')
    summ.string = '本节目录 · 展开查看'
    toc_div.append(summ)
    ol = soup.new_tag('ol')
    for anchor, name in toc:
        li = soup.new_tag('li')
        a = soup.new_tag('a', href='#' + anchor)
        a.string = name
        li.append(a)
        ol.append(li)
    toc_div.append(ol)
    section.append(toc_div)
section.append(article)

# Clarify that the reader is an HTML preview, not the released/verified lesson.
soup.title.string = f'现代嵌入式产品工程 | 阅读预览 {VERSION}'
small = soup.select_one('aside small')
if small:
    small.clear()
    small.append('产品构想 → 架构 → 实现 → 验证 → 交付')
    small.append(soup.new_tag('br'))
    small.append(f'HTML 阅读预览 · {VERSION}')
home_panel = soup.select_one('#home .panel p')
if home_panel:
    home_panel.string = ('当前已确认 14 章课程架构与教材编校规范；'
                         '第 1.1 节扩展为可连续阅读的教材正文，'
                         '第 1.2 节仍为未发布 Markdown 草稿。'
                         '硬件设计、工程源码与测试证据尚未完成。')

rules_panel = soup.select_one('#rules .panel')
if rules_panel:
    h = soup.new_tag('h3')
    h.string = '教材正文质量要求'
    p = soup.new_tag('p')
    p.string = ('以完整案例和连贯因果推导为主体；不能把教学检查表当作正文，'
                '不能只列出“需求、架构、验证”等标题。'
                '章节须经过连续阅读审查和独立迁移练习审查。')
    rules_panel.append(h)
    rules_panel.append(p)

nav_lesson = soup.select_one('nav button[data-section="lesson"]')
if nav_lesson:
    nav_lesson.string = '第 1 章 · 1.1（扩展稿）'
footer = soup.select_one('.footer')
if footer:
    footer.string = f'HTML 阅读预览 {VERSION} · 1.1 来源：chapters/ch01-lesson01.md。正文尚待学习者审阅与实验验收。'

extra_css = '''
.textbook-article{max-width:820px;margin:22px auto 35px;line-height:1.95;font-size:16px;color:#293747}
.textbook-article h2{font-size:30px;line-height:1.35;letter-spacing:-.02em;margin:18px 0 18px}
.textbook-article h3{font-size:22px;line-height:1.4;margin:40px 0 14px;padding-top:7px}
.textbook-article p{max-width:none;margin:15px 0 19px}
.textbook-article blockquote{margin:18px 0 26px;border-left:4px solid #7299c6;padding:9px 17px;background:#eff5fb;color:#40566c;border-radius:0 8px 8px 0}
.textbook-article blockquote p{margin:7px 0}
.textbook-article code{background:#eaf0f6;padding:2px 4px;border-radius:4px;font-size:.91em}
.textbook-article pre{white-space:pre;overflow-x:auto;padding:20px 22px;background:#162333;line-height:1.5;margin:22px 0 28px}
.textbook-article pre code{padding:0;background:none;color:#ecf2fa;font-size:13px}
.textbook-article table{display:block;overflow-x:auto;margin:24px 0 30px;background:#fff;border:1px solid #e1e8f0;border-radius:10px}
.textbook-article th,.textbook-article td{min-width:130px}
.textbook-article ul,.textbook-article ol{padding-left:25px}
.textbook-article li{margin-bottom:9px}
.textbook-article hr{border:0;border-top:1px solid #d8e2ed;margin:35px 0}
.lesson-toc{max-width:820px;margin:20px auto;padding:12px 18px;border:1px solid #d7e1ec;background:#fff;border-radius:12px}
.lesson-toc summary{font-weight:600;cursor:pointer}
.lesson-toc ol{columns:2;padding-left:24px;margin:10px 0 0}
.lesson-toc li{break-inside:avoid;font-size:13px;margin:4px 0}
.lesson-toc a{color:#245c98;text-decoration:none}
@media(max-width:700px){.textbook-article{font-size:15px;line-height:1.87}.textbook-article h2{font-size:25px}.textbook-article h3{font-size:20px}.lesson-toc ol{columns:1}}
@media print{aside,.buttons{display:none!important}.shell{display:block}main{max-width:none;padding:0}.textbook-article{max-width:none}.textbook-article pre{white-space:pre-wrap}}
'''
style = soup.new_tag('style')
style.string = extra_css
soup.head.append(style)
TARGET.write_text('<!doctype html>\n' + str(soup.html), encoding='utf-8')
print(f'Generated {TARGET} ({TARGET.stat().st_size} bytes) from {MD_PATH.name}; version={VERSION}')
