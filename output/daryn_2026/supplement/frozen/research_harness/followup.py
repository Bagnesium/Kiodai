"""One separately frozen full-development evaluation using the existing Pair."""
import json
import math
from pathlib import Path

from .hashing import sha256_file
from .live import Budget
from .model_gateway import RunStopped
from .paired import ROOT, configs, estimate_pair

FREEZE = ROOT / 'research/followup_freeze_v1.json'


def preflight():
    """Local-only validation. Does not read credentials or contact a provider."""
    study = json.loads(FREEZE.read_text())
    if (study['evaluation_id'] != 'full-development-followup-v1' or study['suite'] != 'development'
            or study['repeats'] != 1 or study['order'] != ['A0', 'A1']
            or study['output_root'] != 'results/followup_v1'
            or study['proposed_budget_usd'] != 0.70):
        raise RunStopped('The frozen one-pair follow-up specification is required.')
    for name, digest in study['files'].items():
        if sha256_file(ROOT / name) != digest:
            raise RunStopped('Follow-up frozen file changed: ' + name)
    preserved = json.loads((ROOT / 'research/pilot1_preservation_v1.json').read_text())
    if sha256_file(ROOT / preserved['archive']) != preserved['archive_sha256']:
        raise RunStopped('First pilot preservation archive changed.')
    for name, digest in preserved['files'].items():
        # Original method/defense drafts are preserved inside the fixed archive;
        # later legitimate documentation edits need not block a study. The live
        # evidence and original result report remain independently protected.
        if (name.startswith('results/') or name in {'RESULTS.md', 'RESULTS.json'}) and sha256_file(ROOT / name) != digest:
            raise RunStopped('First pilot evidence changed: ' + name)
    cfgs, _ = configs('development', None, 'LIVE')
    estimate = estimate_pair(cfgs)
    if (estimate['maximum_attempts'] != study['maximum_attempts'] or
            not math.isclose(estimate['conservative_pair_estimate_usd'],
                             study['conservative_allowance_usd'], rel_tol=0, abs_tol=1e-10)):
        raise RunStopped('Recomputed allowance differs from the follow-up freeze.')
    budget = Budget(study['proposed_budget_usd'], cfgs['A0']['model']['pricing_usd_per_million_tokens'],
                    protocol_ceiling=study['proposed_budget_usd'])
    budget.require(estimate['conservative_pair_estimate_usd'])
    return study, cfgs, estimate


def authorize(study, cfgs, estimate, *, live, budget_usd, root=None):
    """Validate an explicit new opt-in, without creating files or making calls."""
    if not live:
        raise RunStopped('This new evaluation requires its own explicit --live opt-in.')
    if budget_usd != study['proposed_budget_usd']:
        raise RunStopped('Explicit --budget-usd 0.70 is required for this frozen follow-up.')
    root = Path(root or ROOT / study['output_root'])
    if root.exists():
        raise RunStopped('Follow-up output already exists. Preserve and audit it; automatic restart is forbidden.')
    budget = Budget(budget_usd, cfgs['A0']['model']['pricing_usd_per_million_tokens'],
                    protocol_ceiling=study['proposed_budget_usd'])
    budget.require(estimate['conservative_pair_estimate_usd'])
    return root, budget
