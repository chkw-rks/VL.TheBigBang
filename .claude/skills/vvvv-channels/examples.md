# Channel Examples

## Contents

- [Hierarchical Model with CanBePublished](#hierarchical-model-with-canbeublished)
- [Channel Accessor Node — Leaf Parameter](#channel-accessor-node--leaf-parameter)
- [Channel Accessor Node — Indexed Spread Element](#channel-accessor-node--indexed-spread-element)
- [Writing to Channels](#writing-to-channels)
- [Bang Channel Subscription](#bang-channel-subscription)
- [Dynamic Spread Manager Pattern](#dynamic-spread-manager-pattern)
- [Feedback Loop Prevention](#feedback-loop-prevention)
- [Scene Save/Load via Root Channel](#scene-saveload-via-root-channel)

## Hierarchical Model with CanBePublished

A nested model hierarchy where every level is published as channels:

```csharp
using VL.Core.EditorAttributes;
using System.Reactive;

// Group level — standard .NET types work directly as channel values
[CanBePublished(true)]
public class AudioSettings
{
    public float Volume { get; set; } = 0.8f;
    public float Pan { get; set; } = 0.5f;
    public bool Muted { get; set; } = false;
}

// Page level
[CanBePublished(true)]
public class SettingsModel
{
    public AudioSettings Audio { get; } = new();
    public DisplaySettings Display { get; } = new();
}

// Dynamic instance with bang channels
[CanBePublished(true)]
public class SceneItem : IDynamicEntry
{
    [CanBePublished(false)]
    public string InstanceId { get; } = Guid.NewGuid().ToString();

    public float Intensity { get; set; } = 1f;
    public float Speed { get; set; } = 1f;

    // Bang channels for lifecycle management
    public Unit DeleteInstance { get; set; }
    public Unit InsertAfterInstance { get; set; }
    public Unit MoveUpInstance { get; set; }
    public Unit MoveDownInstance { get; set; }
}
```

When `SettingsModel` is published to the "Settings" channel, vvvv automatically creates:

```
Settings                       → SettingsModel
Settings.Audio                 → AudioSettings
Settings.Audio.Volume          → float
Settings.Audio.Pan             → float
Settings.Audio.Muted           → bool
Settings.Display               → DisplaySettings
```

## Channel Accessor Node — Leaf Parameter

A ProcessNode that reads a single typed parameter from a known channel path:

```csharp
[ProcessNode]
public class AudioVolume : IDisposable
{
    private readonly PublicChannelHelper _ch = new();

    /// <summary>Reads the audio volume channel.</summary>
    public void Update(out float value, out IChannel<object>? channel)
    {
        if (!_ch.IsBound)
        {
            var hub = IChannelHub.HubForApp;
            if (hub != null) _ch.TryBind(hub, "Settings.Audio.Volume");
        }
        value = _ch.Channel?.Object is float f ? f : 0f;
        channel = _ch.Channel;
    }

    public void Dispose() => _ch.Dispose();
}
```

## Channel Accessor Node — Indexed Spread Element

For accessing one element from a `Spread<T>` channel by index. Rebinds when the index changes:

```csharp
[ProcessNode]
public class SceneItemAccessor : IDisposable
{
    private PublicChannelHelper _ch = new();
    private int _boundIndex = -1;

    /// <summary>Reads one SceneItem instance by index.</summary>
    public void Update(out SceneItem? value, out IChannel<object>? channel, int index = 0)
    {
        if (index != _boundIndex)
        {
            _ch.Dispose();
            _ch = new();
            _boundIndex = index;
        }
        if (!_ch.IsBound)
        {
            var hub = IChannelHub.HubForApp;
            if (hub != null) _ch.TryBind(hub, $"App.Effects[{index}]");
        }
        value = _ch.Channel?.Object as SceneItem;
        channel = _ch.Channel;
    }

    public void Dispose() => _ch.Dispose();
}
```

## Writing to Channels

All channel writes use `IChannel<object>.Object`:

```csharp
// Write a leaf value
var ch = hub.TryGetChannel("Settings.Audio.Volume");
if (ch != null)
    ch.Object = 0.75f;

// Write a model (all child channels auto-update)
var settingsCh = hub.TryGetChannel("Settings");
if (settingsCh != null)
    settingsCh.Object = newSettingsModel;

// Update a spread (sub-channels auto-update)
var effectsCh = hub.TryGetChannel("App.Effects");
if (effectsCh != null)
{
    var newSpread = modifiedItems.ToArray().AsSpreadUnsafe();
    effectsCh.Object = newSpread;
}

// Update a value directly
if (ch != null)
    ch.Object = 0.9f;
```

## Bang Channel Subscription

Subscribe to `Unit` bang channels to detect delete/insert/move events:

```csharp
private readonly List<IDisposable> _bangSubscriptions = new();
private readonly List<int> _pendingDeletions = new();
private bool _suppressBangs;

private void SubscribeToBangs(IChannelHub hub, string spreadPath, int instanceCount)
{
    // Dispose previous subscriptions
    foreach (var sub in _bangSubscriptions)
        sub.Dispose();
    _bangSubscriptions.Clear();

    for (int i = 0; i < instanceCount; i++)
    {
        string deletePath = $"{spreadPath}[{i}].DeleteInstance";
        var ch = hub.TryGetChannel(deletePath);
        if (ch == null) continue;

        int capturedIndex = i;
        var sub = ch.Subscribe(new BangObserver(() =>
        {
            if (!_suppressBangs)
                _pendingDeletions.Add(capturedIndex);
        }));
        _bangSubscriptions.Add(sub);
    }
}

private sealed class BangObserver : IObserver<object?>
{
    private readonly Action _onBang;
    public BangObserver(Action onBang) => _onBang = onBang;
    public void OnNext(object? value) => _onBang();
    public void OnError(Exception error) { }
    public void OnCompleted() { }
}
```

## Dynamic Spread Manager Pattern

A simplified pattern for managing add/remove/reorder of spread elements via bang channels. The full pattern uses a dedicated manager class per dynamic section:

```csharp
// In Update(), process pending commands (zero cost when idle):
if (_pendingDeletions.Count == 0 && _pendingInsertions.Count == 0)
    return false;  // Nothing to do

// Copy spread into working list
var spread = _spreadChannel.Object as Spread<SceneItem>;
var workingList = new List<SceneItem>(spread);

// Apply deletes (descending order to preserve indices)
_pendingDeletions.Sort();
_pendingDeletions.Reverse();
foreach (int idx in _pendingDeletions)
    if (idx >= 0 && idx < workingList.Count)
        workingList.RemoveAt(idx);

// Apply inserts
foreach (int idx in _pendingInsertions)
{
    int insertAt = Math.Min(idx + 1, workingList.Count);
    workingList.Insert(insertAt, new SceneItem());
}

_pendingDeletions.Clear();
_pendingInsertions.Clear();

// Write new spread back (suppress our own subscription)
_suppressBangs = true;
_spreadChannel.Object = workingList.ToArray().AsSpreadUnsafe();
_suppressBangs = false;

// Rebuild bang subscriptions for new instance set
SubscribeToBangs(hub, spreadPath, workingList.Count);

// Sync count channel
if (_countChannel != null)
    _countChannel.Object = (float)workingList.Count;
```

## Feedback Loop Prevention

When writing to a channel you're also subscribed to, use suppression flags:

```csharp
[ProcessNode]
public class BidirectionalNode : IDisposable
{
    private readonly PublicChannelHelper _ch;
    private bool _suppressFeedback;

    public BidirectionalNode()
    {
        _ch = new(OnValueChanged);
    }

    private void OnValueChanged(object? value)
    {
        if (_suppressFeedback) return;
        // Process external changes...
    }

    public void Update(out float value, float newValue = 0f, bool write = false)
    {
        if (!_ch.IsBound)
        {
            var hub = IChannelHub.HubForApp;
            if (hub != null) _ch.TryBind(hub, "MyApp.SomeValue");
        }

        if (write && _ch.IsBound)
        {
            _suppressFeedback = true;
            _ch.Channel!.Object = newValue;
            _suppressFeedback = false;
        }

        value = _ch.Channel?.Object is float f ? f : 0f;
    }

    public void Dispose() => _ch.Dispose();
}
```

## Scene Save/Load via Root Channel

Serialize/deserialize the entire model hierarchy through the root channel:

```csharp
[ProcessNode]
public class LoadScene : IDisposable
{
    private readonly PublicChannelHelper _ch = new();

    /// <summary>Loads a scene from JSON and pushes it to the root channel.</summary>
    public void Update(out bool success, string filePath = "", bool load = false)
    {
        success = false;

        if (!_ch.IsBound)
        {
            var hub = IChannelHub.HubForApp;
            if (hub != null) _ch.TryBind(hub, "Project");
        }

        if (load && _ch.IsBound && !string.IsNullOrEmpty(filePath) && File.Exists(filePath))
        {
            var json = File.ReadAllText(filePath);
            var model = JsonSerializer.Deserialize<AppModel>(json, serializerOptions);
            if (model != null)
            {
                _ch.Channel!.Object = model;  // ALL sub-channels update automatically
                success = true;
            }
        }
    }

    public void Dispose() => _ch.Dispose();
}
```

Writing to the root "Project" channel propagates to every sub-channel in the hierarchy — no need to iterate individual channels.
