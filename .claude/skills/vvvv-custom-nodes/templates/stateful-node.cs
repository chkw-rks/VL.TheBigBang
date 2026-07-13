using VL.Core;
using VL.Core.Import;

/// <summary>
/// TODO: Describe what this node does (shown as tooltip in vvvv).
/// </summary>
[ProcessNode]
public class MyStatefulNode : IDisposable
{
    // Track previous inputs for change detection
    private float _lastParam1;
    private int _lastParam2;

    // Cached output — always output this, even when no work is done
    private float _cachedResult;

    /// <param name="nodeContext">Provided by the VL runtime</param>
    /// <param name="initialValue">The starting value for the computation</param>
    public MyStatefulNode(NodeContext nodeContext, float initialValue = 0f)
    {
        _cachedResult = initialValue;
    }

    /// <summary>
    /// Called every frame (~60 FPS). Keep fast — zero allocations.
    /// </summary>
    /// <param name="result">The computed result</param>
    /// <param name="error">Error message if something went wrong, null otherwise</param>
    /// <param name="param1">First input value</param>
    /// <param name="param2">Second input value</param>
    public void Update(
        out float result,
        out string error,
        float param1 = 0f,
        int param2 = 0)
    {
        error = null;

        // Change detection — only recompute when inputs change
        if (param1 != _lastParam1 || param2 != _lastParam2)
        {
            _cachedResult = DoWork(param1, param2);
            _lastParam1 = param1;
            _lastParam2 = param2;
        }

        // ALWAYS output cached data
        result = _cachedResult;
    }

    private float DoWork(float a, int b)
    {
        // Expensive computation goes here
        return a * b;
    }

    public void Dispose()
    {
        // Clean up native/unmanaged resources
    }
}
