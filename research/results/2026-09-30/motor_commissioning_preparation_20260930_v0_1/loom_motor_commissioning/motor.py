"""Fixed blind temporal processes; original downstream motor law copied verbatim.

No world, reserve, raw-sensor or learned input is accepted by the process law.
The subclass is installed only on copied birth snapshots, never a running life.
Legacy phase/noise continue for stream/rollback compatibility but are unused in
candidate drive. Candidate state uses replacement, not in-place mutation.
"""
import copy
import math
import numpy as np
from loom_p.neural import Motor as OriginalMotor, follow
from loom_p.schema import Streams

PARAMETERS = {
    'schema': 1, 'amplitude': 0.35, 'latent_sd': 0.5,
    'refresh_seconds': 0.5, 'refresh_native_steps': 50,
    'M1': {'mean_common': 0.0, 'tau_common': 16.0, 'tau_differential': 8.0,
           'innovation': 'independent standard Gaussian via Box-Muller',
           'initialization': 'independent stationary Gaussian latents'},
    'M2': {'mean_common': 0.0, 'tau_follow': 1.0,
           'duration_ticks_inclusive': [8, 24],
           'target': 'independent Gaussian with sd 0.5',
           'initialization': 'fresh renewal; latents equal first targets'},
}

def gaussian_pair(rng, label):
    u = rng.draw(label, (2,))
    radius = math.sqrt(-2.0 * math.log(float(u[0])))
    angle = 2.0 * math.pi * float(u[1])
    return radius * np.array([math.cos(angle), math.sin(angle)])

def duration(rng):
    return 8 + min(16, int(17 * float(rng.draw('motor-screen-v1-m2-duration', (1,))[0])))

def initialize(process, seed, life):
    if process not in ('M1', 'M2'):
        raise ValueError('unknown experimental process')
    rng = Streams(seed, life)
    latent = PARAMETERS['latent_sd'] * gaussian_pair(rng, 'motor-screen-v1-' + process.lower() + '-initial')
    state = dict(process=process, tick=0, latent=latent, rng=rng)
    if process == 'M2':
        state.update(target=latent.copy(), renew_at=duration(rng) * 50)
    return state

def signal(state, dt):
    if not 0 < dt <= 0.01:
        raise ValueError('native or terminal-fraction interval required')
    s = dict(state)
    s['rng'] = copy.copy(state['rng'])
    s['rng'].counters = state['rng'].counters.copy()
    k = s['tick']
    if type(k) is not int or k < 0:
        raise ValueError('invalid motor native index')
    if s['process'] == 'M1':
        if k > 0 and k % 50 == 0:
            a = np.exp(-0.5 / np.array([16.0, 8.0]))
            z = gaussian_pair(s['rng'], 'motor-screen-v1-m1-innovation')
            s['latent'] = a * s['latent'] + 0.5 * np.sqrt(1 - a*a) * z
    elif s['process'] == 'M2':
        if k == s['renew_at']:
            s['target'] = 0.5 * gaussian_pair(s['rng'], 'motor-screen-v1-m2-target')
            s['renew_at'] = k + 50 * duration(s['rng'])
        if k > s['renew_at']:
            raise ValueError('missed renewal')
    else:
        raise ValueError('unknown process')
    common, differential = s['latent']
    output = 0.35 * np.tanh(np.array([common-differential, common+differential]))
    if s['process'] == 'M2':
        s['latent'] = follow(s['latent'], s['target'], dt, 1.0)
    s['tick'] = k + 1
    if not np.isfinite(output).all() or not np.isfinite(s['latent']).all():
        raise ValueError('nonfinite candidate motor')
    return output, s

class Motor(OriginalMotor):
    def step(self, c, raw, q_motor, current, attenuation, dt):
        if not hasattr(self, 'commissioning'):
            return super().step(c, raw, q_motor, current, attenuation, dt)
        if (c.native_dt, c.noise_refresh, c.tau_motor) != (0.01, 0.5, 0.1):
            raise ValueError('unexpected original motor cadence')
        p = np.concatenate((raw[3], raw[2]))
        oscillator, following = signal(self.commissioning, dt)
        direct = self.feedback@p; evoked = q_motor[2:4].copy()
        target = np.tanh(oscillator+direct+evoked+current)
        self.tendency = follow(self.tendency, target, dt, c.tau_motor)
        self.command = (1-attenuation)*self.tendency
        self.nu = follow(self.nu, self.drive, dt, c.tau_noise)
        self.phase += 2*np.pi/np.array(c.motor_periods)*dt
        self.integral += dt*self.command
        self.diagnostic = dict(oscillator=oscillator, direct_feedback=direct, evoked=evoked,
            current=current.copy(), target=target, tendency=self.tendency.copy(),
            command=self.command.copy(), phase=self.phase.copy(), nu=self.nu.copy(), drive=self.drive.copy())
        self.commissioning = following

def install(engine, process):
    if process not in ('CURRENT', 'M1', 'M2'):
        raise ValueError('process must be declared')
    if engine.native_index != 0 or engine.time != 0 or engine.organism.native_count != 0:
        raise ValueError('installation only at original birth')
    if hasattr(engine.organism.motor, 'commissioning'):
        raise ValueError('motor already replaced')
    if process == 'CURRENT':
        return engine
    old = engine.organism.motor
    motor = Motor.__new__(Motor)
    motor.__dict__ = copy.deepcopy(vars(old))
    rng = engine.organism.rng
    motor.commissioning = initialize(process, rng.seed, rng.life)
    engine.organism.motor = motor
    return engine
