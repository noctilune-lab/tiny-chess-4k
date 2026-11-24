# tiny-chess-01 engine (MIT): alpha-beta + quiescence, fixed node budget, no clock/random.
import json,os,sys
import urllib.request as U
E=os.environ.get("MAKEFUN_ENV_URL")or sys.exit("MAKEFUN_ENV_URL is not set")
def post(p,b):
    return json.load(U.urlopen(U.Request(E+p,json.dumps(b).encode(),{"content-type":"application/json"})))
V=dict(P=100,N=320,B=330,R=500,Q=900,K=60000)
P={}
for p in V:
    P[p]=t=[0]*120
    for i in range(21,99):
        if 0<i%10<9:
            r=9-i//10;c=min(i%10-1,8-i%10);m=min(r,7-r)+c
            t[i]=V[p]+dict(P=r*r//2+3*c,N=7*m,B=4*m,R=2*c+5*(r==6),Q=2*m,K=-12*r+8*(c<3))[p]
Q=(-10,1,10,-1,-9,11,9,-11)
D=dict(N=(-19,-8,12,21,19,8,-12,-21),B=Q[4:],R=Q[:4],Q=Q,K=Q)
class Z(Exception):0
def M(b,s,i,j):
    p=b[i];t=b[j]
    s+=P[p][j]-P[p][i]
    if t!='.':s+=P[t.upper()][119-j]
    if p=='P'and j<29:p='Q';s+=P['Q'][j]-P['P'][j]
    b=b[:i]+'.'+b[i+1:]
    b=b[:j]+p+b[j+1:]
    return -s,i,j,b[::-1].swapcase()
def K(b,s,q):
    r=[]
    for i,p in enumerate(b):
        if p.isupper():
            if p=='P':
                for j in(i-9,i-11):
                    if b[j].islower():r+=[M(b,s,i,j)]
                j=i-10
                if b[j]=='.'and not q:
                    r+=[M(b,s,i,j)]
                    if i>80 and b[j-10]=='.':r+=[M(b,s,i,j-10)]
                continue
            for d in D[p]:
                j=i+d
                while 1:
                    t=b[j]
                    if t.isspace()or t.isupper():break
                    if t!='.'or not q:r+=[M(b,s,i,j)]
                    if p in'NK'or t!='.':break
                    j+=d
    r.sort()
    return r
def S(b,s,d,a,B):
    global n
    n+=1
    if n>CAP:raise Z
    if s<-30000:return s-d
    best=-99999
    if d<1:
        best=s
        if s>=B:return s
        a=max(a,s)
    for c,i,j,x in K(b,s,d<1):
        v=-S(x,c,d-1,-B,-a)
        if v>best:
            best=v
            if v>a:a=v
            if a>=B:break
    if d>0 and best<-30000:
        x=b[::-1].swapcase()
        if not any(x[j]=='k'for c,i,j,y in K(x,0,1)):return 0
    return best
def nm(i):return"abcdefgh"[i%10-1]+str(10-i//10)
def choose(fen,leg):
    global n
    f=fen.split();b=' '*20+''.join(' '+''.join('.'*int(c)if c.isdigit()else c for c in w)+'\n'for w in f[0].split('/'))+' '*20
    if f[1]=='b':b=b[::-1].swapcase()
    s=sum(P[p][i]if p.isupper()else-P[p.upper()][119-i]for i,p in enumerate(b)if p.isalpha())
    def u(k):
        a,z=(k[1],k[2])if f[1]=='w'else(119-k[1],119-k[2])
        return nm(a)+nm(z)
    ks=[k for k in K(b,s,0)if u(k)in leg or u(k)+'q'in leg]or K(b,s,0)
    n=0;res=ks[0]
    for d in range(1,30):
        try:
            a=-99999;bk=None
            for k in ks:
                v=-S(k[3],k[0],d-1,-99999,-a)
                if k[3]in H:v=0
                if v>a:a=v;bk=k
        except Z:break
        res=bk;ks.remove(bk);ks.insert(0,bk)
        if a>30000:break
    H.add(res[3]);m=u(res)
    return m if m in leg else m+'q'if m+'q'in leg else leg[0]
CAP=120000;H=set()
while 1:
    g=post("/game",{})
    if g["status"]=="done":break
    H.clear()
    while g["status"]=="your_move":
        g=post("/move",{"game":g["game"],"move":choose(g["fen"],g["legal_moves"])})
    print(f"game {g['game']}: {g['outcome']} by {g['reason']}",file=sys.stderr)
print(f"done: {g.get('wins')} won, {g.get('draws')} drawn, {g.get('losses')} lost",file=sys.stderr)
