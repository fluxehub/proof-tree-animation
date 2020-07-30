# Proof Tree Animation

Animating proof reductions as part of Philip Wadler's ["Propositions as Types"](https://www.youtube.com/watch?v=IOiZatlZtGU) talk, built off of [Manim](https://github.com/3b1b/manim)

# Documentation

Manim is an excellent library for animating LaTeX, and I've built this library around the framework. Whilst Manim is an often woefully undocumented and complex library, I'll try to give a short explanation of how the proof animation library works.

Here's an overview of the files used in the animations
```
- lib/
	- constants.py (symbol constants for proofs, e.g. ARROW, TIMES, FST, SND, etc.)
	- proof.py (contains all logic for rendering proof trees in manim)
	- sequent.py (an extension of Manim's TexMobject, with color markup)
- old/
	- simplify.py (old version of the non-typed simplification animations)
	- typed.py (old version of the typed simplification animations)
- simplify.py (non-typed simplification animations)
- typed.py (typed simplification animations)
```

## Getting Started

1. Install Python 3.7 or newer. It's possible the code works on earlier versions, but I haven't tested it.
2. Install Manim following the steps here [https://github.com/3b1b/manim](https://github.com/3b1b/manim)
3. Install NetworkX using `pip3 install NetworkX`
4. 
	a) If Manim was installed directly, paste the animation library directly into the **root** folder of the Manim library (i.e. `simplify.py` should be in the same directory level as `setup.py` from the Manim library.
	b) Otherwise, the animation library can go anywhere.
5.
	a) If Manim was installed directly, an animation can be rendered using the command `python3 ./manim.py <file with animations.py> <AnimationClass>`, e.g. `python3 ./manim.py simplify.py DotProofOne`
	b) If Manim was installed as a library, an animation can be rendered using the command `manim <file with animations.py> <AnimationClass>`, e.g. `manim simplify.py DotProofOne`

The proof will be rendered to `./media/videos/`. Optionally, if working on an animation, add the `-l` flag to the end of the `manim` command to render in reduced quality for preview.

Now that everything is setup, we're ready to get started.

## Creating a proof animation

I'll go over the animation of a simple proof, in this instance, the class `DotProofOne` from `simplify.py`. Whilst I won't dwell too much on the animation methods available in Manim, I will go over the structure of an animation.

Here's the code for `DotProofOne`

![Dot Proof One](https://i.imgur.com/Sr6sPMa.png)

```python
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
```

### Creating an animation

Going over each step of the animation, we start with the simple class declaration
```python
class DotProofOne(ProofScene):
```
To create an animation in Manim, you create a class which extends `Scene`. In the proof animation library, a similar method is used, except that a class should extend `ProofScene`, which itself is an extension of `Scene` which holds the proof properties as well as rendering the proof.

### Configuring the proof tree

Next, the scene is configured here:
```python
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
```

To create a proof tree, the start and end states need to be defined as nodes and edges on a graph. Each node represents one element of the proof. To colour the element, surround the part to be coloured with `<>` as well as the colour before, e.g. `[b<A>]^x`, which colours the `A` blue (`b` represents blue and `r` represents red). 

One thing to note is that every colour change will create a new sub-object of the overall node. In this case, the generated TexMobject of `[b<A>]^x` will contain three elements: `[`, `A`, and `]^x`. This can be handy in cases where individual parts of an overall element need to be animated. In this instance `f"b<A>b<{ARROW}>b<B>"` may look redundant compared to `f"b<A {ARROW} B>"`, however this causes the generated object to contain the elements `A`, `ARROW`, and `B`, which is necessary as each part is animated separately in the code. If an object is not split, any animation applied to a sub-section of the LaTeX will also apply to any other LaTeX contained in the sub-object. Later, we'll see how to manipulate the sub-objects.

To create the separation lines with the rule, define a tuple in the `edges` array. The first number represents the index of the node above the line. The second number represents the index of the node below the line. The string represents the rule to be displayed on the right-hand side of the line, defined in `TeX`. Keep in mind that, unlike the node objects, rules are not created in math mode, so to use math mode code, surround it with `$ $`.

If multiple nodes are above the line, simply define each nodes to go to the same node below the line. For example,

```python
(3, 5, ARROW_E),
(4, 5, ARROW_E)
```

places the `A {ARROW} B` and `A` above the line, and the `B` below, as in the proof image. Whilst strictly speaking, the rule only needs to be defined for the *first* node, it's good practice to use the same rule for both.

**NOTE: This will only work when 2 elements are above the line. If three or more elements are required, such as in disjunction, the rendering code needs to be modified. Please refer to line 115 of `lib/proof.py`**

One exception here is when vertical dots need to be inserted. To create a rule using vertical dots, use the word `"assumption"` as the rule, and the code will automatically convert the rule to vertical dots. The side-effect of this is that if there are no elements *above* the dots, a **unique** blank node needs to be created, as all rules must have an above and below node. A blank node is used in this way to create the vertical dots leading to `A` on the right-hand side of the proof.

If you've correctly set up the config, the proof tree will render and be contained in the properties `proof`, for the starting tree state, and `proof_out`, for the ending tree state.

Each `Proof` object contains the following:

`.nodes`: a list of all nodes in the proof tree, as `Sequent` objects (effectively `TexMobject`)
`.rules`: a dictionary of rules in the proof tree, containing the line and the text on the right hand side (or in cases of dots, simply the dots). The dictionary is indexed by the rule *under* the line.
`.graph`: the overall proof tree as a NetworkX `digraph`. This is never used in the animation code.

`self.nodes` is also a useful shorthand which will contain all nodes of the starting state, and is generally how I grab individual nodes in animation. Please note that no shorthand exists for `.rules`.

#### A note on `f"{}"`

If you are unfamiliar with this syntax, this is Python's string interpolation syntax implemented in Python 3.6. It's similar in function to JavaScript's `` `${<JS Code>}` `` syntax, and simply inserts into the string the variable or string output of python code into an overall string. This is used throughout the code to insert the animation constants such as the `ARROW`

#### A note on spacing

Elsewhere in the code, you may see another entry in the `CONFIG` dictionary, for example in `ProofOne`, which looks like this:

```python
CONFIG = {
	"spacing": Spacing(regular = 0.65, orphan = 2),
	"start": ...
	"end": ...
}
```

This allows you to override the default spacing between nodes in the case where two nodes above lead to the same node below. `regular` represents the spacing for nodes *with* parent nodes (i.e. nodes above), whilst `orphan` represents the spacing for nodes *without* parent nodes (e.g. `A` and `B` sitting above an `A & B` when introduced). When creating more complex animation, it's worth experimenting with the spacing to find the optimal width.

### Animating the proof tree

```python
def construct(self):
    self.add(self.proof)
    self.ARightBUp()
    self.AnimateToEnd()
```

All animations need to be inserted in the `construct` method of the class so that Manim can correctly animate. As this can become unwieldy, it's suggested to create methods that contain the individual animations and then place them in order in the `construct` method, as done here.

`self.add(self.proof)` is ***required*** to be at the start of the method, as this will display the proof on-screen. If this is forgotten, you will get very odd results!

Here's the code for the first half of the animation, where `A {ARROW} B` splits, the A goes right, the B goes up, and the arrow disappears.

```python
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
```

### Selecting nodes and elements

Throughout the code, animations are generally structured in two halves. The first half involves selecting the individual elements to animate, whilst the second half involves the actual animation.

```python
full_sequent = self.nodes[3]
a_left = full_sequent.get_part_by_tex("A")
...

b_bot = full_sequent.get_part_by_tex("B")
...

arrow = full_sequent.get_part_by_tex(f"{ARROW}")
```

If you recall, earlier in the code `A {ARROW} B` was written such that it was split into three elements: `A`, `ARROW`, and `B`. We can now use this to our advantage to isolate each section of the overall node, and animate each separately. First, select the full node through normal array indexing.

```python
full_sequent = self.nodes[3]
```

Next, there are two options to selecting each individual part of the overall node. We could select each element through an index like so:

```python
a_left = full_sequent[0]
b_bot = full_sequent[2]
arrow = full_sequent[1]
```

However, this requires you to remember what order the elements are broken up, and if in future text is added before or after, the indexes need to be update for the code to still work (think adding variables to the types). Luckily, Manim includes a handy function `get_part_by_tex()` which will let us select the element simply by its tex string, and is far more readable. Generally throughout the code, I use this approach, although there are some advantages to the index method (I normally use indexes to select the red variables, as the tex strings can become quite long and it's guaranteed to be at index 0).

Now that we have the elements selected from the node, we can go ahead and get the elements we want these parts to move to.

```python
a_right = self.nodes[4]
...

b_top = self.nodes[1]
```

I like to label variables in respect to where they are relative to each other. Here, there are two `A`s on the same line, so I've labelled the left one with `_left` and the right one with `_right`. Similarly, there are two `B`s, one above and the other below, so I've labelled the bottom one with `_bot` and the top one with `_top`. This makes it far easier to understand the animation.

### Animating the elements

Now that everything is selected, we can animate the elements.
```python
self.play(
    ReplacementTransform(a_left, a_right),
    ReplacementTransform(b_bot, b_top),
    FadeOut(arrow)
)

self.wait(1)
```

All animations must go inside a call to `self.play()`. Here, we `Transform` the A and B to their new positions, and `FadeOut` the arrow. The reason we use a replacement transform is so that `a_left` and `b_bot` are deleted at the end of the animation. Otherwise, we'd have to delete it manually or we would have two copies of it on screen. The arrow can simply fade out. Finally, we wait 1 second before moving on to the next animation.

#### A note on transform

Here, since the As and Bs are the same size and color, a transform just looks like a move to the node. If the objects didn't look the same, Manim would do a complex transformation animation to convert one to the other. If this is undesired, you can move a node to the other's center with `ApplyMethod(<start>.move_to, <end>)`, and then manually animate elements away. This can be handy in cases where one element isn't exactly the same size as the other, which can happen occasionally due to typesetting.

### Animating out

To finish off the animation, we need to move from this intermediate state to the end state, like so:

```python
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
```

This is very similar to the previous code, so I'll only go over the new parts used here.

#### Proof Out

```python
a_top = self.nodes[0]
a_bot = self.nodes[4]
a_out = self.proof_out.nodes[1]
```

As stated earlier, the tree expressed in the `"end"` state of `CONFIG` is placed into the property `proof_out`. To select nodes from this tree, a similar process is used, except we add `proof_out.`.

#### Rules

```python
a_dots = self.proof.rules[a_bot]
a_dots_out = self.proof_out.rules[a_out]

b_dots = self.proof.rules[b_top]
b_dots_out = self.proof_out.rules[b_out]

rule_one = self.proof.rules[self.nodes[3]]
rule_two = self.proof.rules[self.nodes[5]]
```

To isolate the rules (including lines and dots), we use the `proof.rules` dictionary, indexed by the node ***below*** the line.

#### A note on subproof

Elsewhere in the code, you may see `subproof` used, like in `DotProofTwo`:

```python
def AnimateToEnd(self):
	a_top = self.proof.subproof(self.nodes[2])
	b_top = self.proof.subproof(self.nodes[3])
```

A subproof will return a group of a tree containing every node and rule ***above*** the start node, including the start node. This can be useful when working with vertical dots as a way to group both the node and the dots into one element. It's also used in `ProofOne` to clone and shift the right-hand side of the tree. You can also specify which node to end on and nodes to exclude with `subproof(<start_node>, end = <end_node>,  exclude = [<excluded_nodes>])`

### The End

If you've made it here, congrats! We now have a finished animation for this proof tree, and a framework from which to understand the rest of the code from.
