# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['keyring_subprocess',
 'keyring_subprocess._internal',
 'keyring_subprocess._vendor',
 'keyring_subprocess._vendor.importlib_metadata',
 'keyring_subprocess._vendor.keyring',
 'keyring_subprocess._vendor.keyring.backends',
 'keyring_subprocess._vendor.keyring.backends.macOS',
 'keyring_subprocess._vendor.keyring.testing',
 'keyring_subprocess._vendor.keyring.util',
 'keyring_subprocess.backend']

package_data = \
{'': ['*']}

extras_require = \
{'sitecustomize': ['sitecustomize-entrypoints']}

entry_points = \
{'keyring.backends': ['keyring-subprocess = '
                      'keyring_subprocess.backend:SubprocessBackend'],
 'sitecustomize': ['keyring-subprocess = '
                   'keyring_subprocess._internal:sitecustomize'],
 'virtualenv.seed': ['keyring-subprocess = '
                     'keyring_subprocess._internal:KeyringSubprocessFromAppData']}

setup_kwargs = {
    'name': 'keyring-subprocess',
    'version': '0.3.0',
    'description': '',
    'long_description': '# keyring-subprocess\nA zero dependency keyring backend that queries an executable `keyring` which can be\nfound on PATH.\n\n## Pros\n- Zero dependencies for a clean `pip list` command and to always be\n  compatible with the rest of your dependencies. Which makes it more\n  suitable to be added to `PYTHONPATH` after installing with Pip\'s\n  `--target` flag.\n- Has [keyring](https://pypi.org/project/keyring) and the minimal required\n  dependencies vendored to make the `chainer` and `null` backends work.\n  - It uses the ModuleSpec apis provided by [PEP451](https://peps.python.org/pep-0451/)\n    to make the vendored `keyring` importable.\n- Provides a `virtualenv` [Seeder](https://virtualenv.pypa.io/en/latest/user_guide.html#seeders)\n  named `keyring-subprocess`.\n  - Set `VIRTUALENV_SEEDER` to `keyring-subprocess` or set `seeder` in the\n    config file to the same value.\n- Provides a `sitecustomize` entry point for the `sitecustomize-entrypoints`\n  package. This can be useful if you install it somewhere that is not a\n  so-called site directory by using Pip\'s `--target` flag.\n  - You can install both `keyring-subprocess` and `sitecustomize-entrypoints`\n    in one go by executing `pip install keyring-subprocess[sitecustomize]`.\n    - `sitecustomize-entrypoints` is required if you if `keyring-subprocess`\n      is installed into a `PYTHONPATH` location.\n\n## Cons\n- It does require `keyring-subprocess` to be installed in the virtual\n  environment associated with the `keyring` executable that is found.\n- Adds, or replaces, points of failures. Depending on how you look at it.\n- Being able to import `keyring`, `importlib_metadata` and `zipp` but\n  `pip list` not listing them might be confusing and not very helpful during\n  debugging.\n\n# Example on Windows\n\nThis is a Powershell script which installs [Pipx](https://pypa.github.io/pipx/)\ninto C:\\Users\\Public\\.local\\pipx.\n- First it sets some environment variables, including `VIRTUALENV_SEEDER`.\n- Then it installs keyring via Pipx and injects artifacts-keyring into\nkeyring\'s virtual environment.\n- Lastly it installs\nkeyring-subprocess and sitecustomize-entrypoints into Pipx\'s shared virtualenv\nwhich Pipx makes sure is available to all of the virtual environments it\nmanages.\n\nWhen using your new Pipx installation to install Poetry or Pipenv the virtual\nenvironment created by virtualenv will contain keyring-subprocess. This should\ncause installing the project dependencies from your private repository to\nsucceed!\n\nAssuming of couse that your private repository requires artifacts-keyring to\nauthenticate, and is therefor a Azure DevOps Artifact Feed. If this is not the\ncase this should be easily fixed by replacing artifacts-keyring by the\npackage that provides the keyring backend that you actually need. \n\n```powershell\n$EnvironmentVariableTarget = $(Read-Host "Target environment (User/Machine) [Machine]").Trim(); `\nif ($EnvironmentVariableTarget -eq "") { `\n  $EnvironmentVariableTarget = "Machine"; `\n} `\nif ($EnvironmentVariableTarget -inotin @("User", "Machine")) { `\n  Write-Host "Invalid option."; `\n} else { `\n  try { `\n    [Environment]::SetEnvironmentVariable("PIPX_HOME", "C:\\Users\\Public\\.local\\pipx", $EnvironmentVariableTarget); `\n    [Environment]::SetEnvironmentVariable("PIPX_BIN_DIR", "C:\\Users\\Public\\.local\\bin", $EnvironmentVariableTarget); `\n    [Environment]::SetEnvironmentVariable("VIRTUALENV_SEEDER", "keyring-subprocess", $EnvironmentVariableTarget); `\n    [Environment]::SetEnvironmentVariable("Path", "C:\\Users\\Public\\.local\\bin;" + [Environment]::GetEnvironmentVariable("Path", $EnvironmentVariableTarget), $EnvironmentVariableTarget); `\n    $PIP_NO_INPUT = $env:PIP_NO_INPUT; `\n    $env:PIP_NO_INPUT = \'1\'; `\n    $env:PIPX_HOME = [Environment]::GetEnvironmentVariable("PIPX_HOME", $EnvironmentVariableTarget); `\n    $env:PIPX_BIN_DIR = [Environment]::GetEnvironmentVariable("PIPX_BIN_DIR", $EnvironmentVariableTarget); `\n    $env:PATH = "C:\\Users\\Public\\.local\\bin;"+$env:PATH; `\n    Set-Location (Get-Item $env:TEMP).FullName; `\n    `\n    <# Use the py executable if it can be found and default to the python executable #> \n    `\n    $py = $(where.exe py python)[0]; `\n    `\n    & $py -m venv .venv; `\n    .\\.venv\\Scripts\\Activate.ps1; `\n    & $py -m pip install -qqq --no-input --isolated --index https://pypi.org/simple/ pipx; `\n    pipx install --pip-args="--no-input --isolated" --index-url https://pypi.org/simple/ pipx; `\n    pipx install --pip-args="--no-input --isolated" --index-url https://pypi.org/simple/ keyring; `\n    pipx inject --pip-args="--no-input --isolated" --index-url https://pypi.org/simple/ keyring artifacts-keyring; `\n    `\n    <# Minor hack since Pipx does not allow us to do this via the cli #> `\n    & "$env:PIPX_HOME\\shared\\Scripts\\pip.exe" install --no-input --isolated --index-url https://pypi.org/simple/ keyring-subprocess[sitecustomize]; `\n    `\n    deactivate; `\n    Remove-Item -path .\\.venv -Recurse -Force `\n  } catch { `\n    throw "Run as Administrator or choose `"User`" as the target environment" `\n  } finally { `\n    $env:PIP_NO_INPUT = $PIP_NO_INPUT; `\n  }\n}\n```\n',
    'author': 'Dos Moonen',
    'author_email': 'darsstar@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://keyring-subprocess.darsstar.dev/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
