# Service Consumption & Constructor Injection

## Contents
- Service consumption via NodeContext
- IFrameClock access
- Stride Game access
- Logging
- Real-world examples (VL.Rive, VL.IO.Redis)

## Service Consumption via NodeContext

Nodes access library-registered services through `NodeContext`:

```csharp
[ProcessNode]
public class MyNode : IDisposable
{
    private readonly MyService _service;

    public MyNode(NodeContext nodeContext)
    {
        _service = nodeContext.AppHost.Services.GetRequiredService<MyService>();
    }
}
```

For service REGISTRATION patterns (RegisterService, IResourceProvider factories), see vvvv-node-libraries.

## Accessing Frame Clock

`IFrameClock` is the source of truth for frame timing. Two patterns:

**Constructor injection** (VL auto-injects):
```csharp
[ProcessNode]
public class MyAnimatedNode
{
    private readonly IFrameClock _clock;

    public MyAnimatedNode(IFrameClock clock)
    {
        _clock = clock;
    }

    public void Update(out float time)
    {
        time = (float)_clock.Time.Seconds;
    }
}
```

**Via NodeContext**:
```csharp
public MyNode(NodeContext nodeContext)
{
    var clock = nodeContext.FrameClock;
    // Or via services:
    var clock2 = nodeContext.AppHost.Services.GetRequiredService<IFrameClock>();
}
```

Key properties:
- `IFrameClock.Time` — `TimeSpan` of current frame
- `IFrameClock.TimeDifference` — delta time between frames

## Accessing Stride's Game

For nodes that need the Stride rendering engine:

```csharp
[ProcessNode]
public class MyStrideNode : IDisposable
{
    private readonly IResourceHandle<Game> _gameHandle;

    public MyStrideNode(NodeContext nodeContext)
    {
        _gameHandle = nodeContext.AppHost.Services.GetGameHandle();
        var game = _gameHandle.Resource;
        // Access: game.GraphicsDevice, game.Services, game.GameSystems
    }

    public void Dispose() => _gameHandle?.Dispose();
}
```

Or using `GetRequiredService` directly:
```csharp
var graphicsDeviceService = appHost.Services
    .GetRequiredService<Game>()
    .Services.GetService<IGraphicsDeviceService>();
```

Always dispose `IResourceHandle<Game>` — each node gets its own handle.

## Logging

```csharp
public MyNode(NodeContext nodeContext)
{
    var logger = nodeContext.GetLogger();
    logger.LogInformation("Node created");
    logger.LogError("Something went wrong: {Error}", errorMessage);
}
```

## Real-World Examples

### VL.Rive — Renderer Node (Official)

Shows Fragment, constructor injection, IFrameClock, logging:

```csharp
[ProcessNode(HasStateOutput = true, FragmentSelection = FragmentSelection.Explicit)]
[Smell(SymbolSmell.Advanced)]
public sealed partial class RiveRenderer : RendererBase
{
    readonly AppHost appHost;
    readonly ILogger logger;
    IFrameClock frameClock;

    [Fragment]
    public RiveRenderer([Pin(Visibility = Model.PinVisibility.Hidden)] NodeContext nodeContext)
    {
        appHost = nodeContext.AppHost;
        logger = nodeContext.GetLogger();
        frameClock = appHost.Services.GetRequiredService<IFrameClock>();
    }

    [Fragment]
    public void Update(Path? file, string? artboardName, ...)
    {
        // ... change detection, resource loading ...
        riveScene.AdvanceAndApply((float)frameClock.TimeDifference);
    }
}
```

### VL.IO.Redis — Module Pattern (Official)

Shows IModule, Fragment, Channel, service consumption:

```csharp
[ProcessNode(FragmentSelection = FragmentSelection.Explicit, HasStateOutput = true)]
public sealed class RedisClient : IModule, IDisposable
{
    [Fragment]
    public RedisClient(
        [Pin(Visibility = PinVisibility.Hidden)] NodeContext nodeContext,
        [Pin(Visibility = PinVisibility.Optional)] IChannel<...> model)
    {
        _appHost = nodeContext.AppHost;
        var frameClock = _appHost.Services.GetRequiredService<IFrameClock>();
        // Subscribe to frame events for sync
    }
}
```
