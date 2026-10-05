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
    if section_id == 'copy-on-air':
        content = re.sub(r'(<section class="collection-heading">.*?<h3>.*?</h3>)<p>.*?</p>', r'\1', content, count=1, flags=re.S)
    if section_id:
        return f'<section class="copy-collection" id="{section_id}">{content}</section>'
    return content

index = root / 'index.html'
page = index.read_text()
start = '<!-- INLINE WORK PANELS START -->'
end = '<!-- INLINE WORK PANELS END -->'
brand = collection('on-k')
ppl = collection('contents-solution')
copy = ('<section class="collection-heading copy-overview"><h3>Copywriting</h3>'
        '<p>채널 연간 플래닝부터 30억 원 규모의 공익광고 캠페인까지, 폭넓은 카피라이팅을 경험했습니다. '
        '브랜드의 문제를 인사이트로 풀고, 콘텐츠와 캠페인의 메시지로 구체화했습니다.</p></section>'
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
