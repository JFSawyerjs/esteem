"""
scanner.py

Modulo responsabile della scansione dei file di progetto e del conteggio degli
elementi definiti nel profilo di configurazione.

Qui si trovano:
- funzioni per espandere pattern (ex: "*. {js,ts}" → "*.js", "*.ts")
- funzioni di file walking
- funzioni di matching file con fnmatch
- modalità di conteggio: glob, text, e fallback
- applicazione dei parametri per/per asset come definiti nel profilo

Questo modulo non contiene alcuna logica legata ai linguaggi o ai tipi di progetto:
tutto deriva dalla configurazione passata dal profilo attivo.
"""

import os
import re
import fnmatch
import math
from typing import List, Dict, Any


# ---------------------------------------------------------------------------
# Pattern helpers
# ---------------------------------------------------------------------------

def expand_pattern_list(pat) -> List[str]:
    """
    Espande pattern del tipo "*. {js,ts}" in ["*.js", "*.ts"].
    Accetta una stringa o lista di stringhe.
    """
    if not pat:
        return []
    arr = pat if isinstance(pat, list) else [pat]
    out = []
    for p in arr:
        m = re.match(r"^(.*)\{(.+)\}(.*)$", str(p))
        if m:
            # es: file.{js,ts} → file.js, file.ts
            for e in m.group(2).split(","):
                out.append(m.group(1) + e.strip() + m.group(3))
        else:
            out.append(p)
    return out


# ---------------------------------------------------------------------------
# File iteration and matching
# ---------------------------------------------------------------------------

def iter_files(base_path: str):
    """Itera ricorsivamente nei file di una directory."""
    for root, _, files in os.walk(base_path):
        for f in files:
            yield root, f, os.path.join(root, f)


def file_matches(filename: str, patterns: List[str]) -> bool:
    """Ritorna True se il file combacia con almeno un pattern wildcard."""
    for p in patterns:
        try:
            if fnmatch.fnmatch(filename, p):
                return True
        except:
            pass
    return False


def safe_read(path: str) -> str:
    """Legge un file in modo sicuro senza sollevare eccezioni critiche."""
    try:
        return open(path, "r", encoding="utf-8", errors="ignore").read()
    except:
        return ""


def count_regex_occurrences(path: str, regex_pattern: str) -> int:
    """
    Conta tutte le occorrenze di un pattern regex all'interno di un file.
    """
    try:
        text = safe_read(path)
        return len(re.compile(regex_pattern, re.MULTILINE).findall(text))
    except:
        return 0


# ---------------------------------------------------------------------------
# Core: conteggio asset guidato dal profilo
# ---------------------------------------------------------------------------

def count_asset(base: str, name: str, weights: Dict[str, Any],
                default_includes: List[str]) -> int:
    """
    Conta gli elementi per un asset secondo il profilo.

    Parametri:
    - base: path progetto
    - name: nome asset (es: "Controller")
    - weights: sezione weights del profilo
    - default_includes: wildcard predefiniti del profilo

    Logica configurabile via config:
    - mode: glob | text | fallback
    - pattern: pattern da usare (glob o regex)
    - include: filtri wildcard per limitare i file da analizzare
    - per: divisione finale del conteggio
    - oneIfAny: ritorna 1 se almeno un match

    Ritorna un intero.
    """

    cfg = weights.get(name, {})
    mode = (cfg.get("mode") or "glob").lower()

    patterns = expand_pattern_list(cfg.get("pattern"))
    includes = expand_pattern_list(cfg.get("include"))

    # include effettivi: include specifici o default del profilo
    effective_includes = includes or default_includes

    raw = 0

    # -----------------------------
    # MODE: glob (conta file)
    # -----------------------------
    if mode == "glob":
        pats = patterns or effective_includes
        raw = sum(1 for _, f, _ in iter_files(base) if file_matches(f, pats))

    # -----------------------------
    # MODE: text (conta pattern nei file)
    # -----------------------------
    elif mode == "text":
        # prima seleziono i file rilevanti
        matching_files = [
            fp for _, f, fp in iter_files(base)
            if file_matches(f, effective_includes)
        ]

        # poi conto le occorrenze dei pattern regex
        for pat in patterns:
            raw += sum(count_regex_occurrences(fp, pat) for fp in matching_files)

    # -----------------------------
    # FALLBACK: usa i include
    # -----------------------------
    else:
        pats = patterns or effective_includes
        raw = sum(1 for _, f, _ in iter_files(base) if file_matches(f, pats))

    # -----------------------------
    # applicazione opzioni configurabili
    # -----------------------------
    per = int(cfg.get("per", 1) or 1)
    if cfg.get("oneIfAny"):
        return 1 if raw > 0 else 0

    return int(math.ceil(raw / per))
