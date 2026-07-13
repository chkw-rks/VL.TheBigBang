# Publishing & Help

Creating distributable libraries, help patches, and NuGet publishing.

## Creating a Library (Source NuGet)

For vvvv to recognize a directory as a source NuGet:
- Must be in a configured **package-repository** directory
- Must contain two files sharing the package name: a `.nuspec` and a `.vl` file

### Minimum Required Files

```
VL.MyLibrary/
├── VL.MyLibrary.nuspec
└── VL.MyLibrary.vl
```

### Full Structure

```
VL.MyLibrary/
├── lib/              # Managed .dlls
├── runtimes/         # Native/unmanaged .dlls (architecture-specific)
├── src/              # C# sources
├── help/             # Help patches
├── VL.MyLibrary.nuspec
└── VL.MyLibrary.vl
```

**Critical rule**: No `.vl` file within a package should reference a `.csproj` file — this forces the package into editable mode.

## Help Patches

### File Categories

| Category | Purpose | Example |
|---|---|---|
| Explanation | Library-wide overview | `Explanation Overview of available nodes.vl` |
| HowTo | Specific node combinations | `HowTo Do something.vl` |
| Reference | Coverage of one specific node | `Reference Nodename.vl` |
| Tutorial | Links to video tutorials | `Tutorial Getting started.vl` |
| Example | Broader use-case demos | `Example Something Beautiful.vl` |

### File Naming

Files live under `\help\` with this pattern:
```
\help\Explanation Overview of available nodes.vl
\help\HowTo Do something.vl
\help\Reference Nodename.vl
\help\Example Something Beautiful.vl
```

Subdirectories supported up to two levels:
```
\help\Topic\Subtopic\HowTo Do something.vl
```

### Help.xml (Optional)

Custom ordering and online resource links:
```xml
<Pack>
  <Topic title="Overview">
    <UriItem title="Video Tutorial" link="https://..." mediaType="video"/>
  </Topic>
  <Topic title="Topics">
    <Subtopic title="Images">
      <VLDocument link="Topics\Images\HowTo Draw images.vl" tags="picture render"/>
    </Subtopic>
  </Topic>
</Pack>
```

### Help Flags

- `Ctrl+H` on a node in a HowTo patch: toggles high-priority → low-priority → clear
- **High-priority**: F1 opens this patch for the flagged node
- **Low-priority**: listed in Node Info as related HowTo patches

## Publishing to NuGet

### GitHub Actions Workflow

```yaml
name: push_nuget
on:
  push:
    branches: [main]
    paths-ignore: [README.md]
jobs:
  build:
    runs-on: windows-latest
    steps:
    - uses: actions/checkout@master
    - uses: microsoft/setup-msbuild@v2
    - uses: nuget/setup-nuget@v2.0.0
    - uses: vvvv/PublishVLNuget@1.0.43
      with:
        csproj: src\VL.MyLib.csproj
        nuspec: deployment\VL.MyLib.nuspec
        icon-src: https://example.com/nugeticon.png
        icon-dst: ./nugeticon.png
        nuget-key: ${{ secrets.NUGET_KEY }}
```

### Recommended Repo Structure

```
.github/workflows/main.yml
deployment/VL.MyLib.nuspec
help/Basics/
src/MyLib/
  MyLib.cs
  MyLib.csproj
  MyLib.sln
VL.MyLib.vl
```

### Versioning

- Must follow semver
- Pre-release: append `-alpha` (e.g., `1.0.0-alpha`)
- Version must be bumped for each publish

### Package Visibility

1. Add tag **"VL"** on nuget.org
2. Add to curated `Libraries.xml` at `github.com/vvvv/PublicContent`

### Nuspec Metadata for HelpBrowser

These fields map to vvvv's HelpBrowser display:
- `<id>`, `<description>`, `<authors>`, `<version>`, `<readme>`, `<projectUrl>`, `<repository>`
