const filterButtons = document.querySelectorAll('[data-filter]');
const workPanels = document.querySelectorAll('[data-work-panel]');
const workCounts = {all: '3개 업무 영역', brand: '브랜딩 · SNS 콘텐츠 총괄', content: 'PPL 콘텐츠', copy: 'ON AIR · IDEA'};
function showWork(filter, updateUrl = false) {
  if (!workCounts[filter] || !workPanels.length) return;
  filterButtons.forEach(button => {
    const active = button.dataset.filter === filter;
    button.classList.toggle('active', active);
    button.setAttribute('aria-pressed', String(active));
  });
  workPanels.forEach(panel => {panel.hidden = panel.dataset.workPanel !== filter;});
  const highlight = document.querySelector(".work-highlight");
  if (highlight) highlight.hidden = filter !== "all";
  
  if (updateUrl) history.pushState(null, '', filter === 'all' ? '#work' : '#work-' + filter);
}
function restoreWork() {
  const hash = location.hash;
  if (hash === '#copy-on-air' || hash === '#copy-idea') showWork('copy');
  else if (hash === '#work' || !hash) showWork('all');
  else if (hash.startsWith('#work-')) showWork(hash.slice(6));
}
filterButtons.forEach(button => button.addEventListener('click', () => showWork(button.dataset.filter, true)));
window.addEventListener('popstate', restoreWork);
window.addEventListener('hashchange', restoreWork);
restoreWork();
// Direct links to a filtered view land at the Work section after it is revealed.
if (location.hash.startsWith('#work-')) document.querySelector('#work')?.scrollIntoView();
else if (location.hash.startsWith('#copy-')) document.querySelector(location.hash)?.scrollIntoView();
const lightbox = document.querySelector('#lightbox');
let lastTrigger;
if (lightbox) {
  document.querySelectorAll('.image-zoom').forEach(button => button.addEventListener('click', () => {
    lastTrigger = button;
    const image = button.querySelector('img');
    lightbox.querySelector('img').src = image.src;
    lightbox.querySelector('img').alt = image.alt;
    lightbox.showModal();
    document.body.style.overflow = 'hidden';
  }));
  lightbox.querySelector('.close-lightbox').addEventListener('click', () => lightbox.close());
  lightbox.addEventListener('click', event => {if (event.target === lightbox) lightbox.close();});
  lightbox.addEventListener('close', () => {document.body.style.overflow = '';if (lastTrigger) lastTrigger.focus();});
}

document.querySelectorAll('.external-thumbnail').forEach(image => {
  const fallback = () => {image.hidden = true;};
  image.addEventListener('error', fallback);
  if (image.complete && !image.naturalWidth) fallback();
});

async function copyText(value) {
  try {
    if (navigator.clipboard && window.isSecureContext) {await navigator.clipboard.writeText(value);return true;}
  } catch (_) {}
  const input = document.createElement('textarea');
  input.value = value;
  input.setAttribute('readonly', '');
  input.style.position = 'fixed';input.style.left = '-9999px';
  document.body.appendChild(input);input.select();
  let ok = false;
  try {ok = document.execCommand('copy');} catch (_) {}
  input.remove();return ok;
}
document.querySelectorAll('[data-copy]').forEach(button => {
  button.addEventListener('click', async () => {
    const ok = await copyText(button.dataset.copy);
    document.querySelector('.copy-status').textContent = ok ? '복사했습니다.' : '복사가 지원되지 않습니다. 위 연락처를 선택해 복사해 주세요.';
    button.focus();
  });
});
