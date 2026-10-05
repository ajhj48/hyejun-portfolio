"""Import the authorized public portfolio, checking every file before replacement."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import tempfile
import urllib.request

config = json.loads(Path('.github/portfolio-source.json').read_text())
assert config['origin'] == 'https://hyejun-creative-portfolio.wnsdn553.chatgpt.site'
files = config['files']

def download(entry):
    path = entry['path']
    assert not Path(path).is_absolute() and '..' not in Path(path).parts
    if 'content' in entry:
        data = entry['content'].encode()
    else:
        request = urllib.request.Request(config['origin'] + '/' + path, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(request, timeout=60) as response:
            data = response.read()
    digest = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    assert digest == entry['sha'], 'Source changed or download failed: ' + path
    return path, data

# Validate all downloads before changing any existing project file.
with tempfile.TemporaryDirectory(prefix='portfolio-import-') as folder:
    staged = Path(folder)
    with ThreadPoolExecutor(max_workers=6) as pool:
        for path, data in pool.map(download, files):
            target = staged / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
    keep = {entry['path'] for entry in files}
    tracked = subprocess.check_output(['git', 'ls-files', '-z']).decode().split('\0')
    for path in tracked:
        if path and path not in keep:
            Path(path).unlink(missing_ok=True)
    for entry in files:
        target = Path(entry['path'])
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(staged / entry['path'], target)
    print(f"Verified and imported {len(files)} final portfolio files.")
