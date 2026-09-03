import numpy as np
THETA=0.25; SIG=0.5; BOUND=1.5
S_STEP=0.25*0.5*np.sqrt(1-(1-THETA)**2); K=4; SHUF=1.3261841709438256
def reflect(x,b=BOUND):
    period=4*b; y=np.mod(x+b,period); y=np.where(y>2*b,period-y,y); return y-b

def sim(v,mode,n=300000,k=11,seed=1):
    rng=np.random.default_rng(seed)
    c=np.clip(SIG*rng.standard_normal((n,K)),-BOUND,BOUND); a=c.copy(); c0=c.copy()
    u=rng.standard_normal((n,K)); u/=np.linalg.norm(u,axis=1,keepdims=True) if v>0 else 1
    P=[c.copy()]; perstep=[]
    for p in range(2,k+1):
        if v>0:
            if mode=='pos_reflect_fixed_heading':      # reconcile_sim: position reflects, u fixed (anchor sticks)
                a=reflect(a+v*u)
            elif mode=='billiard_heading_flip':        # physical: heading component flips at wall, anchor continues
                a_raw=a+v*u
                over=np.abs(a_raw)>BOUND
                u=np.where(over,-u,u)                   # flip heading on axes that hit the wall
                a=reflect(a_raw)
        cn=reflect(c+THETA*(a-c)+S_STEP*rng.standard_normal((n,K)))
        perstep.append(np.linalg.norm(cn-c,axis=1)); c=cn; P.append(c.copy())
    P=np.stack(P,0)
    net=np.linalg.norm(P[-1]-c0,axis=1); path=np.linalg.norm(np.diff(P,0),axis=2).sum(0) if False else np.linalg.norm(np.diff(P,axis=0),axis=2).sum(0)
    ratio=(net/np.where(path>0,path,1)).mean()
    trav=((P.max(0)-P.min(0))/(2*BOUND)).mean(1).mean()
    return ratio,trav

print("net/path@11 (pose), two anchor-reflection readings of §1 'reflecting at the family bounds':")
print(f"{'v':>5} {'POS-reflect(mine)':>18} {'trav':>6}   {'BILLIARD-flip':>14} {'trav':>6}")
for v in [0.0,0.20,0.30,0.40,0.50,0.70]:
    r1,t1=sim(v,'pos_reflect_fixed_heading'); r2,t2=sim(v,'billiard_heading_flip')
    print(f"{v:5.2f} {r1:18.4f} {t1:6.3f}   {r2:14.4f} {t2:6.3f}")
print("\nJason's reported curve: falls 0.611->0.515 over v 0.30->0.50")
