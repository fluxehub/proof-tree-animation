from re import sub
from manimlib.imports import *
from copy import deepcopy

from lib.sequent import Sequent
from lib.proof import Proof, Spacing, ProofData, ProofScene
from lib.constants import *

proof_one = ProofData(
    nodes = [
        #1
        f"r<z:>b<B {TIMES} A>",
        f"r<z:>b<B {TIMES} A>",
        
        #2
        f"r<{SND} z:>b<A>",
        f"r<{FST} z:>b<B>",
        
        #3 
        f"r<({SND} z, {FST} z):>b<A {TIMES} B>",
        "",
        "",
        "r<N:>b<B>",
        "r<M:>b<A>",
        
        #4
        f"r<\\lambda z{FUNC_ARROW} ({SND} z, {FST} z):>b<(>b<B {TIMES} A>b<)>b<{ARROW}>b<(>b<A {TIMES} B>b<)>", # Hack to split the string up so that parts can be manipulated
        f"r<(N,M):>b<B {TIMES} A>",
        
        #5
        f"r<(\\lambda z{FUNC_ARROW}({SND} z, {FST} z)) (M,N):>b<A {TIMES} B>"
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

proof_one_intermediate = ProofData(
    nodes = [
        "",
        "",
        "",
        "",
        "r<N:>b<B>",
        "r<M:>b<A>",
        "r<N:>b<B>",
        "r<M:>b<A>",
        f"r<(N,M):>b<B {TIMES} A>",
        f"r<(N,M):>b<B {TIMES} A>",
        f"r<{SND} (N,M):>b<A>",
        f"r<{FST} (N,M):>b<B>",
        f"r<({SND} (N,M), {FST} (N,M)):>b<A {TIMES} B>",
        f"r<\\lambda z{FUNC_ARROW} ({SND} z, {FST} z):>b<(\\qquad)>b<{ARROW}>b<(>b<A {TIMES} B>b<)>",
        f"r<(\\lambda z{FUNC_ARROW}({SND} z, {FST} z)) (M,N):>b<A {TIMES} B>"
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
        (11, 12, TIMES_I),
        (12, 13, f"{ARROW_I}$^z$"),
        (13, 14, ARROW_E)
    ],
)

proof_two = ProofData(
    nodes = [
        "",
        "",
        "",
        "",
        "r<N:>b<B>",
        "r<M:>b<A>",
        "r<N:>b<B>",
        "r<M:>b<A>",
        f"r<(N,M):>b<B>b<{TIMES}>b<A>",
        f"r<(N,M):>b<B>b<{TIMES}>b<A>",
        f"r<{SND} (N,M):>b<A>",
        f"r<{FST} (N,M):>b<B>",
        f"r<({SND} (N,M), {FST} (N,M)):>b<A {TIMES} B>"
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
        (11, 12, TIMES_I),
    ],
)

proof_three = ProofData(
    nodes = [
        "",
        "",
        "r<M:>b<A>",
        "r<N:>b<B>",
        f"r<(M, N):>b<A {TIMES} B>"
    ],
    edges = [
        (0, 2, "assumption"),
        (1, 3, "assumption"),
        (2, 4, TIMES_I),
        (3, 4, TIMES_I)
    ]
)

class TypedProofOne(ProofScene):
    CONFIG = {
        "start": proof_one,
        "end": proof_two
    }

    def construct(self):
        self.add(self.proof)
        self.wait(1)
        self.BAndARightToLeftAndBack()
        intermediate = self.ABCopyAndTransform()
        self.AAndBDown(intermediate)

    def BAndARightToLeftAndBack(self):
        full_sequent = self.nodes[11]
        b_a_left = full_sequent.get_part_by_tex(f"B {TIMES} A")
        b_a_right = self.nodes[12].get_part_by_tex(f"B {TIMES} A")
        b_a_right.generate_target()
        self.play(ApplyMethod(b_a_right.move_to, b_a_left))
        self.remove(b_a_left)
        full_sequent.remove(b_a_left)
        self.wait(1)

        self.play(MoveToTarget(b_a_right))
        self.wait(1)

    def ABCopyAndTransform(self) -> Proof:
        intermediate = Proof([Sequent(node) for node in proof_one_intermediate.nodes], proof_one_intermediate.edges, self.spacing)

        subproof = self.proof.subproof(self.proof.nodes[12])
        subproof.generate_target()
        intermediate_sub_left = intermediate.subproof(intermediate.nodes[8])

        subproof_copy = deepcopy(subproof)

        subproof_copy[1][1].add_updater(
            lambda text: text.next_to(subproof_copy[1][0], buff=MED_SMALL_BUFF)
        )

        subproof_copy.generate_target()
        intermediate_sub_right = intermediate.subproof(intermediate.nodes[9])
        self.add(subproof_copy)

        transform_a = self.nodes[4]
        a_rule = self.proof.rules[transform_a]
        intermediate_a = intermediate.nodes[10]
        intermediate_a_rule = intermediate.rules[intermediate_a]

        transform_b = self.nodes[5]
        b_rule = self.proof.rules[transform_b]
        intermediate_b = intermediate.nodes[11]
        intermediate_b_rule = intermediate.rules[intermediate_b]

        transform_a_b = self.nodes[6]
        a_b_rule = self.proof.rules[transform_a_b]
        intermediate_a_b = intermediate.nodes[12]
        intermediate_a_b_rule = intermediate.rules[intermediate_a_b]

        transform_implies = self.nodes[11]
        implies_rule = self.proof.rules[transform_implies]
        intermediate_implies = intermediate.nodes[13]
        intermediate_implies_rule = intermediate.rules[intermediate_implies]

        transform_a_b_two = self.nodes[13]
        a_b_two_rule = self.proof.rules[transform_a_b_two]
        intermediate_a_b_two = intermediate.nodes[14]
        intermediate_a_b_two_rule = intermediate.rules[intermediate_a_b_two]

        self.play(
            FadeOutAndShift(self.nodes[2], LEFT),
            FadeOutAndShift(self.nodes[3], RIGHT),
            FadeOutAndShift(self.proof.rules[self.nodes[2]], LEFT),
            FadeOutAndShift(self.proof.rules[self.nodes[3]], RIGHT),
            ReplacementTransform(subproof, intermediate_sub_left),
            ReplacementTransform(subproof_copy, intermediate_sub_right),
            ReplacementTransform(transform_a, intermediate_a),
            ReplacementTransform(transform_b, intermediate_b),
            ReplacementTransform(a_rule, intermediate_a_rule),
            ReplacementTransform(b_rule, intermediate_b_rule),
            ReplacementTransform(transform_a_b, intermediate_a_b),
            ReplacementTransform(a_b_rule, intermediate_a_b_rule),
            ReplacementTransform(transform_implies, intermediate_implies),
            ReplacementTransform(implies_rule, intermediate_implies_rule),
            ReplacementTransform(transform_a_b_two, intermediate_a_b_two),
            ReplacementTransform(a_b_two_rule, intermediate_a_b_two_rule)
        )

        self.wait(2)

        return intermediate 

    def AAndBDown(self, intermediate: Proof):
        a_b = intermediate.nodes[12].get_part_by_tex(f"A {TIMES} B")

        full_sequent = intermediate.nodes[13]
        a_b_two = full_sequent.get_part_by_tex(f"A {TIMES} B")
        a_b_two_rule = intermediate.rules[full_sequent]
        a_b_three = intermediate.nodes[14].get_part_by_tex(f"A {TIMES} B")
        a_b_three_rule = intermediate.rules[intermediate.nodes[14]]

        self.play(ApplyMethod(a_b.move_to, a_b_two))
        full_sequent.remove(a_b_two)
        self.wait(1)

        self.play(
            FadeOut(full_sequent),
            FadeOut(a_b_two_rule),
            ApplyMethod(a_b.move_to, a_b_three)
        )

        intermediate.remove(full_sequent)

        intermediate.nodes[14].remove(a_b_three)
        
        self.wait(1)
        
        # Hey since we're working with simplified version anyway, why not animate to two whilst we're here
        intermediate.remove(a_b)
        self.add(a_b)

        a_b_var = intermediate.nodes[12][0]
        a_b_out = self.proof_out.nodes[12][1]
        a_b_var_out = self.proof_out.nodes[12][0]

        intermediate_top = intermediate.subproof(intermediate.nodes[12], exclude=[intermediate.nodes[12]])
        out_top = self.proof_out.subproof(self.proof_out.nodes[12], exclude=[self.proof_out.nodes[12]])

        self.play(
            FadeOut(intermediate.nodes[14]),
            FadeOut(a_b_three_rule),
            Transform(a_b, a_b_out),
            Transform(a_b_var, a_b_var_out),
            Transform(intermediate_top, out_top)
        )

        self.wait(1)

class TypedProofTwo(ProofScene):
    CONFIG = {
        "start": proof_two,
        "end": proof_three
    }

    def construct(self):
        self.add(self.proof)
        self.wait(2)
        self.ABDown()
        self.AnimateToThree()

    def ABDown(self):
        a_top = self.proof.nodes[5].get_part_by_tex("A")
        a_bottom = self.proof.nodes[10].get_part_by_tex("A")

        b_top = self.proof.nodes[6].get_part_by_tex("B")
        b_bottom = self.proof.nodes[11].get_part_by_tex("B")

        a_top.generate_target()

        b_top.generate_target()

        self.play(
            ApplyMethod(a_top.move_to, a_bottom),
            ApplyMethod(b_top.move_to, b_bottom)
        )
        self.nodes[10].remove(a_bottom)
        self.nodes[11].remove(b_bottom)
        self.wait(2)

    def AnimateToThree(self):
        a = self.proof.nodes[5]
        a_var = a.get_part_by_tex("A")
        b = self.proof.nodes[6]
        b_var = b.get_part_by_tex("B")
        a_b = self.proof.nodes[12]
        a_b_type = a_b.get_part_by_tex(f"({SND} (N,M), {FST} (N,M)):")
        a_b_var = a_b.get_part_by_tex(f"A {TIMES} B")

        rule = self.proof.rules[a_b]

        out_a = self.proof_out.nodes[0]
        out_b = self.proof_out.nodes[1]
        out_a_b = self.proof_out.nodes[2]
        out_a_b_type = out_a_b.get_part_by_tex("(M, N):")
        out_a_b_var = out_a_b.get_part_by_tex(f"A {TIMES} B")
        
        out_rule = self.proof_out.rules[out_a_b]

        remove_left = self.proof.subproof(
            self.proof.nodes[10],
            exclude = [
                a
            ]
        )

        remove_right = self.proof.subproof(
            self.proof.nodes[11],
            exclude = [
                b
            ]
        )

        self.play(
            FadeOutAndShift(remove_left, LEFT),
            FadeOutAndShift(remove_right, RIGHT),
            MoveToTarget(a_var),
            MoveToTarget(b_var)
        )

        self.play(
            ApplyMethod(a.move_to, out_a),
            ApplyMethod(b.move_to, out_b),
            ApplyMethod(a_b_var.move_to, out_a_b_var),
            Transform(rule, out_rule),
            Transform(a_b_type, out_a_b_type)
        )

        self.wait(2)

class TypedDotProofOne(ProofScene):
    CONFIG = {
        "start": ProofData(
            nodes = [
                "[r<z:>b<A>]^z",
                "r<N:>b<B>",
                "",
                f"r<\\lambda z{FUNC_ARROW} N :>b<A>b<{ARROW}>b<B>",
                "r<M:>b<A>",
                f"r<(\\lambda z{FUNC_ARROW} N)M:>b<B>"
            ],
            edges = [
                (0, 1, "assumption"),
                (1, 3, f"{ARROW_I}$^z$"),
                (2, 4, "assumption"),
                (3, 5, ARROW_E),
                (4, 5, ARROW_E)
            ]
        ),
        "end": ProofData(
            nodes = [
                "",
                "r<M:>b<A>",
                "r<N[M := z]:>b<B>"
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
        right_a = self.nodes[4].get_part_by_tex("A")
        right_a.generate_target()

        self.play(ApplyMethod(right_a.move_to, left_a))
        self.wait(1)
        self.nodes[3].remove(left_a)
        self.play(MoveToTarget(right_a))
        self.wait(1)
    
    def ShiftAUp(self):
        top_full = self.nodes[0]
        bottom_a = self.nodes[4]
        bottom_a_dots = self.proof.rules[bottom_a]
        full_bottom = VGroup(bottom_a, bottom_a_dots)

        full_bottom.generate_target()
        full_bottom.target.move_to(top_full)
        full_bottom.target.shift(UP * 0.29)

        self.play(
            FadeOut(top_full),
            MoveToTarget(full_bottom)
        )

        self.wait(1)

    def ShiftBDown(self):
        top_b = self.nodes[1].get_part_by_tex("B")
        full_middle = self.nodes[3]
        middle_b = self.nodes[3].get_part_by_tex("B")
        middle_b_rule = self.proof.rules[full_middle]
        bottom_b = self.nodes[5].get_part_by_tex("B")

        self.play(ApplyMethod(top_b.move_to, middle_b))
        self.wait(1)
        full_middle.remove(middle_b)
        self.play(
            ApplyMethod(top_b.move_to, bottom_b), 
            FadeOut(full_middle),
            FadeOut(middle_b_rule)
        )
        self.remove(bottom_b)
        self.wait(1)

    def AnimateToEnd(self):
        a = self.nodes[4]
        a_rule = self.proof.rules[a]
        a_type = a.get_part_by_tex("M:")
        a_var = a.get_part_by_tex("A")

        b = self.nodes[1]
        b_rule = self.proof.rules[b]
        b_type = b.get_part_by_tex("N:")
        b_var = b.get_part_by_tex("B")

        a_out = self.nodes_out[1]
        a_out_rule = self.proof_out.rules[a_out]
        a_out_type = a_out.get_part_by_tex("M:")
        a_out_var = a_out.get_part_by_tex("A")

        b_out = self.nodes_out[2]
        b_out_rule = self.proof_out.rules[b_out]
        b_out_type = b_out.get_part_by_tex("N[M := z]:")
        b_out_var = b_out.get_part_by_tex("B")

        bottom_rule = self.proof.rules[self.nodes[5]]
        bottom_type = self.nodes[5].get_part_by_tex(f"(\\lambda z{FUNC_ARROW} N)M:")

        self.play(
            ApplyMethod(a_type.move_to, a_out_type),
            ApplyMethod(a_var.move_to, a_out_var),
            ApplyMethod(b_var.move_to, b_out_var),
            Transform(bottom_type, b_out_type),
            ApplyMethod(a_rule.move_to, a_out_rule),
            ApplyMethod(b_rule.move_to, b_out_rule),
            FadeOut(bottom_rule),
            FadeOut(b_type)
        )

        self.wait(1)


    CONFIG = {
        "start": ProofData(
            nodes = [
                "[r<z:>b<A>]^z",
                "r<N:>b<B>",
                "",
                f"r<\\lambda z{FUNC_ARROW} N :>b<A>b<{ARROW}>b<B>",
                "r<M:>b<A>",
                f"r<(\\lambda z{FUNC_ARROW} N)M:>b<B>"
            ],
            edges = [
                (0, 1, "assumption"),
                (1, 3, f"{ARROW_I}$^z$"),
                (2, 4, "assumption"),
                (3, 5, ARROW_E),
                (4, 5, ARROW_E)
            ]
        ),
        "end": ProofData(
            nodes = [
                "",
                "r<M:>b<A>",
                "r<M[N := z]:>b<B>"
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

class TypedDotProofTwo(ProofScene):
    CONFIG = {
        "start": ProofData(
            nodes = [
                "",
                "",
                "r<M>r<:>b<A>",
                "r<N>r<:>b<B>",
                f"r<(>r<M>r<, >r<N>r<):>b<A>b<{TIMES}>b<B>",
                f"r<{FST}(>r<M>r<, >r<N>r<)>r<:>b<A>"
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
                "r<M>r<:>b<A>"
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
        a_top_a = a_top.get_part_by_tex("A")
        # a_top_type = a_top.get_part_by_tex("M")
        # b_top = self.proof.nodes[3]
        # b_top_type = b_top.get_part_by_tex("N")

        middle = self.proof.nodes[4]
        a_mid = middle.get_part_by_tex("A")
        # mid_type_left = middle.get_part_by_tex("M")
        # mid_type_right = middle.get_part_by_tex("N")

        self.play(a_top_a.move_to, a_mid)
                #   a_top_type.move_to, mid_type_left,
                #   b_top_type.move_to, mid_type_right)

        middle.remove(a_mid)
        # middle.remove(mid_type_left)
        # middle.remove(mid_type_right)
        self.wait(1)
        
        bottom = self.proof.nodes[5]
        a_bot = bottom.get_part_by_tex("A")
        # bot_type_left = bottom.get_part_by_tex("M")
        # bot_type_right = bottom.get_part_by_tex("N")

        self.play(a_top_a.move_to, a_bot)
                #   a_top_type.move_to, bot_type_left,
                #   b_top_type.move_to, bot_type_right)

        bottom.remove(a_bot)
        # bottom.remove(bot_type_left)
        # bottom.remove(bot_type_right)
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
            bot_a,
            bot_rule
        )

        a = self.proof.nodes[2]
        a_type = a.get_part_by_tex("M")
        a_type_colon = a.get_part_by_tex(":")
        a_var = a.get_part_by_tex("A")
        a_dots = self.proof.rules[a]

        a_out = self.proof_out.nodes[1]
        a_out_type = a_out.get_part_by_tex("M")
        a_out_type_colon = a_out.get_part_by_tex(":")
        a_out_var = a_out.get_part_by_tex("A")
        a_out_dots = self.proof_out.rules[a_out]

        self.play(
            FadeOutAndShift(remove, RIGHT),
            ApplyMethod(a_type.move_to, a_out_type),
            ApplyMethod(a_type_colon.move_to, a_out_type_colon),
            ApplyMethod(a_var.move_to, a_out_var),
            ApplyMethod(a_dots.move_to, a_out_dots)
        )

        self.wait(1)