# Error Catalog

Error message → diagnosis → solution mappings for common vvvv gamma issues.

## C# Compilation Errors

### CS0177: Out parameter must be assigned before control leaves the method

**Cause**: An `out` parameter in Update is not assigned on all code paths.
**Fix**: Always assign all `out` parameters, even in early-return branches.

```csharp
public void Update(out float result, out string error, bool enabled = true)
{
    error = null;
    if (!enabled)
    {
        result = _cached; // Must assign before return
        return;
    }
    // ... rest of logic
    result = _cached;
}
```

### CS0128: Local variable already defined

**Cause**: Duplicate variable name in scope.
**Fix**: Rename or restructure to avoid name collision.

## vvvv Runtime Errors

### NullReferenceException in Update

**Cause**: Accessing a null Spread element or uninitialized field.
**Fix**: Always check `.Count` before indexing Spreads. Initialize fields in constructor.

### IndexOutOfRangeException

**Cause**: Accessing Spread element beyond `.Count - 1`.
**Fix**: Bounds-check before access, or use cyclic indexing pattern:

```csharp
float value = spread.Count > 0 ? spread[index % spread.Count] : 0f;
```

### TypeLoadException / FileLoadException

**Cause**: Assembly version mismatch between your DLL and vvvv's bundled assemblies.
**Fix**: Align NuGet package versions with vvvv's version. Check installed vvvv version and match `VL.Core`, `VL.Stride` versions.

### InvalidOperationException: Collection was modified during enumeration

**Cause**: Modifying a list while iterating over it (common in Parallel.For scenarios).
**Fix**: Use separate read/write buffers, or iterate over a snapshot.

## SDSL Shader Errors

### "unexpected token 'const'"

**Cause**: Using bare `const` at shader root scope.
**Fix**: Use `static const` instead.

### "method X not found in parent"

**Cause**: Trying to override a method that doesn't exist in the parent shader.
**Fix**: Check parent shader for exact method signature. SDSL is case-sensitive.

### "cannot find type/class X"

**Cause**: Missing shader mixin reference or typo in inheritance.
**Fix**: Verify the parent shader file exists and is spelled correctly in the inheritance list.

### Enum shows as integer

**Cause**: Enum binding format is wrong or assembly not found.
**Fix**: Use format `[EnumType("Namespace.EnumName, AssemblyName")]`. Ensure DLL is built and vvvv restarted.

## Performance Issues

### Symptom: High CPU with no visible computation

**Diagnosis**: Missing change detection in ProcessNode.
**Fix**: Add `_lastX != x` checks before expensive work.

### Symptom: GC spikes every few seconds

**Diagnosis**: Allocations in Update loop.
**Fix**: Profile with `dotnet-counters` or Visual Studio diagnostics. Remove `new`, LINQ, string ops from hot path.

### Symptom: GPU frame time high

**Diagnosis**: Branch divergence in shaders or excessive texture sampling.
**Fix**: Use branchless patterns (`step`, `lerp`, `select`). Reduce texture fetches.
