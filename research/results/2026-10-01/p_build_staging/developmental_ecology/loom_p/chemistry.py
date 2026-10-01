"""Conservative finite-volume backward Euler, exact occupied/emitting areas."""
import numpy as np
from .geometry import disk_areas, rectangle_areas, mover

class FieldSolver:
    def __init__(self,c):
        self.c=c; self.cell_area=(c.world_side/c.grid_n)**2
        self.sources=np.stack([disk_areas(c,p,c.source_radius) for p in c.source_positions])
        self.repairs=np.stack([rectangle_areas(c,r) for r in c.repair_rectangles])
        self.static=self.sources.sum(axis=0)+self.repairs.sum(axis=0)
        self.source_distributions=self.sources/(np.pi*c.source_radius**2)
        areas=np.array([(r[1]-r[0])*(r[3]-r[2]) for r in c.repair_rectangles])
        self.repair_distributions=self.repairs/areas[:,None,None]
        self.last={}
    def coefficients(self,t,phase,body_position=None):
        c=self.c; rect,_=mover(c,t,phase)
        solid=self.static+rectangle_areas(c,rect)
        if body_position is not None: solid=solid+disk_areas(c,body_position,c.body_radius)
        fraction=solid/self.cell_area
        if fraction.min() < -1e-12 or fraction.max()>1+1e-8: raise ArithmeticError('Invalid overlapping field solid geometry')
        diffusion=1/((1-fraction)/c.medium_diffusion+fraction/c.solid_diffusion)
        faces_x=2*diffusion[:,:-1]*diffusion[:,1:]/(diffusion[:,:-1]+diffusion[:,1:])
        faces_y=2*diffusion[:-1,:]*diffusion[1:,:]/(diffusion[:-1,:]+diffusion[1:,:])
        return diffusion,faces_x,faces_y
    def emission(self,stocks):
        amplitude=.05*(.1+.9*np.asarray(stocks)/self.c.source_capacity)
        source=np.einsum('s,sij->ij',amplitude,self.source_distributions,optimize=False)
        repair=.05*self.repair_distributions.sum(axis=0)
        return np.stack((source+.25*repair,.5*source+.35*repair))/self.cell_area
    def step(self,fields,stocks,t,phase,dt,body_position=None,maxiter=100):
        c=self.c
        if not np.isfinite(fields).all() or np.min(fields)<-c.arithmetic_tol: raise ArithmeticError('Invalid incoming chemical state')
        diffusion,fx,fy=self.coefficients(t,phase,body_position)
        kx=dt/self.cell_area*fx; ky=dt/self.cell_area*fy
        diagonal=np.full_like(diffusion,1+dt*c.chemical_decay)
        diagonal[:,:-1]+=kx; diagonal[:,1:]+=kx; diagonal[:-1,:]+=ky; diagonal[1:,:]+=ky
        def apply(x):
            result=diagonal[None,:,:]*x
            result[:,:,:-1]-=kx[None,:,:]*x[:,:,1:]
            result[:,:,1:]-=kx[None,:,:]*x[:,:,:-1]
            result[:,:-1,:]-=ky[None,:,:]*x[:,1:,:]
            result[:,1:,:]-=ky[None,:,:]*x[:,:-1,:]
            return result
        emission=self.emission(stocks); rhs=fields+dt*emission
        norms=np.linalg.norm(rhs.reshape(2,-1),axis=1)
        thresholds=np.where(norms>0,c.field_rtol*norms,c.arithmetic_tol)
        x=fields.copy(); residual=rhs-apply(x); z=residual/diagonal
        direction=z.copy(); rz=np.sum(residual*z,axis=(1,2)); iterations=0
        active=np.linalg.norm(residual.reshape(2,-1),axis=1)>thresholds
        for iterations in range(1,maxiter+1):
            if not active.any(): break
            ad=apply(direction); denom=np.sum(direction*ad,axis=(1,2))
            if np.any(denom[active]<=0): raise ArithmeticError('Field CG lost positive definiteness')
            alpha=np.zeros(2); alpha[active]=rz[active]/denom[active]
            x+=alpha[:,None,None]*direction; residual-=alpha[:,None,None]*ad
            active=np.linalg.norm(residual.reshape(2,-1),axis=1)>thresholds
            z=residual/diagonal; new_rz=np.sum(residual*z,axis=(1,2)); beta=np.zeros(2)
            beta[active]=new_rz[active]/rz[active]
            direction=z+beta[:,None,None]*direction; direction[~active]=0; rz=new_rz
        actual=np.linalg.norm((rhs-apply(x)).reshape(2,-1),axis=1)
        if not np.isfinite(x).all() or np.any(actual>thresholds*(1+1e-5)) or np.min(x)<-c.arithmetic_tol:
            raise ArithmeticError(f'Chemical solver failure: residual={actual}, limits={thresholds}, minimum={x.min()}')
        old_mass=fields.sum(axis=(1,2))*self.cell_area; mass=x.sum(axis=(1,2))*self.cell_area
        emitted=dt*emission.sum(axis=(1,2))*self.cell_area; decay=dt*c.chemical_decay*mass
        self.last=dict(iterations=iterations,residual=actual,relative_residual=np.divide(actual,norms,out=np.zeros_like(actual),where=norms>0),old_mass=old_mass,new_mass=mass,emission=emitted,decay=decay,mass_balance=mass-old_mass-emitted+decay,minimum=float(x.min()),negative_roundoff_count=int((x<0).sum()),diffusion_min=float(diffusion.min()),diffusion_max=float(diffusion.max()))
        return x
