# VL File Format — Complete Element Reference

This document provides the full specification of all XML elements, attributes, Choice kinds, and serialization rules for the `.vl` file format. It supplements the overview in [SKILL.md](SKILL.md).

---

## Class Hierarchy (Serialization)

```
Element (base)
├── Compound (has Children)
│   ├── Document
│   ├── Patch
│   ├── Canvas
│   └── NodeOrPatch
│       └── Node
│           └── ProcessDefinition
├── DataHub (has TypeAnnotation, Comment)
│   ├── Pin
│   ├── Pad
│   └── ControlPoint
├── Link
├── Fragment
├── Slot
├── Overlay
└── Dependency (abstract)
    ├── NugetDependency
    ├── DocumentDependency
    ├── PlatformDependency
    ├── ProjectDependency
    └── NodeFactoryDependency
```

---

## Document Element

| Property | XML Form | Description |
|----------|----------|-------------|
| `Id` | Attribute | Unique document ID (base62 GUID) |
| `LanguageVersion` | Attribute | VL language version string |
| `Version` | Attribute | Always `"0.128"` |
| `FilePath` | `<p:FilePath>` | Only written for non-local serialization |
| `Summary` | `<p:Summary>` | Document description |
| `Authors` | `<p:Authors>` or Attribute | Comma-separated author list |
| `Credits` | `<p:Credits>` | Third-party credits |
| `LicenseUrl` | `<p:LicenseUrl>` or Attribute | URL to license |
| `ProjectUrl` | `<p:ProjectUrl>` or Attribute | URL to project |

Direct children: `NugetDependency`, `DocumentDependency`, `PlatformDependency`, `Patch` (exactly one).

---

## Dependency Elements

### NugetDependency

```xml
<NugetDependency Id="..." Location="VL.CoreLib" Version="2024.6.0" />
```

| Attribute | Required | Description |
|-----------|----------|-------------|
| `Id` | Yes | Unique ID |
| `Location` | Yes | NuGet package ID |
| `Version` | No | NuGet version string |

### DocumentDependency

```xml
<DocumentDependency Id="..." Location="./MyOtherFile.vl" />
```

### PlatformDependency

```xml
<PlatformDependency Id="..." Location="VL.Core.dll" />
```

### Common Dependency Attributes

| Attribute | Default | Description |
|-----------|---------|-------------|
| `IsForward` | `false` | Re-export types to consumers |
| `IsFriend` | `false` | Grant friend access |

---

## Patch Element

| Attribute | Required | Description |
|-----------|----------|-------------|
| `Id` | Yes | Unique ID |
| `Name` | No | e.g. `"Create"`, `"Update"`, `"Dispose"`, `"Then"`, `"Split"` |
| `IsGeneric` | No | `"true"` if generic |
| `SortPinsByX` | No | Pin ordering by X position |
| `ManuallySortedPins` | No | Manual pin order |
| `ParticipatingElements` | No | Comma-separated IDs |

---

## Canvas Element

| Attribute | Required | Default | Description |
|-----------|----------|---------|-------------|
| `Id` | Yes | — | Unique ID |
| `Name` | No | — | Sub-canvas category name |
| `Position` | No | `"0,0"` | Position as `"X,Y"` |
| `DefaultCategory` | No | — | Full category name |
| `BordersChecked` | No | `"true"` | Border control points checked |
| `CanvasType` | No | `"Category"` | `Category`, `FullCategory`, or `Group` |

---

## Node Element — Full Attribute List

| Attribute | Required | Description |
|-----------|----------|-------------|
| `Id` | Yes | Unique ID |
| `Name` | No* | Type/operation name (required for definitions) |
| `Bounds` | No | `"X,Y"` or `"X,Y,W,H"` |
| `Category` | No | Category full name |
| `AutoConnect` | No | Auto-connect pins |
| `Aspects` | No | Symbol smell aspects |
| `StructureOfTypeDefinition` | No | `Class`, `Record`, etc. |
| `HideCategory` | No | Hide in node browser |
| `ForwardAllNodesOfTypeDefinition` | No | Forward all nodes for Forward types |
| `HelpFocus` | No | Help priority: `High`, `Low` |
| `Summary` | No | Documentation text (tooltip) |
| `Remarks` | No | Extended documentation |
| `Tags` | No | Search keywords (e.g. `"hittest,picking"`) |

Children: `<p:NodeReference>`, `<Pin>`, `<Patch>`, `<Canvas>`, `<ProcessDefinition>`, `<Slot>`, `<p:TypeAnnotation>`, `<p:Interfaces>`.

---

## NodeReference — All Choice Kinds

### Node Call Kinds (used with NodeFlag)

| Kind | Description |
|------|-------------|
| `NodeFlag` | Base flag for all node calls (first choice, `Fixed="true"`) |
| `ProcessAppFlag` | Process node call (stateful) |
| `OperationCallFlag` | Operation call (stateless) |
| `OperationNode` | Direct .NET static method call |
| `ProcessNode` | Process node reference |

### Definition Kinds

| Kind | Description |
|------|-------------|
| `ContainerDefinition` | Process type definition |
| `ClassDefinition` | Class definition |
| `RecordDefinition` | Record (immutable) definition |
| `InterfaceDefinition` | Interface definition |
| `ForwardDefinition` | Forward type (wrapping .NET mutable type) |
| `ForwardRecordDefinition` | Forward immutable type |
| `OperationDefinition` | Operation definition |
| `ProcessDefinition` | Process node definition |

### Region Kinds

| Kind | Description |
|------|-------------|
| `StatefulRegion` | Base flag for regions (first choice, `Fixed="true"`) |
| `ApplicationStatefulRegion` | If, ForEach, ForLoop, Using, Try, ManageProcess |
| `ProcessStatefulRegion` | Cache region |
| `ApplicationRegion` | Delegate region |

### Type Reference Kinds

| Kind | Description |
|------|-------------|
| `TypeFlag` | Base type reference |
| `ImmutableTypeFlag` | Immutable type |
| `MutableTypeFlag` | Mutable type |

### Category Kinds (for CategoryReference)

| Kind | Description |
|------|-------------|
| `Category` | Category by name |
| `ClassType` | Class type as category |
| `RecordType` | Record type as category |
| `MutableInterfaceType` | Interface type as category |
| `InterfaceType` | Interface type reference |
| `AssemblyCategory` | .NET namespace as category |
| `ArrayType` | Array type (e.g. `Name="MutableArray"`) |

### CategoryReference Attributes

| Attribute | Description |
|-----------|-------------|
| `NeedsToBeDirectParent` | Category must be direct parent |
| `IsGlobal` | Global category lookup |

### NodeReference Attributes

| Attribute | Description |
|-----------|-------------|
| `LastCategoryFullName` | Full category path |
| `LastDependency` | Dependency file/package where node was resolved |
| `LastSymbolSource` | Legacy alias for `LastDependency` (pre-2024) |
| `OverloadStrategy` | e.g. `"AllPinsThatAreNotCommon"` |

---

## Pin Element — Full Attribute List

| Attribute | Required | Default | Description |
|-----------|----------|---------|-------------|
| `Id` | Yes | — | Unique ID |
| `Name` | Yes | — | Pin name |
| `Kind` | Yes | — | `InputPin`, `OutputPin`, `StateInputPin`, `StateOutputPin`, `ApplyPin` |
| `Bounds` | No | — | `"X,Y,W,H"` |
| `DefaultValue` | No | — | Default value as string |
| `Visibility` | No | `"Visible"` | `Visible`, `Optional`, `OnCreateDefault`, `Hidden` |
| `IsHidden` | No | `false` | Hide the pin |
| `Exposition` | No | — | Pin exposition mode |
| `IsPinGroup` | No | `false` | Pin group flag |
| `PinGroupName` | No | — | Pin group name |
| `PinGroupDefaultCount` | No | `0` | Default pin count |
| `PinGroupEditMode` | No | — | Pin group edit mode |

Children: `<p:TypeAnnotation>`, `<p:DefaultValue>`, `<p:Comment>`, `<p:Summary>`, `<p:Remarks>`.

---

## Pad Element — Full Attribute List

| Attribute | Required | Default | Description |
|-----------|----------|---------|-------------|
| `Id` | Yes | — | Unique ID |
| `Bounds` | No | — | `"X,Y,W,H"` |
| `Comment` | No | — | Display label |
| `ShowValueBox` | No | `false` | Show value editor |
| `isIOBox` | No | `false` | IOBox flag (lowercase `i`!) |
| `SlotId` | No | — | Reference to Slot element |
| `Value` | No | — | Serialized value |

Children: `<p:TypeAnnotation>`, `<p:ValueBoxSettings>`.

### ValueBoxSettings

```xml
<p:ValueBoxSettings>
  <p:fontsize p:Type="Int32">9</p:fontsize>
  <p:stringtype p:Assembly="VL.Core" p:Type="VL.Core.StringType">Comment</p:stringtype>
  <p:buttonmode p:Assembly="VL.UI.Forms"
                p:Type="VL.HDE.PatchEditor.Editors.ButtonModeEnum">Bang</p:buttonmode>
</p:ValueBoxSettings>
```

---

## Link Element

| Attribute | Required | Default | Description |
|-----------|----------|---------|-------------|
| `Id` | Yes | — | Unique ID |
| `Ids` | Yes | — | `"sourceId,sinkId"` (output→input) |
| `IsHidden` | No | `false` | Reference link (not drawn) |
| `IsFeedback` | No | `false` | Feedback link (bottom-to-top) |

Links connect Pin, Pad, and ControlPoint IDs.

---

## ProcessDefinition Element

| Attribute | Required | Default | Description |
|-----------|----------|---------|-------------|
| `Id` | Yes | — | Unique ID |
| `IsHidden` | No | `false` | Hide in node browser |
| `HasStateOut` | No | `false` | Explicit state output |

Inherits all Node attributes.

## Fragment Element

| Attribute | Required | Default | Description |
|-----------|----------|---------|-------------|
| `Id` | Yes | — | Unique ID |
| `Patch` | Yes | — | ID of the sibling Patch element |
| `Enabled` | No | — | `"true"` if active |
| `IsDefault` | No | `false` | Default fragment |

---

## Slot Element

| Attribute | Required | Description |
|-----------|----------|-------------|
| `Id` | Yes | Unique ID |
| `Name` | Yes | Field name |

Children: `<p:TypeAnnotation>`, `<p:Value>`, `<p:Summary>`, `<p:Remarks>`.

---

## ControlPoint Element

| Attribute | Required | Description |
|-----------|----------|-------------|
| `Id` | Yes | Unique ID |
| `Bounds` | No | `"X,Y"` (position only) |
| `Name` | No | Display name |
| `Alignment` | No | `Top` or `Bottom` (region border position) |

Children: `<p:TypeAnnotation>`, `<p:Comment>`.

---

## Overlay Element

| Attribute | Required | Description |
|-----------|----------|-------------|
| `Id` | Yes | Unique ID |
| `Bounds` | No | Position/size |
| `Name` | No | Display name |
| `InViewSpace` | No | Whether in view space |

---

## TypeAnnotation Patterns

### Simple

```xml
<p:TypeAnnotation>
  <Choice Kind="TypeFlag" Name="Float32" />
</p:TypeAnnotation>
```

### With Dependency Info

```xml
<p:TypeAnnotation LastCategoryFullName="Primitive" LastDependency="CoreLibBasics.vl">
  <Choice Kind="TypeFlag" Name="Boolean" />
</p:TypeAnnotation>
```

### Generic (with TypeArguments)

```xml
<p:TypeAnnotation LastCategoryFullName="Collections" LastDependency="VL.Collections.vl">
  <Choice Kind="TypeFlag" Name="Spread" />
  <p:TypeArguments>
    <TypeReference LastCategoryFullName="Color" LastDependency="CoreLibBasics.vl">
      <Choice Kind="TypeFlag" Name="RGBA" />
    </TypeReference>
  </p:TypeArguments>
</p:TypeAnnotation>
```

For generic .NET types with multiple type params, use backtick notation: `ImmutableDictionary`2`.

### External .NET Type

```xml
<p:TypeAnnotation LastCategoryFullName="Some.Namespace" LastDependency="SomeAssembly.dll">
  <Choice Kind="TypeFlag" Name="MyTypeName" />
</p:TypeAnnotation>
```

### Interface References

```xml
<p:Interfaces>
  <TypeReference LastCategoryFullName="VL.Skia" LastDependency="VL.Skia.dll">
    <Choice Kind="MutableInterfaceType" Name="IBehavior" />
  </TypeReference>
</p:Interfaces>
```

### PinReference (Overload Disambiguation)

```xml
<p:NodeReference ...>
  <Choice Kind="OperationNode" Name="MyOperation" />
  <PinReference Kind="InputPin" Name="Input">
    <p:DataTypeReference p:Type="TypeReference" LastCategoryFullName="Collections"
                         LastDependency="VL.Collections.vl">
      <Choice Kind="TypeFlag" Name="Spread" />
    </p:DataTypeReference>
  </PinReference>
</p:NodeReference>
```

### Common VL Type Names

| Name | .NET Type |
|------|-----------|
| `Boolean` | `bool` |
| `Byte` | `byte` |
| `Int32` | `int` |
| `Int64` | `long` |
| `Float32` | `float` |
| `Float64` | `double` |
| `String` | `string` |
| `Vector2` | `Vector2` |
| `Vector3` | `Vector3` |
| `Vector4` | `Vector4` |

### Null Values

```xml
<p:Value r:IsNull="true" />
```

Requires `xmlns:r="reflection"` on Document.

### LastDependency vs LastSymbolSource

- `LastDependency` — preferred (2024+)
- `LastSymbolSource` — legacy (pre-2024), both accepted
- `"Builtin"` — sentinel for built-in VL constructs

---

## Property Serialization

### Flat Properties (Attributes)

Simple values: `Id`, `Name`, `Bounds`, `Kind`, `Fixed`, `Position`, booleans, enums, numbers.

### Complex Properties (p: Children)

```xml
<Node ...>
  <p:NodeReference>...</p:NodeReference>
  <p:TypeAnnotation>...</p:TypeAnnotation>
  <p:HelpFocus p:Assembly="VL.Lang" p:Type="VL.Model.HelpPriority">High</p:HelpFocus>
</Node>
```

### Type Disambiguation

`p:Type` and `p:Assembly` attributes identify the .NET type of a property value:

```xml
<p:HelpFocus p:Assembly="VL.Lang" p:Type="VL.Model.HelpPriority">High</p:HelpFocus>
```

---

## Type Definition Patterns

### Process (Most Common)

```xml
<Node Name="MyProcess" Bounds="100,100" Id="...">
  <p:NodeReference>
    <Choice Kind="ContainerDefinition" Name="Process" />
    <CategoryReference Kind="Category" Name="Primitive" />
  </p:NodeReference>
  <Patch Id="...">
    <Canvas Id="..." CanvasType="Group" />
    <Patch Id="createId" Name="Create" />
    <Patch Id="updateId" Name="Update" />
    <ProcessDefinition Id="...">
      <Fragment Id="..." Patch="createId" Enabled="true" />
      <Fragment Id="..." Patch="updateId" Enabled="true" />
    </ProcessDefinition>
  </Patch>
</Node>
```

### Forward (Wrapping .NET Types)

```xml
<Node Name="MyDotNetType" Bounds="100,100" Id="...">
  <p:NodeReference>
    <Choice Kind="ForwardDefinition" Name="Forward" />
    <CategoryReference Kind="Category" Name="Primitive" />
  </p:NodeReference>
  <p:TypeAnnotation LastCategoryFullName="Some.Namespace" LastDependency="SomeAssembly.dll">
    <Choice Kind="TypeFlag" Name="MyDotNetType" />
  </p:TypeAnnotation>
  <p:ForwardAllNodesOfTypeDefinition p:Type="Boolean">true</p:ForwardAllNodesOfTypeDefinition>
  <Patch Id="...">
    <Canvas Id="..." CanvasType="Group" />
    <ProcessDefinition Id="..." IsHidden="true" />
  </Patch>
</Node>
```

---

## Region Patch Names

| Region | Patch Names |
|--------|------------|
| If | `Then` (and optionally `Else`) |
| ForEach | `Create`, `Update`, `Dispose` |
| Cache | `Create`, `Update` |
| Try | `Try`, `Catch` |

---

## Complete Working Example

A program that adds two floats and displays the result:

```xml
<?xml version="1.0" encoding="utf-8"?>
<Document xmlns:p="property" Id="X1y2Z3a4B5c6D7e8F9g0Hi"
          LanguageVersion="2024.6.0" Version="0.128">
  <NugetDependency Id="Y2z3A4b5C6d7E8f9G0h1Ij" Location="VL.CoreLib"
                   Version="2024.6.0" />
  <Patch Id="Z3a4B5c6D7e8F9g0H1i2Jk">
    <Canvas Id="A4b5C6d7E8f9G0h1I2j3Kl" DefaultCategory="Main"
            BordersChecked="false" CanvasType="FullCategory" />
    <Node Name="Application" Bounds="100,100" Id="B5c6D7e8F9g0H1i2J3k4Lm">
      <p:NodeReference>
        <Choice Kind="ContainerDefinition" Name="Process" />
        <CategoryReference Kind="Category" Name="Primitive" />
      </p:NodeReference>
      <Patch Id="C6d7E8f9G0h1I2j3K4l5Mn">
        <Canvas Id="D7e8F9g0H1i2J3k4L5m6No" CanvasType="Group">
          <!-- Add node -->
          <Node Bounds="300,300,65,19" Id="E8f9G0h1I2j3K4l5M6n7Op">
            <p:NodeReference LastCategoryFullName="Primitive.Math"
                             LastDependency="CoreLibBasics.vl">
              <Choice Kind="NodeFlag" Name="Node" Fixed="true" />
              <Choice Kind="OperationCallFlag" Name="+" />
            </p:NodeReference>
            <Pin Id="F9g0H1i2J3k4L5m6N7o8Pq" Name="Input" Kind="InputPin" />
            <Pin Id="G0h1I2j3K4l5M6n7O8p9Qr" Name="Input 2" Kind="InputPin" />
            <Pin Id="H1i2J3k4L5m6N7o8P9q0Rs" Name="Output" Kind="OutputPin" />
          </Node>
          <!-- Input Pad A -->
          <Pad Id="I2j3K4l5M6n7O8p9Q0r1St" Comment="Value A"
               Bounds="200,230,80,20" ShowValueBox="true" isIOBox="true" Value="3.14">
            <p:TypeAnnotation LastCategoryFullName="Primitive"
                              LastDependency="CoreLibBasics.vl">
              <Choice Kind="TypeFlag" Name="Float32" />
            </p:TypeAnnotation>
          </Pad>
          <!-- Input Pad B -->
          <Pad Id="J3k4L5m6N7o8P9q0R1s2Tu" Comment="Value B"
               Bounds="300,230,80,20" ShowValueBox="true" isIOBox="true" Value="2.71">
            <p:TypeAnnotation LastCategoryFullName="Primitive"
                              LastDependency="CoreLibBasics.vl">
              <Choice Kind="TypeFlag" Name="Float32" />
            </p:TypeAnnotation>
          </Pad>
          <!-- Output Pad -->
          <Pad Id="K4l5M6n7O8p9Q0r1S2t3Uv" Comment="Result"
               Bounds="302,370,80,20" ShowValueBox="true" isIOBox="true">
            <p:TypeAnnotation LastCategoryFullName="Primitive"
                              LastDependency="CoreLibBasics.vl">
              <Choice Kind="TypeFlag" Name="Float32" />
            </p:TypeAnnotation>
          </Pad>
        </Canvas>
        <Patch Id="L5m6N7o8P9q0R1s2T3u4Vw" Name="Create" />
        <Patch Id="M6n7O8p9Q0r1S2t3U4v5Wx" Name="Update" />
        <ProcessDefinition Id="N7o8P9q0R1s2T3u4V5w6Xy">
          <Fragment Id="O8p9Q0r1S2t3U4v5W6x7Yz"
                   Patch="L5m6N7o8P9q0R1s2T3u4Vw" Enabled="true" />
          <Fragment Id="P9q0R1s2T3u4V5w6X7y8Za"
                   Patch="M6n7O8p9Q0r1S2t3U4v5Wx" Enabled="true" />
        </ProcessDefinition>
        <!-- Links: Pad A → Input, Pad B → Input 2, Output → Result Pad -->
        <Link Id="Q0r1S2t3U4v5W6x7Y8z9Ab"
              Ids="I2j3K4l5M6n7O8p9Q0r1St,F9g0H1i2J3k4L5m6N7o8Pq" />
        <Link Id="R1s2T3u4V5w6X7y8Z9a0Bc"
              Ids="J3k4L5m6N7o8P9q0R1s2Tu,G0h1I2j3K4l5M6n7O8p9Qr" />
        <Link Id="S2t3U4v5W6x7Y8z9A0b1Cd"
              Ids="H1i2J3k4L5m6N7o8P9q0Rs,K4l5M6n7O8p9Q0r1S2t3Uv" />
      </Patch>
    </Node>
  </Patch>
</Document>
```

---

## Element Serialization Summary

| XML Element | Base Class | Key Attributes | Key p: Children |
|-------------|-----------|----------------|-----------------|
| `Document` | Compound | `Id`, `LanguageVersion`, `Version` | `FilePath`, `Summary`, `Authors` |
| `Patch` | Compound | `Id`, `Name`, `IsGeneric`, `SortPinsByX`, `ManuallySortedPins` | — |
| `Canvas` | Compound | `Id`, `Name`, `Position`, `DefaultCategory`, `CanvasType` | — |
| `Node` | Compound | `Id`, `Name`, `Bounds`, `Category`, `Summary`, `Tags` | `NodeReference`, `TypeAnnotation`, `Interfaces` |
| `ProcessDefinition` | Node | + `IsHidden`, `HasStateOut` | (inherits Node) |
| `Pin` | DataHub | `Id`, `Name`, `Kind`, `DefaultValue`, `Visibility` | `TypeAnnotation`, `DefaultValue` |
| `Pad` | DataHub | `Id`, `Bounds`, `Comment`, `ShowValueBox`, `isIOBox`, `Value` | `TypeAnnotation`, `ValueBoxSettings` |
| `Link` | Element | `Id`, `Ids`, `IsHidden`, `IsFeedback` | — |
| `Fragment` | Element | `Id`, `Patch`, `Enabled`, `IsDefault` | — |
| `Slot` | Element | `Id`, `Name` | `TypeAnnotation`, `Value` |
| `ControlPoint` | DataHub | `Id`, `Bounds`, `Alignment` | `TypeAnnotation` |
| `Overlay` | Element | `Id`, `Bounds`, `Name`, `InViewSpace` | — |

---

## Encoding Notes

- **Numeric values**: InvariantCulture (`.` decimal separator, no thousands)
- **String encoding**: Standard XML escaping; `&lt;` for `<` in values
- **Newlines in comments**: `\r\n`, entitized per XML spec
- **LanguageVersion**: Valid NuGet version string; default `"2024.6.0"` if unknown
