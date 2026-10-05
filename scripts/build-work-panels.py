"""Keep homepage work panels synchronized with the project detail pages."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]

def collection(name, section_id=None):
    page = (root / f'{name}.html').read_text()
    content = re.search(r'<main\b[^>]*>(.*?)</main>', page, re.S).group(1)
    content = re.sub(r'<a class="breadcrumb".*?</a>', '', content, flags=re.S)
    content = re.sub(r'<section class="next-project".*?</section>', '', content, flags=re.S)
    # One homepage h1; collections, individual cases and captions nest beneath it.
    for level in (3, 2, 1):
        target = {3: 5, 2: 4, 1: 3}[level]
        content = re.sub(fr'<(/?)h{level}(\b[^>]*)>', fr'<\1h{target}\2>', content)
    if section_id:
        return f'<section class="copy-collection" id="{section_id}">{content}</section>'
    return content

index = root / 'index.html'
page = index.read_text()
start = '<!-- INLINE WORK PANELS START -->'
end = '<!-- INLINE WORK PANELS END -->'
brand = collection('on-k')
ppl = collection('contents-solution')
copy = ('<nav class="copy-sections" aria-label="카피라이팅 섹션">'
        '<a href="#copy-on-air">Copywriting / ON AIR</a>'
        '<a href="#copy-idea">Copywriting / IDEA</a></nav>'
        + collection('on-air', 'copy-on-air')
        + collection('ideas', 'copy-idea'))
panels = start + ''.join(
    f'<div class="work-panel inline-collection" id="work-panel-{key}" '
    f'data-work-panel="{key}" role="region" aria-labelledby="filter-{key}" hidden>'
    f'{content}</div>'
    for key, content in [('brand', brand), ('content', ppl), ('copy', copy)]
) + end
page = re.sub(re.escape(start) + '.*?' + re.escape(end), lambda _: panels, page, flags=re.S)
index.write_text(page)
