from pathlib import Path
import concurrent.futures as F, subprocess, hashlib, zipfile, json
R=Path(__file__).resolve().parent
D=R/'deps';D.mkdir(exist_ok=True)
items=[
 ('build-tools.zip','https://dl.google.com/android/repository/build-tools_r35_windows.zip','sha1','af059bb67cf7786f45ee0db85e2d24985df1b4b6'),
 ('platform.zip','https://dl.google.com/android/repository/platform-35_r02.zip','sha1','0bb560a90a7a2cbd0dd8348224d518b638fe7949'),
 ('jre.zip','https://cdn.azul.com/zulu/bin/zulu21.54.201-ca-jre21.0.13.1-win_x64.zip',None,None),
 ('ecj-3.38.0.jar','https://repo.maven.apache.org/maven2/org/eclipse/jdt/ecj/3.38.0/ecj-3.38.0.jar','sha256','97c566b120009c203a2fc8b291f4a9adbc171cf1ccb70f06f6b4e1828c00ce8e'),
 ('icu4j-74.2.jar','https://repo.maven.apache.org/maven2/com/ibm/icu/icu4j/74.2/icu4j-74.2.jar','sha256','95c055080e14c093ebeeba5b733e1a1be7a4af5854668c774cedf070d4240e43'),
 ('cardview-v7-21.0.3.aar','https://dl.google.com/dl/android/maven2/com/android/support/cardview-v7/21.0.3/cardview-v7-21.0.3.aar','sha256','45c48c2ab056bc7a8573970b10f8902742c5d443f180dae43c56557397ac39af'),
 ('palette-v7-21.0.3.aar','https://dl.google.com/dl/android/maven2/com/android/support/palette-v7/21.0.3/palette-v7-21.0.3.aar','sha256','8108a4f77d58844f61ebc1aba24d6da3c42747470fa44d08ae8cae619be0d1b3')]
def fetch(v):
 n,u,alg,expected=v;p=D/n
 if not p.exists():
  subprocess.run(['curl.exe','--ssl-revoke-best-effort','-f','-sS','-L','--connect-timeout','15','--max-time','300','--retry','2','-o',str(p)+'.part',u],check=True)
  Path(str(p)+'.part').rename(p)
 if alg:assert hashlib.new(alg,p.read_bytes()).hexdigest()==expected,n
 print(n,p.stat().st_size,hashlib.sha256(p.read_bytes()).hexdigest(),flush=True)
 if n in ('build-tools.zip','platform.zip','jre.zip'):
  with zipfile.ZipFile(p) as z:z.extractall(D/n.removesuffix('.zip'))
 return {'file':n,'url':u,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
with F.ThreadPoolExecutor(max_workers=7) as ex:
 result=list(ex.map(fetch,items))
(D/'download-manifest.json').write_text(json.dumps(result,indent=2))
