# Design Guidelines

Naming conventions, pin rules, and standard types for vvvv gamma node libraries.

## Node Naming: Name (Version) [Category]

- **Name**: CamelCase, no spaces. Process nodes use nouns (`Sequencer`, `FlipFlop`). Operations use verbs (`Map`, `Copy`).
- **Version**: Optional. Simpler variant has no version; more specific gets a descriptive version.
- **Category**: Dot-separated subcategories (`Math.Ranges`, `Color.RGBA`).

Avoid `As..` prefixes — use `To..` or `From..` instead.

### Constructor Naming

| Pattern | Use When |
|---|---|
| `Create` | Complex datatypes beyond property storage |
| `Join` / `Split` | Container-like types (one pin per property) |
| `From..` / `To..` | Type conversions. Direction depends on which library defines the node |
| `..To..` | Unit converters without type change: `CyclesToRadians` |

## Pin Guidelines

- Space-separated words, each uppercase: `First Input`
- camelCase C# parameter names auto-split: `firstInput` → "First Input"
- Default return value label is "Output"
- Avoid generic names like `"Do"`, `"Update"`

### Apply Pin (Reserved)

`Apply` is a **reserved pin name** with compiler-enforced semantics:
- Auto-created for operations with no output, or one Input + one Output of matching type
- Default value = `true`
- When `false` = pass-through (input flows directly to output)
- Do not use `Apply` as a pin name for other purposes

### Dynamic Pin Counts

- `Ctrl+` / `Ctrl-` on selected node adds/removes inputs
- Auto-enabled for operations with exactly two inputs + one output of same type as first input

## Aspects

Keywords that control node visibility and behavior:

| Keyword | Purpose |
|---|---|
| `Advanced` | Hidden by default in NodeBrowser (show via filter) |
| `Internal` | Visible only in the defining `.vl` document |
| `Experimental` | Marks unstable/WIP nodes |
| `Obsolete` | Deprecated; kept for backwards compatibility |
| `Adaptive` | Enrolls nodes in adaptive type dispatch |

### Applying Aspects

Three methods:
1. **Group-level**: Use keyword as a category name segment. `MyLib.Particles.Advanced` → all nodes inside get `Advanced` aspect
2. **Datatype-level**: Set in Patch Explorer on Process/Record/Class. Applies to all nested elements
3. **Operation-level**: Embed keyword in the Version portion: `GetBytes (Advanced)`, `Transform (Normal Advanced)`

Aspect keywords are **stripped** from resolved category: both `MyLib.Particles.Advanced` and `MyLib.Advanced.Particles` resolve to `MyLib.Particles`.

### Adaptive Nodes

Define in top-level `Adaptive` category with at least one generic pin. Implementations: same signature but fully typed, in different categories. Nodes in an `Adaptive` subcategory appear under the parent category but participate in per-type dispatch.

## Standard Types and Units

| Type | Convention |
|---|---|
| Angles | **Cycles** (0–1, counter-clockwise) |
| Color components | Range 0–1 |
| Standard types | `Boolean, Byte, Integer32, Float32, Vector2/3/4, Matrix, Char, String, Path, Spread` |

## Async Output Pattern

Standard output set for async operations:
- `In Progress` (bool)
- `On Completed` (bang)
- `Success` (bool)
- `Error` (string or Exception)

## Events and Observables

Always expose async data sources as **Observables**, not raw events.

## Resource Providers

| Lifetime | Pattern |
|---|---|
| Short-lived | `Dispose [IDisposable]` |
| Long-lived | `[Resources]` category nodes: `New`, `BindNew`, `Do`, `Execute`, `Using` |

## CreateDefault

Create a `Forward` operation called `"CreateDefault"` for imported types. Must have no side effects. Prevents null pointer exceptions when users create nodes.

## NuGet Self-Reference Rule

Do not reference your own NuGet in `.vl` documents that contribute to another NuGet (except help patches).

## Process Node Reset

Reset always takes precedence — it has lowest priority in the process explorer, meaning it evaluates last.
