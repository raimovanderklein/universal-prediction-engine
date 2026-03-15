# AXIOMS
# Universal Dissipative System Architecture
# Generative Geometry (van der Klein, 2026)
#
# Each axiom: one principle, one formula, one test.
# If the engine is lost, rebuild it from this file.

# ═══════════════════════════════════════════
# A0. THE TWO OPERATIONS
# ═══════════════════════════════════════════
#
# Every dissipative system is produced by two irreducible operations:
#   HOLD — resist separation, maintain coherence
#   CROSS — enable interaction, transform one thing into another
#
# Their combination (each latent or active) produces four regimes:
#   Δ  both latent        — potentiality
#   ᚱ  hold active        — construction
#   ᚷ  both active        — encounter
#   Σ  cross active       — conservation
#
# The regimes cycle in fixed order: Δ → ᚱ → ᚷ → Σ → Δ
# The cycle is generative: Φ > 0 (each turn produces what was not there before)
# The cycle is fractal: 4 → 16 → 64 → 256 → 1024 → 4096 at each resolution

# ═══════════════════════════════════════════
# A1. EFFECTIVE POTENCY
# ═══════════════════════════════════════════
#
# An agent operating on a system has raw potency M and conservation drain D.
# Drain reduces the agent AND strengthens the opponent.
#
# Formula:  M_eff = M × (1 − D) / (1 + D)
#
# Test: In NSCLC, D ≈ 1 − RDI. At RDI < 85%, predicted HR = 1.10.
#       Observed HR = 1.19 (CI 1.04–1.37). Within CI.

# ═══════════════════════════════════════════
# A2. FIVE AGENT FUNCTIONS
# ═══════════════════════════════════════════
#
# Every intervention on a dissipative system is one of five functions:
#
#   Sentinel   hold × same level     guards boundary
#   Miner      hold × deeper level   extracts from below
#   Architect  cross × same level    transforms at level
#   Catalyst   cross × deeper level  accelerates from below
#   Observer   surveillance loop     monitors all cycles
#
# Each function has a specific drain:
#   Sentinel   off-target holding          (prevents healthy change)
#   Miner      extraction depletion        (weakens deeper level)
#   Architect  off-target crossing         (damages healthy systems)
#   Catalyst   collateral acceleration     (accelerates resistance)
#   Observer   fear / paralysis            (monitoring replaces acting)

# ═══════════════════════════════════════════
# A3. COVERAGE BEATS POTENCY
# ═══════════════════════════════════════════
#
# Four sub-phases per position: Signal, Structure, Encounter, Conservation.
# Health = product of per-sub-phase blockades.
# An uncovered sub-phase nullifies gains from covered sub-phases.
#
# Formula:  Health = ∏(blockade_sp) for sp in [SP1, SP2, SP3, SP4]
#           blockade_sp = 1 − ∏(1 − M_eff_i) for agents i covering sp
#           uncovered sp: blockade = 0 → penalty 0.25
#
# Test: 91% of gains in drug combination therapy come from coverage, not potency.

# ═══════════════════════════════════════════
# A4. PHASE-LOCKED POTENCY → NEXT-PHASE DRAIN
# ═══════════════════════════════════════════
#
# The dominant agent's strength in one phase becomes the drain in the next.
# What built you becomes what blocks you.
#
# Formula:  D_next = M_dominant × φ
#           φ = 0.3 (same-axis transition: Δ→ᚱ, ᚷ→Σ)
#           φ = 0.6 (cross-axis transition: ᚱ→ᚷ, Σ→Δ)
#
# Test: Sentinel M=0.9 at ᚱ→ᚷ (cross-axis) → D_carryover = 0.54.
#       Predicts encounter blockage proportional to orientation strength.

# ═══════════════════════════════════════════
# A5. OBSERVER DRAIN CASCADES
# ═══════════════════════════════════════════
#
# Observer drain propagates to every subordinate agent.
# No other function has this property.
#
# Formula:  M_eff_sub = M_sub × (1−D_sub)/(1+D_sub) × (1 − D_observer)
#
# Test: Oncologist who under-doses (Observer fear) reduces all drugs'
#       effective potency regardless of drug properties.

# ═══════════════════════════════════════════
# A6. OVERSTAY PENALTY
# ═══════════════════════════════════════════
#
# An agent operating past its assigned phase loses potency and becomes harmful.
#
# Formula:  overstay_factor(realms_past) =
#             0 realms:  1.0   (full potency)
#             1 realm:   0.5   (diminishing)
#             2 realms:  0.0   (neutral — present but useless)
#             3 realms: −0.5   (pathological — actively harmful)
#
# Test: Pacmed Sentinel at position 5, org at position 35 (2 realms past)
#       → effective potency = 0. Occupies the function, contributes nothing.

# ═══════════════════════════════════════════
# A7. SUPPORTIVE CARE = POTENCY MULTIPLIER
# ═══════════════════════════════════════════
#
# A Sentinel protecting a non-target conservation cycle reduces D for the
# primary agent. This increases M_eff at the target. Supportive care is
# not a comfort measure. It is a potency multiplier.
#
# Formula:  D_new = D_old − d_per_sentinel
#           M_eff improves via A1 formula
#
# Test: G-CSF (bone marrow Sentinel) → maintains RDI → RR 0.93 for
#       all-cause mortality. Predicted RR = 0.96.

# ═══════════════════════════════════════════
# A8. COMPLEXITY FORCES ABSTRACTION
# ═══════════════════════════════════════════
#
# When internal complexity exceeds hold capacity, the system must cross
# to encounter or collapse. The threshold event is: the creator can no
# longer explain the product's value in one sentence.
#
# Formula:  if components > 4^depth → cross threshold imminent
#
# Test: The abstraction comes from the first user who tells someone else,
#       not from the creator. Explanation failure = readiness signal.

# ═══════════════════════════════════════════
# A9. LOWEST TRUE EVENT = POSITION
# ═══════════════════════════════════════════
#
# The lowest-resolution event that genuinely happened confirms everything
# above it. If a paid transaction occurred, the product shipped, was built,
# was chosen, was designed, was planned, was committed to.
#
# Formula:  position = lowest verified event
#           proof_chain = events 1 through (position − 1) confirmed
#           speed = position / age
#           lifecycle = age / fraction_complete (with deceleration)
#
# Precision: every event must have a binary test with no ambiguity.
#           "From their own resources" — not grant, not pilot, not friend.

# ═══════════════════════════════════════════
# A10. CYCLE STRESS = SPEED MISMATCH
# ═══════════════════════════════════════════
#
# Parallel cycles (founder, org, product, process) must stay within
# one realm of each other. Stress = realm gap at interface.
#
# Formula:  stress(a, b) = |realm_a − realm_b|
#           0 = aligned, 1 = tension, 2 = structural stress, 3 = critical
#
# Test: Product at ᚷ, Process at Δ (gap = 2) → "shipping faster than
#       systems sustain." Observable as quality collapse.

# ═══════════════════════════════════════════
# A11. OBSERVER FUNCTIONS BORN AT POSITIONS
# ═══════════════════════════════════════════
#
# Each Observer function is born the moment what it sustains settles.
# Cannot sustain what does not yet exist.
#
# 12 functions born at: 12, 16, 20, 28, 36, 40, 44, 48, 52, 56, 60, 64
#
# Formula:  required_observers(position) = count(birth ≤ position)
#
# Test: At position 35, four functions should be active (vision,
#       commitment, architecture, capability). If fewer are carried,
#       something that exists is not being sustained.

# ═══════════════════════════════════════════
# A12. DECELERATION
# ═══════════════════════════════════════════
#
# Later steps take longer. Conservation is heavier than construction.
# Each completed cycle adds monitoring load.
#
# Formula:  step_time(i) = base × (1 + 3 × (i/N)^1.5)
#           where N = total steps, base = full_cycle / N
#
# Test: Product creation period = Raido phase = 1/4 of full cycle.
#       Full cycle with deceleration ≈ 1.8 × nominal full cycle.
