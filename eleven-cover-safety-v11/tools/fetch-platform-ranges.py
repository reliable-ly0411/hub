from pathlib import Path
import subprocess,concurrent.futures as F,hashlib,zipfile
r=Path('work/cover-safety-v11/deps').resolve();d=r/'platform-parts';d.mkdir(exist_ok=True)
u='https://dl.google.com/android/repository/platform-35_r02.zip';size=64273788;chunk=1048576

def get(i):
 p=d/str(i);start=i*chunk;end=min(size,start+chunk)-1
 if p.exists() and p.stat().st_size==end-start+1:return p
 for retry in range(4):
  q=subprocess.run(['curl.exe','--ssl-revoke-best-effort','-4','-f','-sS','-L','--connect-timeout','10','--max-time','45','--range',f'{start}-{end}','-o',str(p),u],capture_output=True)
  if q.returncode==0 and p.stat().st_size==end-start+1:
   print('part',i,flush=True);return p
 raise RuntimeError((i,q.stderr.decode(errors='replace')))
with F.ThreadPoolExecutor(max_workers=12) as ex:parts=list(ex.map(get,range((size+chunk-1)//chunk)))
p=r/'platform.zip'
with p.open('wb') as out:
 for f in parts:out.write(f.read_bytes())
assert hashlib.sha1(p.read_bytes()).hexdigest()=='0bb560a90a7a2cbd0dd8348224d518b638fe7949'
with zipfile.ZipFile(p) as z:z.extractall(r/'platform')
print('platform verified',flush=True)
