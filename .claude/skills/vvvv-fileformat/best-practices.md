# VL File Best Practices

Layout, positioning, and visual organization guide for generating well-structured `.vl` files. Based on analysis of 769+ production files in VL.StandardLibs.

---

## Data Flow Direction

**Data always flows top-to-bottom.** This is the most important layout rule.

- Inputs at the **top**, outputs at the **bottom**
- Input Pads above the nodes they feed
- Output Pads below the nodes they receive from
- Links go from smaller Y to larger Y (top → bottom)
- Only feedback links (`IsFeedback="true"`) flow bottom-to-top

```
[Input Pad]        y = 200
     |
     v
[Processing Node]  y = 300
     |
     v
[Output Pad]       y = 370
```

---

## Coordinate System

- Origin `(0,0)` at **top-left**
- X increases right, Y increases down
- All values in pixels (floating-point)
- **No grid snapping** — coordinates are arbitrary
- For code generation, use round numbers (multiples of 5 or 10) for readability
- Content area typically spans X:100-700, Y:120-600

---

## Vertical Spacing

| Connection Type | Recommended | Observed Median |
|----------------|------------|-----------------|
| Input Pad → Node | **50 px** | 47 px |
| Node → Node (chain) | **40 px** | 41 px |
| Node → Output Pad | **65 px** | 66 px |
| Comment → First element | **100 px** | ~80 px |

---

## Node Positioning

### Horizontal Alignment

Connected elements should be roughly X-aligned. Input pads align within 1-4 px of their node. Output pads offset +2 px right of source node.

### Staircase Pattern (Multiple Inputs)

When a node has multiple inputs, arrange pads diagonally to avoid crossing links:

```
Pad "Red"      Bounds="112,187,35,15"
Pad "Green"    Bounds="139,216,35,15"    offset: +27x, +29y
Pad "Blue"     Bounds="165,243,35,15"    offset: +26x, +27y
Pad "Alpha"    Bounds="192,270,35,15"    offset: +27x, +27y
     ↓ ↓ ↓ ↓
Node "RGBA Join"  Bounds="110,305,73,26"
```

### Multiple Outputs

Spread output pads horizontally:

```
        [Node]              y=298
       /      \
 [Output A]  [Output B]    y=367
 x=150       x=255
```

Typical X-gap between side-by-side output pads: 80-120 px.

---

## Element Sizes

### Node Sizes (Width x Height)

| Node Type | Width | Height | Example |
|-----------|-------|--------|---------|
| Simple operation (+, -, *) | 22-25 | 19 | `"200,300,25,19"` |
| Standard CoreLib node | 45-85 | 19 | `"200,300,65,19"` |
| Long-named node | 85-165 | 19 | `"200,300,145,19"` |
| Join/Split/stateful ops | 41-73 | 26 | `"200,300,52,26"` |
| Skia primitive | 105-145 | 13 | `"200,300,105,13"` |

Standard node height is **19 px** (~80% of all nodes).

### Pad Sizes (Width x Height)

| Pad Type | Width | Height | Example |
|----------|-------|--------|---------|
| Float32 | 33-35 | 15-19 | `"200,160,35,15"` |
| Boolean (toggle/bang) | 35-45 | 35-43 | `"200,160,35,35"` |
| String (value) | 64-273 | 15-20 | `"200,160,170,20"` |
| String (comment, font=14) | 139-632 | 25-39 | `"100,100,400,25"` |
| String (comment, font=9) | 95-472 | 19-312 | `"100,140,350,40"` |
| Vector2 | 35-45 | 27-38 | `"200,160,38,38"` |

### Bounds Convention

- **Definition nodes** (Application, type defs): 2-value `"X,Y"`
- **Processing nodes** (operation calls): 4-value `"X,Y,W,H"`
- **Pads**: 4-value `"X,Y,W,H"`
- **ControlPoints**: 2-value `"X,Y"`

---

## Comment and Title Placement

### Title Comment (font=14)

```xml
<Pad Id="..." Bounds="119,100,400,25" ShowValueBox="true" isIOBox="true"
     Value="HowTo Do Something">
  <p:TypeAnnotation><Choice Kind="TypeFlag" Name="String" /></p:TypeAnnotation>
  <p:ValueBoxSettings>
    <p:fontsize p:Type="Int32">14</p:fontsize>
    <p:stringtype p:Assembly="VL.Core" p:Type="VL.Core.StringType">Comment</p:stringtype>
  </p:ValueBoxSettings>
</Pad>
```

### Description Comment (font=9)

```xml
<Pad Id="..." Bounds="119,145,350,40" ShowValueBox="true" isIOBox="true"
     Value="This example shows how to...">
  <p:TypeAnnotation><Choice Kind="TypeFlag" Name="String" /></p:TypeAnnotation>
  <p:ValueBoxSettings>
    <p:fontsize p:Type="Int32">9</p:fontsize>
    <p:stringtype p:Assembly="VL.Core" p:Type="VL.Core.StringType">Comment</p:stringtype>
  </p:ValueBoxSettings>
</Pad>
```

### Inline Annotation

Use `&lt; ` prefix in Value for arrow-style annotations next to nodes:
```xml
Value="&lt; this is important"
```

---

## Canvas Organization

| Context | CanvasType | Other Attributes |
|---------|-----------|------------------|
| Root (document level) | `FullCategory` | `DefaultCategory="Main"`, `BordersChecked="false"` |
| Inside Application/Process | `Group` | — |
| Sub-category (packages) | (default) | `Name="SubCategory"`, `Position="X,Y"` |

Category hierarchy via nesting:
```xml
<Canvas DefaultCategory="Graphics.Skia" CanvasType="FullCategory">
  <Canvas Name="Drawing" Position="100,100">         <!-- Graphics.Skia.Drawing -->
    <Canvas Name="Primitives" Position="200,200">     <!-- Graphics.Skia.Drawing.Primitives -->
      <Node Name="Circle" ... />
    </Canvas>
  </Canvas>
</Canvas>
```

---

## Multi-Section Layouts

When showing multiple related concepts side by side:

- Arrange sections **left-to-right** with 350-400 px horizontal gaps
- **Y-align corresponding elements** across sections (titles, nodes, outputs at same Y)
- Each section has its own title, inputs, processing nodes, outputs

```
y=100:  [Title A]                   [Title B]
y=145:  [Description A]            [Description B]
y=200:  [Input Pads A]             [Input Pads B]
y=300:  [Node A]                   [Node B]
y=370:  [Output A]                 [Output B]

        x: 100-350                 x: 550-800
```

### Fan-Out Pattern

One source feeding multiple parallel nodes:

- All destination nodes at **identical Y**
- Spread horizontally at ~100-165 px intervals
- Each output pad X-aligned +2 px right of its node

---

## Region Layout

Regions use 4-value Bounds with explicit size:

| Region Type | Typical Size | Minimum |
|-------------|-------------|---------|
| If | 300-530 x 200-530 | 200 x 150 |
| ForEach | 190-400 x 120-300 | 150 x 100 |
| Cache | 200-350 x 150-250 | 150 x 100 |

ControlPoint placement:
- Top: `Alignment="Top"`, Y = region top
- Bottom: `Alignment="Bottom"`, Y = region top + height
- Leave 20-30 px padding from region borders for content

---

## Process Definition Patterns

### Standard Process (Create + Update)

Application node at `Bounds="100,100"`. Inner Patch contains:
1. Canvas (`CanvasType="Group"`) with visual content
2. Named Patches (`Create`, `Update`)
3. ProcessDefinition with Fragments referencing those Patches

### Additional Fragments

| Patch Name | Purpose |
|-----------|---------|
| `Dispose` | Cleanup |
| `Notify` | Event handler |
| `Render` | Skia/Stride rendering |
| `Split` | Decomposition |

### Forward Types

Use `<ProcessDefinition Id="..." IsHidden="true" />` to hide from node browser.

---

## Package File Organization

### Aggregator Documents

Facade files with minimal content, forwarding dependencies:
```xml
<DocumentDependency Id="..." Location="./VL.Animation.vl" IsForward="true" />
```

### Type Definition Files

Organize via Canvas hierarchy:
```
Canvas (FullCategory, DefaultCategory="Domain")
├── Canvas (Name="Sub1", Position="100,100")
│   ├── Node (ForwardDefinition "TypeA")
│   └── Node (ForwardDefinition "TypeB")
└── Canvas (Name="Sub2", Position="300,100")
    └── Node (ContainerDefinition "ProcessC")
```

Forward definitions use 2-value Bounds and always include:
```xml
<p:ForwardAllNodesOfTypeDefinition p:Type="Boolean">true</p:ForwardAllNodesOfTypeDefinition>
```

---

## Naming Conventions

| Context | Convention | Examples |
|---------|-----------|----------|
| Process | PascalCase noun | `OrbitCamera`, `Sequencer` |
| Operation | PascalCase verb | `CircleContainsPoint` |
| Overload | Parenthetical suffix | `Create (KeyComparer)` |
| Forward type | Match .NET name | `LabelAttribute` |
| Pin names | PascalCase with spaces | `"Near Plane"`, `"Key Comparer"` |
| State pins | `(this)` suffix | `"Input (this)"` |
| Root categories | Dotted paths | `"Graphics.Skia"`, `"IO"` |

Standard patch names: `Create`, `Update`, `Dispose`, `Then`, `Else`, `Split`, `Render`, `Notify`.

---

## Complete Layout Recipe

### Help File Y-Position Guidelines

```
y = 100    [Title Comment]         font=14, stringtype=Comment
y = 145    [Description Comment]   font=9, stringtype=Comment
y = 200    [Input Pad 1]           isIOBox=true
y = 230    [Input Pad 2]           offset +30y
y = 300    [Processing Node]       Main operation
y = 350    [Processing Node 2]     Chained (if needed)
y = 420    [Output Pad]            Display result
y = 800    [Renderer Node]         (if visual, e.g. Skia)
```

### Spacing Checklist

- Input pads: 50-80 px above target node
- Sequential nodes: 40-50 px apart vertically
- Output pads: 60-70 px below source node
- Connected elements: roughly X-aligned
- Multi-input pads: staircase pattern
- Multiple sections: 350-400 px horizontal gap
- Title/description: top of canvas (y=100-190)
- Renderer: bottom (y=800+)

---

## Quick Reference: Layout Dimensions

| Metric | Value |
|--------|-------|
| Application node position | `Bounds="100,100"` |
| Title comment Y | ~100-120 |
| Description comment Y | ~140-190 |
| First input pad Y | ~200-250 |
| Main processing area Y | ~280-400 |
| Output display area Y | ~370-500 |
| Renderer Y | ~800-900 |
| Vertical pad-to-node gap | 50-80 px |
| Vertical node-to-node gap | 40-50 px |
| Vertical node-to-output gap | 60-70 px |
| Horizontal section gap | 350-400 px |
| Standard node height | 19 px |
| Boolean pad size | 35x35 px |
| X-alignment precision | 1-4 px |
| Output pad X-offset | +2 px |
| Fan-out spacing | 100-165 px |
