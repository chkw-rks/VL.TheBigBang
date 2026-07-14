# VL.TheBigBang - Part V: The Origin of Life - Chapter Drafts

> Paste-ready IOBox text, column positions, and example-patch specs for all nine chapters. Build the `.vl` patches by hand in vvvv from these specs. See `part-v-context.md` for the reasoning behind the structure.

**Structure (9 chapters, 38–46):**

```
38. Object-Oriented Patching
39. Custom Operations
40. Records
41. Use Case I: Bundling Properties
42. Use Case II: Creating & Destroying Object Instances
43. Classes & Mutability
44. Records vs Classes
45. Mutable Collections
46. Objects as Process Nodes
```

**Format reminders:**
- Top strip identical every chapter: "VL.TheBigBang" top-left (font 12), 7pt author credit top-right, chapter title at y=126 (font 22).
- Columns at x=92, 592, 1092 (sometimes +1592). Body width ≈430px. Opening paragraph at y=206.
- Font sizes: 22 title, 15 section heading, 12 sub-heading, 9 body, 9 Link, 7 credits.

---
---
---
---
---
---
---
---
---
---
---
---

# Chapter 38 — Object-Oriented Patching

**Role:** Recognition chapter. Names that the reader has used objects since ch. 10 and defined them since ch. 11. Introduces Record as the default custom data type. Plants a tiny placeholder Record ("Thing") so the chapter has a working patch. Forward-points to Class. Does NOT name mutability.

## Layout map

```
y=126     Chapter title (font 22)
y=206     Opening paragraph (full width)
y=~310    COL 1: Objects You Already Know   COL 2: Defining Your Own   COL 3: A Record from Scratch (+ live patch)
y=~900    Tooltip tour (full width, live patch)
y=~1300   Closing: Records, Classes, and What's Coming (full width)
y=~1500   Other Resources (x=1092)
```

## Text content

### H1 (font 22, x=92, y=126)
```
38. Object-Oriented Patching
```

### Opening paragraph (font 9, x=92, y=206, width ~1400)
```
We have been working with objects in vvvv almost from the beginning. Every Circle, every Rectangle, every Material, every Spread you have placed in your patch is an instance of a data type that someone defined somewhere. And ever since the chapter about Process Nodes you have also been defining your own - every Process node is in fact a little object, with its own pins, its own behavior and its own little life inside the patch.

That somewhere is usually a language called VL - the language you have been patching in all along, and the language vvvv itself is built upon. Much of what you have used so far, nodes and types alike, is defined in VL, and the rest comes directly from the .NET world underneath. What makes VL unusual is that it compiles into C# in real time, as you patch. You are not scripting or configuring a runtime - you are writing a compiled, typed programming language with a visual syntax. Everything you build runs as compiled .NET code, the same kind of code a C# programmer writes.

In this final part of the tutorial we will name what you have been doing all along, and then unlock the rest of it. From here on you will be able to define your own data types from the ground up, give them properties, give them behavior and use them to organize your patches in ways that were not possible before.
```

### COLUMN 1 - Objects You Already Know

**H2 (font 15, x=92, y=310):** `Objects You Already Know`

**Body (font 9, x=92, y=347):**
```
You can see an object as a composition of the native data types we have met so far - a few values bundled into something more complex. In this sense a Vector2 is already an object. A Vector2 (Join) takes an X and a Y and bundles them into one type. A Vector2 (Split) takes that bundle apart again. The two values travel together as one thing, with their own name and their own identity in the patch.

A Circle from the chapter about Complex Types does the same on a larger scale. It bundles a Center and a Radius into one type. It also comes with operations - Hit Test tells you whether a point lies inside the Circle. The Circle is a data type someone defined inside vvvv, with properties bundled together and operations that work on them. Hover over the link coming out of a Circle node and you will see its type in the tooltip.

Simple values like Floats, Integers or Booleans are not objects in this sense - they are just single values. Objects are what you get when you compose them into something larger.
```

**Live element (x=92, y=750):** A Circle node with values feeding in, and a Hit Test operation showing the result. Two input IOBoxes, one output. The reader can hover and see "Circle" in the tooltip.

### COLUMN 2 - Defining Your Own

**H2 (font 15, x=592, y=310):** `Defining Your Own`

**Body (font 9, x=592, y=347):**
```
Remember the ColoredCircle from the chapter about Process Nodes? We defined it as a Process node - it had input pins for Position, Size and Color, an Update operation that drew the circle, and we placed it three times in the patch to draw three different circles.

That ColoredCircle was already an object. We did not call it that at the time, but bundling properties and behavior into a named type with a place in the Node Browser is exactly what an object is. Every Process node you have written in this tutorial has been your own custom data type, with its own bundle of pins and behavior.

So we are not starting from zero in this part of the tutorial. We are taking what you can already do and going one step further - from defining types as Process nodes to defining them as Records, which is the default and most flexible way to define a data type in VL.
```

### COLUMN 3 - A Record from Scratch

**H2 (font 15, x=1092, y=310):** `A Record from Scratch`

**Body (font 9, x=1092, y=347):**
```
A Record is the default way to define your own data type in VL. You can create one by typing the name you want in the Node Browser and choosing "Record". You can also create one directly from the Patch Explorer in the top-left corner of the document.

You can imagine a Record like a little box with named compartments. Each compartment is a property - a named value of any type: a Float, a String, a Vector, even another Record. Each property can be exposed as an input pin on the Create operation, so you can fill the compartments when you make a new instance.

In the example below we have defined a Record called Thing. It has two properties - a Position and a Size. Right-click on the Thing definition in the Patch Explorer to open it, then come back and look at the Create operation. The two properties are set through input pins on top, and the Thing itself comes out at the bottom.
```

**Live element (x=1092, y=750):** A minimal Record `Thing` (Position: Vector2, Size: Float). Its Create operation shown with two input IOBoxes and one output IOBox carrying a Thing. Definition referenced in the Patch Explorer.

### MID - Tooltip Tour

**H2 (font 15, x=92, y=900):** `Inspecting Your Record`

**Body (font 9, x=92, y=937, width ~1400):**
```
One of the nicest things about defining your own data type is that you can inspect it from anywhere in the patch, just like any built-in type. Hover over a link carrying a Thing and you will see the type name in the tooltip. Right-click on the Thing definition in the Patch Explorer and you can see all its properties at a glance. As you go through the rest of this tutorial, this becomes one of the main ways to understand what is happening in your patch - every link carries a value of a known type, and every value can be inspected.

Since much of vvvv is built in VL, you can also look inside many built-in nodes and see exactly how they were defined - the same way you will define your own types in the chapters ahead. To do this, enable Browsable Packages in Quad Menu > Settings. Once on, right-click a VL-defined node and choose Definition > Open. (Some nodes are implemented in C# instead - those you cannot open this way.) I highly recommend this as a way to learn - find a node you already use and look at how it is built.
```

**Live element (x=92, y=1010):** The Thing placed in an inspection layout with annotated "hover here to see Thing" waypoints. An invitation to interact, not a new lesson.

### CLOSING - Records, Classes, and What's Coming

**H2 (font 15, x=92, y=1300):** `Records, Classes, and What's Coming`

**Body (font 9, x=92, y=1337, width ~1400):**
```
So this is the Record - the default way to define your own data type in VL, and what we will use throughout most of Part V. There is also a second flavor called Class, which is the same idea with one specific difference - Classes can be changed in place, while Records always produce a new copy when you modify them. We will get to Classes in chapter 43, where the difference will become visible and useful. Until then, every example we build will be a Record.

In the next chapters we will give our types real behavior. We will look at operations - first on a Process you already know, then on Records - and see how defining your own operations turns a bundle of properties into a properly useful thing.
```

### Other Resources (x=1092, y=1500)

**H3 (font 12):** `Other Resources`

**Body (font 9, y=1530):** `The Gray Book on Nodes`
**Link (font 9 Link, y=1550):** `https://thegraybook.vvvv.org/reference/language/nodes.html`

**Body (font 9, y=1590):** `The Gray Book on Types`
**Link (font 9 Link, y=1610):** `https://thegraybook.vvvv.org/reference/language/types.html`

## Notes
- "Thing" is a deliberate placeholder - signals the type is incidental, the concept is the point. Particle reserved for chapters 41–42.
- The "Process nodes are objects" move (Column 2) is the most important framing in the chapter.
- Forward pointer to Class is one paragraph in the closing; mutability not named yet.
- Object framing = "composition of primitives," NOT "everything including Float is an object" (that blurs the bundling concept).

---
---
---
---
---
---
---
---
---
---
---
---

# Chapter 39 — Custom Operations

**Role:** Introduce operations on a Process (familiar ground from ch. 11 and 24). The reader has Create and Update; this chapter teaches that a Process can have more operations, including triggerable ones. Stays on Process nodes - Records come next in chapter 40, where the operations concept transfers and the Process→Record contrast becomes the lesson.

## Layout map

```
y=126     Chapter title (font 22)
y=206     Opening paragraph (full width)
y=~310    COL 1: What an Operation Is   COL 2: Create and Update   COL 3: Your Own Operations (+ live patch)
y=~900    Triggerable Operations (full width, live patch)
y=~1400   COL 1: The Reserved Colors   COL 2: Static and Member   COL 3: Other Resources
```

## Text content

### H1 (font 22, x=92, y=126)
```
39. Custom Operations
```

### Opening paragraph (font 9, x=92, y=206, width ~1400)
```
Back in the chapter about Process Nodes we built our first ones, and a few chapters later we met Create and Update - the two operations every Process runs. Create runs once when the Process starts. Update runs every frame. We have been relying on both ever since, often without thinking of them as operations at all.

In this chapter we go further and add our own. Create and Update are operations with reserved meanings, but a Process can have many more - custom ones that run only when you trigger them, like a Reset that returns something to its starting state, or an Increment that bumps a counter on demand. By the end of this chapter you will be able to define your own operations on a Process and call them when you want.
```

### COLUMN 1 - What an Operation Is

**H2 (font 15, x=92, y=310):** `What an Operation Is`

**Body (font 9, x=92, y=347):**
```
An operation is a named action a Process can perform. You can think of an operation as a little patch inside the Process that does one specific job. The Process holds some state - values stored in pads that persist across frames - and its operations are the ways that state can be created, changed or read.

You have been using operations ever since the chapter about Process Nodes without naming them. Every Process you built had a Create operation and an Update operation. Create set up the starting state. Update advanced it each frame. Those were operations all along. What we add in this chapter is the ability to define more of them, and to decide when each one runs.
```

### COLUMN 2 - Create and Update

**H2 (font 15, x=592, y=310):** `Create and Update`

**Body (font 9, x=592, y=347):**
```
Create and Update are the two operations with reserved meanings. Create runs once, when the Process comes into existence. It is where you set up starting values - the initial position, the starting color, whatever the Process needs to begin. Update runs every frame the application is running. It is where the per-frame logic lives - advancing a position, responding to input, drawing to the screen.

The reserved colors mark them. Create is white. Update is gray. When you look inside a Process you can tell these operations apart from any others by their color. They are conventions the runtime understands - the runtime knows to call Create once and Update each frame. You do not trigger them yourself - they run on their own schedule.

Most of what you have built so far lives in Update. In this chapter we add operations that do not run on a schedule at all - they run only when you tell them to.
```

### COLUMN 3 - Your Own Operations

**H2 (font 15, x=1092, y=310):** `Your Own Operations`

**Body (font 9, x=1092, y=347):**
```
To add one, open the Process in the Patch Explorer, right-click and choose to add an operation. Give it a name. Inside, you patch whatever the operation should do.

Unlike Create and Update, an operation you define does not run automatically. When you place the Process node, the operation shows up on it with its own Apply pin - a boolean gate. While the pin is false, the operation sits idle. The frame it flips to true - a Bang from a button, a mouse click, any boolean - the operation runs.

In the patch below we have a Process that holds a Count value. It has the usual Update operation, but we have added a custom operation called Increment. Each time the Bang fires, Increment runs and the Count goes up by one. Update is not involved - the counting happens only on the trigger.
```

**Live element (x=1092, y=750):** A small `Counter` Process holding a Count integer in a pad. Custom operation `Increment` (+1). A Bang wired to Increment's Apply pin. IOBox showing Count climbing per click. Update present but doing nothing visible.

### MID - Triggerable Operations

**H2 (font 15, x=92, y=900):** `Operations That Run on a Trigger`

**Body (font 9, x=92, y=937, width ~1400):**
```
The pattern is worth seeing clearly because it is the basis for everything in the rest of Part V. An operation that runs on a trigger lets you separate "what happens every frame" from "what happens on an event." Update is for the first. A triggerable operation is for the second.

In the patch below we extend the Counter with a second triggerable operation - Reset, which sets Count back to zero. Now the Process has two custom operations: Increment, fired by one Bang, and Reset, fired by another. The Process holds one piece of state, and there are now several named ways to change it, each running only when triggered. This is the shape of a small object - some state, and a set of named operations that act on it.

Notice that you control when each operation runs. The runtime calls Create and Update on its own schedule, but Increment and Reset wait for you. This distinction - operations that run automatically versus operations you trigger - is the foundation for how Records work in the next chapter, where you will see that every operation becomes something you trigger and wire yourself.
```

**Live element (x=92, y=1180, width ~1400):** The Counter Process extended: Count in a pad, Increment (Bang A → +1), Reset (Bang B → 0). Two labeled Bangs. IOBox showing Count. Annotation: Update is doing nothing - all changes are trigger-driven.

### LOWER LEFT - The Reserved Colors

**H2 (font 15, x=92, y=1400):** `The Reserved Colors`

**Body (font 9, x=92, y=1437):**
```
There are three operations with reserved colors and reserved meanings. You have met two of them.

Create, in white, runs once when the Process comes into existence.

Update, in gray, runs every frame.

Dispose, in dark red, runs once when the Process is destroyed - when it is removed from the patch or the application stops. We will not use Dispose until chapter 46, where it earns a proper demonstration, but it is worth knowing the third reserved color exists.

Every other operation you define - Increment, Reset, anything - has no reserved color and no reserved meaning. It runs when you trigger it, and it does whatever you patch inside it. The reserved colors are a hint to anyone reading your patch about which operations the runtime calls automatically and which ones you drive yourself.
```

### LOWER MIDDLE - Static and Member Operations

**H2 (font 15, x=592, y=1400):** `Static and Member Operations`

**Body (font 9, x=592, y=1437):**
```
The operations we have added to the Counter are member operations. They belong to a specific thing - Increment belongs to the Counter, and it works on the Counter's own state. You cannot use Increment on something that is not a Counter.

There is a second kind, the so-called static operation. A static operation does not belong to any one thing. It just takes inputs, does something and produces outputs. The math nodes you have used since the chapter about Simple Math - Add, Multiply, Sin - are all static operations. They work on any compatible value, with no state of their own.

A static operation is the go-to whenever you want to compute something. To define one, open the Patch Explorer, right-click in the document - not inside a Process or type - and choose to add an operation. Give it a name, define its inputs and outputs, and patch the computation inside. Once defined, it appears in the Node Browser just like any built-in node, ready to use anywhere in your patch.

In the example below we define a static operation called Remap that takes a value and two ranges and maps the value from one range to the other. It has no state, no object, no lifetime - it just transforms values. This is exactly the kind of logic that belongs in a static operation.
```

**Live element (x=592, y=1700):** A static operation `Remap` defined in the Patch Explorer at document level. Inside: simple math remapping an input Float from one range to another. Shown being used in the patch with IOBoxes feeding its inputs.

### LOWER RIGHT - Other Resources

**H3 (font 12, x=1092, y=1400):** `Other Resources`

**Body (font 9, y=1430):** `The Gray Book on Operations`
**Link (font 9 Link, y=1450):** `https://thegraybook.vvvv.org/reference/language/operations.html`

## Notes
- Operations taught on a Process on purpose - familiar ground, one new thing at a time.
- The triggerable/automatic distinction is the spine; sets up chapter 40's reveal.
- Dispose named but deferred to chapter 46.
- Counter is the running example - dry placeholder, clearest possible "operation changes state on a trigger."
- Forward pointer to chapter 40 is explicit (the chapter-boundary bridge).

---
---
---
---
---
---
---
---
---
---
---
---

# Chapter 40 — Records

**Role:** Introduce the Record as the first custom data type, by recognizing it has the same operations the reader just learned on a Process - but used differently. On a Process, operations run inside the running Process. On a Record, the same operations become nodes you place and drive yourself, because a Record does not run on its own. State Input/State Output introduced as the mechanism. This recognition is the chapter's opening move and central lesson.

## Layout map

```
y=126     Chapter title (font 22)
y=206     Opening paragraph (full width)
y=~310    COL 1: A Process You Can Hold   COL 2: Defining a Record   COL 3: Operations as Nodes (+ live patch)
y=~900    State Input and State Output (full width, live patch)
y=~1400   COL 1: Create and Split   COL 2: Setters and Getters   COL 3: Other Resources
y=~1700   The Apply Pin Pattern (full width)
```

## Text content

### H1 (font 22, x=92, y=126)
```
40. Records
```

### Opening paragraph (font 9, x=92, y=206, width ~1400)
```
In the last chapter we added operations to a Process - Increment, Reset, operations that run when you trigger them. The Process held some state, and its operations changed that state from inside the running Process. The operations lived in the Process, and you triggered them, but you never had to handle the state yourself. The Process kept it.

A Record is a different kind of thing. It bundles properties together into a custom data type, the way a Vector2 bundles an X and a Y, but with as many properties as you want and a name of your own choosing. And here is the key difference from a Process: a Record does not run on its own. It is data. It just sits there. To do anything with it, you place its operations as nodes in your patch and drive them yourself. The same operations you would add to a Process become, on a Record, nodes you wire up by hand.

This chapter is about defining your first Record, and about how its operations work as nodes - which is where a small but important new idea appears: the State Input and State Output.
```

### COLUMN 1 - A Process You Can Hold

**H2 (font 15, x=92, y=310):** `A Process You Can Hold`

**Body (font 9, x=92, y=347):**
```
Think back to the Counter from the last chapter. It was a Process. It held a Count, and it had operations - Increment, Reset - that changed that Count. The Counter ran by itself in the patch, and you triggered its operations from outside.

A Record is like a Counter you can pick up and hold. It has the same shape - properties bundled together, operations that act on them - but it does not run on its own. You cannot just place a Record and have it tick. Instead, you hold the Record as a value, pass it through its operations as nodes, and get a result back. The Record is data flowing through your patch, and its operations are the nodes that transform it.

This is the difference between a Process and a Record in one sentence - well, two. A Process runs and holds its own state. A Record is held by you, and its state flows through the patch as a value.
```

### COLUMN 2 - Defining a Record

**H2 (font 15, x=592, y=310):** `Defining a Record`

**Body (font 9, x=592, y=347):**
```
To define a Record, open the Patch Explorer, right-click in the document and choose to add a Record. Give it a name. Then give it properties - named values of any type. A property can be a Float, a String, a Vector2, even another Record.

In the example below we define a Record called Thing with two properties - a Position (Vector2) and a Size (Float). You may recognize Thing from chapter 38, where it already appeared as a finished result. This time we build it from scratch, so you can see exactly what each step means. That is the whole definition. Thing is now a data type you can use anywhere in your patch, just like Circle or Rectangle, except you defined it yourself.

Each property you define can be set through an input pin on the Create operation, so a new Thing starts with the values you give it. This is the same Create you know from Processes - it makes a new instance - but on a Record it appears as a node you place in the patch.
```

### COLUMN 3 - Operations as Nodes

**H2 (font 15, x=1092, y=310):** `Operations as Nodes`

**Body (font 9, x=1092, y=347):**
```
Here is where the Process and the Record diverge in practice. On a Process, you added an operation and triggered it from outside, but the operation ran inside the Process and changed the Process's own state. On a Record, the operation becomes a node you place in the patch. You feed the Record into it, the operation does its work, and a Record comes out the other side.

This is not optional. A Record does not run on its own, so there is no "inside" for the operation to run in. The only way to use a Record's operation is to place it as a node and pass the Record through it. Every operation on a Record - Create, Split and any custom ones you define - is a node in your patch.

This changes how state is handled. On a Process, the Process kept the state for you. On a Record, you hold the state, because the Record is a value flowing through your patch. To make this work, every Record operation other than Create has two special pins - a State Input and a State Output.
```

**Live element (x=1092, y=820):** The Thing Record referenced in the Patch Explorer. A Create Thing node with two input IOBoxes (Position, Size) and one output carrying a Thing, carried downstream for inspection.

### MID - State Input and State Output

**H2 (font 15, x=92, y=900):** `State Input and State Output`

**Body (font 9, x=92, y=937, width ~1400):**
```
Open an operation that changes the Record - a setter like SetPosition - and you will see two pins that were not there on the Process operations: a State Input among the inputs on top and a State Output among the outputs at the bottom. The State Input is the Record coming in: the Thing as it exists right now. The State Output is the Record going out: the Thing after the operation has done its work. The operation takes a Record in, and hands a Record back.

This is why a Record's state flows through the patch. The Process kept its state internally and you never touched it. A Record's state is the Record itself, and it travels along the wires - into an operation through State Input, out through State Output, on to the next operation. If you want to change a Thing's Position, you define a SetPosition operation: it takes a Thing on State Input, a new Position from above, and outputs a Thing with the new Position on State Output.

Look closely at the operation and you will notice something. Inside a SetPosition operation, the State Input and the State Output are not visually connected to each other. That is intentional, and it is a detail we will return to in chapter 43. For now it tells you this: the Thing coming out is a fresh copy with the change applied, and the Thing that went in is unchanged. Each operation produces a new Thing and leaves the old one alone.
```

**Live element (x=92, y=1180, width ~1400):** A SetPosition operation on Thing shown opened, State Input/Output annotated. In the application: Create Thing → SetPosition → SetPosition, with IOBoxes feeding new positions and a downstream Split reading the result. Annotation: hovering any link shows "Thing" - each step produces a new Thing.

### LOWER LEFT - Create and Split

**H2 (font 15, x=92, y=1400):** `Create and Split`

**Body (font 9, x=92, y=1437):**
```
Every Record comes with two operations automatically - Create and Split.

Create makes a new instance. Its input pins set the starting properties, and the new Record comes out at the bottom. There is no State Input on Create, because there is no existing Record to take in - Create is where a Record begins. This is the same Create you used on Processes, now as a node.

Split is the opposite. Give it a Record, and it hands you back all the properties as separate outputs. It is how you read what is inside a Record at any point. Split takes a Record on State Input, but its State Output passes the same Record straight through, unchanged - Split only reads, it never modifies.

Between Create to bring a Record into being and Split to read it back out, you can already do a lot. The custom operations you define fill in everything between.
```

### LOWER MIDDLE - Setters and Getters

**H2 (font 15, x=592, y=1400):** `Setters and Getters`

**Body (font 9, x=592, y=1437):**
```
The custom operations you define on a Record usually fall into two kinds. A setter changes one property and returns the modified Record - SetPosition, SetSize, SetColor. It takes the Record on State Input, a new value from above, and outputs the changed Record on State Output. A getter reads one property without changing anything - GetPosition, GetSize. It takes the Record on State Input and outputs the property value on its own pin. Reading takes nothing away - the same Record link can branch to as many readers as you need.

A getter does something Split also does - it reads a property. The difference is convenience. Split gives you everything at once. A getter gives you just one value with a clear name, useful when you only need one or when the calculation is more involved than a plain read.

Define a setter and a getter for each property you want to work with, and your Record has a full set of named operations - each one a node you place in the patch that takes the Record in.
```

### LOWER RIGHT - Other Resources

**H3 (font 12, x=1092, y=1400):** `Other Resources`

**Body (font 9, y=1430):** `The Gray Book on Types`
**Link (font 9 Link, y=1450):** `https://thegraybook.vvvv.org/reference/language/types.html`

**Body (font 9, y=1490):** `The Gray Book on Operations`
**Link (font 9 Link, y=1510):** `https://thegraybook.vvvv.org/reference/language/operations.html`

### FULL WIDTH - The Apply Pin Pattern

**H2 (font 15, x=92, y=1700):** `The Apply Pin Pattern`

**Body (font 9, x=92, y=1737, width ~1400):**
```
There is a refinement worth naming now that you have seen the full read-modify-store pattern in action. The loop - read the Record from the pad, pass it through the operation, store the result back - stays wired permanently, so left alone the operation would run every frame. That is what the Apply pin is for. You have used it on built-in types since chapter 23 - Spread in chapter 25, Dictionary in chapter 26. Apply is a boolean gate: while it is false, the node passes the incoming value through unchanged. The frame it flips to true, the operation runs.

The same Apply pin is available on your own Record operations. A SetPosition node sits in the loop passing the Thing through untouched until a Bang on its Apply pin fires - that frame it produces a Thing with the new Position, and the pad stores the result. Whether the value in the pad is a Spread, a Dictionary, or your own Thing, the pattern is identical. Now that you are defining your own data types, you can use it with them too.
```

**Live element (x=92, y=1830, width ~1400):** A Thing in a pad wired through a SetPosition node and back - the read-modify-store loop. A Bang connected to SetPosition's Apply pin. While Apply is false, the Thing passes through unchanged - on the Bang, the new Position is applied and stored. Annotation marking which pin is the Apply pin.

## Notes
- Opens on the Process→Record recognition - the payoff of splitting operations into its own chapter. The contrast IS the lesson.
- State In/Out introduced as the answer to "where does a Record's state live if it doesn't run?"
- "A Process You Can Hold" is the framing metaphor, tying back to ch. 39's Counter.
- The "not visually connected" cue planted here, pointed forward to chapter 43.
- Thing built out here (from the placeholder in chapter 38). Still not the Particle (chapter 42).
- Reserved colors and static/member NOT repeated - taught in chapter 39.

---
---
---
---
---
---
---
---
---
---
---
---

# Chapter 41 — Use Case I: Bundling Properties

**Role:** First applied chapter, organizational case for Records. Build the same field of shapes twice - first with parallel spreads, then with a single Spread of a Record ("Particle"). The side-by-side comparison IS the argument. No new mechanics. Short chapter.

## Layout map

```
y=126     Chapter title (font 22)
y=206     Opening paragraph (full width)
y=~310    The Old Way (full width, live patch: parallel spreads + ForEach)
y=~900    The New Way (full width, live patch: one Spread of Records)
y=~1400   COL 1: Why This Is Better   COL 2: When to Bundle   COL 3: Other Resources
```

## Text content

### H1 (font 22, x=92, y=126)
```
41. Use Case I: Bundling Properties
```

### Opening paragraph (font 9, x=92, y=206, width ~1400)
```
Now that we know how to define a Record and give it properties, let's look at the first real reason you would reach for one. The case is simple but important - bundling related properties together so they travel as one thing through your patch.

In this chapter we will build the same small application twice. First the way you might build it with what you already knew before chapter 40 - using parallel spreads, one for each property. Then we will rebuild it with a single spread of Records. The patches do exactly the same thing, but the second version is dramatically simpler to read, modify and extend.
```

### TOP - The Old Way

**H2 (font 15, x=92, y=310):** `The Old Way: Parallel Spreads`

**Body (font 9, x=92, y=347):**
```
Imagine we want to draw a field of circles. Each circle has its own position, its own radius and its own color. There are twenty of them, arranged in a spread.

Without a Record, you would do this with three separate spreads - one for positions, one for radii, one for colors. Each spread has twenty values. You would generate these spreads with the techniques from the chapter about Spread Generators, then iterate over all three at once with ForEach.

The patch below shows this approach. Notice how three separate spreads have to be generated, fed in parallel into a ForEach region, and then drawn together. The Position, Radius and Color of each circle live in three completely different parts of the patch, even though they belong together.
```

**Live element (x=92, y=720, width ~1400):** Three Spread Generator chains (Spread<Vector2> positions via grid, Spread<Float> radii, Spread<Color> colors via HSV range), all feeding one ForEach. Inside: Circle drawn at position with radius and color. SkiaRenderer showing twenty circles. Point: visual congestion of three parallel paths.

### MID - The New Way

**H2 (font 15, x=92, y=900):** `The New Way: A Spread of Records`

**Body (font 9, x=92, y=937):**
```
Now let's rebuild the same field using a single Record that bundles Position, Radius and Color together. We define a Record called Particle with these three properties. Then we generate a Spread<Particle> with twenty Particles in it. The ForEach iterates over the spread, and inside it we use Split to read each Particle's three properties at once.

The result on screen is identical. But look at the patch. We have one data stream instead of three. The ForEach takes one input. The relationship between Position, Radius and Color is now structural - they live inside the same Record, so the patch literally cannot mix them up. If you ever need to add a fourth property, like Rotation, you add it to the Record once and every Particle has it.

This is what bundling buys you. Related data stays related, in the patch as much as in your head.
```

**Live element (x=92, y=1220, width ~1400):** A Particle Record (Position, Radius, Color). A generator producing Spread<Particle>. One ForEach. Inside: Split Particle → Circle. Same SkiaRenderer, identical output. The new patch is visibly narrower with fewer crossing lines.

### LOWER LEFT - Why This Is Better

**H2 (font 15, x=92, y=1400):** `Why This Is Better`

**Body (font 9, x=92, y=1437):**
```
The bundled version wins in three ways you can feel directly.

First, the patch is smaller. One data stream instead of three. Fewer links crossing the canvas, fewer parallel structures to keep aligned in your head.

Second, the structure mirrors the meaning. A Particle is one thing, and the patch treats it as one thing. When you read the patch, you do not have to mentally reassemble three parallel spreads into the concept of a "field of particles." The Record does that work for you.

Third, the patch is easier to change. If you want every Particle to also have a Rotation, you add Rotation to the Record once. Every existing patch that uses Particles immediately has access to it. With the parallel-spread version, adding a Rotation means adding a fourth spread, threading it into the ForEach, and making sure its length matches the other three.
```

### LOWER MIDDLE - When to Bundle

**H2 (font 15, x=592, y=1400):** `When to Bundle`

**Body (font 9, x=592, y=1437):**
```
The honest answer is - almost always, if the values belong together.

A good Record bundles properties that conceptually describe one thing. A Particle has a Position, a Radius and a Color because every single particle has its own. A character in a game has Health, Position and Inventory because each character has its own.

The test is simple. If you find yourself maintaining several parallel spreads where the values at each index belong to the same conceptual thing, those values want to be a Record. Bundle them and the parallel structure disappears.

The opposite case - where you should not bundle - is when the values do not belong to one thing. The current time, the mouse position and the application's frame count are all values, but they do not describe one entity. They describe the global state of the world. Bundling them into a Record would be artificial and would make the patch harder to read, not easier.
```

### LOWER RIGHT - Other Resources

**H3 (font 12, x=1092, y=1400):** `Other Resources`

**Body (font 9, y=1430):** `The Gray Book on Types`
**Link (font 9 Link, y=1450):** `https://thegraybook.vvvv.org/reference/language/types.html`

## Notes
- Uses Particle (Position, Radius, Color) - same name as chapter 42 but static/organizational here. Chapter 42 introduces Update and the dynamic version.
- The side-by-side construction IS the argument. No abstract claims about clean code.
- No new mechanics - purely applied use of chapters 38–40. Matches ch. 28 (Collision) as applied use of ch. 27.

---
---
---
---
---
---
---
---
---
---
---
---

# Chapter 42 — Use Case II: Creating & Destroying Object Instances

**Role:** Second applied chapter, the capability case - the thing Process nodes can't do (create instances at runtime). The Particle arrives here as a Record. Mouse-button trio: left-click creates, right-click destroys, middle-click clears. Dispose introduced softly (forward pointer to chapter 46). The Apply pin pattern recognized. Longest chapter in Part V.

## Layout map

```
y=126     Chapter title (font 22)
y=206     Opening paragraph (full width)
y=~310    COL 1: The Particle   COL 2: A Spread of Particles   COL 3: Left Click: Create  (each + live patch)
y=~900    COL 1: Right Click: Destroy   COL 2: Middle Click: Clear   COL 3: Update Each Frame  (each + live patch)
y=~1500   COL 1: A Note on Dispose   COL 2: Other Resources
```

## Text content

### H1 (font 22, x=92, y=126)
```
42. Use Case II: Creating & Destroying Object Instances
```

### Opening paragraph (font 9, x=92, y=206, width ~1400)
```
The first use case showed that Records make patches cleaner. The second use case shows that Records make patches capable of things they could not do before. In this chapter we will build an interactive application where objects appear and disappear during runtime, in response to user input.

This is something a Process node cannot do. Placing a Process is patching - it is you changing the program, not the program acting on its own. Nothing in your patch's logic can create another Process in response to a mouse click. But a Record is data. You can create a new one any time, drop it into a spread, and it lives there until something removes it. That difference is what makes Records and Classes a different kind of tool from Process nodes.

Throughout the rest of Part V we will keep working with the Particle from chapter 41 - but now we give it real behavior. We add Update (which animates Position) and Draw, and we manage a collection of them that grows and shrinks individually at runtime. In chapter 43 we will meet Classes and see the difference mutability makes. In chapter 44 we will compare the two directly on this very Particle.
```

### COLUMN 1 - The Particle

**H2 (font 15, x=92, y=310):** `The Particle`

**Body (font 9, x=92, y=347):**
```
We define a Record called Particle. For this chapter it has two properties - a Position (Vector2) and a Radius (Float). Position is where the Particle is on screen. Radius is its size for drawing and for hit testing.

We also give it operations. Create makes a new Particle at a starting Position with a chosen Radius. Update contains an LFO fed through a Sine that animates the Position - a gentle oscillation that makes the field feel alive. Draw renders the Particle to a SkiaRenderer as a small circle.

Open the Particle definition in the Patch Explorer to see all of this in one place.
```

**Live element (x=92, y=720):** Particle definition referenced in Patch Explorer. Small inspection patch: Create Particle with two input IOBoxes (Position, Radius) and one output carrying a Particle.

### COLUMN 2 - A Spread of Particles

**H2 (font 15, x=592, y=310):** `A Spread of Particles`

**Body (font 9, x=592, y=347):**
```
A single Particle is not much of an application. We want a collection of them, where the collection can grow and shrink at runtime. We store the collection in a pad - a Spread<Particle> that persists across frames.

This pattern should feel familiar from the chapter about Managing Spreads, where we managed spreads of values that changed over time. The same approach works here, just with our own data type instead of a built-in one. The pad starts empty - Spread<Particle> with zero elements. When you click, we add a new Particle to the spread. When you click on an existing one, we remove it. The spread changes, and the next frame draws what is currently in the spread.
```

**Live element (x=592, y=620):** A pad containing Spread<Particle>, labeled. IOBox showing current count. Initial state empty.

### COLUMN 3 - Left Click: Create

**H2 (font 15, x=1092, y=310):** `Left Click: Create`

**Body (font 9, x=1092, y=347):**
```
When you left-click, we want a new Particle to appear at the mouse position. We use a Mouse node (from the chapter about Mouse Input) to get the click event and the position. On the click trigger, we call Create Particle with that position and a random Radius. Then we Add the new Particle to the spread in the pad.

The pattern is: read the current spread from the pad, add the new Particle to it, store the result back into the pad. This is the same explicit-store pattern we have been using since the chapter about Pads - read, modify, store - applied to our own data type.
```

**Live element (x=1092, y=670):** Mouse node, left button filtered to click. Create Particle fed by mouse position + randomized Radius. Spread read from pad, Particle added via Add, stored back. Counter IOBox.

### MID-LEFT - Right Click: Destroy

**H2 (font 15, x=92, y=900):** `Right Click: Destroy`

**Body (font 9, x=92, y=937):**
```
When you right-click, we want to remove the Particle under the cursor - if there is one. This requires two steps: figure out which Particle the click was inside, then remove it from the spread.

For each Particle in the spread, we check whether the mouse position falls inside it. This uses CircleContainsPoint - the same Hit Test approach from the chapter about Collision. If we find a hit, we get its index in the spread, then use RemoveSliceAt to take it out.

If the click misses all Particles, nothing happens. The spread is unchanged.
```

**Live element (x=92, y=1220):** Right click event. Per-Particle distance check vs Radius. Find index of first hit. RemoveSliceAt, store back. Spread count drops by one on a hit.

### MID-MIDDLE - Middle Click: Clear

**H2 (font 15, x=592, y=900):** `Middle Click: Clear`

**Body (font 9, x=592, y=937):**
```
The simplest of the three. On middle-click, we replace the spread in the pad with an empty spread. All Particles disappear at once.

This is a useful pattern to know: sometimes the right move is not to remove a specific item, but to discard the entire collection and start fresh. In a sketch, in a demo, in any application where you want a quick reset, replacing the spread with an empty one is the cleanest way to do it.
```

**Live element (x=592, y=1140):** Middle click event. Writes empty Spread<Particle> to pad. Count drops to zero, all Particles vanish.

### MID-RIGHT - Update Each Frame

**H2 (font 15, x=1092, y=900):** `Update Each Frame`

**Body (font 9, x=1092, y=937):**
```
The mouse input handles creation and destruction. We also need every Particle to update and draw every frame.

We read the spread from the pad, ForEach over it, and inside the ForEach we call Update Particle (the gentle oscillation from the first column) and then Draw Particle (which renders it to a SkiaRenderer). After the ForEach, we store the updated spread back into the pad. Without the store, the updates would be lost between frames - the spread in the pad would always be the original positions.

This is the explicit-store pattern again. Read, modify each item, store back. The Records have to be put back where they came from for the changes to persist.
```

**Live element (x=1092, y=1240):** Read spread from pad. ForEach: Update Particle → Draw Particle (Skia layer). Updated Particles collected to new spread, stored back. Layers grouped and rendered.

### BOTTOM-LEFT - A Note on Dispose

**H2 (font 15, x=92, y=1500):** `A Note on Dispose`

**Body (font 9, x=92, y=1537):**
```
Records and Classes can have a third reserved-color operation called Dispose. It runs automatically once vvvv determines an instance is no longer in use. In our application, that means a Particle removed from the spread via RemoveSliceAt gets its Dispose called (if defined) once nothing in the patch holds on to it anymore.

This is useful when an object owns something that needs to be cleaned up - a file handle, a network connection, a sound that should fade out. For our simple Particle there is nothing to clean up, so we leave Dispose out for now.

We will come back to Dispose in chapter 46, where we look at it more carefully - including the subtle question of when exactly it fires for Records versus Classes.
```

### BOTTOM-RIGHT - Other Resources

**H3 (font 12, x=1092, y=1500):** `Other Resources`

**Body (font 9, y=1530):** `The Gray Book on Operations`
**Link (font 9 Link, y=1550):** `https://thegraybook.vvvv.org/reference/language/operations.html`

## Notes
- The Particle arrives here as a Record - Records-first commitment holds through chapter 42.
- Mouse-button trio is the centerpiece. Particle is Position+Radius only; Update animates Position via an LFO run through a Sine (stateful node, per-iteration in ForEach).
- Dispose introduced softly, forward-pointed to chapter 46.
- The explicit-store pattern named (not labored) - primes the reader for its disappearance with Classes in chapter 43.
- Apply-pin recognition moved to chapter 40, where the pattern first applies.

---
---
---
---
---
---
---
---
---
---
---
---

# Chapter 43 — Classes & Mutability

**Role:** The mechanic chapter. Class enters as the mutable counterpart to Record. State Output pin behavior, solid-vs-dashed links, the MyRecord/MyClass side-by-side patch (three colors on Record side, one on Class side). Does NOT do the decision tree or trade-off discussion - those are chapter 44.

## Layout map

```
y=126     Chapter title (font 22)
y=206     Opening paragraph (full width)
y=~310    COL 1: A Second Flavor   COL 2: Defining a Class   COL 3: The State Output Pin (+ live element)
y=~900    Same Operations, Different Results (full width, the MyRecord/MyClass side-by-side patch)
y=~1500   COL 1: Solid and Dashed Links   COL 2: What This Means   COL 3: Other Resources
```

## Text content

### H1 (font 22, x=92, y=126)
```
43. Classes & Mutability
```

### Opening paragraph (font 9, x=92, y=206, width ~1400)
```
For several chapters now we have been working with Records. Every Record operation produces a new copy of the Record, with changes applied. To make changes persist, we have stored the result back into a pad - explicitly, frame by frame. This is how Records work.

There is a second flavor of object in VL called a Class. A Class looks almost identical to a Record on the outside - properties, operations, the same Patch Explorer interface. The difference is in how operations affect the object. A Class operation does not produce a new copy. It modifies the existing object in place. The same Class instance going into an operation comes out the other side, changed.

This chapter introduces Class as a mechanic. We will see how it differs from Record in the patch, and we will look at a small demonstration that makes the difference visible. The next chapter will help you decide which one to reach for and when.
```

### COLUMN 1 - A Second Flavor

**H2 (font 15, x=92, y=310):** `A Second Flavor`

**Body (font 9, x=92, y=347):**
```
Record and Class are the two flavors of object you can define in VL. You define them the same way - open the Patch Explorer, type a name, choose "Record" or "Class." You give them properties the same way. You define operations on them the same way. The Node Browser shows them with similar nodes - Create, Split and whatever custom operations you define.

The difference is what happens when an operation modifies the object. A Record operation produces a new copy with the change applied. The original Record on the input is unchanged. A Class operation modifies the object on the input directly. There is only one instance, before and after the operation, and it is now different.

You can imagine it like paperwork: a Record operation photocopies the page with the correction applied, a Class operation takes a pen to the original.

This single difference is the entire substance of the chapter. Everything else - the State Output pin, the dashed links, the explicit-store pattern disappearing - follows from it.
```

### COLUMN 2 - Defining a Class

**H2 (font 15, x=592, y=310):** `Defining a Class`

**Body (font 9, x=592, y=347):**
```
To define a Class, open the Patch Explorer, right-click in the document and choose "Add Class." Give it a name. Add properties. Add operations. The interface is identical to Record's.

In our example below we define a Class called MyClass and a Record called MyRecord, both with a single Color property and a single operation called SetColor that changes that property. The definitions look almost the same in the Patch Explorer - you can tell them apart by the icon next to each in the explorer's list of definitions. The R icon marks a Record, the C icon marks a Class.

The operations look slightly different inside, though, and that is where the mechanic becomes visible.
```

### COLUMN 3 - The State Output Pin

**H2 (font 15, x=1092, y=310):** `The State Output Pin`

**Body (font 9, x=1092, y=347):**
```
Open the SetColor operation on the Record and look at it. State Input pin on top, State Output pin at the bottom. Inside the operation, the new Color value is assigned to the Color property of the State Output. The State Input and the State Output are not visually connected. This tells you that the Record coming out is not the same Record that went in - it is a new copy. You met this in chapter 40.

Now open the SetColor operation on the Class. The same two pins, State Input and State Output. But inside, the State Input and the State Output are visually connected to each other. The Class coming out is the same Class that went in. There is no copy. The assignment to Color modifies the Class directly, and the same Class is passed through.

This visual distinction inside the operation is the heart of mutability - a thing you can see, rather than a thing you have to remember.
```

**Live element (x=1092, y=820):** SetColor for MyRecord and MyClass shown side-by-side (nested views or Patch Explorer). Annotations on State In/Out pins noting not-connected (Record) vs connected (Class).

### MID - Same Operations, Different Results

**H2 (font 15, x=92, y=900):** `Same Operations, Different Results`

**Body (font 9, x=92, y=937, width ~1400):**
```
The patch below shows the central demonstration of this chapter. On the left side we have a MyRecord, created and then passed through two SetColor operations - first setting it to blue, then to red. On the right side we have a MyClass, created and passed through two SetColor operations - first blue, then red. The patches are structurally identical.

At three points along each chain - at the start, in the middle between the two SetColor operations, and at the end - we tap an IOBox into the link, showing what it carries.

Look at what the IOBoxes show. On the Record side, three different colors - white at the start, blue in the middle, red at the end. Each link carries a different Record, and each IOBox holds the one from the point it tapped in. On the Class side, three identical colors - all three IOBoxes show red, the final value. Even the one tapped in before the second SetColor shows red - an IOBox does not copy anything at the point it taps in. It holds the instance, and there is only one MyClass instance, which ends up red once the frame has run. The "before" and "after" states are not preserved on the Class side, because there is no copy.

This is the entire mechanic in one screen. A Record holds its history along the chain because every step is a new value. A Class does not - it is one thing that changes, and every reference to it sees the latest state.
```

**Live element (x=92, y=1180, width ~1400):** Left: Create MyRecord → SetColor(blue) → SetColor(red), three IOBoxes tapped into the links at start/middle/end showing white/blue/red, solid links. Right: Create MyClass → SetColor(blue) → SetColor(red), three IOBoxes showing red/red/red, dashed links. Annotation at the middle IOBoxes: "this is where they disagree."

### LOWER LEFT - Solid and Dashed Links

**H2 (font 15, x=92, y=1500):** `Solid and Dashed Links`

**Body (font 9, x=92, y=1537):**
```
You may have already noticed it in the patch above. The links carrying MyRecord are drawn as solid lines. The links carrying MyClass are drawn as dashed lines. This is the visual signature of mutability across the entire vvvv environment.

Solid link: the value being carried is immutable. Whatever flows through this link is a value, like a number or a Record. Each step in the patch produces a new one. The link is a stream of values.

Dashed link: the value being carried is mutable. The link is not a stream of values - it is a reference to one thing. The same thing might be modified anywhere along the link's path, and every part of the patch holding this reference sees the change.

You will see this distinction throughout your patches once you start using Classes. Any link carrying a Class will be dashed. Any link carrying a Record will be solid. The patch tells you, just by looking, which kind of object is flowing through.
```

### LOWER MIDDLE - What This Means

**H2 (font 15, x=592, y=1500):** `What This Means`

**Body (font 9, x=592, y=1537):**
```
The mechanic has practical consequences that ripple through the rest of your patch. The most visible one: the write-back half of the explicit-store pattern from the chapter about Pads onward does not apply to Classes. When you modify a Class via an operation, the change persists automatically, because the Class is the same object before and after. The instance still lives in a pad - but you never store anything back into it. The pad keeps holding the same object, and the object changed.

That is the headline feature of Classes, and it is what makes them tempting. But it is not the whole story. There are things Records do automatically that Classes do not - change detection, snapshots, the natural clarity of order when multiple operations modify a value. These are not abstract concerns - they show up the moment you start building things with Classes that you used to build with Records.

The next chapter looks at this honestly. When to reach for a Class, when to stay with a Record, and what you give up by switching. Class is not free, and the decision is worth making deliberately.
```

### LOWER RIGHT - Other Resources

**H3 (font 12, x=1092, y=1500):** `Other Resources`

**Body (font 9, y=1530):** `The Gray Book on Types`
**Link (font 9 Link, y=1550):** `https://thegraybook.vvvv.org/reference/language/types.html`

**Body (font 9, y=1590):** `Mutability in vvvv Gamma (Record vs Class) by TobyK`
**Link (font 9 Link, y=1610):** `https://youtu.be/zGufG64WSF4`

## Notes
- MyRecord/MyClass placeholders, not Particle - the demonstration is purely mechanical.
- State In/Out cue was primed in chapter 40; dashed links are genuinely new vocabulary introduced here.
- Closing column previews "Class is not free." No decision tree here, no Particle rebuild here.

---
---
---
---
---
---
---
---
---
---
---
---

# Chapter 44 — Records vs Classes

**Role:** The decision chapter. The decision tree as a DERIVATION (Records-as-default → two reasons to switch → what you give up → concrete example), not a memorized list. The Particle from chapter 42 rebuilt as a Class for comparison.

## Layout map

```
y=126     Chapter title (font 22)
y=206     Opening paragraph (full width)
y=~310    COL 1: Records as Default   COL 2: When to Switch to Class   COL 3: What You Give Up (+ Changed demo)
y=~1500   COL 1: Common Mistakes   COL 2: Collections Are a Separate Question   COL 3: Other Resources
```

## Text content

### H1 (font 22, x=92, y=126)
```
44. Records vs Classes
```

### Opening paragraph (font 9, x=92, y=206, width ~1400)
```
The last chapter showed the mechanic. This chapter helps you choose. When should you reach for a Class instead of a Record? The honest answer is - less often than you might think. Records are the default for almost everything you will build in VL, and the cases where Classes are the right move are specific and worth recognizing.

We will look at the genuine reasons to choose a Class, the real costs of that choice and how to recognize the cases where it matters. By the end of this chapter you will be able to make the call confidently, instead of switching based on a hunch.
```

### COLUMN 1 - Records as Default

**H2 (font 15, x=92, y=310):** `Records as Default`

**Body (font 9, x=92, y=347):**
```
VL is a functional environment at its core. Values flow through your patch from one operation to the next, each step producing a new result, and the language is designed around that flow. Records fit this design naturally. They are values. They behave the way numbers, strings and built-in types behave - passed through operations, transformed, copied along the way.

This is why Record is the default choice for almost any custom data type. The functional model is not just a style - it is how the rest of the language works. Change detection assumes values flow through the patch and that new ones differ from old ones. Caching assumes the same. Snapshots and history rely on the fact that each value is preserved at the moment it existed.

When you use a Record, you get all of this automatically. You can detect when the Record changed. You can cache results. You can hold a snapshot and compare it later. None of this requires extra work - it is what the language does when you let values flow through it.

The starting question is therefore not "should I use a Class?" The starting question is "do I have a specific reason not to use a Record?" If you cannot point at one, you almost certainly want a Record.
```

### COLUMN 2 - When to Switch to Class

**H2 (font 15, x=592, y=310):** `When to Switch to Class`

**Body (font 9, x=592, y=347):**
```
There are two reasons that are worth recognizing as a beginner.

The first is access from multiple locations. Suppose you have an object that needs to be modified from several different places in your patch - one part changes its Position, another changes its Color, a third changes its State. With a Record, each modification has to read the current Record from its pad, apply the change, and store it back. If three places are doing this in the same frame, you have to be careful about which one runs first, and the wiring gets dense. With a Class, each location simply calls the appropriate operation directly. The Class modifies itself, and every part of the patch sees the change immediately. The wiring disappears.

The second is performance. A Record copies itself on every modification. For a single Record this cost is invisible. For a thousand Records all updating every frame, the cost can add up. A Class has no such cost - it modifies itself in place. If you have measured a performance problem and traced it to object copying, switching to a Class is one tool that can help.

Notice the qualifier on the second reason - if you have measured. We will come back to this under Common Mistakes below.
```

### COLUMN 3 - What You Give Up

**H2 (font 15, x=1092, y=310):** `What You Give Up`

**Body (font 9, x=1092, y=347):**
```
The relief of not wiring back to a pad comes at a price. The features that Records give you automatically do not work the same way with Classes.

The most visible loss is change detection. The Changed node and Cache regions watch a link for changes. With a Record link, every modification produces a new value, and Changed fires. With a Class link, the link carries the same reference even when the underlying object is modified, and Changed does not fire. TobyK's mutability series (linked below) puts it well: Changed could really be called ChangedReference. It detects when a new Class instance arrives, not when the existing one is modified.

Snapshots and Undo work similarly. With Records, holding a snapshot of a value means holding that value - the Record will not change because it cannot. With Classes, holding a "snapshot" means holding a reference, and the referenced Class can be modified between when you took the snapshot and when you tried to use it. SampleHold has the same issue.

Order of operations becomes less obvious too. With Records, modifications happen serially because you explicitly wire them. With Classes, two parts of the patch can both modify the same Class instance in the same frame, and the order is sometimes determined by the execution order rather than anything visible in the patch.

You can work around all of these - patterns using BehaviourSubject, ticket counters and explicit Clone operations. But the workarounds are advanced material, and they exist to recover what Records give you for free.
```

**Live element (x=1092, y=920):** Changed-not-firing demo. A Record in a pad with SetColor on button click → Changed fires each click. A Class in a pad with SetColor on click → Changed does not fire (reference unchanged). Labeled IOBoxes making the contrast unmissable.

### LOWER LEFT - Common Mistakes

**H2 (font 15, x=92, y=1500):** `Common Mistakes`

**Body (font 9, x=92, y=1537):**
```
The Particle from chapter 42 works equally well as a Record or a Class - either choice produces the same result, and neither reveals a meaningful difference. That is not a failure of the example - it is the point. The Particle does not need the things a Class offers, so the choice is genuinely interchangeable there. The cases where it is not interchangeable are the ones described in the columns above.

Two patterns to watch for, both common when patchers first discover Classes.

Reaching for a Class because the Record wiring feels verbose. The wiring is not noise - it is the patch making the data flow explicit. Verbosity that you can read is more valuable than terseness that hides behavior. Switch to a Class when you have a specific reason from the columns above, not because the Record version "feels" heavier than it should.

Reaching for a Class for performance without measuring. The cost of Record copying is usually negligible. If you are unsure whether you have a performance problem, you do not have one. If you do have one, measure first - find out where the cost actually is. The answer is often a different patch structure or a mutable collection (chapter 45), not a switch from Record to Class.
```

### LOWER MIDDLE - Collections Are a Separate Question

**H2 (font 15, x=592, y=1500):** `Collections Are a Separate Question`

**Body (font 9, x=592, y=1537):**
```
One last thing worth naming before the next chapter. The choice between Record and Class is about individual objects. There is a separate choice about collections - whether to use Spread (immutable) or SpreadBuilder (mutable) for the container that holds many of them. These two questions are independent.

You can have an immutable Spread of mutable Classes. You can have a mutable SpreadBuilder of immutable Records. Both are sensible patterns for different reasons. Chapter 45 looks at the collection question on its own terms - when to use mutable collection types, what they cost, and how they relate to object mutability.

For now, just notice that "I need performance" rarely means "I should switch from Records to Classes." It often means "I should use a mutable collection." The distinction matters.
```

### LOWER RIGHT - Other Resources

**H3 (font 12, x=1092, y=1500):** `Other Resources`

**Body (font 9, y=1530):** `Mutability in vvvv Gamma - full tutorial series by TobyK`
**Link (font 9 Link, y=1550):** `https://youtu.be/zGufG64WSF4`

**Body (font 9, y=1590):** `When to pick a Process, a Record or a Class`
**Link (font 9 Link, y=1610):** `https://forum.vvvv.org/t/when-to-pick-a-process-a-record-or-a-class/21624`

## Notes
- Decision tree as derivation, not a numbered list. "Records as Default" column does the heavy lifting.
- Particle rebuild dropped - the Particle works equally as Record or Class, so the comparison reveals nothing. Brief acknowledgement placed in Common Mistakes instead.
- "What You Give Up" is the most important content - name the losses specifically (Changed, Cache, Snapshots, SampleHold, order).
- Two common mistakes only - tight and memorable.
- Beginner caveat: keep the Class section to the two reasons. Don't add stateful-internal-logic / resources / identity (intermediate+).

---
---
---
---
---
---
---
---
---
---
---
---

# Chapter 45 — Mutable Collections

**Role:** The collection chapter. The independence of the two axes (object mutability vs collection mutability) is the lead point. SpreadBuilder, MutableDictionary, ObservableCollection. Performance argument located at the collection level. Lands chapter 26's promise. Dry placeholder examples only.

## Layout map

```
y=126     Chapter title (font 22)
y=206     Opening paragraph (full width)
y=~310    COL 1: A Separate Axis   COL 2: SpreadBuilder (+ live)   COL 3: MutableDictionary (+ live)
y=~900    COL 1: The Four Combinations   COL 2: When to Reach For Them
y=~1500   COL 1: A Pattern to Know (Clear Each Frame)   COL 2: Other Resources
```

## Text content

### H1 (font 22, x=92, y=126)
```
45. Mutable Collections
```

### Opening paragraph (font 9, x=92, y=206, width ~1400)
```
The last two chapters were about whether your objects should be Records or Classes. This chapter is about something different but related - whether the collections holding them should be immutable or mutable. The two questions sound similar, but they are independent, and confusing them is the single most common mistake in this corner of VL.

Every collection type you have used so far in this tutorial - Spread, Dictionary - has been immutable. You add an element by producing a new collection with the element included. You remove an element by producing a new collection without it. The original collection is unchanged, and you store the new one back. This is the same pattern you have used with Records.

For most applications this works fine. But when you have many elements changing rapidly - hundreds or thousands of particles each frame, a constantly-updating set of objects in a game - the cost of producing a new collection every step starts to show. For those cases there are mutable collection types. They change in place, like Classes do.
```

### COLUMN 1 - A Separate Axis

**H2 (font 15, x=92, y=310):** `A Separate Axis`

**Body (font 9, x=92, y=347):**
```
The mutability of the collection and the mutability of its contents are two different questions. You can mix them freely. The four combinations are all valid and each makes sense for different reasons.

An immutable Spread of immutable Records - what you have been using throughout this tutorial. Values flowing through, every modification producing a new collection.

An immutable Spread of mutable Classes - useful when you want to control when the collection itself changes, but the individual objects need to be modified from multiple places.

A mutable SpreadBuilder of immutable Records - useful when you want fast modification of the collection (adding, removing, clearing) but the individual elements stay as values.

A mutable SpreadBuilder of mutable Classes - the most mutable option, useful when both axes need to change rapidly.

The choice is not Records-or-Classes - it is two independent questions. This chapter looks at the collection side.
```

### COLUMN 2 - SpreadBuilder

**H2 (font 15, x=592, y=310):** `SpreadBuilder`

**Body (font 9, x=592, y=347):**
```
SpreadBuilder is the mutable counterpart to Spread. Where a Spread is a value - adding to it produces a new Spread - a SpreadBuilder is a mutable container that you modify in place. You add elements with Add, remove them with RemoveAt, clear it all with Clear, and the SpreadBuilder itself stays the same instance throughout.

When you need to hand the contents to something that expects a regular Spread - a ForEach, a downstream operation, a renderer - you call ToSpread on the SpreadBuilder. This produces a snapshot Spread of its current state. The SpreadBuilder remains, and you can keep modifying it.

The patch on the right shows a small example. A SpreadBuilder in a pad, with Add fired by a Bang. Each click adds a number to the collection. ToSpread produces a current Spread for inspection.
```

**Live element (x=592, y=720):** SpreadBuilder<Float> in a pad. Bang feeding Add with a random Float. ToSpread → Spread<Float>. IOBox showing the Spread. Second Bang for Clear.

### COLUMN 3 - MutableDictionary

**H2 (font 15, x=1092, y=310):** `MutableDictionary`

**Body (font 9, x=1092, y=347):**
```
MutableDictionary is the mutable counterpart to Dictionary, which you met in the chapter about Dictionaries. The relationship is the same as SpreadBuilder's relationship to Spread. A Dictionary is a value - every modification produces a new one. A MutableDictionary changes in place.

You use the same operations you know - SetValue with a key, Remove, Clear - but the MutableDictionary itself remains the same instance throughout. When you need a regular Dictionary for downstream use, ToImmutable gives you a snapshot.

This is what that chapter was pointing at when it said collections become more interesting once you have your own data types. A MutableDictionary of Particles keyed by name - a lookup table you can grow, shrink and modify in place without ever copying the dictionary itself - is exactly the kind of structure many applications need.
```

**Live element (x=1092, y=750):** MutableDictionary<String, Float> in a pad. IOBoxes for key and value feeding SetValue, with a Bang. Second Bang for Remove with a key. ToImmutable → IOBox showing contents.

### MID-LEFT - The Four Combinations

**H2 (font 15, x=92, y=900):** `The Four Combinations`

**Body (font 9, x=92, y=937):**
```
Going back to where this chapter started - four combinations, each with its own niche.

Immutable Spread of Records is the default. Use it whenever you can, which is most of the time. Everything in VL is designed to flow this way, and you keep all the features Records give you automatically.

Immutable Spread of Classes is useful when the collection itself is stable but individual objects need to be modified from elsewhere. A common pattern for objects with internal state that updates each frame.

Mutable SpreadBuilder of Records is useful when you are adding or removing elements rapidly but each element is still a value. Particle systems where particles get added and removed but each is a stable record of its properties. Often the right pick when you have measured a performance problem with Spread-of-Records.

Mutable SpreadBuilder of Classes is the most mutable and the most performant for many-element, fast-changing collections. It also gives up the most of Records' features. Reach for it when you need it, not before.
```

### MID-RIGHT - When to Reach For Them

**H2 (font 15, x=592, y=900):** `When to Reach For Them`

**Body (font 9, x=592, y=937):**
```
The signal for switching to a mutable collection is the same as for switching to a Class - measure first. If your application runs at the framerate you need with an immutable Spread, you do not need a SpreadBuilder. If it does not, profile to find out where the cost actually is before assuming the answer is the collection type.

That said, there are situations where mutable collections are almost always the right call from the start.

Collections that change every frame and have hundreds or thousands of elements - particle systems, agents in a simulation, points in a constantly-updating dataset.

Collections that are accumulated incrementally - appending log entries, collecting measurements, building up a result over many frames. The accumulation pattern is what SpreadBuilder is designed for.
```

### BOTTOM-LEFT - A Pattern to Know

**H2 (font 15, x=92, y=1500):** `A Pattern to Know: Clear Each Frame`

**Body (font 9, x=92, y=1537):**
```
One pattern with SpreadBuilder is worth naming because it confuses people the first time they hit it. If you want to rebuild a SpreadBuilder's contents every frame - for example, recomputing a list from scratch each tick - the temptation is to create a new SpreadBuilder each frame.

Better: keep the same SpreadBuilder instance in a pad. At the start of each frame, call Clear on it to empty it. Then add the new contents. The SpreadBuilder is the same instance throughout - only its contents change. A fresh builder each frame is not wrong - the big win over plain Spreads is avoiding a full copy on every modification - but reusing one instance keeps per-frame allocation flat and the patch simpler.

This is the pattern that gives mutable collections their actual performance benefit. The collection persists - only the data inside changes.
```

### BOTTOM-MIDDLE - Other Resources

**H3 (font 12, x=592, y=1500):** `Other Resources`

**Body (font 9, y=1530):** `Spread vs SpreadBuilder and Performance of Immutable Collections - TobyK`
**Link (font 9 Link, y=1550):** `https://youtu.be/zGufG64WSF4`

**Body (font 9, y=1590):** `The Gray Book on Collections`
**Link (font 9 Link, y=1610):** `https://thegraybook.vvvv.org/reference/language/types.html`

## Notes
- The independence framing leads and is hammered - without it "I need performance" becomes "use Classes," which chapter 44 warned against.
- SpreadBuilder gets the most space; MutableDictionary parallels it.
- "Clear each frame" is the most common SpreadBuilder mistake - its own column.
- Lands chapter 26's promise.

---
---
---
---
---
---
---
---
---
---
---
---

# Chapter 46 — Objects as Process Nodes

**Role:** The synthesis closer. The "Enable as Process" toggle. Process/Record/Class revealed as one family. The Counter example (Process-enabled Record running by itself). Dispose finally demonstrated visibly (Logger). Closes with a look back across Part V. Dry placeholder examples.

## Layout map

```
y=126     Chapter title (font 22)
y=206     Opening paragraph (full width)
y=~310    COL 1: A Mode We Have Not Used   COL 2: Enabling Process   COL 3: The Counter Example (+ live)
y=~900    COL 1: Dispose, Properly Demonstrated (+ live)   COL 2: When Dispose Fires   COL 3: When to Reach For It
y=~1500   COL 1: The Family Revealed   COL 2: Looking Back at Part V   COL 3: Other Resources
```

## Text content

### H1 (font 22, x=92, y=126)
```
46. Objects as Process Nodes
```

### Opening paragraph (font 9, x=92, y=206, width ~1400)
```
We have come a long way in Part V. We started with the recognition that our Process nodes were already objects - we just had not called them that. We then learned to define our own - Records first, then Classes - and built complete applications with both. We also learned when to choose each, and how to think about collections separately.

In this final chapter we close the circle. Records and Classes can themselves become Process nodes, with a single setting in the Patch Explorer. When you flip it, your type can be placed directly in the patch, its Create runs on placement, its Update runs each frame, and its Dispose runs when removed. This was always available - we just did not use it, because the rest of Part V was about types as data, managed by hand.

This is also where Dispose finally makes full sense. We mentioned it in chapter 42 as the third reserved-color operation. Here we will see it fire visibly.
```

### COLUMN 1 - A Mode We Have Not Used

**H2 (font 15, x=92, y=310):** `A Mode We Have Not Used`

**Body (font 9, x=92, y=347):**
```
Throughout Part V we have used Records and Classes as data. We created instances by calling Create, modified them by calling other operations, drew them by calling Draw, and stored them in pads or spreads to keep them around between frames. Every operation we used, we called by hand - placing nodes in the patch, wiring inputs, deciding when each one would run.

There is another way to use a Record or Class. You can place the type itself directly into your patch, like a Process node. When you do, the type behaves as a Process - its Create operation runs once, the moment the node is placed. Its Update operation runs every frame, automatically. Its Dispose operation runs when the node is removed.

This was available the whole time. We did not use it because Part V's use cases were about types as data being manipulated by hand. The Process behavior is the other mode of the same type. It is useful when you want one specific instance of a type to live in your patch and run by itself.
```

### COLUMN 2 - Enabling Process Behavior

**H2 (font 15, x=592, y=310):** `Enabling Process Behavior`

**Body (font 9, x=592, y=347):**
```
The setting is a single toggle in the Patch Explorer. Right-click your Record or Class definition, find "Enable as Process" in the menu, and turn it on. Nothing about the type changes - its properties stay, its operations stay, the existing places in your patch where you create instances by hand keep working.

What changes is that you can now also place the type itself as a node, by typing its name in the Node Browser. The node has no State Input pin - it does not need one, it is the instance. Its Create runs when the node is placed. Its Update runs on every frame the patch is running. Its Dispose runs when the node is removed.

Having worked through Part V, you can now recognize that this is exactly how Process nodes have always worked. The "Enable as Process" toggle is the bridge that reveals it.
```

### COLUMN 3 - The Counter Example

**H2 (font 15, x=1092, y=310):** `The Counter Example`

**Body (font 9, x=1092, y=347):**
```
Remember the Counter from chapter 39? Back then it was a Process that held a Count and incremented it on a trigger. Here we define a Counter as a Record, with a single property Count, and an Update operation that increments Count by one each frame. With "Enable as Process" turned on, we place the Counter directly in the patch.

The Counter starts at zero on placement. Every frame, Update fires, incrementing Count. An IOBox connected to the Counter shows the count climbing. There is no spread, no pad, no manual call to Update - the type is running by itself.

This is a singleton pattern at its simplest. One Counter, placed once, running for as long as the patch is open. The Counter is a Process node in everything but origin - it just happens to also be a Record, which means it could also be used as data elsewhere if you wanted.
```

**Live element (x=1092, y=820):** A Counter Record (Process enabled) placed directly in the patch. IOBox showing Count climbing. Second IOBox showing "frames since placement" to make per-frame Update visible.

### MID-LEFT - Dispose, Properly Demonstrated

**H2 (font 15, x=92, y=900):** `Dispose, Properly Demonstrated`

**Body (font 9, x=92, y=937):**
```
We mentioned Dispose in chapter 42 as the third reserved-color operation - the dark-red one - that runs when an instance is destroyed. Until now we did not have a clear, demonstrable moment for it to fire. With Process-enabled types, we do.

The patch on the right shows a Record called Logger, with a Create operation that prints "Logger started" to the console and a Dispose operation that prints "Logger stopped." With Process enabled, we place the Logger in the patch and watch its messages appear.

When the patch loads, Create fires and the console reads "Logger started." When you delete the Logger node from the patch - or close the patch entirely - Dispose fires, and the console reads "Logger stopped."

This is Dispose in its purest form. A clear moment for it to fire, a clear behavior to observe.
```

**Live element (x=92, y=1300):** A Logger Record (Process enabled) with Create and Dispose only. Create logs "Logger started", Dispose logs "Logger stopped". Console region showing output. Annotation: "Delete the Logger node and watch the console."

### MID-MIDDLE - When Dispose Fires

**H2 (font 15, x=592, y=900):** `When Dispose Fires`

**Body (font 9, x=592, y=937):**
```
Dispose fires when the type leaves the patch - when you delete the node, when the patch closes, or when the application stops. This is true for both Records and Classes used as Process nodes.

You can rely on it for any cleanup that should happen at the end of a type's life: closing a file, stopping a sound, logging a final message. Dispose is the right place for that logic. If a type does not need cleanup, leave Dispose out entirely.
```

### MID-RIGHT - When to Reach For It

**H2 (font 15, x=1092, y=900):** `When to Reach For It`

**Body (font 9, x=1092, y=937):**
```
"Enable as Process" is for the place-and-forget case. When you want one specific instance of a type to exist in your patch and run autonomously, this is the mode for it.

Singletons. A global audio engine that initializes once and runs for the life of the application. A debug overlay that draws each frame. A configuration manager that loads settings on Create and saves them on Dispose. These are all single, persistent instances - not collections that grow and shrink.

When you do not want this mode is when you have many instances created and destroyed at runtime - the patterns from chapter 42. There, you want types used as data, with spreads and pads doing the management. Mixing the two - a Process-enabled type used in a spread - generally does not work the way you would expect.

The decision is straightforward: one of these in your patch, or many of these in a spread? If one, Enable as Process. If many, leave it off and use the patterns from earlier in Part V.
```

### BOTTOM-LEFT - The Family Revealed

**H2 (font 15, x=92, y=1500):** `The Family Revealed`

**Body (font 9, x=92, y=1537):**
```
Looking at all of this together, Process, Record and Class come into focus as a single family of choices about how to define and use objects.

The classic Process node is essentially a type with Process behavior enabled by default. You place it, it runs by itself, and that is all - your program's logic never creates or destroys one.

A Record is the default object type. You can use it as data - passed through operations as values - or you can enable Process behavior and place it directly in your patch as a self-running unit. Both modes work - the type itself does not change.

A Class is the mutable counterpart. Same flexibility - usable as data via reference, or with Process behavior enabled - but with reference semantics and in-place modification.

The three names that seemed like three different things at the start of Part V are different settings on the same underlying machinery. The unity was always there. This chapter just made it visible.
```

### BOTTOM-MIDDLE - Looking Back at Part V

**H2 (font 15, x=592, y=1500):** `Looking Back at Part V`

**Body (font 9, x=592, y=1537):**
```
Part V started with the recognition that you had been using objects almost from the beginning and defining them since your first Process node. It ends with the recognition that Process, Record and Class are one family.

In between you learned to define your own data types from the ground up. You gave them properties and custom operations. You used them to bundle related data into clean spreads. You created and destroyed instances at runtime in response to user input. You met the mutability fork and learned to choose between Records and Classes deliberately. You met the collection question and learned to separate it from the object question.

That is a lot. If you absorbed even half of it, you have moved from being a patcher who uses what vvvv provides to being one who extends vvvv with your own building blocks. The next part of the tutorial picks up from here and looks at how your applications begin to interact with everything outside themselves.
```

### BOTTOM-RIGHT - Other Resources

**H3 (font 12, x=1092, y=1500):** `Other Resources`

**Body (font 9, y=1530):** `The Gray Book on Operations and Lifecycle`
**Link (font 9 Link, y=1550):** `https://thegraybook.vvvv.org/reference/language/operations.html`

**Body (font 9, y=1590):** `Mutability - Architecture and Design Patterns by TobyK`
**Link (font 9 Link, y=1610):** `https://youtu.be/zGufG64WSF4`

## Notes
- Three jobs in sequence: teach the toggle (Counter), demonstrate Dispose (Logger), reveal the family + look back.
- Counter deliberately threads back to chapter 39's Counter - "remember the Counter... here it is as a Record with Process enabled."
- "Two reasons Dispose fires" is the most nuanced moment - kept brief. OPEN: could simplify to "fires when the type leaves the patch."
- The Create/Update/Dispose life arc quietly honors the "Origin of Life" theme.
- Gentle forward pointer to Part VI (The Emergent Mind) without naming it.
- Longest chapter apart from 42 - a closer should be substantial.

---
---

# END OF PART V DRAFTS

## Final reconciliation checklist

- [ ] Gray Book URLs and per-tutorial TobyK YouTube links verified. (chk to review before publishing)
- [ ] Counter example in chapter 46 to be replaced - example TBD (chk to decide).
