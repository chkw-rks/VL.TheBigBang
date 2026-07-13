# SDSL Syntax Rules and Gotchas

## Contents

- [Critical Rules](#critical-rules)
- [Common Mistakes](#common-mistakes)
- [Mixin Composition](#mixin-composition)
- [Compute Shader Pattern](#compute-shader-pattern)
- [DrawFX Pattern](#drawfx-pattern)

## Critical Rules

### 1. static const at Root Scope

```hlsl
// CORRECT — at shader root scope
static const float PI = 3.14159265;
static const float3x3 MY_MATRIX = float3x3(1,0,0, 0,1,0, 0,0,1);

// WRONG — will cause compilation error
const float PI = 3.14159265;  // ERROR at root scope
```

`const` without `static` only works inside functions.

### 2. Semicolon After Shader Class

```hlsl
shader MyShader : FilterBase
{
    // ...
};  // <-- REQUIRED semicolon
```

Missing this causes cryptic compilation errors.

### 3. override Keyword Required

When overriding methods from parent shaders, `override` is mandatory:

```hlsl
shader Child : Parent
{
    override float4 Shading()  // MUST have 'override'
    {
        return base.Shading() * 2.0;
    }
};
```

### 4. stream vs stage

- `stream` — member accessible at every shader stage (VS, PS, GS, etc.)
- `stage` — ensures member is defined only once across all mixins in a composition

```hlsl
stream float3 MyCustomAttribute;  // Per-vertex/pixel data flowing through pipeline
stage float GlobalScale;          // Shared across all mixins, defined once
```

### 5. Variable Initialization

Local variables should be initialized on declaration:

```hlsl
float result = 0.0;  // CORRECT
float result;         // WRONG — may contain garbage
```

### 6. bool Is Valid

Unlike some HLSL compilers, SDSL supports `bool` as a type — no workaround needed.

## Common Mistakes

### Wrong: Redundant Inheritance with VS_PS_Base

`VS_PS_Base` already inherits `ShaderBase, PositionStream4, NormalStream, Transformation`. Do NOT re-inherit these:

```hlsl
// WRONG — Transformation is already in VS_PS_Base
shader Bad : VS_PS_Base, Transformation { ... };

// CORRECT
shader Good : VS_PS_Base { ... };
```

### Wrong: Using const at Root Scope

```hlsl
shader Bad : ComputeVoid
{
    const int N = 16;  // ERROR: use 'static const'
};
```

### Wrong: Missing override

```hlsl
shader Bad : FilterBase
{
    float4 Filter(float4 tex0col)  // ERROR: missing 'override' if parent defines Filter
    {
        return tex0col;
    }
};
```

### Wrong: Enum Binding Format

```hlsl
// WRONG — missing assembly name
[EnumType("MyNamespace.MyEnum")]
int Mode = 0;

// CORRECT
[EnumType("MyNamespace.MyEnum, MyAssemblyName")]
int Mode = 0;
```

### Wrong: Branch-Heavy GPU Code

```hlsl
// BAD — causes GPU thread divergence
if (uv.x > 0.5)
    color = expensive_function_a(color);
else
    color = expensive_function_b(color);

// GOOD — both paths execute, blend result
float3 a = expensive_function_a(color);
float3 b = expensive_function_b(color);
color = lerp(b, a, step(0.5, uv.x));
```

## Mixin Composition

Shaders compose via mixins (multiple inheritance):

```hlsl
// Define a utility mixin
shader ColorUtils
{
    float3 GammaToLinear(float3 c)
    {
        return pow(max(c, 0.0), 2.2);
    }

    float3 LinearToGamma(float3 c)
    {
        return pow(max(c, 0.0), 1.0 / 2.2);
    }
};

// Use it
shader MyEffect_TextureFX : FilterBase, ColorUtils
{
    float4 Filter(float4 tex0col)
    {
        float3 linear = GammaToLinear(tex0col.rgb);
        // process in linear space...
        return float4(LinearToGamma(linear), tex0col.a);
    }
};
```

## Compute Shader Pattern

```hlsl
shader MyCompute_ComputeFX : ComputeVoid
{
    RWStructuredBuffer<float4> OutputBuffer;
    int Count;

    override void Compute()
    {
        uint id = streams.DispatchThreadId.x;
        if (id >= (uint)Count) return;

        OutputBuffer[id] = float4(id / (float)Count, 0, 0, 1);
    }
};
```

## DrawFX Pattern

```hlsl
shader MyDraw_DrawFX : VS_PS_Base
{
    float Scale = 1.0;

    override stage void VSMain()
    {
        streams.Position = float4(streams.Position.xyz * Scale, 1);
        base.VSMain();
    }

    override stage void PSMain()
    {
        streams.ColorTarget = float4(1, 0, 0, 1);  // Solid red
    }
};
```
