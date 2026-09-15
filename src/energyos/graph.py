"""Energy graph primitives.

CONTRACT (not implementation theater):
- Nodes hold measured/estimated state in one energy domain.
- Edges are conversions or transfers. Efficiency and parasitics are
  first-class, never hidden inside a coupling matrix coefficient.
- No energy is created. External source nodes inject energy from
  the environment. All other nodes only store, convert, or consume.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class Domain(str, Enum):
    ELECTRICAL = "electrical"
    THERMAL = "thermal"
    MECHANICAL = "mechanical"
    ENVIRONMENT = "environment"


class NodeKind(str, Enum):
    SOURCE = "source"
    STORAGE = "storage"
    LOAD = "load"
    BUS = "bus"
    SINK = "sink"  # curtailment / loss to ambient


@dataclass
class Node:
    id: str
    domain: Domain
    kind: NodeKind
    capacity_j: float = 0.0
    energy_j: float = 0.0
    p_available_w: float = 0.0
    p_max_charge_w: float = 0.0
    p_max_discharge_w: float = 0.0
    p_idle_parasitic_w: float = 0.0
    eta_charge: float = 1.0
    eta_discharge: float = 1.0
    self_discharge_frac_per_s: float = 0.0
    t_k: Optional[float] = None
    safe: bool = True
    notes: str = ""

    @property
    def soc(self) -> float:
        if self.capacity_j <= 0:
            return 0.0
        return max(0.0, min(1.0, self.energy_j / self.capacity_j))

    @property
    def headroom_j(self) -> float:
        return max(0.0, self.capacity_j - self.energy_j)


@dataclass
class Edge:
    id: str
    src: str
    dst: str
    eta: float
    parasitic_w: float = 0.0
    p_max_w: float = float("inf")
    enabled: bool = True
    min_net_w: float = 0.0
    notes: str = ""


@dataclass
class GraphState:
    nodes: dict[str, Node] = field(default_factory=dict)
    edges: dict[str, Edge] = field(default_factory=dict)

    def node(self, nid: str) -> Node:
        return self.nodes[nid]

    def add(self, obj: Node | Edge) -> None:
        if isinstance(obj, Node):
            if obj.id in self.nodes:
                raise ValueError(f"duplicate node {obj.id}")
            self.nodes[obj.id] = obj
        else:
            if obj.id in self.edges:
                raise ValueError(f"duplicate edge {obj.id}")
            self.edges[obj.id] = obj
