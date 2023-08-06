try:
    import keyring
except ImportError:
    import sys
    from ._loader import KeyringSubprocessFinder

    sys.meta_path.append(KeyringSubprocessFinder())

try:
    import virtualenv
    from ._seeder import KeyringSubprocessFromAppData
except ImportError:
    pass


def sitecustomize() -> None:
    pass


class KeyringEntryPointNotFoundError(Exception):
    pass


def keyring_subprocess():
    try:
        from importlib import metadata
    except ImportError:
        import importlib_metadata as metadata

    eps = metadata.entry_points(group="console_scripts")

    if "keyring" not in eps.names:
        raise KeyringEntryPointNotFoundError(
            "No 'keyring' entry point found in the 'console_scripts' group, is keyring installed?"
        )

    keyring = eps["keyring"].load()

    return keyring()
