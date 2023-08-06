# Move everything in _cli_objects into the module namespace
# Python Fire will give us access to everything in the module's namespace
# from vinca._cli_objects import *
def run():
    from fire import Fire
    from vinca import _cli_objects
    Fire(component=_cli_objects, name='vinca')
