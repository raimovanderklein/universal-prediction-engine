"""
LAYER7 — Universal Dissipative System Tool
Generative Geometry (van der Klein, 2026)

Seven layers of intervention on any dissipative system:
  L1. Position    — where is the system in its cycle
  L2. Sub-phase   — what is happening here (Signal/Structure/Encounter/Conservation)
  L3. Agent       — who/what covers each sub-phase
  L4. Parameters  — potency, drain, overstay, depth
  L5. Combination — coverage × health = product of blockades
  L6. Move        — the best next structural intervention
  L7. Execution   — getting the agent to make the move (depth 4)

Backend serves all computation. Frontend is display only.
"""

from __future__ import annotations
import json
import math
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum
from pathlib import Path

# ═══════════════════════════════════════════
# FOUNDATIONAL STRUCTURE (domain-agnostic)
# ═══════════════════════════════════════════

class Realm(Enum):
    DELTA=0; RAIDO=1; GEBO=2; SIGMA=3

class SubPhase(Enum):
    SIGNAL=0; STRUCTURE=1; ENCOUNTER=2; CONSERVATION=3

class AgentFunction(Enum):
    SENTINEL='sentinel'; MINER='miner'; ARCHITECT='architect'; CATALYST='catalyst'; OBSERVER='observer'

REALMS = {
    Realm.DELTA:  {'sym':'Δ','name':'Delta','label':'Potentiality','color':'#3B82F6','mode':'hold',
                   'principle':'Both latent. Everything potential. Orient before acting.'},
    Realm.RAIDO:  {'sym':'ᚱ','name':'Raido','label':'Construction','color':'#E5A000','mode':'cross',
                   'principle':'Hold active. Structure forms. Build.'},
    Realm.GEBO:   {'sym':'ᚷ','name':'Gebo','label':'Encounter','color':'#0EA472','mode':'cross',
                   'principle':'Both active. Meets the world. Encounter.'},
    Realm.SIGMA:  {'sym':'Σ','name':'Sigma','label':'Conservation','color':'#8B5CF6','mode':'hold+cross',
                   'principle':'Cross active. Maintains what was won. Tend.'},
}

SUB_PHASES = {
    SubPhase.SIGNAL:       {'name':'Signal','abbr':'SP1','color':'#2563EB',
                            'principle':'Something changed. The system registers.',
                            'observable':'A signal that was not there before'},
    SubPhase.STRUCTURE:    {'name':'Structure','abbr':'SP2','color':'#7C3AED',
                            'principle':'The system builds a response.',
                            'observable':'A new structure'},
    SubPhase.ENCOUNTER:    {'name':'Encounter','abbr':'SP3','color':'#059669',
                            'principle':'The response meets reality.',
                            'observable':'Something failed or won'},
    SubPhase.CONSERVATION: {'name':'Conservation','abbr':'SP4','color':'#DC2626',
                            'principle':'What encountered settles.',
                            'observable':'A fact that will not revert'},
}

FUNCTIONS = {
    AgentFunction.SENTINEL:  {'name':'Sentinel','op':'hold','depth':'same','color':'#3B82F6',
                              'principle':'Guards boundary','drain_type':'Off-target holding'},
    AgentFunction.MINER:     {'name':'Miner','op':'hold','depth':'deeper','color':'#8B5CF6',
                              'principle':'Extracts from below','drain_type':'Extraction depletion'},
    AgentFunction.ARCHITECT: {'name':'Architect','op':'cross','depth':'same','color':'#0EA472',
                              'principle':'Transforms at level','drain_type':'Off-target crossing'},
    AgentFunction.CATALYST:  {'name':'Catalyst','op':'cross','depth':'deeper','color':'#E5543E',
                              'principle':'Accelerates from below','drain_type':'Collateral acceleration'},
    AgentFunction.OBSERVER:  {'name':'Observer','op':'both','depth':'meta','color':'#E5A000',
                              'principle':'Surveillance loop','drain_type':'Fear/paralysis'},
}

TRANSITIONS = [
    {'from':Realm.DELTA,'to':Realm.RAIDO,'phi':0.3,'name':'Integration','type':'same_axis'},
    {'from':Realm.RAIDO,'to':Realm.GEBO,'phi':0.6,'name':'Birth','type':'cross_axis'},
    {'from':Realm.GEBO,'to':Realm.SIGMA,'phi':0.3,'name':'Release','type':'same_axis'},
    {'from':Realm.SIGMA,'to':Realm.DELTA,'phi':0.6,'name':'Death','type':'cross_axis'},
]

OBSERVER_BIRTHS = [
    {'name':'Sustain-vision','born':3,'sustains':'shared vision / initial configuration'},
    {'name':'Sustain-commitment','born':4,'sustains':'irreversibility of founding threshold'},
    {'name':'Sustain-architecture','born':5,'sustains':'structural coherence of the build'},
    {'name':'Sustain-capability','born':7,'sustains':'proven capability'},
    {'name':'Sustain-encounter','born':9,'sustains':'presence in the world'},
    {'name':'Sustain-dialogue','born':10,'sustains':'honest understanding from encounter'},
    {'name':'Sustain-operations','born':11,'sustains':'self-sustaining rhythm'},
    {'name':'Sustain-formula','born':12,'sustains':'reproducible success pattern'},
    {'name':'Sustain-structure','born':13,'sustains':'continuity through departure'},
    {'name':'Sustain-truth','born':14,'sustains':'honest self-observation'},
    {'name':'Sustain-quality','born':15,'sustains':'intrinsic quality motivation'},
    {'name':'Sustain-mission','born':16,'sustains':'mission through form-change'},
]

# Foundational 16 position names (domain-agnostic)
POSITION_NAMES_16 = [
    'Disturbance','Accumulation','Preview','Commitment',
    'Initiation','Architecture','Testing','Selection',
    'Output','Discovery','Integration','Equilibrium',
    'Differentiation','Surveillance','Compensation','Continuation'
]


# ═══════════════════════════════════════════
# L1. THE FORMULA
# ═══════════════════════════════════════════

def effective_potency(M: float, D: float) -> float:
    """M_eff = M × (1−D)/(1+D)"""
    if D >= 1: return 0.0
    if D <= 0: return M
    return M * (1 - D) / (1 + D)

def overstay_realms(assigned_pos: int, current_pos: int) -> int:
    return max(0, (current_pos - 1) // 4 - (assigned_pos - 1) // 4)

def overstay_factor(assigned_pos: int, current_pos: int) -> float:
    os = overstay_realms(assigned_pos, current_pos)
    return [1.0, 0.5, 0.0, -0.5][min(os, 3)]


# ═══════════════════════════════════════════
# DOMAIN REGISTRY
# ═══════════════════════════════════════════

class Domain:
    """A domain provides the vocabulary for a specific type of dissipative system.
    Structure is universal. Content is domain-specific."""

    def __init__(self, domain_id: str, name: str, perspective: str):
        self.id = domain_id
        self.name = name
        self.perspective = perspective  # "We are the [company/tumour/immune system]"
        self.events_16: List[Dict] = []    # 16 position events
        self.events_64: List[Dict] = []    # 64 sub-phase events
        self.sp_nouns: Dict[int, Dict] = {}  # sub-phase vocabulary per position
        self.agent_templates: List[Dict] = []  # available agents for this domain
        self.challenges_16: List[Dict] = []  # 16 challenge names + settles

    def event_at(self, position: int) -> Optional[Dict]:
        """Get the event at a given position (1-indexed, 1-64)."""
        if self.events_64 and position <= len(self.events_64):
            return self.events_64[position - 1]
        elif self.events_16 and position <= 16:
            return self.events_16[position - 1]
        return None

    def sp_vocab_at(self, position: int) -> Dict:
        """Get the sub-phase vocabulary for a given position."""
        return self.sp_nouns.get(position, {
            0: 'Signal', 1: 'Structure', 2: 'Encounter', 3: 'Conservation'
        })

    def agents_for_sp(self, sp: int) -> List[Dict]:
        """Get available agent templates for a given sub-phase."""
        return [a for a in self.agent_templates if a.get('subphase') == sp]

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'name': self.name,
            'perspective': self.perspective,
            'events_16': self.events_16,
            'events_64': self.events_64,
            'challenges_16': self.challenges_16,
            'agent_templates': self.agent_templates,
            'has_64': len(self.events_64) > 0,
            'has_agents': len(self.agent_templates) > 0,
        }


# ═══════════════════════════════════════════
# DOMAIN: ORGANISATION
# ═══════════════════════════════════════════

def _build_org_domain() -> Domain:
    d = Domain('org', 'Organisation', 'We are the company')

    d.challenges_16 = [
        {'n':1,'nm':'Recognise','settles':'a named, shared problem'},
        {'n':2,'nm':'Energise','settles':'a self-organising founding team'},
        {'n':3,'nm':'Envision','settles':'a shared vision owned by the group'},
        {'n':4,'nm':'Commit','settles':'an irreversible commitment'},
        {'n':5,'nm':'Plan','settles':'an aligned plan with owners'},
        {'n':6,'nm':'Conceive','settles':'a buildable spec proven on riskiest assumption'},
        {'n':7,'nm':'Prove','settles':'a working prototype validated externally'},
        {'n':8,'nm':'Choose','settles':'a single committed design'},
        {'n':9,'nm':'Manifest','settles':'a discoverable product in the world'},
        {'n':10,'nm':'Interact','settles':'honest understanding of what the world wants'},
        {'n':11,'nm':'Operate','settles':'a self-sustaining operational rhythm'},
        {'n':12,'nm':'Win','settles':'a reproducible winning formula'},
        {'n':13,'nm':'Organise','settles':'a structure that survives departure'},
        {'n':14,'nm':'Monitor','settles':'honest self-observation habit'},
        {'n':15,'nm':'Maintain','settles':'quality by pride not compliance'},
        {'n':16,'nm':'Defend','settles':'mission carried through form-change'},
    ]

    # 16 position events (summary level)
    d.events_16 = [
        {'pos':1,'nm':'The recurring thought','ev':'Same thought about what is broken >3 times in one week','test':'Can you name the thought?'},
        {'pos':2,'nm':'Co-founders gathering','ev':'People approaching about the same problem without being asked','test':'Did they come to you?'},
        {'pos':3,'nm':'Vision taking shape','ev':'Vision exists outside head — a sketch a stranger could read','test':'Could someone not in the room understand it?'},
        {'pos':4,'nm':'Burning boats','ev':'Resigned, signed, transferred capital — cannot be quietly undone','test':'Can it be quietly undone?'},
        {'pos':5,'nm':'Product named','ev':'Team named the specific product that must exist','test':'Can you say it in one noun phrase?'},
        {'pos':6,'nm':'Solutions designed','ev':'3+ distinct approaches exist as specs or prototypes','test':'Name three and what makes each different'},
        {'pos':7,'nm':'Prototypes tested','ev':'Prototype tested beyond design limits — failure point known','test':'What broke and at what threshold?'},
        {'pos':8,'nm':'One version selected','ev':'Stopped work on all designs except one','test':'Is anyone still on a killed alternative?'},
        {'pos':9,'nm':'First real user','ev':'Person with no personal connection used the product','test':'Friend, referral, or stranger?'},
        {'pos':10,'nm':'Feedback loop closed','ev':'User issue fixed, user told, user confirmed improvement','test':'Name user, issue, confirmation'},
        {'pos':11,'nm':'Month without founder','ev':'30 days without founder making operational decisions','test':'Did founder touch operations?'},
        {'pos':12,'nm':'Formula reproduced','ev':'Non-founder reproduced conversion using only documentation','test':'Who? Did they use the docs only?'},
        {'pos':13,'nm':'Survived departure','ev':'Key person left, org continued without degradation 30+ days','test':'Who left? What metric shows?'},
        {'pos':14,'nm':'Junior speaks, room follows','ev':'Non-senior person flagged drift, discussion changed direction','test':'Who? Did the room follow?'},
        {'pos':15,'nm':'Said no to revenue','ev':'Declined paying customer because it violated core standard','test':'How much left on the table?'},
        {'pos':16,'nm':'Farewell held','ev':'Org honoured what ended before beginning what comes next','test':'Was there a real ritual?'},
    ]

    # 64 events — full sub-phase resolution
    # (imported from engine.py POSITIONS_64)
    d.events_64 = _load_org_64()

    return d


def _load_org_64() -> List[Dict]:
    """Load org 64 events. Inline for portability."""
    return [
        {'p':1,'ch':0,'sp':0,'nm':'The recurring thought','ev':'Same thought about what is broken >3 times in one week','test':'Can you name the thought?','produces':'an unspoken discomfort'},
        {'p':2,'ch':0,'sp':1,'nm':'Written down','ev':'Problem statement written in a document or notebook','test':'Does the written record exist?','produces':'a draft problem statement'},
        {'p':3,'ch':0,'sp':2,'nm':'Said out loud','ev':'Problem described to another person with substantive response','test':'Who did you tell and what did they say?','produces':'a tested observation'},
        {'p':4,'ch':0,'sp':3,'nm':'Shared fact','ev':'Two+ people independently confirm problem is real and worth solving','test':'Would they say the same separately?','produces':'a named, shared problem'},
        {'p':5,'ch':1,'sp':0,'nm':'Unprompted response','ev':'Someone approached about same problem without being asked','test':'Did they come to you?','produces':'a resonance signal'},
        {'p':6,'ch':1,'sp':1,'nm':'Space created','ev':'Specific gathering created for potential co-founders','test':'Does the invite exist?','produces':'a gathering structure'},
        {'p':7,'ch':1,'sp':2,'nm':'Energy tested','ev':'Group met and energy was either charged or performative','test':'If you cancelled, would they ask why?','produces':'a tested group dynamic'},
        {'p':8,'ch':1,'sp':3,'nm':'Self-organising','ev':'Group coordinates without initiator — scheduled something themselves','test':'Did they schedule without you?','produces':'a self-organising founding team'},
        {'p':9,'ch':2,'sp':0,'nm':'Recurring image','ev':'Specific image of solved future returns unbidden','test':'Can you draw it in 30 seconds?','produces':'a private vision fragment'},
        {'p':10,'ch':2,'sp':1,'nm':'Externalised vision','ev':'Vision outside head — sketch, deck, one-pager a stranger could read','test':'Could someone not in the room understand it?','produces':'a shareable vision document'},
        {'p':11,'ch':2,'sp':2,'nm':'Vision challenged','ev':'Co-founder changed substantive element and it was accepted','test':'What did they change?','produces':'a co-owned vision'},
        {'p':12,'ch':2,'sp':3,'nm':'Shared ownership','ev':'Each co-founder describes vision in own words — descriptions converge','test':'Ask separately. Do they match?','produces':'a shared vision owned by the group'},
        {'p':13,'ch':3,'sp':0,'nm':'Decision pending','ev':'All preparation complete — only remaining act is irreversible','test':'Waiting for information or courage?','produces':'a readiness to commit'},
        {'p':14,'ch':3,'sp':1,'nm':'Legal structure ready','ev':'Incorporation papers, shareholders agreement, bank account','test':'Could you sign today?','produces':'a legal commitment structure'},
        {'p':15,'ch':3,'sp':2,'nm':'Irreversible act','ev':'Resigned, signed, transferred capital — cannot be quietly undone','test':'Can it be quietly undone?','produces':'a crossed threshold'},
        {'p':16,'ch':3,'sp':3,'nm':'New identity','ev':'Introduces self as founder of [company], not employee of [previous]','test':'What did you say last time?','produces':'an irreversible founding commitment'},
        {'p':17,'ch':4,'sp':0,'nm':'Product named','ev':'Team named the specific product that must exist','test':'One noun phrase?','produces':'a named product concept'},
        {'p':18,'ch':4,'sp':1,'nm':'Sequenced plan','ev':'Document with tasks, owners, dependencies, dates','test':'Open it. Names and dates?','produces':'a project plan with critical path'},
        {'p':19,'ch':4,'sp':2,'nm':'Plan stress-tested','ev':'Someone outside team found a dependency the team missed','test':'What did they find?','produces':'a stress-tested plan'},
        {'p':20,'ch':4,'sp':3,'nm':'Team aligned','ev':'Every member states what, for whom, by when, riskiest assumption — all match','test':'Ask them. All four match?','produces':'an aligned plan with owners'},
        {'p':21,'ch':5,'sp':0,'nm':'Design space open','ev':'Began with no predetermined solution — 2+ approaches','test':'Name two different approaches','produces':'an open design space'},
        {'p':22,'ch':5,'sp':1,'nm':'Multiple designs','ev':'3+ distinct approaches as specs or prototypes','test':'Name three, what makes each different','produces':'competing solution designs'},
        {'p':23,'ch':5,'sp':2,'nm':'Riskiest assumption tested','ev':'Most uncertain element tested with definitive result','test':'Pass or fail?','produces':'a proven core assumption'},
        {'p':24,'ch':5,'sp':3,'nm':'Buildable spec','ev':'Spec detailed enough new engineer can begin without calling designer','test':'Hand it to someone new. Can they start?','produces':'a buildable spec'},
        {'p':25,'ch':6,'sp':0,'nm':'First build started','ev':'First commit, prototype cut, or material ordered','test':'Does commit/part/receipt exist?','produces':'a first build artefact'},
        {'p':26,'ch':6,'sp':1,'nm':'Measurable improvement','ev':'V(N+1) outperforms V(N) on pre-defined metric','test':'What metric? Two numbers?','produces':'a learning curve with evidence'},
        {'p':27,'ch':6,'sp':2,'nm':'Failure under load','ev':'Prototype tested beyond design limits — failure point known','test':'What broke at what threshold?','produces':'known failure boundaries'},
        {'p':28,'ch':6,'sp':3,'nm':'External validation','ev':'Non-team person used prototype for intended purpose — worked without help','test':'Who? Without help?','produces':'a working prototype validated externally'},
        {'p':29,'ch':7,'sp':0,'nm':'Decision paralysis','ev':'Multiple viable options, team not selected — weeks passing','test':'How many weeks?','produces':'a visible cost of indecision'},
        {'p':30,'ch':7,'sp':1,'nm':'Criteria before scoring','ev':'Evaluation criteria agreed and written before scores','test':'Were criteria written before scores?','produces':'a fair evaluation framework'},
        {'p':31,'ch':7,'sp':2,'nm':'Alternatives killed','ev':'Stopped work on all except one — resources redirected','test':'Anyone still on killed alternative?','produces':'a selection decision with real loss'},
        {'p':32,'ch':7,'sp':3,'nm':'Single design in production','ev':'Engineering builds one version — no parallel tracks','test':'How many active branches?','produces':'a single committed design'},
        {'p':33,'ch':8,'sp':0,'nm':'Launch avoidance','ev':'Product could ship but someone keeps finding reasons to delay','test':'Quality or fear?','produces':'a visible avoidance pattern'},
        {'p':34,'ch':8,'sp':1,'nm':'First-touch designed','ev':'Onboarding/first interaction explicitly designed','test':'Describe first 30 seconds','produces':'a designed first encounter'},
        {'p':35,'ch':8,'sp':2,'nm':'First non-affiliated user','ev':'Person with no connection used the product','test':'Friend, referral, or stranger?','produces':'a real-world encounter'},
        {'p':36,'ch':8,'sp':3,'nm':'Discoverable','ev':'Someone found product without team directing them','test':'Analytics: untraceable user?','produces':'a discoverable product'},
        {'p':37,'ch':9,'sp':0,'nm':'Unexpected use','ev':'User did something never designed or intended','test':'What did they do?','produces':'an unexpected use signal'},
        {'p':38,'ch':9,'sp':1,'nm':'Feedback system','ev':'Structured process collects, categorises, prioritises feedback','test':'Where does feedback go?','produces':'a structured feedback process'},
        {'p':39,'ch':9,'sp':2,'nm':'Loop closed','ev':'User issue fixed, user told, user confirmed','test':'Name user, issue, confirmation','produces':'a closed feedback loop'},
        {'p':40,'ch':9,'sp':3,'nm':'Honest paragraph','ev':'Team wrote what market actually wants vs what was planned','test':'Does it make you uncomfortable?','produces':'honest understanding'},
        {'p':41,'ch':10,'sp':0,'nm':'Scale failure','ev':'Something that worked in testing failed at real volume','test':'What broke? Who fixed it by hand?','produces':'a known scaling vulnerability'},
        {'p':42,'ch':10,'sp':1,'nm':'System replaces hero','ev':'Heroic fix now has automated or documented system','test':'If person is sick, does it still work?','produces':'a systematised operation'},
        {'p':43,'ch':10,'sp':2,'nm':'Week without escalation','ev':'7 days of production, zero escalations to founder','test':'Check messages for 7 days','produces':'a tested operational rhythm'},
        {'p':44,'ch':10,'sp':3,'nm':'Month without founder','ev':'30 days, founder made no operational decisions','test':'Did founder touch operations?','produces':'a self-sustaining rhythm'},
        {'p':45,'ch':11,'sp':0,'nm':'Pattern felt','ev':'Customers convert, team feels pattern but 3 give 3 explanations','test':'Ask three. Three different answers?','produces':'an unnamed conversion pattern'},
        {'p':46,'ch':11,'sp':1,'nm':'Formula articulated','ev':'One person stated reason in one sentence, room went quiet','test':'Write that sentence now','produces':'an articulated winning formula'},
        {'p':47,'ch':11,'sp':2,'nm':'Formula tested','ev':'Campaign/pricing built on named formula produced measurable lift','test':'Intervention and measured delta?','produces':'a validated formula'},
        {'p':48,'ch':11,'sp':3,'nm':'Reproduced by stranger','ev':'Non-founder reproduced conversion using only documentation','test':'Who? Docs only?','produces':'a reproducible winning formula'},
        {'p':49,'ch':12,'sp':0,'nm':'Dependency visible','ev':'Founder unavailable 5+ days, specific functions stopped','test':'What stopped?','produces':'a visible dependency map'},
        {'p':50,'ch':12,'sp':1,'nm':'Knowledge in systems','ev':'Critical processes as docs or automated workflows, not in heads','test':'Delete one account — process still runs?','produces':'a documented process library'},
        {'p':51,'ch':12,'sp':2,'nm':'New person test','ev':'Recent hire tried core process from docs, got stuck at specific point','test':'Where did they get stuck?','produces':'a gap-tested doc set'},
        {'p':52,'ch':12,'sp':3,'nm':'Survived departure','ev':'Key person left, org continued without degradation 30+ days','test':'Who left? What metric?','produces':'a structure that survives departure'},
        {'p':53,'ch':13,'sp':0,'nm':'Leading indicator red','ev':'Dashboards green but leading indicator trends wrong','test':'Name the leading indicator','produces':'a visible measurement gap'},
        {'p':54,'ch':13,'sp':1,'nm':'Drift metric built','ev':'Metric measuring gap between intended and actual state','test':'What does it measure?','produces':'a drift-detection instrument'},
        {'p':55,'ch':13,'sp':2,'nm':'Metric forced decision','ev':'Drift metric crossed threshold, team changed behaviour','test':'Number, threshold, what changed?','produces':'evidence measurement changes behaviour'},
        {'p':56,'ch':13,'sp':3,'nm':'Junior speaks, room follows','ev':'Non-senior flagged drift, discussion changed direction','test':'Who? Did room follow?','produces':'honest self-observation habit'},
        {'p':57,'ch':14,'sp':0,'nm':'Quality drift named','ev':'Customer said "it used to be better" — team wanted to disagree','test':'What did customer say?','produces':'a named quality drift'},
        {'p':58,'ch':14,'sp':1,'nm':'Standards explicit','ev':'3-5 standards defining product soul made visible','test':'Recite without looking','produces':'explicit quality standards'},
        {'p':59,'ch':14,'sp':2,'nm':'Said no to revenue','ev':'Declined paying customer because it violated core standard','test':'How much left on table?','produces':'a tested standard'},
        {'p':60,'ch':14,'sp':3,'nm':'Pride not compliance','ev':'Quality holds without audits — maintained because they want to','test':'Remove checks for a month','produces':'quality by pride'},
        {'p':61,'ch':15,'sp':0,'nm':'3am knowing','ev':'Senior leader woke knowing something shifted — cannot name what','test':'Can you name it?','produces':'pre-verbal awareness of the turn'},
        {'p':62,'ch':15,'sp':1,'nm':'Core vs shell','ev':'Listed everything, marked core mission vs current form','test':'How many items are shell?','produces':'a core-vs-shell inventory'},
        {'p':63,'ch':15,'sp':2,'nm':'Loss arrived','ev':'Key product/market/person lost — discovered if mission survived','test':'Did mission survive?','produces':'evidence of mission persistence'},
        {'p':64,'ch':15,'sp':3,'nm':'Farewell held','ev':'Org honoured what ended before beginning what comes next','test':'Was there a real ritual?','produces':'mission carried through form-change'},
    ]

    return d


# ═══════════════════════════════════════════
# DOMAIN: CANCER
# ═══════════════════════════════════════════

def _build_cancer_domain() -> Domain:
    d = Domain('cancer', 'Cancer', 'We are the human body being rescued from the tumour')

    d.challenges_16 = [
        {'n':1,'nm':'Disturbance','settles':'mutagenic exposure registered'},
        {'n':2,'nm':'Accumulation','settles':'driver mutations accumulated'},
        {'n':3,'nm':'Preview','settles':'pre-malignant lesion visible'},
        {'n':4,'nm':'Commitment','settles':'oncogene activation — irreversible'},
        {'n':5,'nm':'Initiation','settles':'microenvironment construction begun'},
        {'n':6,'nm':'Architecture','settles':'vascular channels established'},
        {'n':7,'nm':'Testing','settles':'immune system tests tumour — some clones fail'},
        {'n':8,'nm':'Selection','settles':'immune-resistant configuration selected'},
        {'n':9,'nm':'Output','settles':'metastasis — observable output at distant sites'},
        {'n':10,'nm':'Discovery','settles':'tumour-host interaction reveals biology'},
        {'n':11,'nm':'Integration','settles':'tumour integrates resistance to first-line'},
        {'n':12,'nm':'Equilibrium','settles':'growth-treatment equilibrium achieved'},
        {'n':13,'nm':'Differentiation','settles':'resistant and sensitive subclones differentiate'},
        {'n':14,'nm':'Surveillance','settles':'tumour surveils own state (immune evasion)'},
        {'n':15,'nm':'Compensation','settles':'tumour compensates for therapeutic pressure'},
        {'n':16,'nm':'Continuation','settles':'conservation exhausted — recurrence or transformation'},
    ]

    d.events_16 = [
        {'pos':1,'nm':'Mutagenic exposure','ev':'Tissue registers perturbation — UV, carcinogen, viral insertion, or inherited mutation','test':'Is there a known mutagenic exposure?'},
        {'pos':2,'nm':'Mutations accumulate','ev':'Driver mutations accumulate — genomic instability increases','test':'Can driver mutations be identified?'},
        {'pos':3,'nm':'Pre-malignant lesion','ev':'A visible pre-malignant configuration prefigures the tumour form','test':'Is there a visible lesion (polyp, dysplasia, DCIS)?'},
        {'pos':4,'nm':'Oncogene activation','ev':'Irreversible threshold crossed — oncogene activated, tumour suppressor lost','test':'Has a definitive oncogenic event been confirmed?'},
        {'pos':5,'nm':'Angiogenesis initiated','ev':'Microenvironment construction begins — new blood vessels recruited','test':'Is angiogenic activity detectable?'},
        {'pos':6,'nm':'Pathways established','ev':'Vascular channels and signalling pathways are established','test':'Are established signalling pathways identifiable?'},
        {'pos':7,'nm':'Immune testing','ev':'Immune system tests tumour — some clonal configurations fail','test':'Is there evidence of immune editing?'},
        {'pos':8,'nm':'Resistant clone selected','ev':'The immune-resistant configuration is selected','test':'Has the dominant clone been characterised?'},
        {'pos':9,'nm':'Metastasis appears','ev':'Tumour produces observable output at distant sites','test':'Are metastases detected on imaging?'},
        {'pos':10,'nm':'Biology revealed','ev':'Tumour-host interaction produces information that did not exist before treatment','test':'Has treatment response revealed tumour biology?'},
        {'pos':11,'nm':'Resistance integrated','ev':'Tumour integrates resistance to first-line treatment','test':'Has first-line treatment failed?'},
        {'pos':12,'nm':'Treatment equilibrium','ev':'Growth and treatment forces balance — stable disease','test':'Is the tumour in stable equilibrium?'},
        {'pos':13,'nm':'Subclones differentiate','ev':'Resistant and sensitive subclones form distinct populations','test':'Is clonal heterogeneity documented?'},
        {'pos':14,'nm':'Tumour self-surveillance','ev':'Tumour maintains immune evasion through active surveillance','test':'Are immune evasion mechanisms active?'},
        {'pos':15,'nm':'Therapeutic compensation','ev':'Tumour compensates for therapeutic pressure through alternative pathways','test':'Are resistance/bypass pathways active?'},
        {'pos':16,'nm':'Cycle turns','ev':'Conservation exhausted — tumour transforms, recurs, or seeds next cycle','test':'Has the tumour evolved past current treatment paradigm?'},
    ]

    # Cancer sub-phase vocabulary
    d.sp_nouns = {
        0: {0:'Growth factor receptor activation',1:'RTK signalling cascade',2:'Autocrine loop test',3:'Sustained mitogenic signal'},
        1: {0:'DNA damage signal',1:'Replication fork assembly',2:'Cell cycle checkpoint test',3:'Committed replication'},
        2: {0:'Neoantigen presentation signal',1:'T-cell activation structure',2:'Immune synapse encounter',3:'Immune memory settled'},
        3: {0:'Survival pathway signal',1:'Anti-apoptotic structure',2:'Drug efflux pump encounter',3:'Angiogenic maintenance settled'},
    }

    # Load agents from calibration_db.json
    d.agent_templates = _load_cancer_agents()

    return d


def _load_cancer_agents() -> List[Dict]:
    """Load cancer agent templates from calibration database."""
    db_path = Path(__file__).parent / 'calibration_db.json'
    if not db_path.exists():
        return []

    with open(db_path) as f:
        db = json.load(f)

    agents = []
    for ct_id, ct in db.get('cancer_types', {}).items():
        for a in ct.get('agents', []):
            agents.append({
                'id': f"{ct_id}_{a['id']}",
                'cancer_type': ct_id,
                'cancer_name': ct.get('name', ct_id),
                'name': a['name'],
                'potency': a.get('M', 0.5),
                'subphase': a.get('subphase', 1),
                'function': a.get('function', 'Architect').lower(),
                'action': a.get('action', ''),
                'mechanism': a.get('mechanism', ''),
                'drug_class': a.get('class', ''),
                'calibration': a.get('calibration', {}),
            })

    return agents


# ═══════════════════════════════════════════
# DOMAIN REGISTRY
# ═══════════════════════════════════════════

DOMAINS: Dict[str, Domain] = {}

def register_domain(domain: Domain):
    DOMAINS[domain.id] = domain

def get_domain(domain_id: str) -> Optional[Domain]:
    return DOMAINS.get(domain_id)

# Register built-in domains
register_domain(_build_org_domain())
register_domain(_build_cancer_domain())


# ═══════════════════════════════════════════
# L3-L4. AGENT
# ═══════════════════════════════════════════

@dataclass
class L7Agent:
    """An agent operating on the system. Not a person — a function."""
    id: int
    function: AgentFunction
    subphase: SubPhase
    potency: float           # M (0-1)
    drain: float             # D (0-1) — personal/structural drain
    position_assigned: int   # where this agent was born/assigned (1-16)
    depth: int               # fractal depth this agent operates at
    label: str               # human-readable name
    witness: str = ''        # what event was witnessed to know this agent exists
    specificity: float = 1.0
    n_non_target_cycles: int = 0
    sub_witnesses: Dict[int, str] = field(default_factory=dict)  # depth 4 witnesses

    def D_total(self) -> float:
        """Total drain including non-target cycle drain."""
        base = (1 - self.specificity) * (self.n_non_target_cycles / (self.n_non_target_cycles + 1)) if self.n_non_target_cycles > 0 else 0
        return min(0.95, base + self.drain)

    def M_eff(self, current_pos: int, obs_cascade: float = 1.0) -> float:
        return effective_potency(self.potency, self.D_total()) * overstay_factor(self.position_assigned, current_pos) * obs_cascade

    def overstay(self, current_pos: int) -> int:
        return overstay_realms(self.position_assigned, current_pos)

    def to_dict(self, current_pos: int = None) -> Dict:
        d = {
            'id': self.id, 'function': self.function.value, 'subphase': self.subphase.value,
            'potency': self.potency, 'drain': self.drain, 'D_total': round(self.D_total(), 3),
            'position_assigned': self.position_assigned, 'depth': self.depth,
            'label': self.label, 'witness': self.witness, 'specificity': self.specificity,
            'n_non_target_cycles': self.n_non_target_cycles,
            'sub_witnesses': self.sub_witnesses,
            'function_meta': FUNCTIONS[self.function],
            'subphase_meta': SUB_PHASES[self.subphase],
        }
        if current_pos is not None:
            me = self.M_eff(current_pos)
            d.update({
                'M_eff': round(me, 4),
                'overstay': self.overstay(current_pos),
                'overstay_factor': overstay_factor(self.position_assigned, current_pos),
                'pathological': me < 0,
            })
        return d


# ═══════════════════════════════════════════
# THE SEVEN LAYERS
# ═══════════════════════════════════════════

class Layer7Engine:
    """The computational engine. Takes system state, returns all seven layers."""

    def __init__(self, name: str, domain_id: str, interacting_with: str,
                 intent: str, position: int, agents: List[L7Agent] = None,
                 age: float = 0):
        self.name = name
        self.domain = get_domain(domain_id)
        self.domain_id = domain_id
        self.interacting_with = interacting_with
        self.intent = intent  # 'rescue' | 'win'
        self.position = position  # 1-16 at macro level
        self.agents = agents or []
        self.age = age

    @property
    def realm(self) -> Realm:
        return Realm((self.position - 1) // 4)

    @property
    def mode(self) -> str:
        return REALMS[self.realm]['mode']

    # ── L1. POSITION ──

    def l1_position(self) -> Dict:
        """Layer 1: Where is the system."""
        r = self.realm
        rm = REALMS[r]
        event = self.domain.event_at(self.position) if self.domain else None
        ch_idx = (self.position - 1) // 4
        challenge = self.domain.challenges_16[ch_idx] if self.domain and ch_idx < len(self.domain.challenges_16) else None

        return {
            'position': self.position,
            'position_name': POSITION_NAMES_16[self.position - 1],
            'realm': {'index': r.value, **rm},
            'challenge': challenge,
            'event': event,
            'mode': self.mode,
            'observer_births': {
                'active': [o for o in OBSERVER_BIRTHS if o['born'] <= self.position],
                'next': [o for o in OBSERVER_BIRTHS if o['born'] > self.position][:3],
                'total': len(OBSERVER_BIRTHS),
            }
        }

    # ── L2. SUB-PHASE ──

    def l2_subphase(self) -> Dict:
        """Layer 2: What is happening at this position."""
        result = {}
        for sp in SubPhase:
            agents_here = [a for a in self.agents if a.subphase == sp]
            covered = len(agents_here) > 0
            total_meff = sum(a.M_eff(self.position, self._obs_cascade()) for a in agents_here)

            result[sp.value] = {
                **SUB_PHASES[sp],
                'covered': covered,
                'total_meff': round(total_meff, 4) if covered else 0,
                'status': 'covered' if covered and total_meff > 0.3 else 'weak' if covered else 'gap',
                'agents': [a.to_dict(self.position) for a in agents_here],
                'agent_count': len(agents_here),
            }
        return result

    # ── L3. AGENTS ──

    def l3_agents(self) -> List[Dict]:
        """Layer 3: All agents and their structural position."""
        return [a.to_dict(self.position) for a in self.agents]

    # ── L4. PARAMETERS ──

    def l4_parameters(self) -> Dict:
        """Layer 4: Aggregate parameter view — drain, overstay, observer cascade."""
        cascade = self._obs_cascade()
        phase_drain = self._phase_drain()

        return {
            'observer_cascade': round(cascade, 4),
            'phase_drain': phase_drain,
            'overstayed': [
                {'agent': a.to_dict(self.position), 'realms_past': a.overstay(self.position)}
                for a in self.agents if a.overstay(self.position) >= 2
            ],
            'pathological': [
                a.to_dict(self.position) for a in self.agents if a.M_eff(self.position) < 0
            ],
        }

    # ── L5. COMBINATION ──

    def l5_combination(self) -> Dict:
        """Layer 5: Coverage × health."""
        cascade = self._obs_cascade()
        sp_scores = {}
        warnings = []
        coverage = 0

        for sp in SubPhase:
            agents_here = [a for a in self.agents if a.subphase == sp]
            if not agents_here:
                sp_scores[sp.value] = {'score': 0, 'covered': False}
                warnings.append(f'{SUB_PHASES[sp]["name"]} uncovered')
                continue

            coverage += 1
            product = 1.0
            for a in agents_here:
                e = a.M_eff(self.position, cascade)
                if e > 0:
                    product *= (1 - e)
                elif e < 0:
                    product *= (1 - e)
                    warnings.append(f'{a.label} pathological')

            score = max(0, min(1, 1 - product))
            sp_scores[sp.value] = {'score': round(score, 4), 'covered': True}

        # Overall health = product of sp scores (uncovered = 0.25 penalty)
        overall = 1.0
        for sp in SubPhase:
            v = sp_scores[sp.value]['score'] if sp_scores[sp.value]['covered'] else 0
            overall *= v if v > 0 else 0.25

        return {
            'overall_health': round(max(0, min(1, overall)), 4),
            'coverage': coverage,
            'sp_scores': sp_scores,
            'warnings': warnings,
        }

    # ── L6. MOVE ──

    def l6_move(self, n: int = 5) -> Dict:
        """Layer 6: Best next structural intervention moves."""
        current = self.l5_combination()
        candidates = []

        for fn in AgentFunction:
            for sp in SubPhase:
                # Create test agent
                test = L7Agent(
                    id=-1, function=fn, subphase=sp, potency=0.6, drain=0,
                    position_assigned=self.position, depth=2, label=f'test-{fn.value}-{sp.value}'
                )
                self.agents.append(test)
                new_health = self.l5_combination()
                self.agents.pop()

                delta = new_health['overall_health'] - current['overall_health']
                if delta > 0.0001:
                    sp_was_gap = not current['sp_scores'][sp.value]['covered']
                    candidates.append({
                        'function': fn.value,
                        'function_name': FUNCTIONS[fn]['name'],
                        'subphase': sp.value,
                        'subphase_name': SUB_PHASES[sp]['name'],
                        'delta': round(delta, 4),
                        'delta_pct': round(delta * 100, 1),
                        'new_health': new_health['overall_health'],
                        'new_coverage': new_health['coverage'],
                        'closes_gap': sp_was_gap,
                        'reason': f"Close {SUB_PHASES[sp]['name']} gap" if sp_was_gap else f"Strengthen {SUB_PHASES[sp]['name']}",
                    })

        candidates.sort(key=lambda x: x['delta'], reverse=True)

        # Gaps — structural opportunities
        gaps = [
            {'subphase': sp.value, 'name': SUB_PHASES[sp]['name'], 'principle': SUB_PHASES[sp]['principle']}
            for sp in SubPhase if not current['sp_scores'][sp.value]['covered']
        ]

        # Supportive care
        supportive = self._supportive()

        return {
            'next_moves': candidates[:n],
            'gaps': gaps,
            'supportive': supportive,
            'current_health': current['overall_health'],
            'current_coverage': current['coverage'],
        }

    # ── L7. EXECUTION ──

    def l7_execution(self, agent_id: int) -> Optional[Dict]:
        """Layer 7: Execution detail for a specific agent — depth 4."""
        agent = next((a for a in self.agents if a.id == agent_id), None)
        if not agent:
            return None

        return {
            'agent': agent.to_dict(self.position),
            'depth_4': {
                sp.value: {
                    'name': SUB_PHASES[sp]['name'],
                    'principle': SUB_PHASES[sp]['principle'],
                    'question': f"Can this agent {['detect what it needs to do','build the structure to do it','actually encounter the problem','sustain the intervention'][sp.value]}?",
                    'witness': agent.sub_witnesses.get(sp.value, ''),
                }
                for sp in SubPhase
            },
            'drain_type': FUNCTIONS[agent.function]['drain_type'],
            'execution_risk': self._execution_risk(agent),
        }

    # ── FULL STATE ──

    def full_state(self) -> Dict:
        """All seven layers + structural metadata."""
        return {
            'system': self.name,
            'domain': self.domain_id,
            'interacting_with': self.interacting_with,
            'intent': self.intent,
            'l1_position': self.l1_position(),
            'l2_subphase': self.l2_subphase(),
            'l3_agents': self.l3_agents(),
            'l4_parameters': self.l4_parameters(),
            'l5_combination': self.l5_combination(),
            'l6_move': self.l6_move(),
            'structure': {
                'realms': {r.name: REALMS[r] for r in Realm},
                'subphases': {s.name: SUB_PHASES[s] for s in SubPhase},
                'functions': {f.value: FUNCTIONS[f] for f in AgentFunction},
                'transitions': [{'from':t['from'].name,'to':t['to'].name,'phi':t['phi'],'name':t['name']} for t in TRANSITIONS],
                'position_names': POSITION_NAMES_16,
                'observer_births': OBSERVER_BIRTHS,
            },
        }

    # ── INTERNALS ──

    def _obs_cascade(self) -> float:
        md = 0
        for a in self.agents:
            if a.function == AgentFunction.OBSERVER:
                d = a.D_total() + max(0, 1 - overstay_factor(a.position_assigned, self.position)) * 0.2
                md = max(md, d)
        return max(0, 1 - md)

    def _phase_drain(self) -> Dict:
        cr = self.realm.value
        pr = (cr - 1) % 4
        trans = next((t for t in TRANSITIONS if t['from'].value == pr and t['to'].value == cr), None)
        if not trans:
            return {'d': 0, 'source': None}
        prior_agents = [a for a in self.agents if (a.position_assigned - 1) // 4 == pr]
        if not prior_agents:
            return {'d': 0, 'source': None, 'phi': trans['phi']}
        strongest = max(prior_agents, key=lambda a: a.potency)
        return {
            'd': round(strongest.potency * trans['phi'], 4),
            'source': strongest.label,
            'M': strongest.potency,
            'phi': trans['phi'],
            'transition': trans['name'],
        }

    def _supportive(self) -> List[Dict]:
        results = []
        cascade = self._obs_cascade()
        for a in self.agents:
            if a.function not in (AgentFunction.ARCHITECT, AgentFunction.CATALYST):
                continue
            if a.D_total() <= 0:
                continue
            m_before = a.M_eff(self.position, cascade)
            new_d = max(0, a.D_total() - 0.05)
            m_after = effective_potency(a.potency, new_d) * overstay_factor(a.position_assigned, self.position) * cascade
            if m_after > m_before:
                results.append({
                    'target': a.label,
                    'M_before': round(m_before, 4),
                    'M_after': round(m_after, 4),
                    'gain': round(m_after - m_before, 4),
                    'mechanism': 'Sentinel protecting conservation cycle reduces drain',
                })
        return results

    def _execution_risk(self, agent: L7Agent) -> Dict:
        os = agent.overstay(self.position)
        me = agent.M_eff(self.position, self._obs_cascade())
        risks = []
        if os >= 2:
            risks.append({'type': 'overstay', 'severity': 'critical' if os >= 3 else 'high',
                          'msg': f'{os} realms past assignment — {"actively harmful" if os >= 3 else "contributing nothing"}'})
        if agent.D_total() > 0.3:
            risks.append({'type': 'drain', 'severity': 'high',
                          'msg': f'Drain {agent.D_total():.2f} — {FUNCTIONS[agent.function]["drain_type"]}'})
        if me < 0:
            risks.append({'type': 'pathological', 'severity': 'critical',
                          'msg': 'Agent is actively harmful at current position'})
        cascade = self._obs_cascade()
        if cascade < 0.7:
            risks.append({'type': 'observer_cascade', 'severity': 'high',
                          'msg': f'Observer fear reducing all agents to {cascade:.0%} effectiveness'})
        return {'risks': risks, 'risk_count': len(risks)}


# ═══════════════════════════════════════════
# EVENT WALK (for the build-back flow)
# ═══════════════════════════════════════════

def event_walk(domain_id: str, resolution: int = 16) -> List[Dict]:
    """Return the events for binary walking. Used in the setup flow
    to find the lowest true event and determine position."""
    domain = get_domain(domain_id)
    if not domain:
        return []

    if resolution == 64 and domain.events_64:
        return domain.events_64
    return domain.events_16


def build_back(domain_id: str, position: int) -> List[Dict]:
    """Given a confirmed position, return the events from position back to 1
    for the agent population flow. Each event needs: who made this happen?"""
    domain = get_domain(domain_id)
    if not domain:
        return []

    events = domain.events_64 if domain.events_64 else domain.events_16
    # Return events from position down to 1 (reverse order for build-back)
    return [e for e in events if e.get('p', e.get('pos', 0)) <= position][::-1]


# ═══════════════════════════════════════════
# SELF-TEST
# ═══════════════════════════════════════════

if __name__ == '__main__':
    print("=== LAYER7 ENGINE TEST ===\n")

    # Test org domain
    engine = Layer7Engine(
        name='Pacmed', domain_id='org', interacting_with='Dutch hospital market',
        intent='rescue', position=10, age=72,
        agents=[
            L7Agent(1, AgentFunction.SENTINEL, SubPhase.SIGNAL, 0.9, 0.1, 5, 2, 'Founder-sentinel',
                    witness='Founder still makes every product decision'),
            L7Agent(2, AgentFunction.ARCHITECT, SubPhase.STRUCTURE, 0.7, 0.2, 8, 2, 'CTO-architect',
                    witness='CTO built the technical architecture'),
            L7Agent(3, AgentFunction.OBSERVER, SubPhase.ENCOUNTER, 0.5, 0.3, 3, 2, 'Board-observer',
                    witness='Board reviews quarterly but struggles to act on findings'),
        ]
    )

    state = engine.full_state()

    print(f"System: {state['system']} vs {state['interacting_with']}")
    print(f"Intent: {state['intent']}")
    print(f"Position: {state['l1_position']['position']} — {state['l1_position']['position_name']}")
    print(f"Realm: {state['l1_position']['realm']['sym']} {state['l1_position']['realm']['label']}")
    print(f"Mode: {state['l1_position']['mode']}")
    print(f"\nL5 Health: {state['l5_combination']['overall_health']:.1%}")
    print(f"Coverage: {state['l5_combination']['coverage']}/4")
    print(f"Warnings: {state['l5_combination']['warnings']}")
    print(f"\nL6 Next moves:")
    for m in state['l6_move']['next_moves'][:3]:
        print(f"  {m['function_name']} @ {m['subphase_name']}: +{m['delta_pct']}% — {m['reason']}")
    print(f"\nL4 Overstayed: {len(state['l4_parameters']['overstayed'])}")
    print(f"Observer cascade: {state['l4_parameters']['observer_cascade']}")
    print(f"Phase drain: {state['l4_parameters']['phase_drain']}")

    # Test cancer domain
    print("\n\n=== CANCER DOMAIN ===")
    cancer = get_domain('cancer')
    print(f"Domain: {cancer.name}")
    print(f"Perspective: {cancer.perspective}")
    print(f"16 events: {len(cancer.events_16)}")
    print(f"Agent templates: {len(cancer.agent_templates)}")
    for i, e in enumerate(cancer.events_16[:4]):
        print(f"  P{i+1}: {e['nm']} — {e['ev'][:60]}...")

    # Test available domains
    print(f"\n=== REGISTERED DOMAINS ===")
    for did, dom in DOMAINS.items():
        print(f"  {did}: {dom.name} — {len(dom.events_16)} events, {len(dom.agent_templates)} agent templates")
