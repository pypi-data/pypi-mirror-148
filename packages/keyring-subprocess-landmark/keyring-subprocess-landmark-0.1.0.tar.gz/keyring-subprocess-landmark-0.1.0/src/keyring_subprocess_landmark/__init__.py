__version__ = "0.1.0"


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
