"""Direct tests for mastery mapping and mutual enrollment."""

import json


GRAPH = {
    "nodes": [
        {"id": "FOUNDATION", "description": "Understand the basic tools, vocabulary, and supervised starter exercise.", "requires": []},
        {"id": "INTERMEDIATE", "description": "Apply the foundation skills independently in a multi-step community project.", "requires": ["FOUNDATION"]},
        {"id": "ADVANCED", "description": "Plan, troubleshoot, and evaluate an independent project using the intermediate skill set.", "requires": ["INTERMEDIATE"]},
    ]
}
EVIDENCE = "The participant completed the introductory workshop, correctly named the core tools, and demonstrated the supervised starter exercise. No independent multi-step project has been completed yet."


def _pathway(contract, direct_vm, instructor):
    direct_vm.sender = instructor
    return contract.publish_pathway("WOODWORK", "Community woodworking pathway", GRAPH)


def _journey(contract, direct_vm, participant, pathway_id):
    direct_vm.sender = participant
    return contract.open_journey(pathway_id, "LEARNER-1", EVIDENCE)


def _map(contract, direct_vm, participant, journey_id, mastered):
    direct_vm.sender = participant
    direct_vm.mock_llm(
        r".*independently map demonstrated learning.*",
        json.dumps({"mastered_nodes": mastered}),
    )
    contract.map_mastery(journey_id)


def test_pathway_rejects_non_topological_graph(contract, direct_vm, direct_bob):
    direct_vm.sender = direct_bob
    bad = {"nodes": [GRAPH["nodes"][1], GRAPH["nodes"][0]]}
    with direct_vm.expect_revert("graph_must_be_topologically_ordered"):
        contract.publish_pathway("BAD", "Broken pathway graph", bad)


def test_mastery_creates_deterministic_frontier(contract, direct_vm, direct_alice, direct_bob):
    pathway_id = _pathway(contract, direct_vm, direct_bob)
    journey_id = _journey(contract, direct_vm, direct_alice, pathway_id)
    _map(contract, direct_vm, direct_alice, journey_id, ["FOUNDATION"])
    journey = contract.get_journey(journey_id)
    assert journey["mastery_mask"] == 1
    assert journey["frontier"] == ["INTERMEDIATE"]


def test_only_participant_can_map_mastery(contract, direct_vm, direct_alice, direct_bob):
    pathway_id = _pathway(contract, direct_vm, direct_bob)
    journey_id = _journey(contract, direct_vm, direct_alice, pathway_id)
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("only_participant"):
        contract.map_mastery(journey_id)


def test_instructor_offer_and_participant_acceptance_complete_flow(contract, direct_vm, direct_alice, direct_bob):
    pathway_id = _pathway(contract, direct_vm, direct_bob)
    journey_id = _journey(contract, direct_vm, direct_alice, pathway_id)
    _map(contract, direct_vm, direct_alice, journey_id, ["FOUNDATION"])
    direct_vm.sender = direct_bob
    contract.offer_class(journey_id, "INTERMEDIATE")
    direct_vm.sender = direct_alice
    contract.answer_offer(journey_id, True)
    journey = contract.get_journey(journey_id)
    assert journey["status"] == "ENROLLED"
    assert journey["offered_node"] == "INTERMEDIATE"


def test_instructor_cannot_offer_locked_node(contract, direct_vm, direct_alice, direct_bob):
    pathway_id = _pathway(contract, direct_vm, direct_bob)
    journey_id = _journey(contract, direct_vm, direct_alice, pathway_id)
    _map(contract, direct_vm, direct_alice, journey_id, ["FOUNDATION"])
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("node_not_in_frontier"):
        contract.offer_class(journey_id, "ADVANCED")


def test_mastery_must_be_prerequisite_closed(contract, direct_vm, direct_alice, direct_bob):
    pathway_id = _pathway(contract, direct_vm, direct_bob)
    journey_id = _journey(contract, direct_vm, direct_alice, pathway_id)
    direct_vm.sender = direct_alice
    direct_vm.mock_llm(
        r".*independently map demonstrated learning.*",
        json.dumps({"mastered_nodes": ["ADVANCED"]}),
    )
    with direct_vm.expect_revert("mastery_not_prerequisite_closed"):
        contract.map_mastery(journey_id)
    assert contract.get_journey(journey_id)["status"] == "OPEN"


def test_participant_may_cancel_before_terminal_state(contract, direct_vm, direct_alice, direct_bob):
    pathway_id = _pathway(contract, direct_vm, direct_bob)
    journey_id = _journey(contract, direct_vm, direct_alice, pathway_id)
    contract.cancel_journey(journey_id)
    assert contract.get_journey(journey_id)["status"] == "CANCELLED"
