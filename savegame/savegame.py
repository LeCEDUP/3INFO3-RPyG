import importlib

def _load_save_game():
    try:
        mod = importlib.import_module('.salvar.salvar_jogo', package=__package__)
        return getattr(mod, 'save_game')
    except Exception:
        pass
    try:
        mod = importlib.import_module('salvar.salvar_jogo')
        return getattr(mod, 'save_game')
    except Exception:
        pass
    try:
        mod = importlib.import_module('..salvar.salvar_jogo', package=__package__)
        return getattr(mod, 'save_game')
    except Exception:
        pass
    raise ImportError("Could not import save_game from salvar.salvar_jogo or relative locations")

save_game = _load_save_game()
def _load_load_game():
    try:
        mod = importlib.import_module('.salvar.salvar_jogo', package=__package__)
        return getattr(mod, 'load_game')
    except Exception:
        pass
    try:
        mod = importlib.import_module('salvar.salvar_jogo')
        return getattr(mod, 'load_game')
    except Exception:
        pass
    try:
        mod = importlib.import_module('..salvar.salvar_jogo', package=__package__)
        return getattr(mod, 'load_game')
    except Exception:
        pass
    raise ImportError("Could not import load_game from salvar.salvar_jogo or relative locations")

load_game = _load_load_game()