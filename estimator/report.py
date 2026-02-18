"""
report.py

Modulo dedicato alla generazione dell'output testuale del tool di analisi.
Qui non si fanno calcoli: tutto ciò che viene stampato è già fornito da altre
parti del sistema (scanner e cli).

Funzionalità principali:
- stampa colorata tramite colorama
- separatori e intestazioni
- tabelle del dettaglio progetti e dei riepiloghi
- calcolo e visualizzazione della distribuzione delle stime
- gestione opzionale della sezione "complessità"
"""

from typing import List, Dict, Any
from colorama import init as colorama_init, Fore, Style

colorama_init(autoreset=True)

# ---------------------------------------------------------------------------
# Color helpers
# ---------------------------------------------------------------------------

COLOR_MAP = {
    "Red": Fore.RED, "DarkRed": Fore.LIGHTRED_EX,
    "Green": Fore.GREEN, "DarkGreen": Fore.LIGHTGREEN_EX,
    "Yellow": Fore.YELLOW, "DarkYellow": Fore.LIGHTYELLOW_EX,
    "Blue": Fore.BLUE, "DarkBlue": Fore.LIGHTBLUE_EX,
    "Magenta": Fore.MAGENTA, "DarkMagenta": Fore.LIGHTMAGENTA_EX,
    "Cyan": Fore.CYAN, "DarkCyan": Fore.LIGHTCYAN_EX,
    "Gray": Fore.LIGHTBLACK_EX, "White": Fore.WHITE,
    "Reset": Style.RESET_ALL
}


def cwrite(text: str, color: str = "Reset", end: str = "\n"):
    """Stampa testo con colore opzionale."""
    prefix = COLOR_MAP.get(color, "")
    reset = COLOR_MAP.get("Reset", "")
    print(f"{prefix}{text}{reset}", end=end)


def print_separator(ch: str = "-", width: int = 120):
    cwrite(ch * width, "DarkCyan")


# ---------------------------------------------------------------------------
# Tabelle e intestazioni
# ---------------------------------------------------------------------------

def build_header_line(asset_names: List[str], labels: Dict[str, str]) -> (str, List[int]):
    """
    Costruisce la riga di intestazione della tabella principale
    e determina la larghezza delle colonne.
    """
    col_widths = [38]  # colonna applicazione
    for a in asset_names:
        col_widths.append(max(7, len(labels.get(a, a[:8]))))
    col_widths.extend([7, 9])  # TotElm, TotStm

    parts = [f"{'Applicazione':<{col_widths[0]}}"]

    for i, a in enumerate(asset_names):
        lbl = labels.get(a, a[:8])
        parts.append(f"| {lbl:>{col_widths[i+1]}}")

    parts.append(f"| {'TotElm':>{col_widths[-2]}}")
    parts.append(f"| {'TotStm':>{col_widths[-1]}}")

    return " ".join(parts), col_widths


def build_row_line(app: str, counts: Dict[str, int], assets: List[str],
                   estimate: float, col_widths: List[int]) -> str:
    """Costruisce una singola riga del dettaglio progetti."""
    parts = [f"{app:<{col_widths[0]}}"]

    for i, a in enumerate(assets):
        parts.append(f"| {counts.get(a, 0):>{col_widths[i+1]}}")

    totElm = sum(counts.get(a, 0) for a in assets)
    parts.append(f"| {totElm:>{col_widths[-2]}}")
    parts.append(f"| {estimate:>{col_widths[-1]}.1f}")

    return " ".join(parts)


# ---------------------------------------------------------------------------
# Report: legenda pesi
# ---------------------------------------------------------------------------

def print_legend(weights: Dict[str, Any], asset_order: List[str], separator_width: int):
    print()
    print_separator("=", separator_width)
    cwrite("==== LEGENDA PESI (gg/u per elemento) ====", "Cyan")
    print_separator("=", separator_width)

    print(f"{'Elemento':<15} | {'Peso':<8} | Descrizione")
    print("-" * 60)

    for name in asset_order:
        w = weights[name]
        val = str(w.get("value", ""))
        desc = w.get("desc", "")
        print(f"{name:<15} | {val:<8} | {desc}")


# ---------------------------------------------------------------------------
# Report: dettaglio progetti
# ---------------------------------------------------------------------------

def print_project_details(results: List[Dict[str, Any]], asset_order: List[str],
                          labels: Dict[str, str], separator_width: int):
    print()
    print_separator("=", separator_width)
    cwrite("==== DETTAGLIO ELEMENTI E STIME PER PROGETTO ====", "Cyan")
    print_separator("=", separator_width)

    header, col_widths = build_header_line(asset_order, labels)
    print(header)
    print("-" * len(header))

    for r in results:
        app = r["Project"]
        counts = r["Counts"]
        estimate = r["TotEst"]
        print(build_row_line(app, counts, asset_order, estimate, col_widths))


# ---------------------------------------------------------------------------
# Report: complessità
# ---------------------------------------------------------------------------

def print_complexity(results: List[Dict[str, Any]], complexity_cfg: Dict[str, Any],
                     separator_width: int):
    if not complexity_cfg:
        return

    print()
    print_separator("=", separator_width)
    cwrite("==== COMPLESSITÀ DEFINITA DAL PROFILO ====", "Cyan")
    print_separator("=", separator_width)

    ratio = complexity_cfg["ratio"]
    num = ratio["numerator"]
    den = ratio["denominator"]
    thresholds = complexity_cfg.get("thresholds", [])

    for r in results:
        numv = r["Counts"].get(num, 0)
        denv = r["Counts"].get(den, 0)
        value = (numv / denv) if denv > 0 else 0.0

        label = "?"
        for th in thresholds:
            op = th.get("op", "<")
            maxv = th.get("max")

            if op == "<" and (maxv is None or value < maxv):
                label = th["label"]
                break
            if op == ">=" and (maxv is not None and value >= maxv):
                label = th["label"]
                break

        cwrite(f"{r['Project']:<36} -> {value:>6.2f} ({label})", "Yellow")


# ---------------------------------------------------------------------------
# Report: riepilogo globale
# ---------------------------------------------------------------------------

def print_global_summary(totCounts: Dict[str, int], totStima: Dict[str, float],
                         total: float, asset_order: List[str],
                         labels: Dict[str, str], n_projects: int,
                         separator_width: int, migration_factor: float):
    print()
    print_separator("=", separator_width)
    cwrite("==== RIEPILOGO GLOBALE ELEMENTI E STIME ====", "Cyan")
    print_separator("=", separator_width)

    header, col_widths = build_header_line(asset_order, labels)
    print(header)
    print("-" * len(header))

    parts = [f"{n_projects} progetti".ljust(col_widths[0])]
    for i, name in enumerate(asset_order):
        parts.append(f"| {totCounts.get(name, 0):>{col_widths[i+1]}}")

    totElmAll = sum(totCounts.values())
    parts.append(f"| {totElmAll:>{col_widths[-2]}}")
    parts.append(f"| {total:>{col_widths[-1]}.1f}")

    print(" ".join(parts))

    if migration_factor != 1.0:
        adj_total = total * migration_factor
        print()
        cwrite(f"Stima complessiva dopo migrazione x{migration_factor}: {adj_total:.1f} gg/u",
               "Cyan")


# ---------------------------------------------------------------------------
# Report: distribuzione stime
# ---------------------------------------------------------------------------

def print_weights_distribution(asset_order: List[str], totStima: Dict[str, float],
                               total: float, palette: List[str], separator_width: int):
    print()
    print_separator("=", separator_width)
    cwrite("==== DISTRIBUZIONE DELLE STIME PER TIPO DI ELEMENTO ====", "Cyan")
    print_separator("=", separator_width)

    print(f"{'Elemento':<15} {'Barra':<45} {'Stima':>10} {'%Totale':>10}")
    print("-" * 80)

    maxVal = max(totStima.values()) if totStima else 0

    for i, name in enumerate(asset_order):
        val = totStima.get(name, 0)
        if val <= 0:
            continue

        perc = (val / total * 100) if total > 0 else 0
        bar = "#" * int(round((val / maxVal) * 40)) if maxVal > 0 else ""
        color = palette[i % len(palette)]

        cwrite(f"{name:<15} {bar:<45} {val:10.1f} {perc:9.1f}%", color)


# ---------------------------------------------------------------------------
# Report: tempi per team
# ---------------------------------------------------------------------------

def print_team_times(total: float, migration_factor: float,
                     team_sizes: List[int]):
    print()
    cwrite("=" * 60, "DarkCyan")
    cwrite("==== STIMA TEMPI IN FUNZIONE DEL NUMERO DI SVILUPPATORI ====", "Cyan")
    cwrite("=" * 60, "DarkCyan")
    print()

    if migration_factor != 1.0:
        cwrite(f"{'Team Size':<15} | {'Base':>10} | {'Migrazione':>12}", "Yellow")
        print("-" * 40)

        adj_total = total * migration_factor
        for t in team_sizes:
            base = int((total + t - 1) // t)
            adj = int((adj_total + t - 1) // t)
            cwrite(f"{('Team da ' + str(t)):<15} | {base:>10} | {adj:>12}", "White")

    else:
        cwrite(f"{'Team Size':<15} | {'Gg/u':>10}", "Yellow")
        print("-" * 28)
        for t in team_sizes:
            days = int((total + t - 1) // t)
            cwrite(f"{('Team da ' + str(t)):<15} | {days:>10}", "White")


import html
import math
from datetime import datetime

def save_html_report(
    profile_name,
    asset_order,
    weights,
    labels,
    results,
    totCounts,
    totStima,
    total,
    palette,
    migration_factor,
    team_sizes,
    complexity_cfg,
    output_path="estimator_report.html"
):
    """
    Genera un report HTML 'premium' coerente con lo stile dell'Estimator.
    Nessuna libreria esterna, solo HTML+CSS inline.
    """

    def esc(x):
        return html.escape(str(x)) if x is not None else ""

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    total_projects = len(results)
    totElmAll = sum(totCounts.values()) if totCounts else 0

    # ------------------------------------------------------------------ #
    # LEGENDA PESI – versione completa
    # ------------------------------------------------------------------ #
    legenda_rows = []
    for a in asset_order:
        w = weights[a]

        legenda_rows.append(f"""
            <tr>
                <td>{esc(a)}</td>
                <td>{esc(labels.get(a, a))}</td>
                <td>{'✓' if w.get('enabled') else '—'}</td>
                <td>{esc(w.get('mode', ''))}</td>
                <td>{esc(', '.join(w.get('pattern', [])))}</td>
                <td>{esc(', '.join(w.get('include', []))) or '—'}</td>
                <td>{esc(w.get('per', 1))}</td>
                <td>{'✓' if w.get('oneIfAny') else '—'}</td>
                <td style="text-align:right;">{w.get('value','')}</td>
            </tr>
        """)

    legenda_html = "\n".join(legenda_rows)


    # ------------------------------------------------------------------ #
    # DETTAGLIO PROGETTI
    # ------------------------------------------------------------------ #
    header_assets = "".join(
        f"<th>{esc(labels.get(a, a))}</th>" for a in asset_order
    )

    project_rows = []
    for r in results:
        counts = r["Counts"]
        totElm = sum(counts.get(a, 0) for a in asset_order)
        asset_cells = "".join(f"<td>{counts.get(a, 0)}</td>" for a in asset_order)
        project_rows.append(
            f"""
            <tr>
                <td>{esc(r['Project'])}</td>
                {asset_cells}
                <td>{totElm}</td>
                <td style="text-align:right;">{r['TotEst']:.1f}</td>
            </tr>
            """
        )
    projects_html = "\n".join(project_rows)

    # ------------------------------------------------------------------ #
    # DISTRIBUZIONE PER ASSET (barre orizzontali)
    # ------------------------------------------------------------------ #
    max_val = max(totStima.values()) if totStima else 0
    dist_rows = []
    for a in asset_order:
        val = totStima[a]
        if val <= 0:
            continue
        perc = (val / total * 100) if total > 0 else 0
        width = int((val / max_val) * 100) if max_val > 0 else 0

        dist_rows.append(
            f"""
            <tr>
                <td>{esc(labels.get(a, a))}</td>
                <td style="width:60%;">
                    <div class="progress">
                        <div class="progress-bar" style="width:{width}%;"></div>
                    </div>
                </td>
                <td style="text-align:right; white-space:nowrap;">
                    {val:.1f} gg/u
                </td>
                <td style="text-align:right; white-space:nowrap;">
                    {perc:.1f}%
                </td>
            </tr>
            """
        )
    dist_html = "\n".join(dist_rows)

    # ------------------------------------------------------------------ #
    # TEMPI PER TEAM
    # ------------------------------------------------------------------ #
    team_rows = []
    for t in team_sizes:
        if t <= 0:
            continue
        base = math.ceil(total / t) if t > 0 else 0
        if migration_factor != 1.0:
            mig = math.ceil((total * migration_factor) / t)
            team_rows.append(
                f"""
                <tr>
                    <td>Team da {t}</td>
                    <td style="text-align:right;">{base}</td>
                    <td style="text-align:right;">{mig}</td>
                </tr>
                """
            )
        else:
            team_rows.append(
                f"""
                <tr>
                    <td>Team da {t}</td>
                    <td style="text-align:right;">{base}</td>
                </tr>
                """
            )
    team_html = "\n".join(team_rows)

    # ------------------------------------------------------------------ #
    # COMPLEXITY (opzionale)
    # ------------------------------------------------------------------ #
    complexity_block = ""
    if complexity_cfg:
        num_key = complexity_cfg["ratio"]["numerator"]
        den_key = complexity_cfg["ratio"]["denominator"]
        thresholds = complexity_cfg.get("thresholds", [])

        def classify(ratio: float) -> str:
            label = "?"
            for th in thresholds:
                op = th.get("op", "<")
                maxv = th.get("max")
                if op == "<" and (maxv is None or ratio < maxv):
                    label = th["label"]
                    break
                if op == ">=" and (maxv is not None and ratio >= maxv):
                    label = th["label"]
                    break
            return label

        rows = []
        for r in results:
            numv = r["Counts"].get(num_key, 0)
            denv = r["Counts"].get(den_key, 0)
            ratio = (numv / denv) if denv > 0 else 0.0
            label = classify(ratio)
            rows.append(
                f"""
                <tr>
                    <td>{esc(r['Project'])}</td>
                    <td style="text-align:right;">{ratio:.2f}</td>
                    <td>{esc(label)}</td>
                </tr>
                """
            )
        rows_html = "\n".join(rows)

        complexity_block = f"""
        <div class="card">
            <div class="card-header">
                <h2>Complexity</h2>
                <span class="badge badge-soft">Ratio {esc(num_key)}/{esc(den_key)}</span>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Progetto</th>
                        <th>Ratio</th>
                        <th>Classe</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
        </div>
        """

    # ------------------------------------------------------------------ #
    # HTML COMPLETO
    # ------------------------------------------------------------------ #
    mig_label = ""
    if migration_factor != 1.0:
        mig_label = f"<span class='badge'>Migrazione × {migration_factor}</span>"

    html_doc = f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<title>Estimator Report – {esc(profile_name)}</title>
<style>
    body {{
        margin: 0;
        font-family: -apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", Roboto, Arial, sans-serif;
        background: #f3f4f6;
        color: #111827;
    }}

    .page {{
        max-width: 1200px;
        margin: 0 auto;
        padding: 32px 40px 40px;
    }}

    .hero {{
        display: flex;
        flex-direction: column;
        gap: 6px;
        margin-bottom: 26px;
    }}

    .hero-title {{
        font-size: 30px;
        font-weight: 600;
        color: #4D606E;
    }}

    .hero-subtitle {{
        font-size: 14px;
        color: #6b7280;
    }}

    .hero-meta {{
        font-size: 13px;
        color: #9ca3af;
    }}

    .badge {{
        display: inline-block;
        padding: 3px 9px;
        border-radius: 999px;
        font-size: 11px;
        font-weight: 500;
        background: #5F7F65;
        color: #f9fafb;
        margin-left: 8px;
    }}

    .badge-soft {{
        background: #D9E2E6;
        color: #4D606E;
        margin-left: 8px;
    }}

    .grid-2 {{
        display: grid;
        grid-template-columns: 2fr 1fr;
        gap: 20px;
        margin-bottom: 20px;
    }}

    .card {{
        background: #ffffff;
        border-radius: 12px;
        padding: 18px 20px 18px;
        box-shadow: 0 2px 4px rgba(15,23,42,0.08);
        margin-bottom: 20px;
    }}

    .card-header {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 10px;
    }}

    .card h2 {{
        margin: 0;
        font-size: 18px;
        color: #4D606E;
    }}

    .card p {{
        margin: 4px 0 8px;
        font-size: 13px;
        color: #6b7280;
    }}

    .kpi-row {{
        display: flex;
        gap: 18px;
        font-size: 13px;
        margin-top: 8px;
    }}

    .kpi {{
        background: #D9E2E6;
        border-radius: 999px;
        padding: 6px 10px;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }}

    .kpi-label {{
        color: #4D606E;
    }}

    .kpi-value {{
        font-weight: 600;
        color: #111827;
    }}

    table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 13px;
        margin-top: 8px;
    }}

    th {{
        text-align: left;
        background: #D9E2E6;
        padding: 6px 8px;
        font-weight: 600;
        color: #4D606E;
        border-bottom: 1px solid #cbd5e1;
    }}

    td {{
        padding: 6px 8px;
        border-bottom: 1px solid #e5e7eb;
        vertical-align: top;
    }}

    .progress {{
        position: relative;
        height: 10px;
        background: #E5EDF0;
        border-radius: 999px;
        overflow: hidden;
    }}

    .progress-bar {{
        height: 100%;
        background: linear-gradient(90deg, #88C6C7, #5F7F65);
    }}

    .small-muted {{
        font-size: 12px;
        color: #9ca3af;
    }}

</style>
</head>
<body>
<div class="page">

    <header class="hero">
        <div class="hero-title">Estimator Report – {esc(profile_name)}</div>
        <div class="hero-subtitle">
            Snapshot della stima per gli asset configurati nel profilo.
            {mig_label}
        </div>
        <div class="hero-meta">
            Generato il {esc(now_str)} · Progetti analizzati: {total_projects} · Totale stima: {total:.1f} gg/u
        </div>
    </header>

    <!-- OVERVIEW ---------------------------------------------------- -->
    <section class="grid-2">
        <div class="card">
            <div class="card-header">
                <h2>Overview</h2>
            </div>
            <p class="small-muted">
                Riepilogo globale della stima e delle dimensioni del portafoglio progetti.
            </p>
            <div class="kpi-row">
                <div class="kpi">
                    <span class="kpi-label">Progetti</span>
                    <span class="kpi-value">{total_projects}</span>
                </div>
                <div class="kpi">
                    <span class="kpi-label">Elementi totali</span>
                    <span class="kpi-value">{totElmAll}</span>
                </div>
                <div class="kpi">
                    <span class="kpi-label">Stima totale</span>
                    <span class="kpi-value">{total:.1f} gg/u</span>
                </div>
            </div>
            {"<p class='small-muted' style='margin-top:10px;'>Con fattore di migrazione × "
              + str(migration_factor) + f": <strong>{(total * migration_factor):.1f} gg/u</strong></p>"
              if migration_factor != 1.0 else ""
            }
        </div>

        <div class="card">
            <div class="card-header">
                <h2>Team & tempi</h2>
            </div>
            <p class="small-muted">
                Stima di durata a seconda della dimensione del team.
            </p>
            <table>
                <thead>
                    <tr>
                        <th>Team</th>
                        <th>Base (gg/u)</th>
                        {("<th>Con migrazione</th>" if migration_factor != 1.0 else "")}
                    </tr>
                </thead>
                <tbody>
                    {team_html}
                </tbody>
            </table>
        </div>
    </section>

    <!-- LEGENDA PESI ------------------------------------------------ -->
    <section class="card">
        <div class="card-header">
            <h2>Legenda Pesi</h2>
        </div>
        <p class="small-muted">
            Ogni asset rappresenta un tipo di elemento conteggiato (file, componenti, occorrenze testuali)
            e viene pesato in giorni/uomo per singola unità.
        </p>
        <table>
            <thead>
                <tr>
                    <th>Chiave</th>
                    <th>Label</th>
                    <th>Enabled</th>
                    <th>Mode</th>
                    <th>Pattern</th>
                    <th>Include</th>
                    <th>Per</th>
                    <th>oneIfAny</th>
                    <th style="text-align:right;">Peso (gg/u)</th>
                </tr>
            </thead>
            <tbody>
                {legenda_html}
            </tbody>
        </table>
    </section>

    <!-- DETTAGLIO PER PROGETTO -------------------------------------- -->
    <section class="card">
        <div class="card-header">
            <h2>Dettaglio per Progetto</h2>
        </div>
        <p class="small-muted">
            Per ogni applicazione vengono riportati i conteggi per asset e la stima complessiva.
        </p>
        <table>
            <thead>
                <tr>
                    <th>Progetto</th>
                    {header_assets}
                    <th>Tot Elem</th>
                    <th style="text-align:right;">Tot Stima (gg/u)</th>
                </tr>
            </thead>
            <tbody>
                {projects_html}
            </tbody>
        </table>
    </section>

    <!-- DISTRIBUZIONE STIME ----------------------------------------- -->
    <section class="card">
        <div class="card-header">
            <h2>Distribuzione Stime per Asset</h2>
        </div>
        <p class="small-muted">
            Peso relativo degli asset sulla stima totale. Le barre mostrano l'incidenza percentuale.
        </p>
        <table>
            <thead>
                <tr>
                    <th>Asset</th>
                    <th>Incidenza</th>
                    <th style="text-align:right;">Stima (gg/u)</th>
                    <th style="text-align:right;">% Totale</th>
                </tr>
            </thead>
            <tbody>
                {dist_html}
            </tbody>
        </table>
    </section>

    {complexity_block}

</div>
</body>
</html>
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_doc)
