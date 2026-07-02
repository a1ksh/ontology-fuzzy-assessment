"""Load and validate the reference ontology (Section 3.2)."""
from __future__ import annotations
import json
import networkx as nx


def load_ontology(path: str) -> nx.DiGraph:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    g = nx.DiGraph()
    for c in data["concepts"]:
        g.add_node(c["id"], **c)
    for e in data["links"]:
        g.add_edge(e["src"], e["dst"])
    return g


def validate(g: nx.DiGraph) -> dict:
    """Acyclicity + coverage checks (Section 3.2)."""
    return {
        "acyclic": nx.is_directed_acyclic_graph(g),
        "n_concepts": g.number_of_nodes(),
        "n_links": g.number_of_edges(),
        "isolated": list(nx.isolates(g)),
    }


def transitive_prerequisites(g: nx.DiGraph, concept: str) -> set:
    """Indirect prerequisites via transitive closure (only immediate ones stored)."""
    return nx.ancestors(g, concept)
