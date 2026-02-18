"""
estimator - Tool di stima e analisi dei progetti basato su profili configurabili.

Questo package fornisce:
- il caricamento della configurazione (config_loader)
- la scansione dei progetti (scanner)
- la generazione dei report (report)
- il comando principale eseguibile via `python -m estimator`

Il nucleo del tool è completamente configurabile tramite config.json.
"""

# Metadati del pacchetto
__title__ = "estimator"
__author__ = "Team Engineering"
__version__ = "1.0.0"
__license__ = "Internal"

# Import di convenienza (facilitano eventuale uso programmatico)
from .cli import main
from .config_loader import load_config
from .scanner import count_asset
from .report import (
    print_legend,
    print_project_details,
    print_complexity,
    print_global_summary,
    print_weights_distribution,
    print_team_times
)

__all__ = [
    "main",
    "load_config",
    "count_asset",
    "print_legend",
    "print_project_details",
    "print_complexity",
    "print_global_summary",
    "print_weights_distribution",
    "print_team_times"
]
