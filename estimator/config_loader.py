"""
config_loader.py

Questo modulo gestisce il caricamento e la validazione del file di configurazione.
Il suo scopo è isolare completamente la logica di lettura di config.json dal resto
del codice, così che tutte le altre parti del sistema possano basarsi su un oggetto
'profilo attivo' già validato e coerente.

Funzionalità principali:
- Lettura di config.json
- Verifica della struttura minima richiesta
- Selezione del profilo attivo (activeProfile)
- Restituzione di un oggetto di configurazione pronto all'uso
"""

import json
import os
import sys
from typing import Dict, Any


class ConfigError(Exception):
    """Errore di validazione della configurazione."""
    pass


def load_config(path: str = "config.json") -> Dict[str, Any]:
    """
    Carica e valida config.json, restituendo un dizionario contenente:
    - config generale
    - profilo attivo già estratto
    - weights, palette, defaultIncludes, teamSizes, complexity, migrationTo

    Se qualcosa non va, solleva ConfigError.
    """

    if not os.path.exists(path):
        raise ConfigError(f"File di configurazione non trovato: {path}")

    try:
        with open(path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except Exception as e:
        raise ConfigError(f"Errore nel parsing di {path}: {e}")

    # Verifica presenza profili
    profiles = config.get("profiles")
    if not profiles or not isinstance(profiles, dict):
        raise ConfigError("La configurazione deve contenere una sezione 'profiles'.")

    # Determinazione profilo attivo
    active_name = config.get("activeProfile")
    if not active_name:
        raise ConfigError("La configurazione deve definire 'activeProfile'.")
    if active_name not in profiles:
        raise ConfigError(f"Profilo attivo '{active_name}' non esistente nei profiles.")

    profile = profiles[active_name]

    # Controllo pesi
    weights = profile.get("weights", {})
    if not weights or not isinstance(weights, dict):
        raise ConfigError(f"Il profilo '{active_name}' non contiene una sezione 'weights' valida.")
    enabled_assets = [k for k, v in weights.items() if v.get("enabled")]
    if not enabled_assets:
        raise ConfigError(f"Il profilo '{active_name}' non ha asset abilitati.")

    # Normalizzazione parametri
    profile.setdefault("defaultIncludes", ["*.*"])
    profile.setdefault("palette", ["Green", "Cyan", "Yellow", "Blue", "Magenta", "Gray"])
    profile.setdefault("teamSizes", [1, 2, 3, 4])
    profile.setdefault("migrationTo", {"factor": 1.0})

    # Restituiamo un oggetto config “flattened”: generale + profilo attivo
    resolved = {
        "apps": config.get("apps", []),
        "ui": config.get("ui", {}),
        "profileName": active_name,
        "profile": profile
    }

    return resolved
