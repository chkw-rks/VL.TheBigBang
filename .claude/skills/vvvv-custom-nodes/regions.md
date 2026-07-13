# Custom Regions

Regions are "nodes with a hole" — blocks where users define inner logic via a callback mechanism. Three API flavors exist.

## Flavor 1: Delegate-Based Regions

Simplest approach. Use `Func<>`, `Action<>`, or custom delegates.

**Stateless** — single delegate:
```csharp
public static float MyRegion(float input, Func<float, float> body)
{
    return body(input);
}
```

**Stateful** — two delegates (create + update):
```csharp
public static void MyStatefulRegion<TState>(
    Func<TState> create,
    Action<TState> update)
{
    var state = create();
    update(state);
}
```

Custom delegate types enable named pins and multiple outputs:
```csharp
public delegate void MyRegionBody(float x, float y, out float result);
```

## Flavor 2: ICustomRegion API (since vvvv 4.0)

Define a Process with an `ICustomRegion` input pin on `Update`.

Key interface members:
- `Input` / `Outputs` — static reflection of border control points (BCPs)
- `InputValues` / `SetOutputValues` — read/write BCP data
- `CreateRegionPatch` — instantiate a user patch, returns `ICustomRegionPatch`

Use the `CustomRegionPatch` helper node to instantiate one patch per frame, handle update, and auto-dispose on shutdown.

### Configuration Options

| Option | Values | Purpose |
|---|---|---|
| `Node Or Region` | Node, Region, Both | How it appears in node browser |
| `Supported Control Points` | None, Border, Accumulator, Splicer | What border shapes users can add |
| `Control Point Type Constraint` | (type) | Restrict allowed types on control points |

### Control Point Shapes

| Shape | Name | Behavior |
|---|---|---|
| Rectangle | **Border** | Data passes through |
| Diamond | **Accumulator** | Output = input if region doesn't execute |
| Triangle | **Splicer** | Split/join semantics |

Limitation: cannot define multiple control point kinds simultaneously on one region.

## Flavor 3: IRegion\<TInlay\> API (since vvvv 7.0)

Most generalized. Define the inner patch shape via an interface.

Required operations on the region:
- `Update`
- `SetPatchInlayFactory`
- `AcknowledgeInput` / `RetrieveInput`
- `AcknowledgeOutput` / `RetrieveOutput`

Example: `IfElse` region with `IIfElsePatch` interface defining `Then` and `Else` operations.

Reference implementation: `VL.StandardLibs/VL.TestNodes/src/IfElseRegion.cs`

Limitations:
- Inlay interface must contain an `Update` operation
- Inlay interface must not inherit from other interfaces
- Generics on inlay interfaces are untested

## When to Use Which

| Flavor | Use When |
|---|---|
| Delegate-based | Simple callbacks, no border control points needed |
| `ICustomRegion` | Need border controls (Border, Accumulator, Splicer) |
| `IRegion<TInlay>` | Need custom patch shapes with multiple operations |
