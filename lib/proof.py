from dataclasses import dataclass
from manimlib.imports import *
from .constants import *
from typing import List, Dict, Tuple
from enum import Enum
import networkx as nx

from .sequent import Sequent

@dataclass
class Spacing():
    regular: float
    orphan: float

# Dataclass for the CONFIG data
# TypedDict isn't in 3.7
@dataclass
class ProofData:
    nodes: List[str]
    edges: List[Tuple[int, int, str]]

class Rule(VMobject):
    def __init__(self, start: List[float], end: List[float], text: TextMobject, **kwargs):
        Mobject.__init__(self, **kwargs)
        digest_config(self, kwargs)

        line = Line(start, end, color=BLACK, stroke_width=1.5)
        self.add(line)

        text.next_to(line, buff=MED_SMALL_BUFF)
        self.add(text)

        def follow_line(text: TextMobject):
            text.next_to(line, buff=MED_SMALL_BUFF)
        
        text.add_updater(follow_line)

class Assumption(TextMobject):
    def __init__(self, **kwargs):
        TextMobject.__init__(self, "$\\vdots$", color=BLACK)
        digest_config(self, kwargs)

class Proof(VMobject):
    def __init__(self, nodes: List[Sequent], edges: List[Tuple[int, int, str]], spacing: Spacing, **kwargs):
        Mobject.__init__(self, **kwargs)

        self.graph = nx.DiGraph()
        self.nodes = nodes
        self.edges = edges

        self.graph.add_nodes_from(self.nodes)

        for edge in self.edges:
            i, j, rule = edge

            if rule == "assumption":
                self.graph.add_edge(self.nodes[i], self.nodes[j], rule=Assumption())
            else:
                self.graph.add_edge(self.nodes[i], self.nodes[j], rule=TextMobject(rule, color=BLACK))
        
        self.rules: Dict[Sequent, VMobject] = {}

        if nodes != []:
            self.create(self.nodes[-1], self, spacing)

    def create(self, node: Sequent, group: VMobject, spacing: Spacing):
        # Start by adding the current node to the group (will already have position set by previous node)
        group.add(node)

        # Get all parent nodes of the current node
        parents: List[Sequent] = list(self.graph.predecessors(node))

        # If there's no parents, there's nothing to do
        if len(parents) > 0:
            # Set up variables for aligning the rule later
            rule_width = 0
            center_x = 0

            # Place parent node above the current node
            for p in parents:
                p.next_to(node, UP)
                p.shift(UP * 0.15)
                
                # Lower lines with descenders to keep alignment
                if p.get_tex_string().find("(") != -1 or p.get_tex_string().find("[") != -1 or p.get_tex_string().find("y") != -1 or p.get_tex_string().find("\\pi") != -1:
                    p.shift(DOWN*0.13)
                p.align_to(node)
            
            if len(parents) > 1:
                if len(parents) != 2:
                    print("Not implemented")
                    sys.exit()

                # We need to split the proof, calculate the width of each branch for smart splitting
                branches: List[VGroup] = []

                shift_multipliers = []

                for p in parents:
                    # Make a temporary group to store the branch so that width can be calculated
                    # This code currently means some nodes will be visited multiple times
                    # In future, optimise (although the cost is likely negligible)

                    branch = VGroup()
                    self.create(p, branch, spacing)
                    branches.append(branch)

                    p_parents: List[Sequent] = list(self.graph.predecessors(p))

                    if len(p_parents) > 0 and p_parents[0].get_tex_string() != "":
                        shift_multipliers.append(spacing.regular)
                    else:
                        shift_multipliers.append(spacing.orphan)

                # Currently this code only works for 2 parents 
                left_shift = branches[0].get_width() * shift_multipliers[0] * LEFT 
                right_shift = branches[1].get_width() * shift_multipliers[1] * RIGHT

                parents[0].shift(left_shift)
                parents[1].shift(right_shift)
                temp_box = VGroup(parents[0], parents[1])
                rule_width = max(node.get_width(), temp_box.get_width())
                center_x = temp_box.get_center()[0]

            else:
                # Only one parent, just grab the first element from the list
                parent = parents[0]

                # Calculate the width of the line based on the widest node
                # and grab the center point of the nodes
                rule_width = max(node.get_width(), parent.get_width())
                center_x = parent.get_center()[0]

            # Make the rule slightly wider than the nodes so that the line doesn't exactly match
            rule_width += 0.2

            # Get the rule text from the graph edge
            # All parents will use the same rule, so just get the rule from the first parent
            rule_text: TextMobject = self.graph.get_edge_data(parents[0], node)['rule']

            # If the rule are vertical dots, we need special alignment code
            if rule_text.get_tex_string() == "$\\vdots$":
                rule = rule_text
                rule.move_to(node, UP)
                rule.shift(UP * 0.65)
                node.move_to([rule.get_center()[0], node.get_center()[1], node.get_center()[2]])
                parent = parents[0]
                parent.shift(UP*0.5)
                if group == self:
                    self.rules[node] = rule

                group.add(rule) 
            else:
                rule = Rule(
                    [(center_x-rule_width*0.5), 0, 0], 
                    [(center_x+rule_width*0.5), 0, 0],
                    rule_text
                )

                rule[0].align_to(node, UP)
                rule[0].shift(UP*0.2)

                node.move_to([rule[0].get_center()[0], node.get_center()[1], node.get_center()[2]])
                if group == self:
                    self.rules[node] = rule

                group.add(rule)

            for p in parents:
                self.create(p, group, spacing)
            
            if group == self and len(list(self.graph.successors(node))) == 0:
                self.center()

    def search(self, group: VGroup, node: Sequent, end_node: Sequent = None):
        group.add(node)
        parents: List[Sequent] = list(self.graph.predecessors(node))

        if len(parents) > 0 and node != end_node:
            group.add(self.rules[node])
            for p in parents:
                self.search(group, p, end_node)

    def subproof(self, node: Sequent, end_node: Sequent = None, exclude: List[Sequent] = None) -> VGroup:
        subproof = VGroup()
        self.search(subproof, node, end_node)

        if exclude != None:
            for obj in subproof:
                if obj in exclude:
                    subproof.remove(obj)

        return subproof

class ProofScene(Scene):
    spacing: Spacing
    start: ProofData
    end: ProofData

    CONFIG = {
        "camera_class": Camera,
        "camera_config": {
            "background_color": WHITE
        },
    }

    def setup(self):
        nodes_in = self.start.nodes
        self.nodes = [Sequent(node) for node in nodes_in]
        self.edges = self.start.edges

        nodes_out = self.end.nodes
        self.nodes_out = [Sequent(node) for node in nodes_out]
        self.edges_out = self.end.edges

        if not hasattr(self, 'spacing'):
            self.spacing = Spacing(regular = 0.85, orphan = 2)

        self.proof = Proof(self.nodes, self.edges, self.spacing)
        self.proof_out = Proof(self.nodes_out, self.edges_out, self.spacing)