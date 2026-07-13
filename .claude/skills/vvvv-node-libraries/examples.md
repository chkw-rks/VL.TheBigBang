# Node Library Examples

Real-world open-source vvvv gamma libraries demonstrating the two initialization patterns.

## 1. Simple Library — VL.IO.MQTT

[github.com/vvvv/VL.IO.MQTT](https://github.com/vvvv/VL.IO.MQTT)

Wraps the MQTTnet library for vvvv. Uses `[assembly: ImportAsIs]` — no Initialization class needed.

### Directory Structure

```
VL.IO.MQTT/
├── VL.IO.MQTT.vl           # Main .vl document (package entry point)
├── src/
│   ├── Properties/
│   │   └── AssemblyInfo.cs  # Just [assembly: ImportAsIs]
│   ├── Utils.cs             # Static helper methods → become nodes
│   ├── VL.IO.MQTT.csproj
│   └── NuGet.config
├── help/                    # Help patches
│   ├── Demo Core.vl
│   └── help.xml
└── deployment/
    └── VL.IO.MQTT.nuspec
```

### AssemblyInfo.cs — Minimal

```csharp
using VL.Core.Import;

[assembly: ImportAsIs]
```

### .csproj

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <OutputPath>..\lib\</OutputPath>
    <GenerateDocumentationFile>True</GenerateDocumentationFile>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="MQTTnet" Version="5.0.1.1416" />
    <PackageReference Include="VL.Core" Version="2024.6.7" />
  </ItemGroup>
  <ItemGroup>
    <Using Include="VL.Core" />
    <Using Include="VL.Core.Import" />
    <Using Include="VL.Lib.Collections" />
    <Using Include="Stride.Core.Mathematics" />
  </ItemGroup>
</Project>
```

**Key pattern**: Public static methods and `[ProcessNode]` classes are auto-discovered. The namespace becomes the node browser category. No service registration, no factory — just compile and go.

---

## 2. Advanced Library — VL.Audio

[github.com/vvvv/VL.Audio](https://github.com/vvvv/VL.Audio)

Audio engine integration with `AssemblyInitializer`, service registration, and a custom node factory that dynamically creates nodes from C# signal types.

### Directory Structure

```
VL.Audio/
├── VL.Audio.vl
├── src/
│   ├── Initialization.cs        # AssemblyInitializer + factory
│   ├── Core/
│   │   ├── AudioEngine.cs
│   │   ├── AudioService.cs
│   │   └── AudioSignal.cs
│   ├── Nodes/
│   │   ├── NodeDescription.cs   # IVLNodeDescription
│   │   ├── PinDescription.cs    # IVLPinDescription
│   │   └── AudioSignalNode.cs   # IVLNode (FactoryBasedVLNode)
│   ├── Signals/
│   │   ├── Sources/             # OscSignal, NoiseSignal, etc.
│   │   ├── Filters/
│   │   └── Sinks/
│   └── VL.Audio.csproj
├── shaders/
│   └── FFTQueue_ComputeFX.sdsl
├── help/
│   ├── Source/
│   ├── Filter/
│   └── help.xml
└── deployment/
    └── VL.Audio.nuspec
```

### Initialization.cs — Service + Node Factory

```csharp
[assembly: AssemblyInitializer(typeof(VL.Audio.Initialization))]

namespace VL.Audio;

public class Initialization : AssemblyInitializer<Initialization>
{
    private IResourceProvider<GlobalEngine>? _engineProvider;

    public override void Configure(AppHost appHost)
    {
        // Register a pooled singleton engine
        if (_engineProvider is null)
            _engineProvider = ResourceProvider.NewPooledSystemWide("VL.Audio", _ => new GlobalEngine());

        appHost.Services.RegisterService(_engineProvider);

        // Register dynamic nodes via factory
        appHost.RegisterNodeFactory("VL.Audio-Factory", nodeFactory =>
        {
            var nodes = ImmutableArray.CreateBuilder<IVLNodeDescription>();

            nodes.Add(new NodeDescription(nodeFactory, _engineProvider, typeof(OscSignal),
                "Oscillator", "Source", "Creates an audio wave", "", "synthesis sine"));
            nodes.Add(new NodeDescription(nodeFactory, _engineProvider, typeof(NoiseSignal),
                "Noise", "Source", "Creates noise", "", "pink white"));
            // ... more signal types ...

            return new(nodes.ToImmutable());
        });
    }
}
```

### .csproj

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0-windows</TargetFramework>
    <OutputPath>..\lib\</OutputPath>
    <AllowUnsafeBlocks>True</AllowUnsafeBlocks>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="NAudio" Version="2.2.1" />
    <PackageReference Include="VL.Core" Version="2024.6.6" />
  </ItemGroup>
</Project>
```

**Key pattern**: `AssemblyInitializer<T>` provides a `Configure(AppHost)` hook for registering services and node factories. Each signal type becomes a VL node via `IVLNodeDescription` + `IVLNode` implementations.

---

## When to Use Which Pattern

| Scenario | Pattern |
|---|---|
| Wrapping a .NET library with helpers | `[assembly: ImportAsIs]` |
| Static utility methods as nodes | `[assembly: ImportAsIs]` |
| Simple ProcessNodes, no shared state | `[assembly: ImportAsIs]` |
| Global singleton service (engine, device) | `AssemblyInitializer` + `RegisterService` |
| Dynamic nodes from C# types | `AssemblyInitializer` + `RegisterNodeFactory` |
| Custom shader path discovery | `AssemblyInitializer` + `DiscoverShaderPaths` |

## Common Conventions

- **Output path**: Always `<OutputPath>..\lib\</OutputPath>` — the `.vl` document expects DLLs in `lib/`
- **Global usings**: `VL.Core`, `VL.Core.Import`, `VL.Lib.Collections`, `Stride.Core.Mathematics`
- **Help patches**: Always in a `help/` directory with a `help.xml` manifest
- **NuGet packaging**: `.nuspec` in `deployment/` — references the `.vl` document and `lib/` DLLs
