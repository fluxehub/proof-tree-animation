from manimlib.imports import *
from copy import deepcopy

from lib.proof import Spacing, ProofData, ProofScene
from lib.constants import *

proof_one = ProofData(
    nodes = [
        #1
        f"[b<B {TIMES} A>]^z",
        f"[b<B {TIMES} A>]^z",
        
        #2
        "b<A>",
        "b<B>",
        
        #3
        f"b<A {TIMES} B>",
        "",
        "",
        "b<B>",
        "b<A>",
        
        #4
        f"b<(>b<B {TIMES} A>b<)>b<{ARROW}>b<(>b<A {TIMES} B>b<)>", # Hack to split the string up so that parts can be manipulated
        f"b<B {TIMES} A>",
        
        #5
        f"b<A {TIMES} B>"
    ],
    edges = [
        (0, 2, TIMES_E_ONE),
        (1, 3, TIMES_E_ZERO),
        (2, 4, TIMES_I),
        (3, 4, TIMES_I),
        (4, 9, f"{ARROW_I}$^z$"),
        (5, 7, "assumption"),
        (6, 8, "assumption"),
        (7, 10, TIMES_I),
        (8, 10, TIMES_I),
        (9, 11, ARROW_E),
        (10, 11, ARROW_E)
    ]
)

proof_two = ProofData(
    nodes = [
        "",
        "",
        "",
        "",
        "b<B>",
        "b<A>",
        "b<B>",
        "b<A>",
        f"b<Bb<{TIMES}>b<A>",
        f"b<Bb<{TIMES}>b<A>",
        "b<A>",
        "b<B>",
        f"b<A {TIMES} B>"
    ],
    edges = [
        (0, 4, "assumption"),
        (1, 5, "assumption"),
        (2, 6, "assumption"),
        (3, 7, "assumption"),
        (4, 8, TIMES_I),
        (5, 8, TIMES_I),
        (6, 9, TIMES_I),
        (7, 9, TIMES_I),
        (8, 10, TIMES_E_ONE),
        (9, 11, TIMES_E_ZERO),
        (10, 12, TIMES_I),
        (11, 12, TIMES_I) 
    ],
)

proof_three = ProofData(
    nodes = [
        "",
        "",
        "b<A>",
        "b<B>",
        f"b<A {TIMES} B>"
    ],
    edges = [
        (0, 2, "assumption"),
        (1, 3, "assumption"),
        (2, 4, TIMES_I),
        (3, 4, TIMES_I)
    ]
)

class ProofOne(ProofScene):
    CONFIG = {
        "spacing": Spacing(regular = 0.65, orphan = 2),
        "start": proof_one,
        "end": proof_two
    }

    def construct(self):
        self.add(self.proof)
        self.BreakImplies()
        self.AnimateToTwo()
    
    def BreakImplies(self):
        implies = self.nodes[9]
        implies_left = implies.get_part_by_tex(f"B {TIMES} A")
        implies_right = implies.get_part_by_tex(f"A {TIMES} B")
        implies_sign = implies.get_part_by_tex(ARROW)
        brackets_open = implies.get_parts_by_tex("(")
        brackets_closed = implies.get_parts_by_tex(")")

        b_a_right = self.nodes[10]
        a_b_top = self.nodes[4]

        self.play(
            ApplyMethod(implies_left.move_to, b_a_right),
            ApplyMethod(implies_right.move_to, a_b_top),
            FadeOut(implies_sign),
            FadeOut(brackets_open),
            FadeOut(brackets_closed)
        )

        self.remove(implies_left)
        self.remove(implies_right)

        self.wait(1)

    def AnimateToTwo(self):
        subproof = self.proof.subproof(self.proof.nodes[10])
        subproof_copy = deepcopy(subproof)

        subproof_copy[1][1].add_updater(
            lambda text: text.next_to(subproof_copy[1][0], buff=MED_SMALL_BUFF)
        )

        out_subproof_left = self.proof_out.subproof(self.proof_out.nodes[8])
        out_subproof_right = self.proof_out.subproof(self.proof_out.nodes[9])

        a_b_top = self.nodes[4]
        a_b_bottom = self.nodes[11]
        a_b_out = self.proof_out.nodes[12]

        ba_left = self.nodes[0]
        ba_left_out = self.proof_out.nodes[8]
        ba_right = self.nodes[1]
        ba_right_out = self.proof_out.nodes[9]

        a = self.nodes[2]
        a_out = self.proof_out.nodes[10]
        b = self.nodes[3]
        b_out = self.proof_out.nodes[11]

        a_rule = self.proof.rules[a]
        a_rule_out = self.proof_out.rules[a_out]
        b_rule = self.proof.rules[b]
        b_rule_out = self.proof_out.rules[b_out]
        a_b_rule = self.proof.rules[a_b_top]
        a_b_rule_out = self.proof_out.rules[a_b_out]

        i_introduce = self.proof.rules[self.nodes[9]]
        i_eliminate = self.proof.rules[self.nodes[11]]

        self.play(
            ReplacementTransform(subproof, out_subproof_left),
            ReplacementTransform(subproof_copy, out_subproof_right),
            ReplacementTransform(a_b_top, a_b_out),
            ReplacementTransform(a_b_bottom, a_b_out),
            ReplacementTransform(ba_left, ba_left_out),
            ReplacementTransform(ba_right, ba_right_out),
            ReplacementTransform(a, a_out),
            ReplacementTransform(b, b_out),
            ReplacementTransform(a_rule, a_rule_out),
            ReplacementTransform(b_rule, b_rule_out),
            ReplacementTransform(a_b_rule, a_b_rule_out),
            FadeOut(i_introduce),
            FadeOut(i_eliminate)
        )

        self.wait(1)

class ProofTwo(ProofScene):
    CONFIG = {
        "spacing": Spacing(regular = 0.65, orphan = 2),
        "start": proof_two,
        "end": proof_three
    }

    def construct(self):
        self.add(self.proof)
        self.ABUp()
        self.AnimateToThree()

    def ABUp(self):
        a_top_left = self.nodes[5]
        b_top_left = self.nodes[4]
        a_top_right = self.nodes[7]
        b_top_right = self.nodes[6]

        a_b_left = self.nodes[8]
        a_b_right = self.nodes[9]

        a_bot_left = a_b_left.get_part_by_tex("A")
        b_bot_left = a_b_left.get_part_by_tex("B")
        a_bot_right = a_b_right.get_part_by_tex("A")
        b_bot_right = a_b_right.get_part_by_tex("B")

        times_left = a_b_left.get_part_by_tex(f"{TIMES}")
        times_right = a_b_right.get_part_by_tex(f"{TIMES}")

        self.play(
            ReplacementTransform(a_bot_left, a_top_left),
            ReplacementTransform(b_bot_left, b_top_left),
            ReplacementTransform(a_bot_right, a_top_right),
            ReplacementTransform(b_bot_right, b_top_right),
            FadeOut(times_left),
            FadeOut(times_right),
        )

        self.wait(1)

    def AnimateToThree(self):
        b_remove = self.proof.subproof(self.nodes[4])
        a_top = self.proof.subproof(self.nodes[5])
        b_top = self.proof.subproof(self.nodes[6])
        a_remove = self.proof.subproof(self.nodes[7])

        a_out_subproof = self.proof_out.subproof(self.proof_out.nodes[2])
        b_out_subproof = self.proof_out.subproof(self.proof_out.nodes[3])

        a_bot = self.nodes[10]
        b_bot = self.nodes[11]
        a_out = self.proof_out.nodes[2]
        b_out = self.proof_out.nodes[3]

        rule_left = self.proof.rules[self.nodes[8]]
        rule_right = self.proof.rules[self.nodes[9]]

        a_b = self.nodes[12]
        a_b_out = self.proof_out.nodes[4]
        rule_keep = self.proof.rules[a_b]
        rule_out = self.proof_out.rules[a_b_out]

        t_eliminate_left = self.proof.rules[self.nodes[10]]
        t_eliminate_right = self.proof.rules[self.nodes[11]]

        self.play(
            FadeOutAndShift(b_remove, LEFT),
            FadeOutAndShift(rule_left, LEFT),
            FadeOutAndShift(a_remove, RIGHT),
            FadeOutAndShift(rule_right, RIGHT),
            ReplacementTransform(a_top, a_out_subproof),
            ReplacementTransform(b_top, b_out_subproof),
            Transform(a_bot, a_out),
            Transform(b_bot, b_out),
            ReplacementTransform(a_b, a_b_out),
            ReplacementTransform(rule_keep, rule_out),
            FadeOut(t_eliminate_left),
            FadeOut(t_eliminate_right)
        )

        self.remove(a_bot, b_bot)

class DotProofOne(ProofScene):
    CONFIG = {
        "start": ProofData(
            nodes = [
                "[b<A>]^x",
                "b<B>",
                "",
                f"b<A>b<{ARROW}>b<B>",
                "b<A>",
                "b<B>"
            ],
            edges = [
                (0, 1, "assumption"),
                (1, 3, f"{ARROW_I}$^x$"),
                (2, 4, "assumption"),
                (3, 5, ARROW_E),
                (4, 5, ARROW_E)
            ]
        ),
        "end": ProofData(
            nodes = [
                "",
                "b<A>",
                "b<B>"
            ],
            edges = [
                (0, 1, "assumption"),
                (1, 2, "assumption")
            ]
        )
    }

    def construct(self):
        self.add(self.proof)
        self.ARightBUp()
        self.AnimateToEnd()
    
    def ARightBUp(self):
        full_sequent = self.nodes[3]
        a_left = full_sequent.get_part_by_tex("A")
        a_right = self.nodes[4]

        b_bot = full_sequent.get_part_by_tex("B")
        b_top = self.nodes[1]

        arrow = full_sequent.get_part_by_tex(f"{ARROW}")

        self.play(
            ReplacementTransform(a_left, a_right),
            ReplacementTransform(b_bot, b_top),
            FadeOut(arrow)
        )

        self.wait(1)

    def AnimateToEnd(self):
        a_top = self.nodes[0]
        a_bot = self.nodes[4]
        a_out = self.proof_out.nodes[1]

        b_top = self.nodes[1]
        b_bot = self.nodes[5]
        b_out = self.proof_out.nodes[2]

        a_dots = self.proof.rules[a_bot]
        a_dots_out = self.proof_out.rules[a_out]

        b_dots = self.proof.rules[b_top]
        b_dots_out = self.proof_out.rules[b_out]

        rule_one = self.proof.rules[self.nodes[3]]
        rule_two = self.proof.rules[self.nodes[5]]

        self.play(
            ReplacementTransform(a_top, a_out),
            ReplacementTransform(a_bot, a_out),
            ReplacementTransform(a_dots, a_dots_out),
            ReplacementTransform(b_top, b_out),
            ReplacementTransform(b_bot, b_out),
            ReplacementTransform(b_dots, b_dots_out),
            FadeOut(rule_one),
            FadeOut(rule_two)
        )

class DotProofTwo(ProofScene):
    CONFIG = {
        "start": ProofData(
            nodes = [
                "",
                "",
                "b<A>",
                "b<B>",
                f"b<A>b<{TIMES}>b<B>",
                "b<A>"
            ],
            edges = [
                (0, 2, "assumption"),
                (1, 3, "assumption"),
                (2, 4, f"{TIMES_I}"),
                (3, 4, f"{TIMES_I}"),
                (4, 5, f"{TIMES_E_ZERO}")
            ]
        ),
        "end": ProofData(
            nodes = [
                "",
                "b<A>"
            ],
            edges = [
                (0, 1, "assumption")
            ]
        )
    }

    def construct(self):
        self.add(self.proof)
        self.ABUp()
        self.AnimateToEnd()
    
    def ABUp(self):
        a_b = self.nodes[4]

        a_top = self.nodes[2]
        a_bot = a_b.get_part_by_tex("A")

        b_top = self.nodes[3]
        b_bot = a_b.get_part_by_tex("B")

        times = a_b.get_part_by_tex(f"{TIMES}")

        self.play(
            ReplacementTransform(a_bot, a_top),
            ReplacementTransform(b_bot, b_top),
            FadeOut(times)
        )

        self.wait(1)

    def AnimateToEnd(self):
        a_top = self.proof.subproof(self.nodes[2])
        b_top = self.proof.subproof(self.nodes[3])

        a_bot = self.nodes[5]
        a_out = self.proof_out.nodes[1]
        rule = self.proof.rules[self.nodes[4]]

        t_eliminate = self.proof.rules[self.nodes[5]]

        self.play(
            FadeOutAndShift(b_top, RIGHT),
            FadeOutAndShift(rule, RIGHT),
            ApplyMethod(a_top.center),
            Transform(a_bot, a_out),
            FadeOut(t_eliminate)
        )

        self.remove(a_bot)