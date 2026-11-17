import json as J,os,time as Z
from urllib.request import*
H=os.environ["MAKEFUN_ENV_URL"]
V=(0,100,320,330,500,900,0)
KN=(-33,-31,-18,-14,14,18,31,33)
BD=(-17,-15,15,17)
RD=(-16,-1,1,16)
# Piece-square tables, a8..h1 (white's view). Classic simplified values.
PST=[
(0,0,0,0,0,0,0,0,50,50,50,50,50,50,50,50,10,10,20,30,30,20,10,10,5,5,10,25,25,10,5,5,0,0,0,20,20,0,0,0,5,-5,-10,0,0,-10,-5,5,5,10,10,-20,-20,10,10,5,0,0,0,0,0,0,0,0),
(-50,-40,-30,-30,-30,-30,-40,-50,-40,-20,0,0,0,0,-20,-40,-30,0,10,15,15,10,0,-30,-30,5,15,20,20,15,5,-30,-30,0,15,20,20,15,0,-30,-30,5,10,15,15,10,5,-30,-40,-20,0,5,5,0,-20,-40,-50,-40,-30,-30,-30,-30,-40,-50),
(-20,-10,-10,-10,-10,-10,-10,-20,-10,0,0,0,0,0,0,-10,-10,0,5,10,10,5,0,-10,-10,5,5,10,10,5,5,-10,-10,0,10,10,10,10,0,-10,-10,10,10,10,10,10,10,-10,-10,5,0,0,0,0,5,-10,-20,-10,-10,-10,-10,-10,-10,-20),
(0,0,0,0,0,0,0,0,5,10,10,10,10,10,10,5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,0,0,0,5,5,0,0,0),
(-20,-10,-10,-5,-5,-10,-10,-20,-10,0,0,0,0,0,0,-10,-10,0,5,5,5,5,0,-10,-5,0,5,5,5,5,0,-5,0,0,5,5,5,5,0,-5,-10,5,5,5,5,5,0,-10,-10,0,5,0,0,0,0,-10,-20,-10,-10,-5,-5,-10,-10,-20),
(-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-20,-30,-30,-40,-40,-30,-30,-20,-10,-20,-20,-20,-20,-20,-20,-10,20,20,0,0,0,0,20,20,20,30,10,0,0,10,30,20),
(-50,-40,-30,-20,-20,-30,-40,-50,-30,-20,-10,0,0,-10,-20,-30,-30,-10,20,30,30,20,-10,-30,-30,-10,30,40,40,30,-10,-30,-30,-10,30,40,40,30,-10,-30,-30,-10,20,30,30,20,-10,-30,-30,-30,0,0,0,0,-30,-30,-50,-30,-30,-30,-30,-30,-30,-50),
]
T={};N=[0];W=[0];KILL=[[0,0] for _ in range(32)];PATH=set();Y={}
class X(Exception):pass
def P(p,b):
 q=Request(H+p,data=J.dumps(b).encode(),headers={"content-type":"application/json"})
 with urlopen(q)as r:return J.load(r)
def sq(s):return ord(s[0])-97+(int(s[1])-1)*16
def nm(x):return chr(97+(x&7))+str((x>>4)+1)
def U(m):return nm(m&127)+nm(m>>7&127)+("q" if m>>14 else "")
def F(f):
 a=f.split();b=[0]*128;i=112
 for c in a[0]:
  if c=="/":i-=24
  elif c.isdigit():i+=int(c)
  else:v="PNBRQK".find(c.upper())+1;b[i]=v if c.isupper() else -v;i+=1
 C=sum((ch in a[2])<<j for j,ch in enumerate("KQkq"))
 return b,1 if a[1]=="w" else -1,C,sq(a[3]) if a[3]!="-" else -1
def A(b,t,s):
 for o in (-15,-17) if s>0 else (15,17):
  x=t+o
  if x&136==0 and b[x]==s:return 1
 for o in KN+BD+RD:
  x=t+o
  if x&136==0 and b[x]==(2 if abs(o) in (14,18,31,33) else 6)*s:return 1
 for d in BD+RD:
  x=t+d
  while x&136==0:
   p=b[x]
   if p:
    if p==5*s or p==(3 if abs(d) in (15,17) else 4)*s:return 1
    break
   x+=d
 return 0
def G(b,s,C,E):
 M=[]
 for f,p in enumerate(b):
  if p*s<=0:continue
  a=p*s
  if a==1:
   d=16*s;t=f+d;z=7 if s>0 else 0
   if b[t]==0:
    for q in (5,4,3,2) if t>>4==z else (0,):M.append(f|t<<7|q<<14)
    if f>>4==(1 if s>0 else 6) and b[f+2*d]==0:M.append(f|f+2*d<<7)
   for o in (-1,1):
    t=f+d+o
    if t&136==0 and (b[t]*s<0 and abs(b[t])<6 or t==E):
     for q in (5,4,3,2) if t>>4==z else (0,):M.append(f|t<<7|q<<14)
  elif a==2 or a==6:
   for o in KN if a==2 else BD+RD:
    t=f+o
    if t&136==0 and b[t]*s<=0 and abs(b[t])<6:M.append(f|t<<7)
  else:
   for d in BD if a==3 else RD if a==4 else BD+RD:
    t=f+d
    while t&136==0 and b[t]==0:M.append(f|t<<7);t+=d
    if t&136==0 and b[t]*s<0 and abs(b[t])<6:M.append(f|t<<7)
 k=4 if s>0 else 116
 for z,t,e,r in ((1,6,(5,6),7),(2,2,(3,2,1),0)) if s>0 else ((4,118,(117,118),119),(8,114,(115,114,113),112)):
  if C&z and b[r]==4*s and all(b[x]==0 for x in e) and not any(A(b,x,-s) for x in (k,)+e[:2]):M.append(k|t<<7)
 return M
def D(b,f,t,pr,C,E,s):
 n=b[:];p=n[f];n[f]=0
 if abs(p)==1 and t==E:n[t-16*s]=0
 n[t]=pr*s if pr else p
 if abs(p)==6 and abs(t-f)==2:
  rf=(4 if s>0 else 116)+(3 if t>f else -4)
  n[rf]=0;n[rf-2 if t>f else rf+3]=4*s
 c=C
 if abs(p)==6:c&=~(3 if s>0 else 12)
 z={0:2,7:1,112:8,119:4}
 c&=~z.get(f,0);c&=~z.get(t,0)
 e=f+16*s if abs(p)==1 and abs(t-f)==32 else -1
 return n,c,e
def S(b,s):
 w=0;wb=0;bb=0;eg=not any(abs(p)==5 for p in b);wf=[0]*8;bf=[0]*8;wp=[];bp=[]
 for f,p in enumerate(b):
  if not p:continue
  a=abs(p)
  r=f>>4;c=f&7
  if p>0:
   v=V[a]+PST[a-1][(7-r)*8+c] if a<6 else PST[6 if eg else 5][(7-r)*8+c]
   if a==3:wb+=1
   if a==1:wf[c]+=1;wp.append((r,c))
  else:
   v=V[a]+PST[a-1][r*8+c] if a<6 else PST[6 if eg else 5][r*8+c]
   if a==3:bb+=1
   if a==1:bf[c]+=1;bp.append((r,c))
  w+=v if p>0 else -v
 if wb>1:w+=30
 if bb>1:w-=30
 for r,c in wp:
  if wf[c]>1:w-=8
  if not (wf[c-1] if c else 0) and not (wf[c+1] if c<7 else 0):w-=10
  if not any(br>r and abs(bc-c)<=1 for br,bc in bp):w+=12+3*r
 for r,c in bp:
  if bf[c]>1:w+=8
  if not (bf[c-1] if c else 0) and not (bf[c+1] if c<7 else 0):w+=10
  if not any(wr<r and abs(wc-c)<=1 for wr,wc in wp):w-=12+3*(7-r)
 return w*s
def O(b,m):
 f=m&127;t=m>>7&127;v=b[t]
 return (V[abs(v)]*10-V[abs(b[f])] if v else 0)+(900 if m>>14 else 0)
def Q(b,s,C,E,al,be,pl):
 N[0]+=1
 if N[0]%512<1 and Z.time()>W[0]:raise X
 st=S(b,s)
 if st>=be:return be
 if st>al:al=st
 if pl>10:return al
 ms=[m for m in G(b,s,C,E) if b[m>>7&127]!=0 or (m>>7&127)==E]
 ms.sort(key=lambda m:-O(b,m))
 for m in ms:
  f=m&127;t=m>>7&127;pr=m>>14
  n,c,ee=D(b,f,t,pr,C,E,s)
  if A(n,n.index(6*s),-s):continue
  sc=-Q(n,-s,c,ee,-be,-al,pl+1)
  if sc>al:al=sc
  if al>=be:return be
 return al
def AB(b,s,C,E,d,al,be,pl):
 N[0]+=1
 if N[0]%512<1 and Z.time()>W[0]:raise X
 tb=tuple(b);kr=(tb,s,C,E)
 if kr in PATH:return 0
 if d<=0:return Q(b,s,C,E,al,be,0)
 k=kr;e=T.get(k);oa=al;tm=e[3] if e else -1
 if e and e[0]>=d:
  if e[2]==0:return e[1]
  if e[2]==1 and e[1]>=be:return e[1]
  if e[2]==2 and e[1]<=al:return e[1]
 if d>=3 and not A(b,b.index(6*s),-s) and any(p*s in(2,3,4,5)for p in b):
  if -AB(b,-s,C,-1,d-3,-be,-be+1,pl+1)>=be:return be
 ms=G(b,s,C,E)
 ms.sort(key=lambda m:(-(m==tm),-(m in KILL[pl])*5000,-O(b,m),-Y.get(m&16383,0)))
 best=-99999;bm=0;fl=2;lg=0
 PATH.add(kr)
 try:
  for m in ms:
   f=m&127;t=m>>7&127;pr=m>>14
   n,c,ee=D(b,f,t,pr,C,E,s)
   if A(n,n.index(6*s),-s):continue
   lg+=1
   sc=-AB(n,-s,c,ee,d-1,-be,-al,pl+1)
   if sc>best:best=sc;bm=m
   if sc>al:al=sc
   if al>=be:Y[m&16383]=Y.get(m&16383,0)+d*d;fl=1;break
 finally:
  PATH.discard(kr)
 if not lg:return -19999+pl if A(b,b.index(6*s),-s) else 0
 if fl!=1 and bm:
  kl=KILL[pl]
  if bm!=kl[0]:kl[1]=kl[0];kl[0]=bm
 T[k]=(d,best,0 if best>oa and fl!=1 else fl,bm)
 return best
def R(b,s,C,E,legal,his):
 ms=[]
 for u in legal:
  f=sq(u[:2]);t=sq(u[2:4]);pr=(5,4,3,2)["qrbn".find(u[4])] if len(u)>4 else 0
  ms.append(f|t<<7|pr<<14)
 ms.sort(key=lambda m:-O(b,m))
 keep=[]
 for m in ms:
  f=m&127;t=m>>7&127;pr=m>>14
  n,c,ee=D(b,f,t,pr,C,E,s)
  if his.get((tuple(n),-s,c,ee),0)<2:keep.append(m)
 if keep:ms=keep
 bm=ms[0];T.clear();o=Z.time();W[0]=o+6
 for d in range(1,30):
  if Z.time()-o>1.2:break
  try:
   al=-99999;cur=bm
   for m in ms:
    f=m&127;t=m>>7&127;pr=m>>14
    n,c,ee=D(b,f,t,pr,C,E,s)
    sc=-AB(n,-s,c,ee,d-1,-99999,-al,1)
    if sc>al:al=sc;cur=m
   bm=cur;ms.remove(bm);ms.insert(0,bm)
  except X:bm=cur;break
 f=bm&127;t=bm>>7&127;pr=bm>>14
 n,c,ee=D(b,f,t,pr,C,E,s);his[(tuple(n),-s,c,ee)]=his.get((tuple(n),-s,c,ee),0)+1
 return bm
HIS={}
while True:
 g=P("/game",{})
 if g["status"]=="done":break
 while g["status"]=="your_move":
  b,s,C,E=F(g["fen"]);HIS[(tuple(b),s,C,E)]=HIS.get((tuple(b),s,C,E),0)+1
  g=P("/move",{"game":g["game"],"move":U(R(b,s,C,E,g["legal_moves"],HIS))})
