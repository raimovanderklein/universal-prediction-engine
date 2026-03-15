"""
LAYER7 — Flask API
Universal Dissipative System Tool
Generative Geometry (van der Klein, 2026)

The loop: HOLD (L1-L5) → MOVE (L6) → LAUNCH (L7) → observe → HOLD again.
Every endpoint returns computed state. Frontend is display only.
"""

from flask import Flask, jsonify, request, send_from_directory
from flask.json.provider import DefaultJSONProvider
from enum import Enum
import os
import json

from layer7 import (
    Layer7Engine, L7Agent, Domain,
    AgentFunction, SubPhase, Realm,
    REALMS, SUB_PHASES, FUNCTIONS, TRANSITIONS, OBSERVER_BIRTHS,
    POSITION_NAMES_16, DOMAINS,
    event_walk, build_back, get_domain,
    effective_potency, overstay_factor,
)

class CustomJSON(DefaultJSONProvider):
    def default(self, o):
        if isinstance(o, Enum):
            return o.value
        return super().default(o)

app = Flask(__name__, static_folder='static', template_folder='templates')
app.json_provider_class = CustomJSON
app.json = CustomJSON(app)


# ═══════════════════════════════════════════
# PAGES
# ═══════════════════════════════════════════

@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

@app.route('/layer7')
def layer7_page():
    return send_from_directory('static', 'layer7.html')


# ═══════════════════════════════════════════
# SETUP
# ═══════════════════════════════════════════

@app.route('/api/l7/domains')
def api_domains():
    """Available domains with their metadata."""
    return jsonify([d.to_dict() for d in DOMAINS.values()])

@app.route('/api/l7/events/<domain_id>')
def api_events(domain_id):
    """Event walk for binary position-finding. resolution=16|64"""
    res = int(request.args.get('resolution', 16))
    events = event_walk(domain_id, res)
    return jsonify(events)

@app.route('/api/l7/build-back/<domain_id>/<int:position>')
def api_build_back(domain_id, position):
    """Events from current position back to 1 for agent population."""
    events = build_back(domain_id, position)
    return jsonify(events)

@app.route('/api/l7/agent-templates/<domain_id>')
def api_agent_templates(domain_id):
    """Available agent templates for a domain (e.g. drugs for cancer)."""
    domain = get_domain(domain_id)
    if not domain:
        return jsonify([])
    sp = request.args.get('sp')
    if sp is not None:
        return jsonify(domain.agents_for_sp(int(sp)))
    return jsonify(domain.agent_templates)


# ═══════════════════════════════════════════
# THE LOOP: HOLD → MOVE → LAUNCH
# ═══════════════════════════════════════════

@app.route('/api/l7/hold', methods=['POST'])
def api_hold():
    """HOLD: L1-L5. Understand the system.
    POST: {
        "name": "Pacmed",
        "domain": "org",
        "interacting_with": "Dutch hospital market",
        "intent": "rescue",
        "position": 10,
        "age": 72,
        "agents": [
            {"id":1, "function":"sentinel", "subphase":0, "potency":0.9,
             "drain":0.1, "position_assigned":5, "depth":2,
             "label":"Founder-sentinel", "witness":"Still makes every decision"}
        ]
    }
    Returns: L1-L5 computed state.
    """
    data = request.get_json()
    engine = _build_engine(data)
    return jsonify({
        'l1_position': engine.l1_position(),
        'l2_subphase': engine.l2_subphase(),
        'l3_agents': engine.l3_agents(),
        'l4_parameters': engine.l4_parameters(),
        'l5_combination': engine.l5_combination(),
        'mode': engine.mode,
    })

@app.route('/api/l7/move', methods=['POST'])
def api_move():
    """MOVE: L6. Best next structural interventions.
    Same input as hold. Returns move recommendations.
    """
    data = request.get_json()
    engine = _build_engine(data)
    n = int(request.args.get('n', 5))
    return jsonify(engine.l6_move(n))

@app.route('/api/l7/launch', methods=['POST'])
def api_launch():
    """LAUNCH: L7. Execution detail for a specific agent.
    Same input as hold + agent_id in query.
    """
    data = request.get_json()
    engine = _build_engine(data)
    agent_id = int(request.args.get('agent_id', 0))
    result = engine.l7_execution(agent_id)
    if result is None:
        return jsonify({'error': 'Agent not found'}), 404
    return jsonify(result)

@app.route('/api/l7/full', methods=['POST'])
def api_full():
    """Full state: all seven layers + structural metadata.
    The one call the frontend makes on every render.
    """
    data = request.get_json()
    engine = _build_engine(data)
    return jsonify(engine.full_state())


# ═══════════════════════════════════════════
# FORMULA CALCULATOR
# ═══════════════════════════════════════════

@app.route('/api/l7/formula')
def api_formula():
    """M_eff = M × (1−D)/(1+D). Quick calculator."""
    M = float(request.args.get('M', 0.5))
    D = float(request.args.get('D', 0.1))
    return jsonify({
        'M': M, 'D': D,
        'M_eff': round(effective_potency(M, D), 4),
        'overstay_factor': overstay_factor(
            int(request.args.get('assigned', 1)),
            int(request.args.get('current', 1))
        ),
    })


# ═══════════════════════════════════════════
# STRUCTURE (reference data)
# ═══════════════════════════════════════════

@app.route('/api/l7/structure')
def api_structure():
    """All structural constants. Fetched once on page load."""
    return jsonify({
        'realms': {r.name: REALMS[r] for r in Realm},
        'subphases': {s.name: SUB_PHASES[s] for s in SubPhase},
        'functions': {f.value: FUNCTIONS[f] for f in AgentFunction},
        'transitions': [
            {'from': t['from'].name, 'to': t['to'].name,
             'phi': t['phi'], 'name': t['name'], 'type': t['type']}
            for t in TRANSITIONS
        ],
        'position_names': POSITION_NAMES_16,
        'observer_births': OBSERVER_BIRTHS,
    })


# ═══════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════

def _build_engine(data: dict) -> Layer7Engine:
    """Build engine from POST data."""
    agents = []
    for a in data.get('agents', []):
        agents.append(L7Agent(
            id=a.get('id', 0),
            function=AgentFunction(a.get('function', 'sentinel')),
            subphase=SubPhase(a.get('subphase', 0)),
            potency=a.get('potency', 0.5),
            drain=a.get('drain', 0.0),
            position_assigned=a.get('position_assigned', 1),
            depth=a.get('depth', 2),
            label=a.get('label', ''),
            witness=a.get('witness', ''),
            specificity=a.get('specificity', 1.0),
            n_non_target_cycles=a.get('n_non_target_cycles', 0),
            sub_witnesses=a.get('sub_witnesses', {}),
        ))

    return Layer7Engine(
        name=data.get('name', 'System'),
        domain_id=data.get('domain', 'org'),
        interacting_with=data.get('interacting_with', ''),
        intent=data.get('intent', 'rescue'),
        position=data.get('position', 1),
        agents=agents,
        age=data.get('age', 0),
    )


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
