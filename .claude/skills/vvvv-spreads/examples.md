# Spread Examples

## Contents

- [Convert ReadOnlySpan to Spread](#convert-readonlyspan-to-spread)
- [Flatten Nested Spreads](#flatten-nested-spreads)
- [Spread with Change Detection in ProcessNode](#spread-with-change-detection-in-processnode)
- [Spread of Configurations](#spread-of-configurations)
- [Interleave Two Spreads](#interleave-two-spreads)

## Convert ReadOnlySpan to Spread

Useful when wrapping native APIs that return spans:

```csharp
public static Spread<T> SpanToSpread<T>(ReadOnlySpan<T> span)
{
    var builder = new SpreadBuilder<T>(span.Length);
    foreach (var item in span)
        builder.Add(item);
    return builder.ToSpread();
}
```

## Flatten Nested Spreads

```csharp
public static Spread<T> Flatten<T>(Spread<Spread<T>> nested)
{
    int total = 0;
    foreach (var inner in nested)
        total += inner.Count;

    var builder = new SpreadBuilder<T>(total);
    foreach (var inner in nested)
        foreach (var item in inner)
            builder.Add(item);
    return builder.ToSpread();
}
```

## Spread with Change Detection in ProcessNode

Pattern for processing spreads only when they change:

```csharp
[ProcessNode]
public class NormalizeSpread
{
    private Spread<float> _lastInput = Spread<float>.Empty;
    private Spread<float> _cachedOutput = Spread<float>.Empty;

    /// <summary>
    /// Normalizes all values to 0..1 range based on min/max of the spread.
    /// </summary>
    public void Update(
        out Spread<float> output,
        Spread<float> input = default)
    {
        input ??= Spread<float>.Empty;

        if (!ReferenceEquals(input, _lastInput))
        {
            if (input.Count == 0)
            {
                _cachedOutput = Spread<float>.Empty;
            }
            else
            {
                float min = float.MaxValue, max = float.MinValue;
                foreach (var v in input)
                {
                    if (v < min) min = v;
                    if (v > max) max = v;
                }

                float range = max - min;
                var builder = new SpreadBuilder<float>(input.Count);
                foreach (var v in input)
                    builder.Add(range > 0 ? (v - min) / range : 0f);
                _cachedOutput = builder.ToSpread();
            }
            _lastInput = input;
        }

        output = _cachedOutput;
    }
}
```

## Spread of Configurations

Common pattern: a Spread of config objects drives a multi-instance system:

```csharp
[ProcessNode]
public class MultiEffectProcessor
{
    private Spread<EffectConfig> _lastConfigs = Spread<EffectConfig>.Empty;
    private List<EffectInstance> _instances = new();

    public void Update(
        out Spread<float> results,
        Spread<EffectConfig> configs = default)
    {
        configs ??= Spread<EffectConfig>.Empty;

        if (!ReferenceEquals(configs, _lastConfigs))
        {
            // Resize instance pool
            while (_instances.Count < configs.Count)
                _instances.Add(new EffectInstance());
            while (_instances.Count > configs.Count)
            {
                _instances[^1].Dispose();
                _instances.RemoveAt(_instances.Count - 1);
            }

            // Apply configs
            for (int i = 0; i < configs.Count; i++)
                _instances[i].Configure(configs[i]);

            _lastConfigs = configs;
        }

        // Always output current results
        var builder = new SpreadBuilder<float>(_instances.Count);
        for (int i = 0; i < _instances.Count; i++)
            builder.Add(_instances[i].CurrentValue);
        results = builder.ToSpread();
    }
}
```

## Interleave Two Spreads

```csharp
public static Spread<T> Interleave<T>(Spread<T> a, Spread<T> b)
{
    var builder = new SpreadBuilder<T>(a.Count + b.Count);
    int max = Math.Max(a.Count, b.Count);
    for (int i = 0; i < max; i++)
    {
        if (i < a.Count) builder.Add(a[i]);
        if (i < b.Count) builder.Add(b[i]);
    }
    return builder.ToSpread();
}
```
