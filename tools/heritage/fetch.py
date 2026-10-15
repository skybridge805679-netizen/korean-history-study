#!/usr/bin/env python3
"""문화재 사진 수집(Wikimedia Commons). 사용: python3 tools/heritage/fetch.py [--only id,id] [--width 640]
targets.json 의 각 항목을 Commons 에서 검색해 라이선스가 자유(PD/CC)인 첫 이미지를 받아
site/heritage/<id>.jpg 로 저장하고 site/heritage/credits.json 에 저작자·라이선스·원본 주소를 기록한다.
검색은 자동이므로 받은 뒤 반드시 사진을 열어 이름과 맞는지 확인하고, 틀리면 targets.json 의 q 를 고쳐 다시 실행한다."""
import json,os,re,sys,time,urllib.parse,urllib.request
ROOT=os.path.join(os.path.dirname(__file__),"..","..")
OUT=os.path.join(ROOT,"site","heritage");os.makedirs(OUT,exist_ok=True)
API="https://commons.wikimedia.org/w/api.php"
UA={"User-Agent":"korean-history-study/1.0 (study-site heritage photos)"}
FREE=re.compile(r"^(CC0|CC BY|CC BY-SA|Public domain|PD|GFDL|KOGL Type 1)",re.I)
def get(url):
    for i in range(6):
        try:return urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=40).read()
        except urllib.error.HTTPError as e:
            if e.code!=429:raise
            time.sleep(10*(i+1))
    raise RuntimeError("429 반복")
def api(**p):
    p["format"]="json";return json.loads(get(API+"?"+urllib.parse.urlencode(p)))
only=None;width=640
a=sys.argv[1:]
if "--only" in a:only=set(a[a.index("--only")+1].split(","))
if "--width" in a:width=int(a[a.index("--width")+1])
T=json.load(open(os.path.join(os.path.dirname(__file__),"targets.json")))
cp=os.path.join(OUT,"credits.json");C=json.load(open(cp)) if os.path.exists(cp) else {}
for t in T:
    if only and t["id"] not in only:continue
    if t["id"] in C and not only:continue
    try:
        pick=None
        for q in ([t["q"]]+t.get("alt",[])):
            r=api(action="query",generator="search",gsrsearch=q,gsrnamespace=6,gsrlimit=8,prop="imageinfo",iiprop="url|extmetadata|size|mime",iiurlwidth=width)
            pages=sorted((r.get("query",{}).get("pages",{})).values(),key=lambda p:p.get("index",99))
            for p in pages:
                ii=(p.get("imageinfo") or [{}])[0];md=ii.get("extmetadata",{})
                lic=md.get("LicenseShortName",{}).get("value","")
                if t.get("exclude") and re.search(t["exclude"],p["title"]):continue
                if ii.get("mime","").startswith("image/jp") or ii.get("mime")=="image/png":
                    if FREE.search(lic) and ii.get("width",0)>=500:pick=(p,ii,md,lic);break
            if pick:break
            time.sleep(4)
        if not pick:print("✗ 없음",t["id"],t["q"],flush=True);continue
        p,ii,md,lic=pick
        data=get(ii["thumburl"])
        fn=t["id"]+".jpg";open(os.path.join(OUT,fn),"wb").write(data)
        strip=lambda s:re.sub(r"<[^>]+>","",s or "").strip()
        C[t["id"]]={"file":"heritage/"+fn,"name":t["name"],"era":t["era"],"commons":p["title"],"author":strip(md.get("Artist",{}).get("value")),"license":lic,"source":ii.get("descriptionurl")}
        json.dump(C,open(cp,"w"),ensure_ascii=False,indent=1)
        print("✓",t["id"],p["title"],lic,flush=True)
        time.sleep(6)
    except Exception as e:print("✗ 오류",t["id"],e,flush=True)
json.dump(C,open(cp,"w"),ensure_ascii=False,indent=1)
