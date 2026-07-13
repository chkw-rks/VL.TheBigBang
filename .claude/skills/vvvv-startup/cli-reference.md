# vvvv Command-Line Arguments Reference

## Named Arguments

| Argument | Short | Default | Description |
|----------|-------|---------|-------------|
| `--open` | `-o` | | Semi-colon separated list of .vl files to open |
| `--settings` | | | Settings file to load |
| `--layout` | | | Window layout file to restore |
| `--allowmultiple` | `-m` | false | Allow multiple vvvv instances to run simultaneously |
| `--nocache` | | false | Re-compile all packages from source instead of using cached assemblies |
| `--noextensions` | | false | Don't load editor extensions (*.HDE.pkg) |
| `--disable-backend` | | false | Don't generate C# code (faster startup, no code gen) |
| `--debug` | | false | Always emit debug symbols for all compiled code |
| `--disable-package-compiler` | | false | Load all packages from source instead of pre-compiled |
| `--editable-packages` | | | Semi-colon separated package names or glob patterns to load from source (e.g., `VL.MyLib*`) |
| `--nuget-path` | | | Custom primary NuGet package repository folder (replaces global package folder) |
| `--package-repositories` | | | Semi-colon separated package repository paths. Each path is a **parent folder** containing package directories. Required together with `--editable-packages` for loading local packages from source. |
| `--export-package-sources` | | | Package sources used during export |
| `--expose-pins` | | false | Show the pin exposure feature in the editor |
| `--enable-attributes-editor` | | false | Show the experimental attributes editor context menu |
| `--check-solution` | | false | Validate the committed solution on startup |
| `--stoppedonstartup` | | false | Don't start the runtime on startup (program is paused) |
| `--log` | | false | Enable logging to `%USERPROFILE%\Documents\vvvv\gamma\vvvv.log` |
| `--no-splash` | | false | Skip the splash screen on startup |

Note: `--no-splash` is parsed separately (not via CommandLineParser) in `GammaSplashForm.SplashAllowed()`.
