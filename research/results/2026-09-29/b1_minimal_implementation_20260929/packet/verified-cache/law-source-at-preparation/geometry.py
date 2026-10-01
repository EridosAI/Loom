"""Observer-side geometry and exact area integration; no learner object IDs."""
import math
import numpy as np

def circle_rect_area(cx,cy,r,x0,x1,y0,y1):
    """Integrate circle/axis-aligned rectangle intersection analytically by segments."""
    lo=max(x0-cx,-r); hi=min(x1-cx,r); yl=y0-cy; yh=y1-cy
    if hi<=lo or yh<=-r or yl>=r: return 0.0
    points=[lo,hi]
    for y in (yl,yh):
        if abs(y)<r:
            x=math.sqrt(max(0,r*r-y*y))
            for t in (-x,x):
                if lo<t<hi: points.append(t)
    points=sorted(set(points))
    def primitive(x):
        return 0.5*(x*math.sqrt(max(0,r*r-x*x))+r*r*math.asin(max(-1,min(1,x/r))))
    area=0.
    for a,b in zip(points[:-1],points[1:]):
        h=math.sqrt(max(0,r*r-((a+b)/2)**2))
        top=min(yh,h); bottom=max(yl,-h)
        if top<=bottom: continue
        sqrt_coeff=(1 if h<yh else 0)+(1 if -h>yl else 0)
        constant=(yh if yh<=h else 0)-(yl if yl>=-h else 0)
        area+=sqrt_coeff*(primitive(b)-primitive(a))+constant*(b-a)
    if area < -1e-12: raise ArithmeticError('Negative geometric intersection')
    return max(0.,area)  # analytic area roundoff, not chemical concentration clipping

def disk_areas(c,centre,radius):
    n=c.grid_n; dx=c.world_side/n; out=np.zeros((n,n))
    cx,cy=centre
    for iy in range(max(0,int((cy-radius)//dx)),min(n,int((cy+radius)//dx)+1)):
        for ix in range(max(0,int((cx-radius)//dx)),min(n,int((cx+radius)//dx)+1)):
            out[iy,ix]=circle_rect_area(cx,cy,radius,ix*dx,(ix+1)*dx,iy*dx,(iy+1)*dx)
    return out

def rectangle_areas(c,rect):
    n=c.grid_n; dx=c.world_side/n; edges=np.arange(n)*dx
    x0,x1,y0,y1=rect
    wx=np.maximum(0,np.minimum(edges+dx,x1)-np.maximum(edges,x0))
    wy=np.maximum(0,np.minimum(edges+dx,y1)-np.maximum(edges,y0))
    return wy[:,None]*wx[None,:]

def mover(c,t,phase):
    angle=2*np.pi*t/c.mover_period+phase
    x=c.mover_centre[0]+c.mover_amplitude*np.sin(angle); y=c.mover_centre[1]
    w,h=c.mover_size
    return np.array([x-w/2,x+w/2,y-h/2,y+h/2]),np.array([c.mover_amplitude*2*np.pi/c.mover_period*np.cos(angle),0.])

def fixtures(c,t,phase):
    values=[]
    for i,(axis,sign,boundary) in enumerate(((0,1,0),(0,-1,c.world_side),(1,1,0),(1,-1,c.world_side))):
        values.append(dict(id=f'wall-{i}',kind='wall',material=1,axis=axis,sign=sign,boundary=boundary,velocity=np.zeros(2)))
    for i,p in enumerate(c.source_positions): values.append(dict(id=f'source-{i}',kind='disk',material=2,centre=np.array(p,dtype=float),radius=c.source_radius,source=i,velocity=np.zeros(2)))
    for i,rect in enumerate(c.repair_rectangles): values.append(dict(id=f'repair-{i}',kind='rect',material=3,rect=np.array(rect,dtype=float),velocity=np.zeros(2)))
    rect,velocity=mover(c,t,phase)
    values.append(dict(id='mover',kind='rect',material=1,rect=rect,velocity=velocity))
    return values

def gap_normal(position,radius,fixture):
    if fixture['kind']=='wall':
        n=np.zeros(2); n[fixture['axis']]=fixture['sign']
        return fixture['sign']*(position[fixture['axis']]-fixture['boundary'])-radius,n
    if fixture['kind']=='disk':
        delta=position-fixture['centre']; length=np.linalg.norm(delta)
        if length==0: return -radius-fixture['radius'],np.array([1.,0.])
        return length-radius-fixture['radius'],delta/length
    x0,x1,y0,y1=fixture['rect']; p=position
    closest=np.array([np.clip(p[0],x0,x1),np.clip(p[1],y0,y1)])
    delta=p-closest; length=np.linalg.norm(delta)
    if length>0: return length-radius,delta/length
    distances=[p[0]-x0,x1-p[0],p[1]-y0,y1-p[1]]; side=int(np.argmin(distances))
    normal=np.array([[-1.,0.],[1.,0.],[0.,-1.],[0.,1.]])[side]
    return -distances[side]-radius,normal

def ray_hit(origin,direction,fixture,max_distance):
    """First nonnegative hit and outward normal, or None."""
    if fixture['kind']=='wall':
        a=fixture['axis']; denom=direction[a]
        if abs(denom)<1e-15: return None
        t=(fixture['boundary']-origin[a])/denom
        normal=np.zeros(2); normal[a]=fixture['sign']
        return (t,normal) if 1e-9<t<=max_distance else None
    if fixture['kind']=='disk':
        delta=origin-fixture['centre']; b=float(delta@direction); d=b*b-float(delta@delta)+fixture['radius']**2
        if d<0: return None
        for t in (-b-math.sqrt(d),-b+math.sqrt(d)):
            if 1e-9<t<=max_distance: return t,(origin+t*direction-fixture['centre'])/fixture['radius']
        return None
    x0,x1,y0,y1=fixture['rect']; lo=-np.inf; hi=np.inf; normal=None
    for axis,(lower,upper) in enumerate(((x0,x1),(y0,y1))):
        if abs(direction[axis])<1e-15:
            if not lower<=origin[axis]<=upper: return None
            continue
        a=(lower-origin[axis])/direction[axis]; b=(upper-origin[axis])/direction[axis]
        n=np.zeros(2); n[axis]=-1 if direction[axis]>0 else 1
        if a>b: a,b=b,a
        if a>lo: lo=a; normal=n
        hi=min(hi,b)
    if lo<=hi and 1e-9<lo<=max_distance: return lo,normal
    return None

def light_readings(c,position,angle,t,phase):
    if c.illumination_boundary not in ('opaque','transmissive'):
        raise ValueError('Directional-light boundary ruling is unresolved; no implicit exception')
    scene=fixtures(c,t,phase); origin=position+c.body_radius*np.array([np.cos(angle),np.sin(angle)])
    rho=np.array([[.2,.2],[.45,.45],[.7,.35],[.35,.65],[.4,.4]])
    spectrum=np.array([1.,.8]); illumination=np.ones(2)/np.sqrt(2); output=[]
    for sector in (-48,-24,0,24,48):
        samples=[]
        for offset in (-8,0,8):
            a=angle+np.deg2rad(sector+offset); direction=np.array([np.cos(a),np.sin(a)])
            hits=[(hit[0],i,hit[1]) for i,f in enumerate(scene) if (hit:=ray_hit(origin,direction,f,12.)) is not None]
            if not hits: samples.append(.1*rho[0]*spectrum); continue
            distance,index,normal=min(hits,key=lambda h:(h[0],h[1])); f=scene[index]
            point=origin+distance*direction+normal*1e-8
            shadow=any(ray_hit(point,illumination,other,40.) is not None for j,other in enumerate(scene) if j!=index and (other['kind']!='wall' or c.illumination_boundary=='opaque'))
            own_body=dict(kind='disk',centre=position,radius=c.body_radius)
            shadow=shadow or ray_hit(point,illumination,own_body,40.) is not None
            samples.append(rho[f['material']]*(.1+.9*max(float(normal@illumination),0)*(not shadow))*spectrum*np.exp(-distance/8.))
        output.extend(np.mean(samples,axis=0))
    return np.array(output)

def bilinear(field,position,side):
    n=field.shape[-1]; cell=side/n
    coord=np.clip(np.asarray(position)/cell-.5,0,n-1)
    x0,y0=np.floor(coord).astype(int); x1=min(n-1,x0+1); y1=min(n-1,y0+1)
    fx,fy=coord-[x0,y0]
    return (1-fy)*((1-fx)*field[:,y0,x0]+fx*field[:,y0,x1])+fy*((1-fx)*field[:,y1,x0]+fx*field[:,y1,x1])

def transduce(c,body,field,t,phase):
    light=light_readings(c,body.position,body.angle,t,phase)
    chemical=[]
    for offset in (-np.pi/4,np.pi/4):
        angle=body.angle+offset
        p=body.position+(c.body_radius+.001)*np.array([np.cos(angle),np.sin(angle)])
        sample=bilinear(field,p,c.world_side)
        mixed=np.array([[1.,.5],[.5,1.]])@sample
        if np.min(mixed)<-c.arithmetic_tol: raise ArithmeticError('Negative chemical receptor input')
        chemical.extend(mixed/(.05+mixed))
    contact=1-np.exp(-body.contact_rates/.25)
    forward=np.array([np.cos(body.angle),np.sin(body.angle)]); lateral=np.array([-forward[1],forward[0]])
    vf=float(body.velocity@forward); vl=float(body.velocity@lateral); omega=body.omega; u=body.command
    proprio=np.array([u[0],u[1],np.tanh(vf),np.tanh(vl),np.tanh(omega/1.75),np.tanh(u[0]-(vf-c.lever*omega)),np.tanh(u[1]-(vf+c.lever*omega))])
    return (light,np.array(chemical),contact,proprio)
