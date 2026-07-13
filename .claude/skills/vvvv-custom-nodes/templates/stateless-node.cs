using VL.Lib.Collections;

/// <summary>
/// TODO: Describe what these operations do.
/// Static methods auto-generate nodes — no [ProcessNode] needed.
/// </summary>
public static class MyOperations
{
    /// <summary>
    /// Remaps a value from one range to another.
    /// </summary>
    public static float Remap(float value, float inMin = 0f, float inMax = 1f,
                              float outMin = 0f, float outMax = 1f)
    {
        float t = (value - inMin) / (inMax - inMin);
        return outMin + t * (outMax - outMin);
    }

    /// <summary>
    /// Clamps a value between min and max.
    /// </summary>
    public static float Clamp(float value, float min = 0f, float max = 1f)
    {
        return value < min ? min : value > max ? max : value;
    }
}
