"""Validated anatomical dimensions and source-derived configuration (spec §§2,10)."""
from dataclasses import dataclass, field, asdict
import hashlib
import json
import math
import numpy as np

CHANNELS = ("light", "chemistry", "contact", "proprioception", "energy", "integrity", "motor", "regulation")
RAW_WIDTHS = (10, 4, 8, 7)

@dataclass
class Config:
    schema_version: int = 1
    identifier: str = "p_engineering_baseline_v0_1"
    status: str = "uncommissioned"
    widths: list = field(default_factory=lambda: [8]*4)
    pools: list = field(default_factory=lambda: [[[0,1,2,3],[4,5,6,7]] for _ in range(4)])
    master_seed: int = 0x50A101
    native_dt: float = 0.01
    wave_dt: float = 0.2
    sweeps: int = 4
    tau_a: float = 0.2
    tau_x: float = 0.1
    tau_motor: float = 0.1
    tau_receptor: float = 30.0
    tau_coactivity: float = 10.0
    tau_packet_mean: float = 60.0
    tau_trace: float = 5.0
    gate_branches: int = 4
    feature_width: int = 32
    gate_epsilon: float = 0.05
    query_floor: float = 0.1
    eta_shared: float = 1e-4
    eta_fine: float = 1e-3
    competition: float = 0.1
    rho_shared: float = 1e-5
    rho_fine: float = 5e-5
    tau_shared_reference: float = 10000.0
    tau_fine_reference: float = 5000.0
    lambda_fine_min: float = 1e-4
    lambda_immature: float = 0.005
    lambda_reclaim: float = 0.005
    tau_open: float = 300.0
    shared_radius: float = 0.3
    fine_radius: float = 0.08
    eta_map: float = 1e-4
    lambda_map_min: float = 1e-4
    lambda_unused: float = 0.001
    tau_use: float = 30.0
    use_epsilon: float = 0.01
    map_radius: float = 0.1
    tau_body: float = 2.0
    tau_eligibility: float = 5.0
    eta_bank: float = 0.05
    rho_bank: float = 1e-4
    tau_bank_reference: float = 5000.0
    bank_radius: float = 1.0
    exploration: float = 0.1
    need_floor: float = 0.25
    current_max: float = 0.5
    attenuation_bias: float = math.log(0.2/0.8)
    motor_amplitude: float = 0.25
    motor_noise_amplitude: float = 0.1
    motor_periods: list = field(default_factory=lambda: [7.0,9.0])
    tau_noise: float = 1.0
    noise_refresh: float = 0.5
    world_side: float = 20.0
    body_radius: float = 0.5
    body_mass: float = 1.0
    body_inertia: float = 0.125
    lever: float = 0.35
    linear_drag: float = 1.0
    angular_drag: float = 0.2
    source_radius: float = 0.5
    source_positions: list = field(default_factory=lambda: [[3,3],[10,3],[17,3],[3,10],[17,10],[3,17],[10,17],[17,17]])
    repair_rectangles: list = field(default_factory=lambda: [[0,0.25,8,12],[19.75,20,8,12],[8,12,19.75,20]])
    source_capacity: float = 0.2
    source_tau: float = 400.0
    uptake_rate: float = 0.04
    basal_cost: float = 0.0015
    effort_cost: float = 0.001
    damage_per_impulse: float = 0.02
    stress_threshold: float = 0.25
    repair_rate: float = 0.02
    exchange_force_scale: float = 0.1
    exchange_speed_scale: float = 0.25
    birth_energy: float = 0.7
    mover_centre: list = field(default_factory=lambda: [10.0,10.0])
    mover_amplitude: float = 4.0
    mover_period: float = 30.0
    mover_size: list = field(default_factory=lambda: [2.0,1.0])
    grid_n: int = 80
    medium_diffusion: float = 0.5
    solid_diffusion: float = 0.025
    chemical_decay: float = 0.02
    prehistory_seconds: float = 600.0
    field_rtol: float = 1e-10
    arithmetic_tol: float = 1e-12
    geometry_tol: float = 1e-10
    overlap_tol: float = 1e-8
    event_time_tol: float = 1e-10
    illumination_boundary: str = 'open'  # Jason's 2026-09-22 optical-domain ruling

    def validate(self):
        if self.illumination_boundary not in ('open','opaque'):
            raise ValueError('Unknown optical-domain boundary condition')
        if self.schema_version != 1 or len(self.widths) != 4 or len(self.pools) != 4:
            raise ValueError("Malformed schema")
        for width, groups in zip(self.widths,self.pools):
            if not isinstance(width,int) or width < 1 or not groups:
                raise ValueError("Positive sensory width and nonempty pools required")
            flat = [i for group in groups for i in group]
            if any(not isinstance(i,int) for i in flat) or sorted(flat) != list(range(width)):
                raise ValueError("Pools must cover each coordinate exactly once")
            if len({len(g) for g in groups}) != 1 or not all(groups):
                raise ValueError("Equal-size nonempty one-level pools required")
        for name,value in asdict(self).items():
            if isinstance(value,float) and not np.isfinite(value):
                raise ValueError(f"Nonfinite configuration: {name}")
        if self.native_dt <= 0 or not math.isclose(self.wave_dt/self.native_dt,round(self.wave_dt/self.native_dt)):
            raise ValueError("Wave must contain an integer number of native steps")
        if self.sweeps != 4 or self.gate_branches != 4:
            raise ValueError("This reviewed implementation requires four sweeps and branches")
        return self

    @property
    def group_count(self): return sum(map(len,self.pools))
    @property
    def outputs(self): return self.group_count+4
    @property
    def packet_widths(self): return [2*w for w in self.widths]+[1,1,4,self.outputs]
    @property
    def central_widths(self): return [2*w for w in self.packet_widths]
    @property
    def central_width(self): return sum(self.central_widths)
    @property
    def map_coefficients(self):
        return self.gate_branches*sum(a*b for m,a in enumerate(self.central_widths) for n,b in enumerate(self.central_widths) if m!=n)
    @property
    def slices(self):
        ends=np.cumsum([0]+self.central_widths)
        return [slice(int(ends[i]),int(ends[i+1])) for i in range(8)]
    def identity(self):
        return hashlib.sha256(json.dumps(asdict(self),sort_keys=True,separators=(",",":"),allow_nan=False).encode()).hexdigest()

class Streams:
    """Spec §9: indexed SHA-256 draws; anatomy omits life, no numpy RNG."""
    def __init__(self, seed, life=0):
        self.seed=int(seed); self.life=int(life); self.counters={}
    @staticmethod
    def interior(n):
        return min(np.nextafter(1.0,0.0), max(np.nextafter(0.0,1.0),(n+0.5)/2**64))
    def draw(self,label,shape,anatomy=False,sign=False):
        if ':' in label: raise ValueError("Stream labels cannot contain colons")
        key=("anatomy/" if anatomy else "life/")+label
        index=self.counters.get(key,0); self.counters[key]=index+1
        prefix=f"{self.seed}:{label}:"+("" if anatomy else f"{self.life}:")+f"{index}:"
        result=[]
        for i in range(int(np.prod(shape))):
            n=int.from_bytes(hashlib.sha256((prefix+str(i)).encode('utf-8')).digest()[:8],'big')
            u=self.interior(n); result.append((1.0 if u>=0.5 else -1.0) if sign else u)
        return np.array(result,dtype=np.float64).reshape(shape)

def radial(a,radius):
    norm=np.linalg.norm(a)
    return a.copy() if norm<=radius else a*(radius/norm)

def signed_anatomy(rng,label,shape,norm,rowwise=False):
    a=rng.draw(label,shape,anatomy=True,sign=True)
    if rowwise: return a*(norm/np.linalg.norm(a,axis=1))[:,None]
    return radial(a,norm)
