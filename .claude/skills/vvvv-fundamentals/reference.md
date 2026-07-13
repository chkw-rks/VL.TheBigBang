# vvvv Fundamentals — Detailed Reference

## Contents

- [Node Lifecycle](#node-lifecycle)
- [NodeContext](#nodecontext)
- [Live Compilation Details](#live-compilation-details)
- [IDevSession — Editor Pin Persistence](#idevsession--editor-pin-persistence)
- [Threading Model](#threading-model)
- [IFrameClock — Frame Timing](#iframeclock--frame-timing)
- [Regions in Visual Patches](#regions-in-visual-patches)
- [AppHost.Services — Per-App Singletons](#apphostservices--per-app-singletons)
- [AssemblyInitializer — Early Startup](#assemblyinitializer--early-startup)
- [Common Global Usings for C# Projects](#common-global-usings-for-c-projects)

## Node Lifecycle

### Process Node Lifecycle

```
Constructor (Create) → Update (per frame) → Dispose (cleanup)
```

1. **Constructor**: Called once when the node is created. Receives `NodeContext` if declared.
2. **Update**: Called every frame (~60 FPS). Must be fast — zero allocations.
3. **Dispose**: Called when the node is removed or the document closes.

### Operation Node Lifecycle

Static methods are called each frame when their outputs are consumed. No persistent state.

## NodeContext

Injected into ProcessNode constructors by the VL runtime:

```csharp
public MyNode(NodeContext nodeContext)
{
    // nodeContext.AppHost — application host
    // nodeContext.AppHost.IsExported — running as exported exe?
    // nodeContext.AppHost.Services — service registry
}
```

## Live Compilation Details

### Source Project Reference — Roslyn In-Process Compilation

When a .vl document references a .csproj source project, vvvv compiles .cs files itself via Roslyn:

1. File watcher detects .cs file change in a referenced source project
2. Roslyn compiles in background (status indicator: gray = building symbols, orange = emitting)
3. New in-memory assembly replaces the old one
4. Affected ProcessNode instances restart: Dispose() → Constructor → Update() resumes
5. On compilation error: error shown in tooltip/compiler panel, old code continues running

### Binary Reference — No Live Reload

When a .vl document references a pre-compiled DLL or NuGet package, the assembly is loaded at startup. To apply changes: rebuild the DLL externally (`dotnet build`), then restart vvvv. This is the standard workflow for larger projects and stable libraries.

### Behavior During Source Reload

- `SetPinValue` calls (via IDevSession) persist across reloads — they are stored in the .vl document, not the node instance
- `NodeContext` provides a fresh context for the new instance
- Services registered via `AppHost.Services` survive reloads — they are per-app, not per-node
- Static fields do not survive — the entire in-memory assembly is replaced

### Shader Live Reload

Shader (.sdsl) files always live-reload regardless of how they are referenced. vvvv recompiles them in the background on save.

### --editable-packages Flag

NuGet packages normally run pre-compiled and do not live-reload. To live-edit a package's source during development:

```bash
vvvv.exe --editable-packages VL.MyPackage
```

This makes vvvv treat the package as a source project and recompile on change.

## IDevSession — Editor Pin Persistence

For nodes that need to persist settings in the vvvv editor with undo/redo:

```csharp
IDevSession.SetPinValue(pinName, value);
```

Only available in editor mode, not in exported applications.

## Threading Model

- The mainloop runs on the **main thread**
- `Update()` is always called on the main thread
- For background work, use `Task.Run` but marshal results back:
  - `_vlSyncContext.Post(_ => { }, null)` — post to VL main thread
  - `_form.Invoke(new Action(() => { }))` — post to UI thread
- `Parallel.For` is safe for stateless/thread-local computations within Update

## IFrameClock — Frame Timing

The source of truth for frame timing in vvvv. Two ways to obtain:

**Constructor injection** (VL auto-injects when it sees the parameter):

```csharp
public class MyNode
{
    private readonly IFrameClock _clock;
    public MyNode(IFrameClock clock) { _clock = clock; }
}
```

**Service lookup** (when you already have AppHost):
```csharp
var frameClock = appHost.Services.GetRequiredService<IFrameClock>();
```

Key properties:

- `frameClock.TimeDifference` — delta time since last frame (seconds, double)
- `frameClock.Time` — absolute time since app start
- `frameClock.GetTicks()` — IObservable for subscribing to frame events

## Regions in Visual Patches

| Region | Purpose |
|---|---|
| ForEach | Iterate over Spread elements |
| If | Conditional execution |
| Switch | Multi-branch selection |
| Repeat | Loop N times |
| Accumulator | Running aggregation (like Aggregate/Fold) |

## AppHost.Services — Per-App Singletons

Register and retrieve application-wide services:

```csharp
public class MyConfigService
{
    public static MyConfigService GetOrCreate(AppHost appHost)
    {
        var existing = appHost.Services.GetService(typeof(MyConfigService)) as MyConfigService;
        if (existing != null) return existing;

        var service = new MyConfigService();
        appHost.Services.RegisterService(service);
        return service;
    }
}
```

Consume in a ProcessNode:
```csharp
[ProcessNode]
public class MyConfigManager : IDisposable
{
    private readonly MyConfigService _service;

    public MyConfigManager(NodeContext nodeContext)
    {
        _service = MyConfigService.GetOrCreate(nodeContext.AppHost);
    }
}
```

Key APIs:

- `appHost.Services.GetService(typeof(T))` — retrieve
- `appHost.Services.RegisterService(instance)` — register
- `appHost.AppBasePath` — application base directory

**Warning**: `AppHost.Current` is thread-local. It is NOT set during `AssemblyInitializer.Configure()` — avoid code that references it during assembly scanning.

## AssemblyInitializer — Early Startup

For initialization before any node runs:

```csharp
[assembly: AssemblyInitializer(typeof(MyInitialization))]

public class MyInitialization : AssemblyInitializer<MyInitialization>
{
    public override void Configure(AppHost appHost)
    {
        // ONLY register services here
        // Do NOT trigger Subject.OnNext() or access AppHost.Current
        MyConfigService.GetOrCreate(appHost);
    }
}
```

Use two-phase init: register service in `Configure()`, load data in the first `Update()` call.

## Common Global Usings for C# Projects

```csharp
global using VL.Core;
global using VL.Core.Import;
global using VL.Lib.Collections;
```

Required assembly attribute for node discovery:
```csharp
[assembly: ImportAsIs]
```
