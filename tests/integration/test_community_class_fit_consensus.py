"""Five-validator GLSim flow for prerequisite placement and enrollment."""

import json
from pathlib import Path

from gltest import get_contract_factory, get_validator_factory
from gltest.accounts import create_accounts
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address


GRAPH = {"nodes": [{"id": "FOUNDATION", "description": "Understand the basic tools, vocabulary, and supervised starter exercise.", "requires": []}, {"id": "INTERMEDIATE", "description": "Apply the foundation skills independently in a multi-step community project.", "requires": ["FOUNDATION"]}, {"id": "ADVANCED", "description": "Plan, troubleshoot, and evaluate an independent project using the intermediate skill set.", "requires": ["INTERMEDIATE"]}]}


def _ok(receipt):
    assert tx_execution_succeeded(receipt), json.dumps(receipt, default=str)


def _context():
    validators = get_validator_factory().batch_create_mock_validators(
        5,
        mock_llm_response={"nondet_exec_prompt": {"independently map demonstrated learning": json.dumps({"mastered_nodes": ["FOUNDATION"]})}},
    )
    return {"validators": [validator.to_dict() for validator in validators]}


def test_five_validator_mastery_offer_and_acceptance():
    instructor_account, participant_account = create_accounts(2)
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "community_class_fit.py")
    deployed = factory.deploy_contract_tx(args=[], account=instructor_account, wait_transaction_status=TransactionStatus.FINALIZED)
    _ok(deployed)
    address = extract_contract_address(deployed)
    instructor = factory.build_contract(address, account=instructor_account)
    participant = factory.build_contract(address, account=participant_account)
    pathway_id = f"{str(instructor_account.address).lower()}:WOODWORK"
    journey_id = f"{str(participant_account.address).lower()}:LEARNER-1"
    _ok(instructor.publish_pathway(args=["WOODWORK", "Community woodworking pathway", GRAPH]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(participant.open_journey(args=[pathway_id, "LEARNER-1", "The participant completed the introductory workshop, correctly named the core tools, and demonstrated the supervised starter exercise. No independent multi-step project has been completed yet."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(participant.map_mastery(args=[journey_id]).transact(transaction_context=_context(), wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(instructor.offer_class(args=[journey_id, "INTERMEDIATE"]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(participant.answer_offer(args=[journey_id, True]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    assert participant.get_journey(args=[journey_id]).call()["status"] == "ENROLLED"
