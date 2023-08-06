from importlib_metadata import version

try:
    # TODO (chiragjn): Why is a try catch even needed here?
    __version__ = version(__name__)
except Exception:
    pass
