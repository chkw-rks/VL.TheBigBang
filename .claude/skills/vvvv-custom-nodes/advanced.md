# Advanced Node Patterns

## Contents
- FragmentSelection (explicit control over node operations)
- Smell Attribute (internal/experimental nodes)
- Dynamic Enums (runtime-updating dropdowns)
- Settings / Split() Pattern (JSON + vvvv pin control)
- Pin Name Derivation (camelCase to pin names)
- Node Browser Categories via ImportType

## FragmentSelection (Advanced Nodes)

For complex nodes where you need explicit control over which methods become node operations:

```csharp
[ProcessNode(Name = "RenderWindow", Category = "Stride.Rendering",
             FragmentSelection = FragmentSelection.Explicit)]
public sealed class RenderWindow : IDisposable
{
    [Fragment]
    public RenderWindow(NodeContext nodeContext) { }

    [Fragment]
    public void SomeMethod(out RectangleF clientBounds, ...) { }
}
```

Only methods marked `[Fragment]` are exposed. Without `FragmentSelection.Explicit`, all public methods become node operations.

## Smell Attribute (Internal/Experimental Nodes)

```csharp
[Smell(SymbolSmell.Internal)]       // Hidden from public node browser
[Smell(SymbolSmell.Experimental)]   // Shown with experimental warning
```

## Dynamic Enums

Runtime-updating dropdowns for vvvv:

```csharp
public class MyEnumDefinition : DynamicEnumDefinitionBase<MyEnumDefinition>
{
    protected override IReadOnlyDictionary<string, object> GetEntries() { ... }
}

public class MyEnum : DynamicEnumBase<MyEnum, MyEnumDefinition>
{
    public MyEnum(string value) : base(value) { }
}
```

Trigger updates via `SetEntries()` which calls `trigger.OnNext("")`.

The definition is a singleton — only one instance exists globally, ensuring all nodes share identical entries.

## Settings / Split() Pattern

When a settings class needs JSON serialization but should NOT auto-expose properties as vvvv pins:

```csharp
public class EffectSettings
{
    // Internal + [JsonInclude] = JSON works, but vvvv does NOT create pins
    [JsonInclude] internal Vector3 offset = new(0, 0, 0);
    [JsonInclude] internal float intensity = 0f;

    // Split() IS the vvvv-visible API — becomes a Split node
    public void Split(out Vector3 offset, out float intensity)
    {
        offset = this.offset;
        intensity = this.intensity;
    }
}
```

Public properties on classes get auto-exposed as pins by vvvv. Use `internal` + `[JsonInclude]` to prevent this.

## Pin Name Derivation

Parameter names are auto-split from camelCase into vvvv pin names:
- `settings` → pin "Settings"
- `settingsJson` → pin "Settings Json"
- `customInstanceId` → pin "Custom Instance Id"

This matters for `SetPinValue()` calls — the name must match exactly.

## Node Browser Categories via ImportType

Control where your node appears in the node browser:

```csharp
[assembly: ImportType(typeof(MyProcessor), Name = "MyProcessor", Category = "My.Category")]
```

Category uses dot notation: `IO.Ports`, `Stride.Textures.Source`, etc.

For library-level `ImportAsIs` namespace/category configuration, see vvvv-node-libraries.
