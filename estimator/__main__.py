"""
__main__.py

Entry point del pacchetto estimator.
Consente l'esecuzione del tool tramite:

    python -m estimator [config.json]

Questo file non contiene logica applicativa: delega tutto al modulo cli.
"""

import sys
from .cli import main


if __name__ == "__main__":
    # Permette: python -m estimator [config.json]
    config_path = sys.argv[1] if len(sys.argv) > 1 else "config.json"
    main(config_path)
