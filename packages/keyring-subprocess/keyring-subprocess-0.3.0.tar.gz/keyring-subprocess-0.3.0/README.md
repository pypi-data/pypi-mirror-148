# keyring-subprocess
A zero dependency keyring backend that queries an executable `keyring` which can be
found on PATH.

## Pros
- Zero dependencies for a clean `pip list` command and to always be
  compatible with the rest of your dependencies. Which makes it more
  suitable to be added to `PYTHONPATH` after installing with Pip's
  `--target` flag.
- Has [keyring](https://pypi.org/project/keyring) and the minimal required
  dependencies vendored to make the `chainer` and `null` backends work.
  - It uses the ModuleSpec apis provided by [PEP451](https://peps.python.org/pep-0451/)
    to make the vendored `keyring` importable.
- Provides a `virtualenv` [Seeder](https://virtualenv.pypa.io/en/latest/user_guide.html#seeders)
  named `keyring-subprocess`.
  - Set `VIRTUALENV_SEEDER` to `keyring-subprocess` or set `seeder` in the
    config file to the same value.
- Provides a `sitecustomize` entry point for the `sitecustomize-entrypoints`
  package. This can be useful if you install it somewhere that is not a
  so-called site directory by using Pip's `--target` flag.
  - You can install both `keyring-subprocess` and `sitecustomize-entrypoints`
    in one go by executing `pip install keyring-subprocess[sitecustomize]`.
    - `sitecustomize-entrypoints` is required if you if `keyring-subprocess`
      is installed into a `PYTHONPATH` location.

## Cons
- It does require `keyring-subprocess` to be installed in the virtual
  environment associated with the `keyring` executable that is found.
- Adds, or replaces, points of failures. Depending on how you look at it.
- Being able to import `keyring`, `importlib_metadata` and `zipp` but
  `pip list` not listing them might be confusing and not very helpful during
  debugging.

# Example on Windows

This is a Powershell script which installs [Pipx](https://pypa.github.io/pipx/)
into C:\Users\Public\.local\pipx.
- First it sets some environment variables, including `VIRTUALENV_SEEDER`.
- Then it installs keyring via Pipx and injects artifacts-keyring into
keyring's virtual environment.
- Lastly it installs
keyring-subprocess and sitecustomize-entrypoints into Pipx's shared virtualenv
which Pipx makes sure is available to all of the virtual environments it
manages.

When using your new Pipx installation to install Poetry or Pipenv the virtual
environment created by virtualenv will contain keyring-subprocess. This should
cause installing the project dependencies from your private repository to
succeed!

Assuming of couse that your private repository requires artifacts-keyring to
authenticate, and is therefor a Azure DevOps Artifact Feed. If this is not the
case this should be easily fixed by replacing artifacts-keyring by the
package that provides the keyring backend that you actually need. 

```powershell
$EnvironmentVariableTarget = $(Read-Host "Target environment (User/Machine) [Machine]").Trim(); `
if ($EnvironmentVariableTarget -eq "") { `
  $EnvironmentVariableTarget = "Machine"; `
} `
if ($EnvironmentVariableTarget -inotin @("User", "Machine")) { `
  Write-Host "Invalid option."; `
} else { `
  try { `
    [Environment]::SetEnvironmentVariable("PIPX_HOME", "C:\Users\Public\.local\pipx", $EnvironmentVariableTarget); `
    [Environment]::SetEnvironmentVariable("PIPX_BIN_DIR", "C:\Users\Public\.local\bin", $EnvironmentVariableTarget); `
    [Environment]::SetEnvironmentVariable("VIRTUALENV_SEEDER", "keyring-subprocess", $EnvironmentVariableTarget); `
    [Environment]::SetEnvironmentVariable("Path", "C:\Users\Public\.local\bin;" + [Environment]::GetEnvironmentVariable("Path", $EnvironmentVariableTarget), $EnvironmentVariableTarget); `
    $PIP_NO_INPUT = $env:PIP_NO_INPUT; `
    $env:PIP_NO_INPUT = '1'; `
    $env:PIPX_HOME = [Environment]::GetEnvironmentVariable("PIPX_HOME", $EnvironmentVariableTarget); `
    $env:PIPX_BIN_DIR = [Environment]::GetEnvironmentVariable("PIPX_BIN_DIR", $EnvironmentVariableTarget); `
    $env:PATH = "C:\Users\Public\.local\bin;"+$env:PATH; `
    Set-Location (Get-Item $env:TEMP).FullName; `
    `
    <# Use the py executable if it can be found and default to the python executable #> 
    `
    $py = $(where.exe py python)[0]; `
    `
    & $py -m venv .venv; `
    .\.venv\Scripts\Activate.ps1; `
    & $py -m pip install -qqq --no-input --isolated --index https://pypi.org/simple/ pipx; `
    pipx install --pip-args="--no-input --isolated" --index-url https://pypi.org/simple/ pipx; `
    pipx install --pip-args="--no-input --isolated" --index-url https://pypi.org/simple/ keyring; `
    pipx inject --pip-args="--no-input --isolated" --index-url https://pypi.org/simple/ keyring artifacts-keyring; `
    `
    <# Minor hack since Pipx does not allow us to do this via the cli #> `
    & "$env:PIPX_HOME\shared\Scripts\pip.exe" install --no-input --isolated --index-url https://pypi.org/simple/ keyring-subprocess[sitecustomize]; `
    `
    deactivate; `
    Remove-Item -path .\.venv -Recurse -Force `
  } catch { `
    throw "Run as Administrator or choose `"User`" as the target environment" `
  } finally { `
    $env:PIP_NO_INPUT = $PIP_NO_INPUT; `
  }
}
```
