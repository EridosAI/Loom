"""Standalone plots from JSON/CSV/NPZ only; does not import Loom code."""
import csv,json,os,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
os.environ['MPLCONFIGDIR']=str(HERE/'plot_runtime_cache')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle,Rectangle

plt.rcParams.update({'font.size':11,'axes.titlesize':13,'axes.labelsize':11,'xtick.labelsize':10,
    'ytick.labelsize':10,'svg.fonttype':'none','savefig.facecolor':'white'})
blue='#2864A5';orange='#BA591B';grey='#59636D'
def load(name):return json.loads((HERE/name).read_bytes())
def finish(fig,stem):
    fig.tight_layout(rect=(0,.03,1,.94))
    fig.text(.02,.008,'Source: sealed Founder Search records; passive analysis only. CSV tables retain exact values. No alternative trajectory.',fontsize=10,color=grey)
    for ext in ('png','svg'):fig.savefig(HERE/(stem+'.'+ext),dpi=160,bbox_inches='tight')
    plt.close(fig)
episodes=load('BEHAVIORAL_EPISODES_ENRICHED.json');probes=load('PASSIVE_LEARNED_I_OMISSIONS.json')
fig,axes=plt.subplots(3,2,figsize=(12,10))
for row,name in enumerate(('FS-002','FS-015','FS-044')):
    e=[z for z in episodes if z['life_id']==name];x=np.arange(1,len(e)+1)
    for col,(key,label) in enumerate((('peak_instant_closing_velocity','Peak closing speed at impact (world units/s)'),('damage','Integrity damage in episode'))):
        ax=axes[row,col];ax.bar(x,[z[key] for z in e],color=[orange]+[blue]*(len(e)-1))
        ax.set_xticks(x,[f'{z["episode"]}\n{z["onset"]:.1f} s' for z in e]);ax.set_xlabel('Episode and onset age')
        ax.set_ylabel(label);ax.set_ylim(bottom=0);ax.set_title(name+' · '+e[0]['collider'])
        ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.15)
fig.suptitle('Later contacts can soften, worsen, or remain mixed',fontsize=17)
finish(fig,'CONTACT_SEVERITY')

fig,axes=plt.subplots(2,2,figsize=(12,7.5))
for row,name in enumerate(('FS-010','FS-017')):
    blocks=load(name+'_EXPOSURE_BLOCKS.json');p=[z for z in probes if z['life_id']==name and z['kind']=='fixed_ageblock_closest']
    x=[z['closest_time'] for z in blocks];ax=axes[row,0]
    ax.plot(x,[z['minimum_clearance'] for z in blocks],'o-',color=blue,label='Closest recorded surface gap')
    ax.axhline(0,color='black',linewidth=.7);ax.set_ylabel('Minimum surface clearance (world units)');ax.set_title(name+' · later clearance')
    ax=axes[row,1];ax.axhline(0,color='black',linewidth=.8)
    y=[z['learned_I_into_force_delta_mean']*1e6 for z in p]
    ax.scatter([z['last_native']*.01 for z in p],y,c=[blue if v<0 else orange for v in y],marker='D')
    ax.set_ylabel('Normal − omitted approach force (×10⁻⁶)');ax.set_title(name+' · immediate learned-I effect')
    ax.text(.02,.95,'Below zero: less force into surface\nAbove zero: more force into surface',transform=ax.transAxes,va='top',fontsize=10)
    lim=max(abs(np.array(y)).max()*1.3,1e-4);ax.set_ylim(-lim,lim)
    for ax in axes[row]:ax.set_xlabel('Recorded age (s)');ax.spines[['top','right']].set_visible(False);ax.grid(alpha=.15)
fig.suptitle('Clearance growth and local I influence are separate observations',fontsize=16)
finish(fig,'CLEARANCE_AND_LOCAL_I')

fig,axes=plt.subplots(2,2,figsize=(12,10))
for ax,name in zip(axes.ravel(),('FS-002','FS-010','FS-015','FS-017')):
    d=np.load(HERE/(name+'_RECORDED_NATIVE.npz'));pos=d['position'];t=d['time'][:,0]
    e=[z for z in episodes if z['life_id']==name];first=e[0];index=np.unique(np.r_[np.arange(0,len(pos),10),len(pos)-1]).astype(int)
    ax.plot(pos[:,0],pos[:,1],color='#B3BCC5',lw=.6,zorder=1)
    sc=ax.scatter(pos[index,0],pos[index,1],c=t[index],s=3,cmap='viridis',vmin=0,vmax=431,zorder=2)
    ax.scatter(pos[0,0],pos[0,1],marker='s',s=55,color=blue,label='First recorded position',zorder=5)
    ax.scatter(pos[-1,0],pos[-1,1],marker='X',s=65,color='black',label='Final position',zorder=5)
    for z in e:
        j=z['first_native']-1;p=pos[j];ax.scatter(p[0],p[1],marker='x',s=65,color=orange,zorder=6)
        ax.annotate(str(z['episode']),(p[0],p[1]),xytext=(4,5),textcoords='offset points',color=orange,fontsize=11)
    j=first['first_native']-1;p=pos[j]
    ax.add_patch(Circle(p,.5,fill=False,color=orange,ls='--',lw=1,label='Body at first contact'))
    if first['collider']=='wall-2':ax.axhspan(-.15,0,color='#B6B6B6');ax.axhline(0,color='black')
    if first['collider']=='mover':
        rect=d['mover_rectangle'][j];ax.add_patch(Rectangle((rect[0],rect[2]),rect[1]-rect[0],rect[3]-rect[2],facecolor='#E3E3E3',edgecolor=grey,label='Mover at first contact'))
    if first['collider']=='repair-0':ax.add_patch(Rectangle((0,8),.25,4,facecolor='#E3E3E3',edgecolor=grey,label='Repair surface'))
    margin=.65;ax.set_xlim(pos[:,0].min()-margin,pos[:,0].max()+margin);ax.set_ylim(pos[:,1].min()-margin,pos[:,1].max()+margin)
    ax.set_aspect('equal');ax.set_xlabel('x (world units)');ax.set_ylabel('y (world units)');ax.set_title(name+' · recorded body-centre path')
    ax.legend(fontsize=8,loc='best');ax.spines[['top','right']].set_visible(False)
fig.suptitle('Actual paths only; orange numbers identify behavioral episodes',fontsize=16)
fig.text(.02,.945,'Path colours progress from early (purple) to late (yellow). Mover rectangles show one recorded pose, not permanent occupancy.',fontsize=10,color=grey)
finish(fig,'RECORDED_CANDIDATE_PATHS')
(HERE/'PLOT_RUNTIME.json').write_text(json.dumps(dict(python=sys.version,executable=sys.executable,numpy=np.__version__,matplotlib=matplotlib.__version__,
    scientific_code_imported=False,inputs='derived JSON and NPZ only',world_steps=0)),encoding='utf-8')
print('Saved three passive figures in PNG and SVG.')
