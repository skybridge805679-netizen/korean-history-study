#!/usr/bin/env python3
"""Download every ZIP part, verify hashes and join without loading the ZIP into memory."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from urllib.request import Request, urlopen
import hashlib, json, shutil, time
MANIFEST = {'filename': 'korean-history-study-all-results-20261012.zip', 'bytes': 2192218758, 'sha256': 'e09e1ec537644a3c5a5c4c17eb731683d9308c5ca7881e6c31e81182d3224aa4', 'repository': 'skybridge805679-netizen/korean-history-study', 'branch': 'pc-handoff-20261012', 'parts': [{'name': 'korean-history-study-all-results-20261012.zip.part01', 'bytes': 94371840, 'sha256': '53fa3d4b251954d0fdc048a8c0112b4f690da5bfc944cc7e0d0bcbd97a027857'}, {'name': 'korean-history-study-all-results-20261012.zip.part02', 'bytes': 94371840, 'sha256': 'c12d5b52ee823fd8eb6ad70287e655b109737f284e635240d5ddeafdde358c43'}, {'name': 'korean-history-study-all-results-20261012.zip.part03', 'bytes': 94371840, 'sha256': '85a62e9f60da9fcf92408af595f5ac5bb170b088306d3ddbf0ac11a724f1710a'}, {'name': 'korean-history-study-all-results-20261012.zip.part04', 'bytes': 94371840, 'sha256': 'ffe3d76b0de85e8035103f124bdbff1900343a79f6cafe2fb232b52854f5a7c0'}, {'name': 'korean-history-study-all-results-20261012.zip.part05', 'bytes': 94371840, 'sha256': 'a09ea59bb012ce9971ea5f6fcab2cb49a73c2803f09378c43eaf136d692db024'}, {'name': 'korean-history-study-all-results-20261012.zip.part06', 'bytes': 94371840, 'sha256': 'd48f6c84362b1e9ceddb249c6353010b5dfbeb030ba46232b1833d508c49abef'}, {'name': 'korean-history-study-all-results-20261012.zip.part07', 'bytes': 94371840, 'sha256': '17f91c221f359a828c1e54bd8098076803c07d7422b818dd4f32ce1909fd63b1'}, {'name': 'korean-history-study-all-results-20261012.zip.part08', 'bytes': 94371840, 'sha256': 'ffe14c914c60e05d691ebc29bc0ea91a9b104cf553d54008a9cb24428a706e83'}, {'name': 'korean-history-study-all-results-20261012.zip.part09', 'bytes': 94371840, 'sha256': 'a23adbfa7ad4da5281f2f2f52ab8ad424369fc4b1de7491b703355b7c36cd02c'}, {'name': 'korean-history-study-all-results-20261012.zip.part10', 'bytes': 94371840, 'sha256': 'f1df4c11673c4877d08235c0301c9cc1277159aeb9ededaee11c42f98d228865'}, {'name': 'korean-history-study-all-results-20261012.zip.part11', 'bytes': 94371840, 'sha256': '0384ecc1cc51eb8b977d7c04345291dc9cc0b7b824f854384e89baeb93409002'}, {'name': 'korean-history-study-all-results-20261012.zip.part12', 'bytes': 94371840, 'sha256': 'd67a4270eba3fc7275a96f236ea20acca928453dc792d837c60b3dd5db29eb8d'}, {'name': 'korean-history-study-all-results-20261012.zip.part13', 'bytes': 94371840, 'sha256': '887e12d908ed4bdc141834620b6eac0b288d19547de17a376c74d7d30a7b11a3'}, {'name': 'korean-history-study-all-results-20261012.zip.part14', 'bytes': 94371840, 'sha256': '4ff9c74bb0837d03071e381d177385b99aa76fbc393421469c56b2209aca8b49'}, {'name': 'korean-history-study-all-results-20261012.zip.part15', 'bytes': 94371840, 'sha256': 'dd76caf0c27a05d0388545d0e57616048e34a848cc712478134fb3ba8b216495'}, {'name': 'korean-history-study-all-results-20261012.zip.part16', 'bytes': 94371840, 'sha256': '915f897ac813429904af078403038add720cb14f5cb6fb2788be486cdd302ae2'}, {'name': 'korean-history-study-all-results-20261012.zip.part17', 'bytes': 94371840, 'sha256': '4479b52189b6f346ec924dd4db82d80c8baf6e13ee56f8584675ba48b6b96c75'}, {'name': 'korean-history-study-all-results-20261012.zip.part18', 'bytes': 94371840, 'sha256': '58b51e19a24347d0cc43e301f6580a575744e5643f37f273eeb30680654bfb68'}, {'name': 'korean-history-study-all-results-20261012.zip.part19', 'bytes': 94371840, 'sha256': '445f836c6ae29fcb66ed21cc60d06ac9788c0f7fc0ba4b506675e4add294e753'}, {'name': 'korean-history-study-all-results-20261012.zip.part20', 'bytes': 94371840, 'sha256': '5374d1d93b50e0095bdbf9f35dfbf10d4dc99e08bac08b26f0c0e2464b998f82'}, {'name': 'korean-history-study-all-results-20261012.zip.part21', 'bytes': 94371840, 'sha256': '653477acabb2a9c41f6baebd65a601aa6e73c87f16ef6ea5cebf0a25f0ab07d0'}, {'name': 'korean-history-study-all-results-20261012.zip.part22', 'bytes': 94371840, 'sha256': '3c3e0728c1c3be2772f8e226bfe5431f414b16364d4aa09a1af02f21881e37a5'}, {'name': 'korean-history-study-all-results-20261012.zip.part23', 'bytes': 94371840, 'sha256': 'e2ffa9c7eb1d1b1148aa547202c189d2f09a88dc62ec8f08c013816a27736798'}, {'name': 'korean-history-study-all-results-20261012.zip.part24', 'bytes': 21666438, 'sha256': '4390f5e6f84acb831fb56cdead5c4bd30ffcc5039e03c0690e0b990c16e5e23a'}]}

BASE = 'https://raw.githubusercontent.com/' + MANIFEST['repository'] + '/' + MANIFEST['branch'] + '/parts/'
OUT = Path.cwd() / 'korean-history-study-download'
PARTS = OUT / 'parts'
PARTS.mkdir(parents=True, exist_ok=True)
def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(4*1024*1024), b''):
            h.update(block)
    return h.hexdigest()
def download(item):
    target = PARTS/item['name']
    if target.exists() and target.stat().st_size == item['bytes'] and digest(target) == item['sha256']:
        print('Verified existing:', item['name'], flush=True)
        return target
    temp = target.with_suffix(target.suffix + '.tmp')
    for attempt in range(1, 5):
        try:
            req = Request(BASE + item['name'], headers={'User-Agent': 'korean-history-study-handoff'})
            with urlopen(req, timeout=180) as response, temp.open('wb') as f:
                shutil.copyfileobj(response, f, length=4*1024*1024)
            if temp.stat().st_size != item['bytes'] or digest(temp) != item['sha256']:
                raise RuntimeError('Part hash/size mismatch: ' + item['name'])
            temp.replace(target)
            print('Downloaded:', item['name'], flush=True)
            return target
        except Exception as exc:
            if attempt == 4:
                raise RuntimeError('Download failed. Run this script again to resume.') from exc
            print('Retry', attempt, item['name'], str(exc), flush=True)
            time.sleep(attempt*2)
with ThreadPoolExecutor(max_workers=3) as pool:
    list(pool.map(download, MANIFEST['parts']))
final = OUT/MANIFEST['filename']
temp_zip = final.with_suffix('.zip.tmp')
hash_zip = hashlib.sha256()
with temp_zip.open('wb') as writer:
    for item in MANIFEST['parts']:
        with (PARTS/item['name']).open('rb') as reader:
            for block in iter(lambda: reader.read(4*1024*1024), b''):
                writer.write(block)
                hash_zip.update(block)
if temp_zip.stat().st_size != MANIFEST['bytes'] or hash_zip.hexdigest() != MANIFEST['sha256']:
    raise RuntimeError('Combined ZIP integrity check failed')
temp_zip.replace(final)
print('COMPLETE:', final.resolve(), flush=True)
print('SHA-256:', MANIFEST['sha256'], flush=True)
print('You may extract this ZIP normally. The parts folder can be removed after extraction.', flush=True)
