# Contributing to an Existing vvvv Library

How to change a vvvv gamma library you **don't own** — submitting fixes or features
upstream to a public repo (e.g. `vvvv/VL.StandardLibs`, `VL.Audio`, `VL.Fuse`) rather
than building your own package. For creating a brand-new library, see [SKILL.md](SKILL.md).

The two hard parts are unique to VL: setting up an **editable source package** so you can
patch the library live, and the fact that **`.vl` documents cannot be meaningfully
text-diffed** — which reshapes how PRs must be structured.

## Before You Start

Conventions taken from upstream vvvv `CONTRIBUTING.md` files and the
[graybook contributing guide](https://thegraybook.vvvv.org/reference/extending/contributing.html):

- **Check the license and its implications.** Many vvvv libraries (incl. VL.StandardLibs)
  are **LGPLv3**. Understand what that means for derivative work before contributing.
- **Search existing issues first** to avoid duplicate effort.
- **Discuss architectural changes before coding** — via the project chat or by opening an
  issue. Don't sink time into a large change the maintainers haven't agreed to.
- **Open a draft PR early.** The recommended flow is to create the pull request up front and
  mark it **DRAFT** while you work, then un-draft when ready. This signals intent and invites
  feedback before you've finished.

## Git Workflow: Fork → Branch → PR

Standard fork-based open-source flow ([Git book: Contributing to a Project](https://git-scm.com/book/en/v2/GitHub-Contributing-to-a-Project)):

1. **Fork** the upstream repo to your account/org.
2. Add the upstream as a remote so you can stay current:
   ```
   git remote add upstream https://github.com/vvvv/VL.StandardLibs.git
   git fetch upstream
   ```
3. **Branch off the upstream default branch** (usually `main`) — see the critical warning below.
4. Make one focused change.
5. Push to your fork and **open a PR against upstream**.

### Critical: keep the diff minimal — base on clean upstream `main`

A PR must show **only your change**. The most common failure is branching off an accumulated
downstream/fork branch instead of upstream `main`, so the PR balloons to hundreds of unrelated
files (e.g. *78 files / +68k* for what is really a *1-file / +4* fix). Reviewers can't review that.

- Branch from `upstream/main`, not from a long-lived internal feature branch.
- If your fix already lives on a divergent fork branch, **cherry-pick just that commit onto a
  fresh branch cut from `upstream/main`**:
  ```
  git fetch upstream
  git switch -c pr/my-fix upstream/main
  git cherry-pick <fix-sha>
  ```
- **One PR per distinct add / remove / change.** Don't bundle unrelated fixes.

## The `.vl` Diff Problem (VL-specific, most important)

GitHub shows `.vl` files as opaque XML — there is **no usable visual diff** between two
versions of a patch. The graybook prescribes working around this:

- **Submit separate PRs** for distinct additions, removals, or changes — small and isolated.
- **Keep new functionality in its own `.vl` document** where possible, rather than weaving
  edits through an existing large patch.
- **Describe your changes clearly in words** in the PR body — reviewers rely on prose, not the diff.
- **Include before/after screenshots** of the patch so reviewers can see what changed visually.

For the underlying XML structure (if you must reason about a raw `.vl` diff), see the
`vvvv-fileformat` skill.

## Setting Up an Editable Dev Environment

To edit a library's source live inside vvvv (instead of using its read-only binary nuget):

1. Place the library folder inside a **package-repository** directory (the *parent* folder that
   contains the package directory).
2. Launch vvvv pointing at it and marking the package editable:
   ```
   vvvv.exe --package-repositories "D:\repos" --editable-packages "VL.StandardLibs*"
   ```
   - `--package-repositories` — semicolon-separated *parent* folders to scan for packages.
   - `--editable-packages` — semicolon-separated package names / globs to load from source.
     Source packages are **read-only by default**; this flag makes them editable.
3. **Source beats binary:** vvvv prefers a source package over a binary nuget of the **same
   name**. So you toggle between dev and production simply by adding/removing the source from the
   package-repository path (or the `--editable-packages` list).

> **Recompile warning:** if the scanned tree contains library **submodules** (e.g. a
> `VL.StandardLibs/` checkout), pointing `--package-repositories` at the whole workspace makes
> vvvv discover and **recompile every standard library from source** — many minutes. Point it at
> a specific subfolder that contains only your package, or accept the one-time cost knowingly.

See the `vvvv-startup` skill for full CLI details and the `vvvv-debugging` skill for attaching
a debugger to the editable package and the launch.json setup.

## Build, Test, Verify

- Build the library's `.csproj`; output DLLs land in `lib/net8.0/` (see [SKILL.md](SKILL.md)).
- For C# node changes, see `vvvv-custom-nodes`; for .NET interop, `vvvv-dotnet`.
- For automated package tests, see `vvvv-testing` (VL.TestFramework + NUnit, CI-ready).
- **Verify in vvvv**: with the editable package loaded, confirm the affected node still appears
  in the node browser and behaves correctly (live reload picks up C# rebuilds).

## PR Hygiene Checklist

- [ ] Branch cut from `upstream/main`; diff contains **only** the intended change
- [ ] One logical change per PR
- [ ] `.vl` changes: isolated document(s) + prose description + before/after screenshots
- [ ] Draft PR opened early for visibility
- [ ] License (often LGPLv3) implications understood
- [ ] Existing issues searched; architectural changes discussed first

## References

- Graybook — [Contributing to an existing library](https://thegraybook.vvvv.org/reference/extending/contributing.html)
- Graybook — [Extending vvvv (overview)](https://thegraybook.vvvv.org/reference/extending/overview.html)
- `vvvv-startup` — `--package-repositories` / `--editable-packages` CLI reference
- `vvvv-debugging` — attaching a debugger; submodule recompile warning
- `vvvv-fileformat` — raw `.vl` XML structure
- `vvvv-testing` — automated tests for packages
