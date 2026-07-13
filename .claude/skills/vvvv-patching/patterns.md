# Patching Patterns Reference

## State Machine Pattern

Use a Process node with an enum-based state:
1. Define states as a C# enum
2. Use Switch region to handle each state
3. Transition states based on input triggers
4. Output current state and state-dependent values

## Configuration-Driven Multi-Instance Pattern

1. Create a configuration Spread (e.g., `Spread<SpeciesConfig>`)
2. Feed it into a ForEach region
3. Each iteration creates/updates an instance
4. Collect results into output Spread

## Dirty-Check Caching Pattern

The most important pattern for C# nodes:
1. Compare current inputs to last-known values
2. Only recompute if something changed
3. Always output the cached result (even when nothing changed)
4. Use `HashCode.Combine()` for multi-input checks

```
Frame 1: inputs=(1,2,3) → compute → cache=(1,2,3,result) → output result
Frame 2: inputs=(1,2,3) → no change → output cached result
Frame 3: inputs=(1,2,4) → compute → cache=(1,2,4,newResult) → output newResult
```

## Resource Lifecycle Pattern

For nodes managing external resources (files, servers, GPU objects):
1. Constructor: acquire resource
2. Update: check if config changed, rebuild if needed, always output status
3. Dispose: release resource
4. Error output pin for diagnostics

## Animation/Interpolation Pattern

1. Use `FrameClock.TimeDifference` for frame-independent animation
2. Lerp between values using normalized time
3. Use dampening for smooth transitions
4. Output both current value and "is animating" flag

## Topology Change Detection

For systems where the number of instances can change:
1. Track previous Spread count
2. On count change: resize pools, reinitialize new instances
3. On config change (same count): update existing instances
4. Use pooling to avoid allocation on resize
