---
name: vvvv-custom-nodes
description: "Helps write C# node classes for vvvv gamma — the [ProcessNode] lifecycle pattern, Update() method, out parameters, pin configuration, change detection, stateless operation nodes, the public-API import model, and service consumption via NodeContext (IFrameClock, Game access, logging). Use when writing a node class, adding pins, implementing change detection, accessing services in node constructors, creating stateless utility methods, or deciding whether a class needs [ProcessNode] at all. Requires the assembly to have one of [assembly: ImportAsIs] / [assembly: ImportNamespace] / [assembly: ImportType] set (see vvvv-node-libraries)."
license: CC-BY-SA-4.0
compatibility: Designed for coding AI agents assisting with vvvv gamma development
metadata:
  author: Tebjan Halm
  version: "1.2"
---

# Writing Custom Nodes for vvvv gamma

## What `[ProcessNode]` actually does (and what it does NOT do)

**Important reality check.** vvvv imports every `public` class, struct, enum, method, and property from the assembly's configured namespaces — `[ProcessNode]` does NOT control whether a class becomes a node. A plain `public class Foo { public int Bar(int x) => x; }` will appear in the node browser exactly the same way as one decorated with `[ProcessNode]`. The attribute affects *how* the runtime treats the class, not *whether* it gets imported.

What `[ProcessNode]` DOES:

- Tells vvvv "this is a stateful node — keep ONE instance alive per node in the patch and call its `Update()` method each frame".
- Lets you set `Name = "..."` (rename for the node browser), `Category = "..."` (override the assembly's category), and `HasStateOutput = true` (expose the instance as an output pin).
- Engages live reload, `IDisposable` cleanup, and the `NodeContext` constructor injection.

What `[ProcessNode]` does NOT do:

- It does NOT make a class visible to vvvv. Visibility comes from the C# `public` access modifier plus an `[assembly: ImportAsIs/ImportNamespace/ImportType]` attribute. See vvvv-node-libraries for the import rules.
- It does NOT hide internal helpers. If a helper is `public`, it's a node — period. Use `internal` to hide.
- It does NOT change pin generation. Pin generation is driven by the `Update()` method signature for `[ProcessNode]` classes, and by public method/property signatures for non-`[ProcessNode]` classes.

**When to use `[ProcessNode]`:** the class needs frame-by-frame updates, persistent state between frames, or `IDisposable` cleanup. **When to skip `[ProcessNode]`:** stateless utility classes, value types, static helper methods — leaving the attribute off avoids the per-frame `Update()` ceremony, and the public methods become operation nodes automatically.

## ProcessNode Pattern — The Core Pattern

The canonical stateful C# node in vvvv gamma:

```csharp
[ProcessNode]
public class MyTransform : IDisposable
{
    private float _lastInput;
    private float _cachedResult;

    /// <summary>
    /// Transforms input values with caching.
    /// </summary>
    public void Update(
        out float result,       // OUT parameters FIRST
        out string error,       // More out params
        float input = 0f,       // Value inputs with defaults AFTER
        bool reset = false)
    {
        error = null;

        if (input != _lastInput || reset)
        {
            _cachedResult = ExpensiveComputation(input);
            _lastInput = input;
        }

        result = _cachedResult; // ALWAYS output cached data
    }

    public void Dispose() { /* cleanup */ }
}
```

**Prerequisite**: vvvv only sees a `[ProcessNode]` class (or any other public class) if its namespace is covered by an assembly-level import attribute — `[assembly: ImportAsIs]`, `[assembly: ImportNamespace]`, or `[assembly: ImportType]` for that specific class. Without one of those, the assembly's public API is invisible to the node browser entirely. Projects scaffolded by vvvv include `[assembly: ImportAsIs]` automatically. For multi-namespace libraries or hand-picked node lists, see vvvv-node-libraries — `ImportAsIs` is `AllowMultiple = false`, so you'll reach for `ImportNamespace` (multi-use) or `ImportType` (per-type) when one root attribute isn't enough.

### Non-Negotiable Rules

1. **`[ProcessNode]` attribute** on every stateful node class
2. **No "Node" in the vvvv-visible name** — everything in vvvv is already a node, so "Node" suffix is redundant
3. **`out` parameters FIRST**, value inputs with defaults AFTER
4. **XML comments** on class and Update method (shown as tooltip in vvvv)
5. **ZERO allocations in Update** — no `new`, no LINQ, cache everything
6. **Change detection** — only recompute when inputs actually change
7. **Always output latest data** — even when no work is done, output cached result
8. **No unnecessary public members** — data flows through Update in/out params only
9. **`IDisposable`** for any node holding native/unmanaged resources

### Live Reload Behavior

When the .vl document references a .csproj source project, vvvv compiles C# via Roslyn at runtime. On .cs file save, vvvv recompiles and restarts affected nodes:

1. `Dispose()` is called on the current instance (if `IDisposable`)
2. The new constructor runs with a fresh `NodeContext`
3. `Update()` resumes on the next frame

Implications for node authors:

- **Instance fields reset** — any state accumulated during runtime (caches, counters, connections) is lost on code change. This is expected.
- **Static fields also reset** — the entire in-memory assembly is replaced. Do not rely on static state to survive edits.
- **Dispose must be thorough** — native handles, network connections, and GPU resources must be released. Leaks accumulate across reloads during development.
- **Constructor must be fast** — it runs each time you save. Defer heavy initialization to the first `Update()` call using a `_needsInit` flag.
- The rules about caching and change detection above exist partly because of this: your code runs in a program that never stops. Allocations in `Update()` cause GC pressure in a 60 FPS loop that may run for hours.

### Class Naming vs Node Name

The rule is: **users must never see "Node" in vvvv's node browser**. How you achieve this:

```csharp
// Simple: class name IS the node name — no suffix needed
[ProcessNode]
public class Wander { }              // vvvv shows: "Wander"

// Class has "Node" suffix + Name property strips it — also fine
[ProcessNode(Name = "Scan")]
public class ScanNode { }            // vvvv shows: "Scan"

// Completely different internal name — fine when class manages another type
[ProcessNode(Name = "MeshRenderer", Category = "Stride.Rendering.Custom")]
public class CustomMeshRenderer { }  // vvvv shows: "MeshRenderer"
```

### HasStateOutput — Exposing Node Instance

```csharp
[ProcessNode(HasStateOutput = true)]
public class ParticleSystem
{
    // The node itself becomes an output pin,
    // allowing downstream nodes to call methods on it
    public void Update(out int particleCount, ...) { ... }
}
```

Alternative: return `this` from a method to expose the instance.

### Pin Visibility

```csharp
public void Update(
    out Spread<float> result,
    [Pin(Visibility = PinVisibility.OnlyInspector)] out string error,
    float input = 0f,
    [Pin(Visibility = PinVisibility.Optional)] bool advanced = false)
{
    // PinVisibility values:
    // Visible       — always shown (default)
    // Optional      — user can show/hide
    // Hidden        — not visible, only via inspector
    // OnlyInspector — only in inspector panel (use for debug/error outputs)
}
```

### Pin Groups (Collection Inputs)

For Spread inputs with add/remove buttons in vvvv:

```csharp
public void Update(
    out float result,
    [Pin(Name = "Input", PinGroupKind = PinGroupKind.Collection, PinGroupDefaultCount = 2)]
    Spread<IRenderer?> input)
{ }
```

### DefaultValue for Complex Types

For defaults that cannot be C# literal expressions:

```csharp
public void Update(
    [DefaultValue(typeof(Color4), "0.1, 0.1, 0.15, 1.0")] Color4 clearColor,
    [DefaultValue(typeof(Int2), "1920, 1080")] Int2 size,
    bool clear = true)
{ }
```

## Attributes — when you actually need them

Verified against `VL.StandardLibs/VL.Core/src/Import/` source. Most attribute properties have sensible defaults — set them only when you want to override the default. Setting an attribute property to its default value is just visual noise.

### `[ProcessNode]` — class-level (`AllowMultiple = false`)

| Property | Default | Set it when… |
|---|---|---|
| `Name` | C# class name | …the node's user-facing name should differ from the class name. If `Name` would equal the class name, omit it. |
| `Category` | from assembly-level import attribute | …you want this specific class to land in a different category than the rest of the assembly. |
| `HasStateOutput` | `false` | …downstream nodes need access to the node instance itself (e.g. to call methods on it). |
| `FragmentSelection` | `Implicit` (all public members become fragments) | …you want only members marked `[Fragment]` to be exposed. |
| `StateOutputNotVisibleByDefault` | `false` | …you have a state output but want it hidden until the user enables it. |
| `Summary`, `Remarks`, `Tags` | `null` | These are alternatives to XML doc comments; prefer the comments unless you need programmatic access. |

So `[ProcessNode]` (bare) is the right default for the common case where the class name = node name and category falls out of the assembly attribute. Adding `[ProcessNode(Name = "Foo", Category = "Bar")]` is only useful when those values diverge from what the defaults would produce.

### `[Pin]` — parameter / property / return-value (`AllowMultiple = false`)

| Property | Default | Set it when… |
|---|---|---|
| `Name` | the parameter name (vvvv applies title-casing automatically) | …you need a name vvvv can't derive — e.g. spaces, punctuation, or a name unrelated to the parameter. **`[Pin(Name = "input")]` on a parameter `input` is redundant** — vvvv already shows it as `Input`. |
| `Visibility` | `PinVisibility.Visible` | …you want the pin `Optional` (collapsible) or `Hidden` (inspector-only). |
| `Exposition` | `PinExpositionMode.Local` | …you want the pin auto-exposed on parent patches (`InfectPatch` / `Expose`). |
| `PinGroupKind` | `PinGroupKind.None` | …the parameter is a `Spread<T>` that should appear as an add/remove pin group. |
| `PinGroupDefaultCount` | `0` | …a pin group should start with N entries. |
| `PinGroupEditMode` | `None` | …you want to limit add/remove to one direction only. |

**The return value attribute** (`[return: Pin(...)]`) is only needed when the auto-derived return-value pin needs an override — e.g. a custom name. The default name is fine for nearly all `Update` methods that only have `out` parameters.

### `[DefaultValue]` — parameter (from `System.ComponentModel`)

NOT a vvvv attribute. Set it only for value types where the literal **isn't** expressible as a C# default — `Color4`, `Vector3`, `Int2`, etc. For `int`, `float`, `bool`, `string`, prefer the C# parameter default (`int x = 5`).

⚠️ **Never combine `[DefaultValue(...)]` with `= default`** on the same parameter — the C# `default` wins and your typed default becomes black/zero/null. See the dedicated section above.

### `[Fragment]` — member-level (`AllowMultiple = false`)

Only relevant when `[ProcessNode(FragmentSelection = FragmentSelection.Explicit)]` is set on the class. With the default `Implicit` selection, `[Fragment]` is unnecessary noise.

| Property | Default | Set it when… |
|---|---|---|
| `Order` | `0` (declaration order) | …you need a specific fragment order independent of source layout. |
| `IsHidden` | `false` | …a member should NOT become a fragment despite being public. |
| `IsDefault` | `false` | …this fragment should run at the default moment when nothing else is wired. |

### Rule of thumb

1. If the attribute has only default values, **don't write the attribute**.
2. If you only need ONE non-default property, write only that one (e.g. `[Pin(Visibility = PinVisibility.Optional)]`).
3. The presence of an attribute should always communicate "I'm overriding a default", never "I'm restating the default".

## Constructor Patterns

**Simple node** (no special context):
```csharp
public MyNode() { }
```

**Node needing NodeContext** (for AppHost, services, Fuse shader graphs):
```csharp
public MyNode(NodeContext nodeContext)
{
    _nodeContext = nodeContext;
    // Access: nodeContext.AppHost.IsExported, nodeContext.AppHost.Services, etc.
}
```

For IFrameClock injection, Stride Game access, logging, and service consumption patterns, see [services.md](services.md).

## Change Detection Patterns

### Simple — Direct Field Comparison

```csharp
private float _lastParam;
private Result _cached;

public void Update(out Result result, float param = 0f)
{
    if (param != _lastParam)
    {
        _cached = Compute(param);
        _lastParam = param;
    }
    result = _cached;
}
```

### Multi-Input — Hash Check

```csharp
private int _lastHash;
private Config _cached;

public void Update(out Config config, float a = 0f, int b = 0, string c = "")
{
    int hash = HashCode.Combine(a, b, c);
    if (hash != _lastHash)
    {
        _cached = new Config(a, b, c);
        _lastHash = hash;
    }
    config = _cached;
}
```

### Reference Types — Identity Check

```csharp
if (!ReferenceEquals(newBuffer, _lastBuffer))
{
    ProcessBuffer(newBuffer);
    _lastBuffer = newBuffer;
}
```

### Rebuild Flag — For Pipeline/Effect State

When multiple setters can invalidate state:

```csharp
private bool _needsRebuild = true;

public void SetShader(ShaderStage vs) { _shader = vs; _needsRebuild = true; }

public void Update(out Effect effect)
{
    if (_needsRebuild)
    {
        RebuildPipeline();
        _needsRebuild = false;
    }
    effect = _cachedEffect;
}
```

### Quick Reference

| Input Type | Comparison | Notes |
|---|---|---|
| Value types (int, float, bool) | `!=` | Direct comparison |
| Reference types (objects) | `ReferenceEquals()` | Identity, not equality |
| Multiple inputs | `HashCode.Combine()` | Single hash for dirty check |
| Collections | Length + sample elements | Full comparison too expensive |
| Multiple setters | `_needsRebuild` flag | Set flag in setters, check in Update |

## Return-Based Output (Single Output)

When a node has a single primary output, you can return it directly instead of using `out`:

```csharp
[ProcessNode]
public class NoiseSteering
{
    private SteeringConfig? _cached;

    public ISteering Update(
        float strength = 2.0f,
        float noiseFrequency = 0.05f,
        int priority = 0)
    {
        if (_cached is null || _cached.Strength != strength ||
            _cached.NoiseFrequency != noiseFrequency || _cached.Priority != priority)
        {
            _cached = new SteeringConfig(strength, noiseFrequency, priority);
        }
        return _cached;
    }
}
```

Mix return + `out` when you have one primary output plus additional outputs:
```csharp
public ReadOnlySpan<ParticleState> Update(
    SimulationConfig config,
    float deltaTime,
    out TimingStats stats)  // Secondary output via out
{
    // Returns primary output, secondary via out
}
```

## Rising Edge Detection (Bang/Trigger)

For boolean inputs that should trigger once (not every frame they're true):

```csharp
private bool _lastTrigger;

public void Update(out bool triggered, bool trigger = false)
{
    triggered = trigger && !_lastTrigger; // Rising edge only
    _lastTrigger = trigger;
}
```

## Operation Nodes

vvvv auto-generates nodes from **all public C# methods** — no attribute needed. Don't create `[ProcessNode]` wrappers for simple methods that just forward calls. Struct `Split()` methods also become nodes automatically.

Static methods auto-generate nodes — no `[ProcessNode]` needed:

```csharp
public static class MathOps
{
    public static float Remap(float value, float inMin = 0f, float inMax = 1f,
                              float outMin = 0f, float outMax = 1f)
    {
        float t = (value - inMin) / (inMax - inMin);
        return outMin + t * (outMax - outMin);
    }
}
```

### When to Use Which

| Pattern | Use When |
|---|---|
| `[ProcessNode]` class | Manages state between frames, caching, dirty-checking |
| Static method | Pure function, no state, transforms input to output |
| Struct + `Split()` | Data containers that unpack into separate pins |

## Memory & Performance in Update Loop

- **No `new` keyword** in hot paths
- **No LINQ** (`.Where`, `.Select`, `.ToList`) — hidden allocations via enumerators
- **Cache collections** — pre-allocate, reuse arrays/lists
- **No string concatenation** — use `StringBuilder` if needed, but avoid in hot path
- **Vector types**: `System.Numerics` internally for SIMD, `Stride.Core.Mathematics` at API boundaries
- **Zero-cost conversion**: `Unsafe.As<StrideVector3, NumericsVector3>(ref val)`

For custom regions (delegate-based, ICustomRegion, IRegion\<TInlay\>), see [regions.md](regions.md).
For advanced patterns (FragmentSelection, Smell, Dynamic Enums, Settings/Split, Pin Name Derivation), see [advanced.md](advanced.md).
For service consumption (IFrameClock, Game, Logging), see [services.md](services.md).
For working with public channels from C# nodes, see vvvv-channels.
For code examples, see [examples.md](examples.md).
For starter templates, see [templates/](templates/).
