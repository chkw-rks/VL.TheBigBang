# Forwarding .NET Libraries

Forwarding wraps .NET libraries in VL without creating new types — forwarded types remain compatible with the originals.

## When to Forward

- Selectively expose types/operations from a .NET library
- Adjust mutability metadata
- Assign VL categories, rename pins/operations/types
- Set defaults, add unit conversions (e.g., radians to cycles)
- Create process nodes from .NET types
- Manage disposable lifetimes

## Creating a Forward

1. Reference the `.dll` or `.csproj` in the .vl document
2. Create a category in the Definition Patch
3. Either drag-drop from Solution Explorer or create a Process patch with `patch type = 'Forward'` and a type annotation

## Configuration

### Forward All Nodes

Default: on — all operations are forwarded automatically. Override selectively by creating manual forwards for specific operations.

### Mutability Flag

Default: mutable. Mark immutable if:
- Only readonly fields
- All field types are themselves immutable
- Optionally has `With*` methods (copy-and-modify pattern)

### CreateDefault

Implement to prevent null pointer exceptions. Required for types that appear as default pin values.

## Pin Modifications

Within a forwarded operation:

| Action | How |
|---|---|
| **Rename** | Manually create the pin and rename it |
| **Set default** | Create the pin, set default via middle-click or Configure |
| **Hide** | Connect an IOBox directly (overrides auto-forwarding for that pin) |
| **Unit conversion** | Place conversion logic in the forward patch body |

## Signature Management

| Mode | Behavior |
|---|---|
| **Locked** (default) | Pin order by x-position; auto-updates when .NET signature changes |
| **Unlocked** | Manual pin ordering; shows warnings instead of auto-updating |

**Connect to Signature**: Auto-connects forwarded node pins to definition signature. Disable for manual control.

## Non-Standard Event Wrapping

Events not following .NET Core Event Pattern require manual wrapping:

```csharp
using System.Reactive.Linq;

public static IObservable<PackageArgs> PackageArrived(Tablet tablet)
{
    return Observable.FromEvent<Tablet.PacketArrivalEventHandler, PackageArgs>(
        handler => {
            Tablet.PacketArrivalEventHandler paHandler = (x, y, z) =>
                handler(new PackageArgs(x, y, z));
            return paHandler;
        },
        paHandler => tablet.PacketArrival += paHandler,
        paHandler => tablet.PacketArrival -= paHandler);
}
```

## Caching Pattern for Update-Placed Observables

When an Observable is created inside Update (called every frame), cache it:

```csharp
public static IObservable<PackageArgs> PackageArrived(Tablet tablet)
{
    return CachedObservables.GetValue(tablet, x => PackageArrived_((Tablet)x));
}
```

This prevents creating a new subscription every frame.
