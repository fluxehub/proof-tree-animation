from manimlib.imports import *
from typing import Tuple
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
        self.wait(2)
        self.BAndARightToLeftAndBack()
        top_left, top_right = self.ABCopyAndShiftUp()
        self.AAndBDown()
        self.AnimateToTwo(top_left, top_right)

    def BAndARightToLeftAndBack(self):
        full_sequent = self.proof.nodes[9]
        b_a_left = full_sequent[1]
        b_a_right = self.proof.nodes[10]
        b_a_right.generate_target()
        self.play(ApplyMethod(b_a_right.move_to, b_a_left))
        self.remove(b_a_left)
        full_sequent.remove(b_a_left)
        self.wait(1)

        self.play(MoveToTarget(b_a_right))
        self.wait(1)

    def ABCopyAndShiftUp(self) -> Tuple[VGroup, VGroup]:
        subproof = self.proof.subproof(self.proof.nodes[10])
        subproof.generate_target()

        subproof.target.move_to(self.proof.nodes[0])
        subproof.target.shift(0.7 * UP + 0.47 * RIGHT)
        
        subproof_copy = deepcopy(subproof)

        subproof_copy[1][1].add_updater(
            lambda text: text.next_to(subproof_copy[1][0], buff=MED_SMALL_BUFF)
        )

        subproof_copy.generate_target()
        self.add(subproof_copy)

        subproof_copy.target.move_to(self.proof.nodes[1])
        subproof_copy.target.shift(0.7 * UP + 0.47 * RIGHT)

        old_top_left = self.proof.nodes[0]
        old_top_right = self.proof.nodes[1]

        self.play(
            MoveToTarget(subproof),
            MoveToTarget(subproof_copy),
        )

        self.remove(old_top_left)
        self.remove(old_top_right)

        self.wait(1)

        return (subproof, subproof_copy)

    def AAndBDown(self):
        a_b = self.proof.nodes[6]
        a_b.generate_target()

        full_sequent = self.proof.nodes[9]
        a_b_two = full_sequent.get_part_by_tex(f"A {TIMES} B")
        a_b_two_rule = self.proof.rules[full_sequent]
        a_b_three = self.proof.nodes[11]
        a_b_three_rule = self.proof.rules[a_b_three]

        self.play(ApplyMethod(a_b.move_to, a_b_two))
        self.remove(a_b_two)
        full_sequent.remove(a_b_two)
        self.wait(1)

        self.play(
            FadeOut(full_sequent),
            FadeOut(a_b_two_rule),
            ApplyMethod(a_b.move_to, a_b_three)
        )

        self.remove(a_b_three)
        
        self.wait(1)

        self.play(
            FadeOut(a_b_three_rule),
            FadeToColor(a_b, "#2681ff")
        )

    def AnimateToTwo(self, top_left: VGroup, top_right: VGroup):
        a = self.proof.nodes[2]
        a_out = self.proof_out.nodes[10]
        b = self.proof.nodes[3]
        b_out = self.proof_out.nodes[11]
        a_b = self.proof.nodes[4]
        a_b_out = self.proof_out.nodes[12]

        a_rule = self.proof.rules[a]
        a_rule_out = self.proof_out.rules[a_out]
        b_rule = self.proof.rules[b]
        b_rule_out = self.proof_out.rules[b_out]
        a_b_rule = self.proof.rules[a_b]
        a_b_rule_out = self.proof_out.rules[a_b_out]

        top_left_out = self.proof_out.subproof(self.proof_out.nodes[8])
        top_right_out = self.proof_out.subproof(self.proof_out.nodes[9])

        # I have to animate each element of the subproof separately because it didn't work otherwise
        top_left_ab = VGroup(*top_left[2:])
        top_left_rule = top_left[1]
        top_left_a_b = top_left[0]
        top_right_ab = VGroup(*top_right[2:])
        top_right_rule = top_right[1]
        top_right_a_b = top_right[0]
        
        top_left_ab_out = VGroup(*top_left_out[2:])
        top_left_rule_out = top_left_out[1]
        top_left_a_b_out = top_left_out[0]
        top_right_ab_out = VGroup(*top_right_out[2:])
        top_right_rule_out = top_right_out[1]
        top_right_a_b_out = top_right_out[0]

        self.play(
            ApplyMethod(a.move_to, a_out),
            ApplyMethod(b.move_to, b_out),
            ApplyMethod(a_b.move_to, a_b_out),
            ApplyMethod(top_left_ab.move_to, top_left_ab_out),
            ApplyMethod(top_right_ab.move_to, top_right_ab_out),
            ApplyMethod(top_left_a_b.move_to, top_left_a_b_out),
            ApplyMethod(top_right_a_b.move_to, top_right_a_b_out),
            Transform(top_left_rule, top_left_rule_out),
            Transform(top_right_rule, top_right_rule_out),
            Transform(a_rule, a_rule_out),
            Transform(b_rule, b_rule_out),
            Transform(a_b_rule, a_b_rule_out),
        )

        self.wait(2)

class ProofTwo(ProofScene):
    CONFIG = {
        "spacing": Spacing(regular = 0.65, orphan = 2),
        "start": proof_two,
        "end": proof_three
    }

    def construct(self):
        self.add(self.proof)
        self.wait(2)
        self.ABDown()
        self.AnimateToThree()

    def ABDown(self):
        a_top = self.proof.nodes[5]
        a_bottom = self.proof.nodes[10]

        b_top = self.proof.nodes[6]
        b_bottom = self.proof.nodes[11]

        a_top.generate_target()
        a_top.target.move_to(a_bottom)

        b_top.generate_target()
        b_top.target.move_to(b_bottom)

        self.play(MoveToTarget(a_top), MoveToTarget(b_top))
        self.proof.remove(a_bottom)
        self.proof.remove(b_bottom)
        self.wait(2)

    def AnimateToThree(self):
        a = self.proof.nodes[5]
        b = self.proof.nodes[6]
        a_b = self.proof.nodes[12]

        rule = self.proof.rules[a_b]

        out_a = self.proof_out.nodes[0]
        out_b = self.proof_out.nodes[1]
        out_a_b = self.proof_out.nodes[2]
        
        out_rule = self.proof_out.rules[out_a_b]

        remove_left = self.proof.subproof(
            self.proof.nodes[10],
            exclude = [
                a,
                self.proof.nodes[10], # Node was already removed in previous animation so don't add it back in
            ]
        )

        remove_right = self.proof.subproof(
            self.proof.nodes[11],
            exclude = [
                b,
                self.proof.nodes[11], # Node was already removed in previous animation so don't add it back in
            ]
        )

        self.play(
            FadeOutAndShift(remove_left, LEFT),
            FadeOutAndShift(remove_right, RIGHT)
        )

        self.play(
            ApplyMethod(a.move_to, out_a), 
            ApplyMethod(b.move_to, out_b),
            ApplyMethod(a_b.move_to, out_a_b),
            Transform(rule, out_rule)
        )

        self.wait(2)

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
        self.wait(1)
        self.ShiftRightAndBack()
        self.ShiftAUp()
        self.ShiftBDown()
        self.AnimateToEnd()

    def ShiftRightAndBack(self):
        left_a = self.nodes[3].get_part_by_tex("A")
        right_a = self.nodes[4]
        right_a.generate_target()

        self.play(ApplyMethod(right_a.move_to, left_a))
        self.wait(1)
        self.remove(left_a)
        self.play(MoveToTarget(right_a))
        self.wait(1)
    
    def ShiftAUp(self):
        top_a_full = self.nodes[0]
        top_a = top_a_full.get_part_by_tex("A")
        bottom_a = self.nodes[4]
        bottom_a_dots = self.proof.rules[bottom_a]
        full_bottom = VGroup(bottom_a, bottom_a_dots)

        full_bottom.generate_target()
        full_bottom.target.move_to(top_a)
        full_bottom.target.shift(UP * 0.29)

        self.play(MoveToTarget(full_bottom))
        top_a_full.remove(top_a)
        self.play(FadeOut(top_a_full))
        self.play(ApplyMethod(full_bottom.shift, 0.1 * RIGHT))
        self.wait(1)

    def ShiftBDown(self):
        top_b = self.nodes[1]
        full_middle = self.nodes[3]
        middle_b = self.nodes[3].get_part_by_tex("B")
        middle_b_rule = self.proof.rules[full_middle]
        bottom_b = self.nodes[5]

        self.play(ApplyMethod(top_b.move_to, middle_b))
        self.wait(1)
        self.remove(middle_b)
        self.play(
            ApplyMethod(top_b.move_to, bottom_b), 
            FadeOut(full_middle[1]),
            FadeOut(middle_b_rule)
        )
        self.remove(bottom_b)
        self.wait(1)

    def AnimateToEnd(self):
        a = self.nodes[4]
        a_rule = self.proof.rules[a]
        b = self.nodes[1]
        b_rule = self.proof.rules[b]

        a_out = self.nodes_out[1]
        a_out_rule = self.proof_out.rules[a_out]
        b_out = self.nodes_out[2]
        b_out_rule = self.proof_out.rules[b_out]

        bottom_rule = self.proof.rules[self.nodes[5]]

        self.play(
            ApplyMethod(a.move_to, a_out),
            ApplyMethod(b.move_to, b_out),
            ApplyMethod(a_rule.move_to, a_out_rule),
            ApplyMethod(b_rule.move_to, b_out_rule),
            FadeOut(bottom_rule)
        )

        self.wait(1)

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
        self.wait(2)
        self.ADown()
        self.AnimateToEnd()

    def ADown(self):
        a_top = self.proof.nodes[2]
        middle = self.proof.nodes[4]
        a_mid = middle[0]
        a_bot = self.proof.nodes[5]

        self.play(a_top.move_to, a_mid)
        middle.remove(a_mid)
        self.wait(1)
        
        self.play(a_top.move_to, a_bot)
        self.remove(a_bot)
        self.wait(1)

    def AnimateToEnd(self):
        top_b = self.proof.nodes[3]
        top_b_dots = self.proof.rules[top_b]

        middle = self.proof.nodes[4]
        mid_rule = self.proof.rules[middle]

        bot_a = self.proof.nodes[5]
        bot_rule = self.proof.rules[bot_a]

        remove = VGroup(
            top_b,
            top_b_dots,
            middle,
            mid_rule,
            bot_rule
        )

        a = self.proof.nodes[2]
        a_dots = self.proof.rules[a]

        a_out = self.proof_out.nodes[1]
        a_out_dots = self.proof_out.rules[a_out]

        self.play(
            FadeOutAndShift(remove, RIGHT),
            ApplyMethod(a.move_to, a_out),
            ApplyMethod(a_dots.move_to, a_out_dots)
        )

        self.wait(1)