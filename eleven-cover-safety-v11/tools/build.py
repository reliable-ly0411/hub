from pathlib import Path
import subprocess,zipfile,os,hashlib,secrets,json
R=Path(__file__).resolve().parent;S=R/'src';D=R/'deps';B=R/'build';B.mkdir(exist_ok=True)
BT=next((D/'build-tools').glob('*'));P=next((D/'platform').glob('*'));J=next((D/'jre').glob('*'))/'bin'
JAVA=J/'java.exe';ANDROID=P/'android.jar';KEY=R/'private-signing';KEY.mkdir(exist_ok=True)
def run(args,cwd=S):
 q=subprocess.run(list(map(str,args)),cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace')
 with (B/'build.log').open('a',encoding='utf-8') as f:f.write(q.stdout)
 if q.returncode: print(q.stdout);raise RuntimeError(f'{args[0]} exited {q.returncode}')
 return q.stdout
def sign(src,out):
 run([JAVA,'-jar',BT/'lib/apksigner.jar','sign','--ks',KEY/'eleven.p12','--ks-pass','file:'+str(KEY/'pass'),'--ks-key-alias','eleven','--out',out,src])
 print(run([JAVA,'-jar',BT/'lib/apksigner.jar','verify','--print-certs',out]).splitlines()[0],flush=True)
if __name__=='__main__':
 for n,h in [('ecj-3.38.0.jar','97c566b120009c203a2fc8b291f4a9adbc171cf1ccb70f06f6b4e1828c00ce8e'),('icu4j-74.2.jar','95c055080e14c093ebeeba5b733e1a1be7a4af5854668c774cedf070d4240e43'),('cardview-v7-21.0.3.aar','45c48c2ab056bc7a8573970b10f8902742c5d443f180dae43c56557397ac39af'),('palette-v7-21.0.3.aar','8108a4f77d58844f61ebc1aba24d6da3c42747470fa44d08ae8cae619be0d1b3')]:assert hashlib.sha256((D/n).read_bytes()).hexdigest()==h,n
 for n in ['gen','classes','dex','card']: (B/n).mkdir(exist_ok=True)
 with zipfile.ZipFile(D/'cardview-v7-21.0.3.aar') as z:z.extractall(B/'card')
 with zipfile.ZipFile(D/'palette-v7-21.0.3.aar') as z:(B/'palette.jar').write_bytes(z.read('classes.jar'))
 run([BT/'aapt.exe','package','-f','-m','-J',B/'gen','-M',S/'AndroidManifest.xml','-S',S/'res','-S',B/'card/res','-A',S/'assets','-I',ANDROID,'--auto-add-overlay','--extra-packages','android.support.v7.cardview','--rename-manifest-package','com.cyanogenmod.eleven.standalone','-F',B/'resources.apk'])
 run([BT/'aidl.exe','-p'+str(P/'framework.aidl'),'-I'+str(S/'src'),'-o'+str(B/'gen'),S/'src/com/cyanogenmod/eleven/IElevenService.aidl'])
 libs=[S/'libs/android-support-v4-21.jar',S/'libs/android-support-v7-recyclerview.jar',B/'palette.jar',B/'card/classes.jar',D/'icu4j-74.2.jar']
 inputs=sorted([*S.glob('src/**/*.java'),*B.glob('gen/**/*.java')])
 (B/'java.inputs').write_text('\n'.join('"'+p.as_posix()+'"' for p in inputs),encoding='utf-8')
 run([JAVA,'-jar',D/'ecj-3.38.0.jar','-nowarn','-encoding','UTF-8','-source','8','-target','8','-bootclasspath',str(ANDROID)+';'+str(BT/'core-lambda-stubs.jar'),'-classpath',';'.join(map(str,libs)),'-d',B/'classes','@'+str(B/'java.inputs')])
 with zipfile.ZipFile(B/'classes.jar','w',zipfile.ZIP_DEFLATED) as z:
  for p in (B/'classes').rglob('*.class'):z.write(p,p.relative_to(B/'classes').as_posix())
 run([JAVA,'-cp',BT/'lib/d8.jar','com.android.tools.r8.D8','--release','--min-api','21','--lib',ANDROID,'--output',B/'dex',B/'classes.jar',*libs])
 import shutil
 shutil.copyfile(B/'resources.apk',B/'unaligned.apk')
 with zipfile.ZipFile(B/'unaligned.apk','a',zipfile.ZIP_DEFLATED) as z,zipfile.ZipFile(D/'icu4j-74.2.jar') as lib:
  for p in sorted((B/'dex').glob('classes*.dex')):z.write(p,p.name)
  for n in lib.namelist():
   if n.startswith('com/ibm/icu/impl/data/') and not n.endswith(('/','.class')):z.writestr(n,lib.read(n))
  z.write(S/'NOTICE','assets/eleven-NOTICE.txt');z.write(R/'baseline/icu4j-LICENSE.txt','assets/icu4j-LICENSE.txt');z.write(S/'standalone/THIRD_PARTY.md','assets/port-THIRD_PARTY.md')
 run([BT/'zipalign.exe','-f','4',B/'unaligned.apk',B/'aligned.apk'])
 if not (KEY/'eleven.p12').exists():
  (KEY/'pass').write_text(secrets.token_hex(20))
  run([J/'keytool.exe','-genkeypair','-keystore',KEY/'eleven.p12','-storetype','PKCS12','-storepass:file',KEY/'pass','-alias','eleven','-keyalg','RSA','-keysize','3072','-dname','CN=Eleven Cover Safety Internal QA','-validity','3650'])
 sign(B/'aligned.apk',B/'Eleven-v11-cover-safety-candidate.apk')
 print(run([BT/'aapt.exe','dump','badging',B/'Eleven-v11-cover-safety-candidate.apk']).splitlines()[0])
 print(hashlib.sha256((B/'Eleven-v11-cover-safety-candidate.apk').read_bytes()).hexdigest(),flush=True)
