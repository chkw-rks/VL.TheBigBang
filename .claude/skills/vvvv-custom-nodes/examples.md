# Custom Node Examples

Real-world examples from production vvvv gamma projects.

## Contents

- [Config Builder with Hash-Based Change Detection](#config-builder-with-hash-based-change-detection)
- [Resource Loader with Error Handling](#resource-loader-with-error-handling)
- [GPU Resource Manager with State Exposure](#gpu-resource-manager-with-state-exposure)
- [Server Node with Enable/Disable](#server-node-with-enabledisable)
- [Generic Utility Node](#generic-utility-node)
- [Compute Dispatcher with Shader Hot-Reload](#compute-dispatcher-with-shader-hot-reload)
- [Return-Based Output with Field-by-Field Change Detection](#return-based-output-with-field-by-field-change-detection)
- [Rising Edge Trigger (Bang Detection)](#rising-edge-trigger-bang-detection)
- [VL.Fuse Shader Graph Node](#vlfuse-shader-graph-node)

## Config Builder with Hash-Based Change Detection

From a particle simulation — builds configuration only when parameters change:

```csharp
[ProcessNode]
public class ParticleSpecies
{
    private int _lastHash;
    private SpeciesConfiguration? _cachedConfig;

    /// <summary>
    /// Configures a particle species for the simulation system.
    /// </summary>
    public void Update(
        out SpeciesConfiguration config,
        string name = "Default",
        int count = 100,
        float agility = 0.7f,
        float cohesion = 0.5f,
        float groupTightness = 0.8f)
    {
        int currentHash = HashCode.Combine(name, count, agility, cohesion, groupTightness);
        if (currentHash != _lastHash)
        {
            var builder = new SpeciesBuilder(name, count);
            builder.Agility = agility;
            builder.Cohesion = cohesion;
            builder.GroupTightness = groupTightness;
            _cachedConfig = builder.Build();
            _lastHash = currentHash;
        }
        config = _cachedConfig!;
    }
}
```

## Resource Loader with Error Handling

Loads a configuration file with error handling and change detection:

```csharp
[ProcessNode]
public class ConfigFileLoader : IDisposable
{
    private readonly NodeContext _nodeContext;
    private string? _lastPath;
    private string _cachedStatus = "No config";

    public ConfigFileLoader(NodeContext nodeContext)
    {
        _nodeContext = nodeContext;
    }

    /// <summary>
    /// Loads a config file and refreshes available settings.
    /// </summary>
    public void Update(
        out string status,
        out string error,
        string path = "")
    {
        error = null;
        if (path != _lastPath && !string.IsNullOrEmpty(path))
        {
            try
            {
                LoadConfig(path);
                _lastPath = path;
                _cachedStatus = "Loaded";
            }
            catch (Exception ex)
            {
                error = ex.Message;
                _cachedStatus = "Error";
            }
        }
        status = _cachedStatus;
    }

    public void Dispose() { /* release native handles */ }
}
```

## GPU Resource Manager with State Exposure

Exposes node instance for downstream consumption via `HasStateOutput`:

```csharp
[ProcessNode(HasStateOutput = true)]
public class GPUUpscaler : IDisposable
{
    private bool _isInitialized;
    private IntPtr _nativeContext;

    /// <summary>
    /// Manages GPU upscaling context. Connect the State output to UpscalerSource.
    /// </summary>
    public void Update(
        out bool isReady,
        out string error,
        int width = 1920,
        int height = 1080,
        bool enabled = true)
    {
        error = null;
        if (!enabled)
        {
            isReady = false;
            return;
        }

        if (!_isInitialized)
        {
            try
            {
                Initialize(width, height);
                _isInitialized = true;
            }
            catch (Exception ex)
            {
                error = ex.Message;
            }
        }
        isReady = _isInitialized;
    }

    public void Dispose()
    {
        if (_nativeContext != IntPtr.Zero)
        {
            ReleaseNative(_nativeContext);
            _nativeContext = IntPtr.Zero;
        }
        _isInitialized = false;
    }
}
```

## Server Node with Enable/Disable

From a color grading tool — runs a WebSocket server:

```csharp
[ProcessNode]
public class ColorGradingServer : IDisposable
{
    private WebSocketServer? _server;
    private int _lastPort;
    private bool _lastEnabled;

    public ColorGradingServer(NodeContext nodeContext) { }

    /// <summary>
    /// Hosts a WebSocket server for external color grading UI.
    /// </summary>
    public void Update(
        out string status,
        out string lastError,
        int port = 9999,
        bool enabled = true)
    {
        lastError = null;

        if (port != _lastPort || enabled != _lastEnabled)
        {
            _server?.Stop();
            _server = null;

            if (enabled)
            {
                try
                {
                    _server = new WebSocketServer(port);
                    _server.Start();
                }
                catch (Exception ex)
                {
                    lastError = ex.Message;
                }
            }

            _lastPort = port;
            _lastEnabled = enabled;
        }

        status = _server?.IsRunning == true ? $"Running on :{port}" : "Stopped";
    }

    public void Dispose()
    {
        _server?.Stop();
        _server = null;
    }
}
```

## Generic Utility Node

Converts a ReadOnlySpan to a vvvv Spread:

```csharp
public static class SpanUtils
{
    /// <summary>
    /// Converts a ReadOnlySpan to a Spread for use in vvvv.
    /// </summary>
    public static Spread<T> SpanToArray<T>(ReadOnlySpan<T> span)
    {
        var builder = new SpreadBuilder<T>(span.Length);
        foreach (var item in span)
            builder.Add(item);
        return builder.ToSpread();
    }
}
```

## Compute Dispatcher with Shader Hot-Reload

Dispatches compute shaders with automatic recompilation:

```csharp
[ProcessNode]
public class ComputeDispatcher : IDisposable
{
    private ComputeEffect? _effect;
    private int _lastShaderVersion;

    /// <summary>
    /// Dispatches a compute shader on the render device.
    /// </summary>
    public void Update(
        out string error,
        RenderDevice? device = null,
        ShaderStage? computeShader = null,
        int groupsX = 1,
        int groupsY = 1,
        int groupsZ = 1)
    {
        error = null;
        if (device == null || computeShader == null) return;

        _effect ??= new ComputeEffect(device);

        if (computeShader.Version != _lastShaderVersion)
        {
            _effect.SetComputeShader(computeShader);
            _lastShaderVersion = computeShader.Version;
        }

        _effect.Dispatch(groupsX, groupsY, groupsZ);
    }

    public void Dispose()
    {
        _effect?.Dispose();
    }
}
```

## Return-Based Output with Field-by-Field Change Detection

Returns a single value with per-field dirty checking:

```csharp
[ProcessNode(Name = "Noise", Category = "Simulation.Behavior")]
public class Noise
{
    private NoiseMovement? _cachedBehavior;

    /// <summary>
    /// Creates a noise-based movement behavior using 3D Simplex noise.
    /// </summary>
    public IBehavior Update(
        float strength = 2.0f,
        float noiseFrequency = 0.05f,
        float noiseTimeScale = 0.5f,
        int priority = 0)
    {
        if (_cachedBehavior is null ||
            _cachedBehavior.Strength != strength ||
            _cachedBehavior.NoiseFrequency != noiseFrequency ||
            _cachedBehavior.NoiseTimeScale != noiseTimeScale ||
            _cachedBehavior.Priority != priority)
        {
            _cachedBehavior = new NoiseMovement
            {
                Strength = strength,
                NoiseFrequency = noiseFrequency,
                NoiseTimeScale = noiseTimeScale,
                Priority = priority
            };
        }
        return _cachedBehavior;
    }
}
```

## Rising Edge Trigger (Bang Detection)

For boolean inputs that should fire once on the false-to-true transition:

```csharp
[ProcessNode(Name = "RisingEdge", Category = "Animation.Triggers")]
public class RisingEdge
{
    private bool _lastPulse;

    /// <summary>
    /// Sends a one-shot pulse when the trigger goes from false to true.
    /// </summary>
    public void Update(
        string triggerName = "default",
        bool pulse = false)
    {
        if (pulse && !_lastPulse) // Rising edge: false → true
        {
            TriggerRegistry.Pulse(triggerName);
        }
        _lastPulse = pulse;
    }
}
```

## VL.Fuse Shader Graph Node

For nodes that build GPU shader graphs using VL.Fuse:

```csharp
[ProcessNode(Name = "BufferSample", Category = "Fuse.Buffer")]
public class BufferSampleNode
{
    private readonly NodeContext _nodeContext;

    public BufferSampleNode(NodeContext nodeContext)
    {
        _nodeContext = nodeContext;
    }

    /// <summary>
    /// Samples a value from a GPU buffer at the given index.
    /// </summary>
    public void Update(
        out ShaderNode<float> result,
        Buffer? buffer = null,
        ShaderNode<int>? index = null)
    {
        var factory = new NodeSubContextFactory(_nodeContext);
        var bufferInput = new BufferInput(factory.NextSubContext(), buffer);
        var getMember = new GetMember(factory.NextSubContext(), bufferInput, index);
        result = getMember.Output;
    }
}
```
