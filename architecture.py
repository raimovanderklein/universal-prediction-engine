"""
UNIVERSAL DISSIPATIVE SYSTEM ARCHITECTURE
Generative Geometry (van der Klein, 2026)
One model. Any dissipative system. Two interaction modes: HOLD (understand) / CROSS (intervene).
Every element carries its axiom, description, formula, test.
If this file is lost, rebuild from AXIOMS.md. If AXIOMS.md is lost, extract from docstrings here.
"""
from __future__ import annotations
import math
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum

# ══════════════════════════════════════════
# A0. TWO OPERATIONS
# ══════════════════════════════════════════
OPERATIONS = {
    'hold': {'name':'Hold','principle':'Resist separation. Maintain coherence.','user_mode':'Understand where the system is'},
    'cross': {'name':'Cross','principle':'Enable interaction. Transform.','user_mode':'Change where the system is'},
}

# ══════════════════════════════════════════
# REALMS
# ══════════════════════════════════════════
class Realm(Enum):
    DELTA=0; RAIDO=1; GEBO=2; SIGMA=3

REALM_META = {
    Realm.DELTA:  {'sym':'Δ','name':'Delta','label':'Potentiality','hold':'latent','cross':'latent','color':'#3B82F6',
                   'principle':'Both latent. Everything potential. Orient before acting.',
                   'org':'Founder Awakening','cancer':'Pre-malignant perturbation','climate':'System disrupted','user_mode':'HOLD'},
    Realm.RAIDO:  {'sym':'ᚱ','name':'Raido','label':'Construction','hold':'active','cross':'latent','color':'#E5A000',
                   'principle':'Hold active. Structure forms. Build.',
                   'org':'Company Building','cancer':'Tumour construction','climate':'Infrastructure build-out','user_mode':'CROSS'},
    Realm.GEBO:   {'sym':'ᚷ','name':'Gebo','label':'Encounter','hold':'active','cross':'active','color':'#0EA472',
                   'principle':'Both active. Meets the world. Encounter.',
                   'org':'Product Meets World','cancer':'Treatment encounter','climate':'Policy meets reality','user_mode':'CROSS'},
    Realm.SIGMA:  {'sym':'Σ','name':'Sigma','label':'Conservation','hold':'latent','cross':'active','color':'#8B5CF6',
                   'principle':'Cross active. Maintains what was won. Tend.',
                   'org':'Sustainable Operation','cancer':'Stable equilibrium/resistance','climate':'New equilibrium maintained','user_mode':'HOLD+CROSS'},
}

# ══════════════════════════════════════════
# SUB-PHASES
# ══════════════════════════════════════════
class SubPhase(Enum):
    SIGNAL=0; STRUCTURE=1; ENCOUNTER=2; CONSERVATION=3

SP_META = {
    SubPhase.SIGNAL:       {'name':'Signal','abbr':'SP1','color':'#2563EB','principle':'System registers. Something changed.','observable':'A signal'},
    SubPhase.STRUCTURE:    {'name':'Structure','abbr':'SP2','color':'#7C3AED','principle':'System builds response.','observable':'A new structure'},
    SubPhase.ENCOUNTER:    {'name':'Encounter','abbr':'SP3','color':'#059669','principle':'Response meets reality.','observable':'Something failed or won'},
    SubPhase.CONSERVATION: {'name':'Conservation','abbr':'SP4','color':'#DC2626','principle':'What encountered settles.','observable':'A fact that will not revert'},
}

# ══════════════════════════════════════════
# A2. AGENT FUNCTIONS
# ══════════════════════════════════════════
class AgentFunction(Enum):
    SENTINEL='sentinel'; MINER='miner'; ARCHITECT='architect'; CATALYST='catalyst'; OBSERVER='observer'

FN_META = {
    AgentFunction.SENTINEL:  {'name':'Sentinel','op':'hold','level':'same','color':'#3B82F6',
        'principle':'Guards boundary','drain':'Off-target holding — prevents healthy change',
        'drain_opponent':'Opponent adapts while you hold still',
        'cancer':'Immunosuppressant','org':'Founder protecting vision past its time'},
    AgentFunction.MINER:     {'name':'Miner','op':'hold','level':'deeper','color':'#8B5CF6',
        'principle':'Extracts from below','drain':'Extraction depletion — deeper level weakened',
        'drain_opponent':'Weaker material for next cycle',
        'cancer':'Stem cell harvest','org':'Senior hire depleting previous org'},
    AgentFunction.ARCHITECT: {'name':'Architect','op':'cross','level':'same','color':'#0EA472',
        'principle':'Transforms at level','drain':'Off-target crossing — healthy systems damaged',
        'drain_opponent':'Damaged allies no longer help against target',
        'cancer':'Cisplatin','org':'Founder building product while crossing family/health'},
    AgentFunction.CATALYST:  {'name':'Catalyst','op':'cross','level':'deeper','color':'#E5543E',
        'principle':'Accelerates from below','drain':'Collateral acceleration — resistance speeds up too',
        'drain_opponent':'Resistance evolves faster',
        'cancer':'Growth factors in leukaemia','org':'Growth hire accelerating burn rate'},
    AgentFunction.OBSERVER:  {'name':'Observer','op':'both','level':'meta','color':'#E5A000',
        'principle':'Surveillance loop — monitors all','drain':'Fear/paralysis — monitoring replaces acting',
        'drain_opponent':'Opponent advances while you watch',
        'cascade':True,  # UNIQUE: propagates to all subordinates
        'cancer':'Risk-averse oncologist under-dosing','org':'Founder hesitation cascading to entire team'},
}

# ══════════════════════════════════════════
# A4. TRANSITIONS
# ══════════════════════════════════════════
TRANSITIONS = {
    (Realm.DELTA,Realm.RAIDO):  {'phi':0.3,'name':'Integration','sym':'|','type':'same_axis',
        'principle':'Hold activates. What was free takes its place.',
        'prior_becomes':'Construction constraint — cannot deviate from plan'},
    (Realm.RAIDO,Realm.GEBO):   {'phi':0.6,'name':'Birth','sym':'+','type':'cross_axis',
        'principle':'Cross activates. Structure meets world. HARDEST TRANSITION.',
        'prior_becomes':'Encounter blockage — it is not ready yet'},
    (Realm.GEBO,Realm.SIGMA):   {'phi':0.3,'name':'Release','sym':'○','type':'same_axis',
        'principle':'Hold deactivates. Resources freed.',
        'prior_becomes':'Stabilisation impossible — cannot slow down'},
    (Realm.SIGMA,Realm.DELTA):  {'phi':0.6,'name':'Death','sym':'−','type':'cross_axis',
        'principle':'Cross deactivates. Coherence lost. New potential.',
        'prior_becomes':'Orientation blind — all metrics stable while world changes'},
}

# ══════════════════════════════════════════
# 16 CHALLENGES
# ══════════════════════════════════════════
CHALLENGES = [
    {'n':1, 'nm':'Recognise','r':Realm.DELTA,'settles':'a named shared problem','org':'Founder sees what is broken','cancer':'Tissue registers perturbation','climate':'System disruption detected'},
    {'n':2, 'nm':'Energise','r':Realm.DELTA,'settles':'a self-organising founding team','org':'Co-founders gather','cancer':'Components accumulate','climate':'Stakeholders mobilise'},
    {'n':3, 'nm':'Envision','r':Realm.DELTA,'settles':'a shared vision owned by the group','org':'Team sees solved future','cancer':'Pre-malignant configuration prefigures form','climate':'Policy vision articulated'},
    {'n':4, 'nm':'Commit','r':Realm.DELTA,'settles':'an irreversible commitment','org':'Incorporates, quits, burns boats','cancer':'Irreversible threshold crossed','climate':'Legislation signed'},
    {'n':5, 'nm':'Plan','r':Realm.RAIDO,'settles':'an aligned plan with owners','org':'Product defined, work sequenced','cancer':'Construction under first constraint','climate':'Implementation plan with targets'},
    {'n':6, 'nm':'Conceive','r':Realm.RAIDO,'settles':'a buildable spec proven on riskiest assumption','org':'Solutions designed and tested','cancer':'Pathway established','climate':'Technology pathways tested'},
    {'n':7, 'nm':'Prove','r':Realm.RAIDO,'settles':'a working prototype validated externally','org':'Prototypes tested','cancer':'Capability tested, prototypes may fail','climate':'Pilots tested, some fail'},
    {'n':8, 'nm':'Choose','r':Realm.RAIDO,'settles':'a single committed design','org':'One version, alternatives killed','cancer':'Configuration selected by criteria','climate':'Pathway selected, alternatives defunded'},
    {'n':9, 'nm':'Manifest','r':Realm.GEBO,'settles':'a discoverable product in the world','org':'Launched to non-affiliated users','cancer':'Observable output for first time','climate':'First measurable emission reduction'},
    {'n':10,'nm':'Interact','r':Realm.GEBO,'settles':'honest understanding of what market wants','org':'Feedback loop closed','cancer':'Encounter-dependent information produced','climate':'Real economic response reveals what works'},
    {'n':11,'nm':'Operate','r':Realm.GEBO,'settles':'a self-sustaining operational rhythm','org':'30 days without founder','cancer':'Sustained processing under pressure','climate':'Sustained reduction under economic pressure'},
    {'n':12,'nm':'Win','r':Realm.GEBO,'settles':'a reproducible winning formula','org':'Formula reproduced by stranger','cancer':'Opposing forces balance','climate':'Growth-reduction equilibrium achieved'},
    {'n':13,'nm':'Organise','r':Realm.SIGMA,'settles':'a structure that survives departure','org':'Key person left, continued','cancer':'Structure differentiates to sustain','climate':'Institution maintains after government change'},
    {'n':14,'nm':'Monitor','r':Realm.SIGMA,'settles':'honest self-observation habit','org':'Junior flags drift, room listens','cancer':'System senses own state','climate':'Monitoring detects backsliding'},
    {'n':15,'nm':'Maintain','r':Realm.SIGMA,'settles':'quality by pride not compliance','org':'Declined revenue to protect standard','cancer':'System corrects for drift','climate':'Standards held against pressure'},
    {'n':16,'nm':'Defend','r':Realm.SIGMA,'settles':'mission carried through form-change','org':'Farewelled what ended','cancer':'Cycle turns — continuation is next perturbation','climate':'Sector transforms'},
]

# ══════════════════════════════════════════
# A11. OBSERVER BIRTHS
# ══════════════════════════════════════════
OBSERVER_BIRTHS = [
    {'nm':'Sustain-vision','born':12,'sustains':'shared vision / initial configuration'},
    {'nm':'Sustain-commitment','born':16,'sustains':'irreversibility of founding threshold'},
    {'nm':'Sustain-architecture','born':20,'sustains':'structural coherence of the build'},
    {'nm':'Sustain-capability','born':28,'sustains':'proven capability'},
    {'nm':'Sustain-encounter','born':36,'sustains':'presence in the world'},
    {'nm':'Sustain-dialogue','born':40,'sustains':'honest understanding from encounter'},
    {'nm':'Sustain-operations','born':44,'sustains':'self-sustaining rhythm'},
    {'nm':'Sustain-formula','born':48,'sustains':'reproducible success pattern'},
    {'nm':'Sustain-structure','born':52,'sustains':'continuity through departure'},
    {'nm':'Sustain-truth','born':56,'sustains':'honest self-observation'},
    {'nm':'Sustain-quality','born':60,'sustains':'intrinsic quality motivation'},
    {'nm':'Sustain-mission','born':64,'sustains':'mission through form-change'},
]

ACTIONS = {
    Realm.DELTA:{SubPhase.SIGNAL:'Prevent',SubPhase.STRUCTURE:'Provoke',SubPhase.ENCOUNTER:'Prevent',SubPhase.CONSERVATION:'Provoke'},
    Realm.RAIDO:{SubPhase.SIGNAL:'Transform',SubPhase.STRUCTURE:'Accelerate',SubPhase.ENCOUNTER:'Transform',SubPhase.CONSERVATION:'Accelerate'},
    Realm.GEBO:{SubPhase.SIGNAL:'Regain control',SubPhase.STRUCTURE:'Catalyse',SubPhase.ENCOUNTER:'Regain control',SubPhase.CONSERVATION:'Catalyse'},
    Realm.SIGMA:{SubPhase.SIGNAL:'Slow',SubPhase.STRUCTURE:'Consolidate',SubPhase.ENCOUNTER:'Slow',SubPhase.CONSERVATION:'Consolidate'},
}
STRATEGIES = ['Dissolution','Disruption','Rejection','Occupation']

# ══════════════════════════════════════════
# A1. THE FORMULA
# ══════════════════════════════════════════
def effective_potency(M:float, D:float) -> float:
    """M_eff = M × (1−D)/(1+D). Test: NSCLC HR predicted 1.10, observed 1.19 (CI 1.04-1.37)."""
    if D>=1: return 0.0
    if D<=0: return M
    return M*(1-D)/(1+D)

# ══════════════════════════════════════════
# AGENT
# ══════════════════════════════════════════
@dataclass
class Agent:
    """Intervention function. Drug/role/policy. Not a person — a FUNCTION."""
    function:AgentFunction; potency:float; subphase:SubPhase; position_assigned:int
    specificity:float=1.0; label:str=''; n_non_target_cycles:int=0; personal_drain:float=0.0

    def D(self)->float:
        base = (1-self.specificity)*(self.n_non_target_cycles/(self.n_non_target_cycles+1)) if self.n_non_target_cycles>0 else 0
        return min(0.95, base+self.personal_drain)

    def overstay(self,pos:int)->int: return max(0,(pos-1)//16-(self.position_assigned-1)//16)
    def overstay_factor(self,pos:int)->float: return [1.0,0.5,0.0,-0.5][min(self.overstay(pos),3)]

    def M_eff(self,pos:int,obs_cascade:float=1.0)->float:
        return effective_potency(self.potency,self.D())*self.overstay_factor(pos)*obs_cascade

    def to_dict(self,pos:int=None)->dict:
        d={'function':self.function.value,'function_meta':FN_META[self.function],'potency':self.potency,
           'subphase':self.subphase.value,'subphase_meta':SP_META[self.subphase],
           'position_assigned':self.position_assigned,'specificity':self.specificity,
           'label':self.label,'D':round(self.D(),3)}
        if pos is not None:
            d.update({'overstay':self.overstay(pos),'M_eff':round(self.M_eff(pos),3),'pathological':self.M_eff(pos)<0})
        return d

# ══════════════════════════════════════════
# SYSTEM
# ══════════════════════════════════════════
@dataclass
class System:
    """Any dissipative system. One class. diagnose() = HOLD. intervene() = CROSS."""
    name:str; domain:str; position:int=1; age:float=0; agents:List[Agent]=field(default_factory=list)
    parallel_cycles:Dict[str,'System']=field(default_factory=dict)

    @property
    def realm(self)->Realm: return Realm((self.position-1)//16)
    @property
    def challenge(self)->dict: return CHALLENGES[(self.position-1)//4]
    @property
    def subphase(self)->SubPhase: return SubPhase((self.position-1)%4)

    # ── HOLD ──
    def diagnose(self)->dict:
        h=self._health(); pd=self._phase_drain(); st=self._stress(); sp=self._speed(); ob=self._observers()
        return {'system':self.name,'domain':self.domain,'position':self.position,
                'realm':REALM_META[self.realm],'challenge':self.challenge,'subphase':SP_META[self.subphase],
                'fraction':self.position/64,'health':h,'phase_drain':pd,'stress':st,'speed':sp,'observers':ob,
                'agents':[a.to_dict(self.position) for a in self.agents],
                'user_mode':REALM_META[self.realm]['user_mode']}

    # ── CROSS ──
    def intervene(self)->dict:
        h=self._health()
        return {'strike_order':self._strike(),'supportive':self._supportive(),'retire':self._overstayed(),
                'gaps':[sp.name for sp in SubPhase if not h['sp'][sp]['covered']]}

    # ── FULL STATE FOR FRONT-END ──
    def frontend(self)->dict:
        d=self.diagnose(); i=self.intervene()
        r=self.realm
        if r==Realm.DELTA: pm,mm='hold','The work is seeing clearly. Do not act yet.'
        elif r in(Realm.RAIDO,Realm.GEBO): pm,mm='cross','The work is building and encountering. Act.'
        else: pm,mm='both','Persist and watch for drift simultaneously.'
        return {'hold':d,'cross':i,'primary_mode':pm,'mode_message':mm,
                'structure':{'realms':{r.name:REALM_META[r] for r in Realm},'subphases':{s.name:SP_META[s] for s in SubPhase},
                             'functions':{f.name:FN_META[f] for f in AgentFunction},'transitions':{f'{a.name}_{b.name}':v for(a,b),v in TRANSITIONS.items()},
                             'challenges':CHALLENGES,'observer_births':OBSERVER_BIRTHS}}

    # ── INTERNALS ──
    def _obs_cascade(self)->float:
        md=0
        for a in self.agents:
            if a.function==AgentFunction.OBSERVER:
                d=a.D()+max(0,1-a.overstay_factor(self.position))*0.2
                md=max(md,d)
        return max(0,1-md)

    def _health(self)->dict:
        c=self._obs_cascade(); sp={}; w=[]
        for s in SubPhase:
            aa=[a for a in self.agents if a.subphase==s]
            if not aa: sp[s]={'score':0,'covered':False,'agents':[]}; w.append(f'{s.name} uncovered'); continue
            p=1.0; dd=[]
            for a in aa:
                e=a.M_eff(self.position,c)
                if e>0: p*=(1-e)
                elif e<0: p*=(1-e); w.append(f'{a.label} pathological')
                dd.append({'label':a.label,'M_eff':round(e,3)})
            sp[s]={'score':max(0,min(1,1-p)),'covered':True,'agents':dd}
        o=1.0
        for s in SubPhase: v=sp[s]['score'] if sp[s]['covered'] else 0; o*=v if v>0 else 0.25
        return {'overall':round(o,4),'coverage':sum(1 for s in SubPhase if sp[s]['covered']),'sp':sp,'warnings':w,'cascade':round(c,3)}

    def _phase_drain(self)->dict:
        pr=Realm((self.realm.value-1)%4); t=TRANSITIONS.get((pr,self.realm))
        if not t: return {'d':0,'source':None}
        pa=[a for a in self.agents if(a.position_assigned-1)//16==pr.value]
        if not pa: return {'d':0,'source':None,'transition':t}
        s=max(pa,key=lambda a:a.potency); return {'d':round(s.potency*t['phi'],3),'source':s.label,'M':s.potency,'transition':t}

    def _stress(self)->dict:
        if not self.parallel_cycles: return {'interfaces':[],'max':0}
        ns=list(self.parallel_cycles.keys()); ii=[]
        for i in range(len(ns)):
            for j in range(i+1,len(ns)):
                a,b=self.parallel_cycles[ns[i]],self.parallel_cycles[ns[j]]
                g=abs(a.realm.value-b.realm.value); s=[0,0.3,0.7,1.0][min(g,3)]
                ii.append({'a':ns[i],'b':ns[j],'gap':g,'stress':s})
        return {'interfaces':ii,'max':max((x['stress'] for x in ii),default=0)}

    def _speed(self)->Optional[dict]:
        if self.age<=0: return None
        def cf(p):
            s=0
            for x in range(int(p*10)): s+=(1+3*(x/640)**1.5)*0.1
            return max(s,.001)
        fn,ff=cf(self.position),cf(64); m=self.age/fn; p=m*ff; r=p-self.age
        ratio=(self.age/p)/(fn/ff) if p>0 and ff>0 else 1
        v='too_fast' if ratio>1.3 else 'too_slow' if ratio<0.7 else 'on_pace'
        return {'verdict':v,'ratio':round(ratio,2),'projected':round(p,1),'remaining':round(r,1)}

    def _observers(self)->dict:
        a=[f for f in OBSERVER_BIRTHS if f['born']<=self.position]
        return {'active':len(a),'total':len(OBSERVER_BIRTHS),'functions':a}

    def _strike(self,n=5)->list:
        cur=self._health(); cc=[]
        for fn in AgentFunction:
            for sp in SubPhase:
                self.agents.append(Agent(fn,0.6,sp,self.position,label=f'{fn.value}/{sp.name}'))
                nw=self._health(); self.agents.pop()
                cc.append({'fn':fn.value,'sp':sp.name,'delta':round(nw['overall']-cur['overall'],4)})
        cc.sort(key=lambda x:x['delta'],reverse=True); return cc[:n]

    def _supportive(self)->list:
        rr=[]
        for a in self.agents:
            if a.function not in(AgentFunction.ARCHITECT,AgentFunction.CATALYST): continue
            d=a.D(); m0=effective_potency(a.potency,d)
            for i in range(min(4,max(1,a.n_non_target_cycles))):
                dn=max(0,d-0.05*(i+1)); mn=effective_potency(a.potency,dn)
                rr.append({'primary':a.label,'n':i+1,'m_before':round(m0,3),'m_after':round(mn,3),'gain':round(mn-m0,3)})
        return rr

    def _overstayed(self)->list:
        return [{'label':a.label,'overstay':a.overstay(self.position),'M_eff':round(a.M_eff(self.position),3)} for a in self.agents if a.overstay(self.position)>=2]


if __name__=='__main__':
    p=System('Pacmed','org',35,72,
        agents=[Agent(AgentFunction.SENTINEL,0.9,SubPhase.SIGNAL,5,label='Founder-sentinel')],
        parallel_cycles={'founder':System('Founder','founder',45),'product':System('Product','product',35),'process':System('Process','process',12)})
    s=p.frontend()
    print(f"Mode: {s['primary_mode']} — {s['mode_message']}")
    print(f"Health: {s['hold']['health']['overall']:.1%}")
    print(f"Gaps: {s['cross']['gaps']}")
    print(f"Overstayed: {len(s['cross']['retire'])}")
    print(f"Strike: {s['cross']['strike_order'][0]}")
    print(f"Structure: {len(s['structure']['realms'])}R {len(s['structure']['functions'])}F {len(s['structure']['challenges'])}C {len(s['structure']['observer_births'])}O")
