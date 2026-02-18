"""
cli.py

Entry point del tool di stima.
Questo modulo:
- carica la configurazione tramite config_loader
- esegue la scansione dei progetti usando scanner
- raccoglie risultati e totali
- invoca tutte le funzioni di report per produrre l'output finale
"""

import os
import sys

from .config_loader import load_config, ConfigError
from .scanner import count_asset
from .report import (
    cwrite,
    print_legend,
    print_project_details,
    print_complexity,
    print_global_summary,
    print_weights_distribution,
    print_team_times,
    save_html_report
)


def main(config_path: str = "config.json"):
    # -----------------------------------------------------------------------
    # Caricamento e validazione configurazione
    # -----------------------------------------------------------------------
    try:
        cfg = load_config(config_path)
    except ConfigError as e:
        print(f"[CONFIG ERROR] {e}")
        sys.exit(1)

    apps = cfg["apps"]
    ui = cfg["ui"]
    profile_name = cfg["profileName"]
    profile = cfg["profile"]

    weights = profile["weights"]
    default_includes = profile["defaultIncludes"]
    separator_width = int(ui.get("separatorWidth", 120))

    palette = profile.get("palette", [])
    team_sizes = profile.get("teamSizes", [])
    complexity_cfg = profile.get("complexity")
    migration_factor = float(profile.get("migrationTo", {}).get("factor", 1.0))

    # Pre-calcolo label asset
    labels = {
        name: (weights[name].get("label") or name[:8])
        for name in weights
        if weights[name].get("enabled")
    }
    asset_order = list(labels.keys())

    # -----------------------------------------------------------------------
    # Stampa del profilo attivo
    # -----------------------------------------------------------------------
    print()
    cwrite(f"Profilo attivo: {profile_name}", "Cyan")

    # -----------------------------------------------------------------------
    # LEGGENDA PESI
    # -----------------------------------------------------------------------
    print_legend(weights, asset_order, separator_width)

    # -----------------------------------------------------------------------
    # DETTAGLIO PER PROGETTO
    # -----------------------------------------------------------------------
    results = []
    totCounts = {a: 0 for a in asset_order}
    totStima = {a: 0.0 for a in asset_order}
    total = 0.0

    for app in apps:

        if isinstance(app, dict):
            app_name = app.get("name")
            base = app.get("path")
        else:
            app_name = str(app)
            base = os.path.join(app_name, "src")

        if not base or not os.path.exists(base):
            cwrite(f"Path non trovato: {base}", "Red")
            continue

        counts = {}
        for name in asset_order:
            counts[name] = count_asset(base, name, weights, default_includes)

        # calcolo stima singolo progetto
        stime = {name: counts[name] * float(weights[name]["value"]) for name in asset_order}
        project_total = sum(stime.values())

        # salvataggio risultati
        results.append({
            "Project": os.path.basename(app_name),
            "Counts": counts,
            "Stime": stime,
            "TotEst": project_total
        })

        for name in asset_order:
            totCounts[name] += counts[name]
            totStima[name] += stime[name]

        total += project_total

    # stampa tabella dettagliata
    print_project_details(results, asset_order, labels, separator_width)

    # -----------------------------------------------------------------------
    # COMPLESSITÀ (se presente)
    # -----------------------------------------------------------------------
    if complexity_cfg:
        print_complexity(results, complexity_cfg, separator_width)

    # -----------------------------------------------------------------------
    # RIEPILOGO GLOBALE
    # -----------------------------------------------------------------------
    print_global_summary(
        totCounts,
        totStima,
        total,
        asset_order,
        labels,
        len(results),
        separator_width,
        migration_factor
    )

    # -----------------------------------------------------------------------
    # DISTRIBUZIONE STIME
    # -----------------------------------------------------------------------
    print_weights_distribution(
        asset_order,
        totStima,
        total,
        palette,
        separator_width
    )

    # -----------------------------------------------------------------------
    # TEMPI PER TEAM
    # -----------------------------------------------------------------------
    print_team_times(
        total,
        migration_factor,
        team_sizes
    )

    # -----------------------------------------------------------------------
    # HTML REPORT (GENERATO QUI!)
    # -----------------------------------------------------------------------
    save_html_report(
        profile_name=profile_name,
        asset_order=asset_order,
        weights=weights,
        labels=labels,
        results=results,
        totCounts=totCounts,
        totStima=totStima,
        total=total,
        palette=palette,
        migration_factor=migration_factor,
        team_sizes=team_sizes,
        complexity_cfg=complexity_cfg
    )

    cwrite("Report HTML generato: estimator_report.html", "Green")
    print()


# ---------------------------------------------------------------------------
# Esecuzione come script
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    config_path = sys.argv[1] if len(sys.argv) > 1 else "config.json"
    main(config_path)
