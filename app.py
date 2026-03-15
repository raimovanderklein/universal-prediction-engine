"""Universal Dissipative System Architecture — Web API"""
from flask import Flask, jsonify, request, send_from_directory
from flask.json.provider import DefaultJSONProvider
import os
from architecture import (System, Agent, AgentFunction, SubPhase, Realm,
                          REALM_META, SP_META, FN_META, TRANSITIONS,
                          CHALLENGES, OBSERVER_BIRTHS, ACTIONS, STRATEGIES,
                          effective_potency)
from enum import Enum

class CustomJSON(DefaultJSONProvider):
    def default(self, o):
        if isinstance(o, Enum):
            return o.value
        return super().default(o)

app = Flask(__name__, static_folder='static', template_folder='templates')
app.json_provider_class = CustomJSON
app.json = CustomJSON(app)

@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

# ── STRUCTURE (reference data) ──

@app.route('/api/structure')
def api_structure():
    """All structural metadata — realms, sub-phases, functions, transitions, challenges, observer births."""
    return jsonify({
        'realms': {r.name: REALM_META[r] for r in Realm},
        'subphases': {s.name: SP_META[s] for s in SubPhase},
        'functions': {f.value: FN_META[f] for f in AgentFunction},
        'transitions': {f'{a.name}_to_{b.name}': v for (a,b), v in TRANSITIONS.items()},
        'challenges': [{'n':c['n'],'nm':c['nm'],'realm':c['r'].name,'settles':c['settles'],
                        'org':c['org'],'cancer':c['cancer'],'climate':c['climate']} for c in CHALLENGES],
        'observer_births': OBSERVER_BIRTHS,
        'actions': {r.name: {s.name: ACTIONS[r][s] for s in SubPhase} for r in Realm},
        'strategies': STRATEGIES,
    })

# ── HOLD MODE (diagnose) ──

@app.route('/api/diagnose', methods=['POST'])
def api_diagnose():
    """HOLD mode. Send system config, get full diagnosis.
    POST: {
      "name": "Pacmed", "domain": "organisation", "position": 35, "age": 72,
      "agents": [{"function":"sentinel","potency":0.9,"subphase":0,"position_assigned":5,"label":"Founder"}],
      "parallel_cycles": {"founder":{"position":45},"product":{"position":35}}
    }"""
    data = request.get_json()
    sys = _build_system(data)
    return jsonify(sys.diagnose())

# ── CROSS MODE (intervene) ──

@app.route('/api/intervene', methods=['POST'])
def api_intervene():
    """CROSS mode. Same input, get intervention recommendations."""
    data = request.get_json()
    sys = _build_system(data)
    return jsonify(sys.intervene())

# ── FULL FRONTEND STATE ──

@app.route('/api/frontend', methods=['POST'])
def api_frontend():
    """Both modes + structural metadata. Everything the UI needs."""
    data = request.get_json()
    sys = _build_system(data)
    return jsonify(sys.frontend())

# ── FORMULA CALCULATOR ──

@app.route('/api/formula')
def api_formula():
    """A1. M_eff = M × (1-D)/(1+D). Quick calculator."""
    M = float(request.args.get('M', 0.5))
    D = float(request.args.get('D', 0.1))
    return jsonify({'M': M, 'D': D, 'M_eff': round(effective_potency(M, D), 4)})

# ── HELPERS ──

def _build_system(data: dict) -> System:
    agents = []
    for a in data.get('agents', []):
        agents.append(Agent(
            function=AgentFunction(a.get('function', 'sentinel')),
            potency=a.get('potency', 0.5),
            subphase=SubPhase(a.get('subphase', 0)),
            position_assigned=a.get('position_assigned', 1),
            specificity=a.get('specificity', 1.0),
            label=a.get('label', ''),
            n_non_target_cycles=a.get('n_non_target_cycles', 0),
            personal_drain=a.get('personal_drain', 0.0),
        ))

    parallel = {}
    for name, cyc in data.get('parallel_cycles', {}).items():
        parallel[name] = System(name=name, domain=data.get('domain', ''), position=cyc.get('position', 1))

    return System(
        name=data.get('name', 'System'),
        domain=data.get('domain', 'unknown'),
        position=data.get('position', 1),
        age=data.get('age', 0),
        agents=agents,
        parallel_cycles=parallel,
    )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
