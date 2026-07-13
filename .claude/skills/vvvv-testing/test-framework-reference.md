# VL.TestFramework API Reference

## TestEnvironmentLoader

Entry point for creating test environments.

```csharp
// Load test environment from vvvv installation
// assemblyPath: path to the test assembly (.dll)
// searchPaths: directories to search for VL packages
static TestEnvironment Load(string assemblyPath, IEnumerable<string> searchPaths)
```

The loader:
1. Finds vvvv.exe relative to the assembly path or via the search paths
2. Sets up assembly resolution for VL.Lang, VL.Core, and all dependencies
3. Creates a `TestEnvironmentHost` with a `PackageProvider`
4. Returns a ready-to-use `TestEnvironment`

### Search Path Setup Pattern

```csharp
static readonly ImmutableArray<string> SearchPaths;

static MyTests()
{
    var searchPaths = ImmutableArray.CreateBuilder<string>();
    var currentDir = Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location);
    var gitRoot = GetGitRoot(currentDir); // walks up to find .git directory

    // Order matters - add package sources in dependency order
    searchPaths.Add(Path.Combine(gitRoot, "my-package"));
    searchPaths.Add(Path.Combine(gitRoot, "dependencies"));

    SearchPaths = searchPaths.ToImmutable();
}
```

## TestEnvironment

Manages the test lifecycle. Disposable -- always dispose after tests.

```csharp
// Load and test a VL document for compilation errors
Task LoadAndTestAsync(string filePath, bool runEntryPoint = false)

// Get all discovered packages
IEnumerable<Package> GetPackages()

// Access the underlying host for advanced scenarios
TestEnvironmentHost Host { get; }
```

### LoadAndTestAsync Behavior

When `runEntryPoint: false` (default):
1. Loads the .vl document
2. Compiles all node definitions
3. Checks for compilation errors above `MessageSeverity.Error`
4. Asserts no errors found

When `runEntryPoint: true`:
1. All of the above, plus:
2. Creates a `RuntimeInstance` for the entry point
3. Calls Constructor (Create patch)
4. Calls Update() in a step loop
5. Calls Dispose() for cleanup

## TestEnvironmentHost

Lower-level access to compilation and runtime.

```csharp
// Load and compile a specific document
Task<Document> LoadAndCompileAsync(string filePath)

// Get the target (C#) compilation for a document
Task<TargetCompilation> GetTargetCompilationAsync(string filePath)

// Unload a previously loaded document
void Unload(Document document)

// Access the package provider
PackageProvider PackageProvider { get; }

// Access the type registry
IVLTypeRegistry TypeRegistry { get; }

// Access services
IServiceProvider Services { get; }
```

## TestAppHost

Minimal app host for running tests. Used when executing entry points or test nodes.

```csharp
var appHost = new TestAppHost(host.TypeRegistry, host.Services);
using (appHost.MakeCurrent())
{
    appHost.SetScope(new[] { assembly }, runUserCode: true);
    // Execute test code here
}
```

## Package Discovery

### Package File Structure

```csharp
// Each package has source files, help files, and test files
package.SourceFiles  // Main .vl documents
package.HelpFiles    // help/ folder .vl documents
package.Identity.Id  // Package name (e.g., "VL.MyPackage")
```

### Discovering Test Documents

```csharp
// Find all .vl files in tests/ folders of VL.* packages
public static IEnumerable<string> GetPackageTestDocuments()
{
    return SearchPaths
        .SelectMany(d => Directory.EnumerateDirectories(d, "VL.*"))
        .SelectMany(d => Directory.EnumerateDirectories(d, "tests"))
        .SelectMany(d => Directory.EnumerateFiles(d, "*.vl"));
}
```

### Discovering Test Nodes

Test nodes are process or operation definitions ending in "Test" or "Tests":

```csharp
foreach (var definition in document.AllTopLevelDefinitions
    .Where(n => !n.IsGeneric && n.IsNodeDefinition))
{
    var name = definition.Name.NamePart;
    if (name.EndsWith("Test") || name.EndsWith("Tests"))
    {
        // This is a test node -- compile and execute it
    }
}
```

## Running Test Nodes Programmatically

For process nodes (stateful):
```csharp
var clrType = targetCompilation.GetClrType(process.StateType);
var state = appHost.CreateInstance(clrType);
foreach (var op in process.Operations.Where(o => !o.IsStatic))
{
    var method = clrType.GetMethod(op.MetadataName);
    var arguments = method.GetParameters()
        .Select(p => !p.IsOut ? (p.HasDefaultValue ? p.DefaultValue : appHost.GetDefaultValue(p.ParameterType)) : null)
        .ToArray();
    state = method.Invoke(state, arguments);
}
(state as IDisposable)?.Dispose();
```

For operation nodes (stateless):
```csharp
var clrMethod = targetCompilation.GetClrMethod(op);
var arguments = clrMethod.GetParameters()
    .Select(p => !p.IsOut ? (p.HasDefaultValue ? p.DefaultValue : appHost.GetDefaultValue(p.ParameterType)) : null)
    .ToArray();
clrMethod.Invoke(null, arguments);
```

## Excluding Known-Failing Tests

Use NUnit's `Ignore()` on `TestCaseData`:

```csharp
var testCase = new TestCaseData(packageId, filePath)
    .SetCategory(packageId);

if (ShouldExclude(filePath))
    yield return testCase.Ignore("Reason for exclusion");
else
    yield return testCase;
```

Common exclusion reasons:
- Missing optional dependencies
- Graphics card requirements (GPU-dependent shaders)
- Submodule not checked out
- Known upstream issue awaiting fix

## Complete Test Class Template

```csharp
using System.Collections.Immutable;
using System.IO;
using System.Reflection;
using NUnit.Framework;
using VL.TestFramework;

[TestFixture]
public partial class MyPackageTests
{
    static readonly ImmutableArray<string> SearchPaths;
    TestEnvironment testEnvironment;

    static MyPackageTests()
    {
        var builder = ImmutableArray.CreateBuilder<string>();
        var assemblyDir = Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location)!;
        var gitRoot = FindGitRoot(assemblyDir);
        builder.Add(Path.Combine(gitRoot, "MyPackage"));
        // Add dependency paths as needed
        SearchPaths = builder.ToImmutable();
    }

    [OneTimeSetUp]
    public void Setup()
    {
        testEnvironment = TestEnvironmentLoader.Load(
            typeof(MyPackageTests).Assembly.Location!, SearchPaths);
    }

    [OneTimeTearDown]
    public void TearDown()
    {
        testEnvironment?.Dispose();
        testEnvironment = null;
    }

    [TestCaseSource(nameof(GetDocuments))]
    public async Task DocumentHasNoError(string filePath)
    {
        await testEnvironment.LoadAndTestAsync(filePath);
    }

    [TestCaseSource(nameof(GetTestDocuments))]
    public async Task TestDocumentCompilesAndRuns(string filePath)
    {
        await testEnvironment.LoadAndTestAsync(filePath, runEntryPoint: true);
    }

    public static IEnumerable<TestCaseData> GetDocuments()
    {
        using var env = TestEnvironmentLoader.Load(
            typeof(MyPackageTests).Assembly.Location!, SearchPaths);
        foreach (var p in env.GetPackages())
        {
            foreach (var f in p.SourceFiles.Concat(p.HelpFiles))
            {
                yield return new TestCaseData(f.AbsolutePath)
                    .SetCategory(p.Identity.Id)
                    .SetArgDisplayNames(f.PackagePath);
            }
        }
    }

    public static IEnumerable<string> GetTestDocuments()
    {
        return SearchPaths
            .SelectMany(d => Directory.EnumerateDirectories(d, "VL.*"))
            .SelectMany(d => Directory.EnumerateDirectories(d, "tests"))
            .SelectMany(d => Directory.EnumerateFiles(d, "*.vl"));
    }

    static string FindGitRoot(string dir)
    {
        if (Directory.Exists(Path.Combine(dir, ".git"))) return dir;
        var parent = Path.GetFullPath(Path.Combine(dir, ".."));
        return Directory.Exists(parent) ? FindGitRoot(parent)
            : throw new DirectoryNotFoundException(".git not found");
    }
}
```
