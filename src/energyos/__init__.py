"""EnergyOS core — measurement-first multi-domain energy arbitration."""

__version__ = "0.1.0"

from .controller import BaselineController, NetBenefitController, stirling_electrical_efficiency
from .graph import Domain, Edge, GraphState, Node, NodeKind
from .simulate import SCENARIOS, campaign, run

__all__ = [
    "BaselineController",
    "NetBenefitController",
    "stirling_electrical_efficiency",
    "Domain",
    "Edge",
    "GraphState",
    "Node",
    "NodeKind",
    "SCENARIOS",
    "campaign",
    "run",
]
