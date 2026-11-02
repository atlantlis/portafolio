#!/usr/bin/env python3
"""LANÏAKEA v2 — Pipeline Académico (Agente_Procesador_Academico).

Estrategia de 4 pasos:
  0 tokens  plomería determinista: scan RAW -> detecta materia -> fusiona frontmatter
  borde     filtro: valida el contrato JSON ANTES de escribir en WIKI
  WIKI      integración: inyecta frontmatter, mueve el archivo a 20_AXÖN
  memoria   idempotente: nunca pisa un archivo existente (sufijo -2)

Uso:
  python3 pipeline_academico.py --scan [--anio 1 --semestre 1] [--materia algebra] \
      [--tipo concepto] [--fase 1_intuicion] [--mover] [--dir <ruta>]
  python3 pipeline_academico.py --nodo <contrato.json> [--mover]
  python3 pipeline_academico.py --validar <contrato.json>

Variables de entorno:
  LANIAKEA_VAULT (raíz del vault; por defecto ./demo_vault)
  ENV_YEAR ('1' o 'y1') · ENV_SEMESTER ('1' o 's1') · ENV_MATERIA (filtro/override en _incoming)

Python 3.12+ · stdlib únicamente · determinista · 0 dependencias
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import unicodedata
from pathlib import Path
from typing import Any

# ── Constantes ───────────────────────────────────────────────────────────
# Raíz del vault: variable LANIAKEA_VAULT o, si no existe, el demo_vault de este repositorio.
VAULT = Path(os.environ.get("LANIAKEA_VAULT", Path(__file__).resolve().parent / "demo_vault"))
RAW_ROOT = VAULT / "10_RAW" / "12_Raw-Academic"
INCOMING = RAW_ROOT / "_incoming"

DESTINOS: dict[str, Path] = {
    "concepto": VAULT / "20_AXÖN" / "23_Wiki-Academic",
    "cuaderno_demostracion": VAULT / "20_AXÖN" / "24_Wiki-Cuaderno",
    "laboratorio_codigo": VAULT / "20_AXÖN" / "26_Wiki-Atlas",
    "log_sistema": VAULT / "20_AXÖN" / "21_Logs",
}
TIPOS = frozenset(DESTINOS)
FASES = frozenset({"1_intuicion", "2_demostracion", "3_examen_socratico"})
FASES_AUTO = FASES | {"auto"}      # 'auto' = enrutador determinista, 0 tokens


def inferir_fase(texto: str) -> str:
    """Enrutador: código -> fase 3 · prueba formal -> fase 2 · resto -> fase 1."""
    if re.search(r"^```", texto, re.MULTILINE):
        return "3_examen_socratico"
    if re.search(r"\b(?:Teorema|Demostración|Demostracion|Prueba|Proposición|Lemma|Corolario|Proof)\b", texto):
        return "2_demostracion"
    return "1_intuicion"
FASE_POR_TIPO: dict[str, str] = {
    "concepto": "1_intuicion",
    "cuaderno_demostracion": "2_demostracion",
    "laboratorio_codigo": "3_examen_socratico",
}
EXT_OK = {".md", ".markdown"}

# ── Utilidades ───────────────────────────────────────────────────────────
def slug(s: str) -> str:
    """NFKD + ASCII + kebab: '303304_Álgebra-I' -> '303304-algebra-i'."""
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-z0-9]+", "-", s.lower())
    return s.strip("-")


def _periodo_env(nombre: str) -> int | None:
    """Lee ENV_YEAR / ENV_SEMESTRE del wrapper Bash: acepta '1' y 'y1'/'s1'."""
    crudo = os.environ.get(nombre)
    if not crudo:
        return None
    m = re.match(r"^[ys]?(\d+)$", crudo.strip().lower())
    return int(m.group(1)) if m else None


def leer_frontmatter(texto: str) -> tuple[dict[str, Any], str]:
    """Devuelve (campos YAML existentes, cuerpo sin frontmatter). No toca nada."""
    if not texto.startswith("---"):
        return {}, texto
    m = re.match(r"^---[ \t]*\n(.*?)\n---[ \t]*(?:\n|$)", texto, re.DOTALL)
    if not m:
        return {}, texto
    fm, cuerpo = m.group(1), texto[m.end():]
    campos: dict[str, Any] = {}
    for linea in fm.splitlines():
        k = re.match(r"^([A-Za-z_][\w-]*):[ \t]*(.*)$", linea)
        if k:
            campos[k.group(1)] = k.group(2).strip()
    return campos, cuerpo


def tags_existentes(campos: dict[str, Any]) -> list[str]:
    """Normaliza tags previos a lista: acepta flow `[a, b]`, bloque `- a` o string."""
    crudo = campos.get("tags", "")
    if isinstance(crudo, list):
        return [t.strip() for t in crudo if t.strip()]
    if isinstance(crudo, str):
        crudo = crudo.strip()
        if crudo.startswith("["):          # flow: [a, b]
            crudo = crudo.strip("[]")
            return [t.strip().strip("\"'") for t in crudo.split(",") if t.strip()]
        if crudo.startswith("-"):          # bloque: "- a"
            return [t.strip().lstrip("- ").strip() for t in crudo.splitlines() if t.strip()]
        if crudo:                          # string suelto
            return [crudo]
    return []


def construir_frontmatter(meta: dict[str, str], previos: list[str], titulo: str) -> str:
    """Frontmatter canónico fusionado: carrera + materia + tags previos (dedup, orden estable)."""
    tags = [f"carrera/{meta['anio_sem']}", f"materia/{slug(meta['materia'])}"]
    for t in previos:
        if t and t not in tags:
            tags.append(t)
    return (
        "---\n"
        f"title: {titulo}\n"
        f"materia: {meta['materia']}\n"
        f"tipo: {meta['tipo']}\n"
        f"fase_spivak: {meta['fase']}\n"
        f"tags: [{', '.join(tags)}]\n"
        "---\n"
    )


# ── Detección de materia ─────────────────────────────────────────────────
def area_y_materia(rel: Path) -> tuple[str, str]:
    """Nivel 1 = área (1_Mathematics); materia = carpeta de curso (prefijo 3-4 dígitos) si existe."""
    partes = rel.parts
    area = partes[0] if partes else "_sin_area"
    materia = area
    for p in partes[1:-1]:                    # excluye área y nombre de archivo
        if re.match(r"^\d{3,4}", p):          # ej. 303002-(1121)_Calculo-I_Diferencial
            materia = p
    if materia == area and len(partes) > 2:   # sin carpeta de curso: usa nivel 2 real
        materia = partes[1]
    return area, materia


def titulo_de(archivo: Path) -> str:
    nombre = archivo.stem
    nombre = re.sub(r"^[\d._-]+", "", nombre).strip(" _-")  # quita prefijos tipo '01_'
    return nombre or archivo.stem


# ── Paso borde: validación del contrato JSON ─────────────────────────────
def validar_nodo(data: Any) -> list[str]:
    """Filtro en el borde: rechaza antes de escribir. Devuelve lista de errores (vacía = OK)."""
    errores: list[str] = []
    if not isinstance(data, dict):
        return ["nodo raíz debe ser objeto JSON"]
    meta = data.get("meta", {})
    if not isinstance(meta, dict) or not meta.get("materia"):
        errores.append("meta.materia obligatorio (string no vacío)")
    tipo = meta.get("tipo", "")
    if tipo not in TIPOS:
        errores.append(f"meta.tipo inválido '{tipo}'. Enums: {sorted(TIPOS)}")
    fase = meta.get("fase_spivak", "")
    if fase and fase not in FASES:
        errores.append(f"meta.fase_spivak inválida '{fase}'. Enums: {sorted(FASES)}")
    intento = meta.get("intento", 1)
    if not isinstance(intento, int) or intento < 1:
        errores.append("meta.intento debe ser entero >= 1 (Ciclo Controlado)")
    elif intento > 3:
        errores.append(f"CICLO_AGOTADO: meta.intento={intento} > 3 -> parada estricta, intervención humana")
    out = data.get("output", {})
    if not isinstance(out, dict) or not out.get("title"):
        errores.append("output.title obligatorio")
    # Fases Spivak: mínimos exigibles por tipo
    if tipo == "concepto" and not out.get("fase_1_intuicion"):
        errores.append("tipo=concepto exige output.fase_1_intuicion")
    if tipo == "cuaderno_demostracion" and not out.get("fase_2_demostracion"):
        errores.append("tipo=cuaderno_demostracion exige output.fase_2_demostracion")
    if tipo == "laboratorio_codigo" and not out.get("verificacion_codigo"):
        errores.append("tipo=laboratorio_codigo exige output.verificacion_codigo")
    # Higiene: campos string no vacíos, sin texto libre redundante
    for clave, valor in out.items():
        if not isinstance(valor, (str, dict)):
            errores.append(f"output.{clave} debe ser string u objeto")
            continue
        if isinstance(valor, str) and (not valor.strip() or len(valor) > 2000):
            errores.append(f"output.{clave} vacío o >2000 chars")
    return errores


# ── Paso WIKI: integración ───────────────────────────────────────────────
def destino_para(tipo: str, materia: str, anio: int) -> Path:
    base = DESTINOS[tipo]
    if tipo == "log_sistema":
        return base / f"y{anio}"
    if tipo == "concepto":
        # resolver carpeta wiki_* REAL (nombres mixtos: wiki_ia, wiki_Business-Admin…)
        s = slug(materia)
        dirs = [d for d in sorted(base.iterdir()) if d.is_dir() and d.name.startswith("wiki")]
        for d in dirs:                       # 1) coincidencia exacta de slug
            resto = slug(d.name)[5:]
            if resto == s:
                return d
        # 2) contención única por tokens (con alias datos<->data)
        alias = {"datos": "data"}          # canonización UNIDIRECCIONAL datos->data
        def tokens(x: str) -> set[str]:
            return {alias.get(t, t) for t in re.findall(r"[a-z0-9]+", x) if re.search(r"[a-z]", t)}
        candidatos = [d for d in dirs if tokens(s) <= tokens(slug(d.name))]
        if len(candidatos) == 1:
            return candidatos[0]
        return base / f"wiki_{s}"            # 3) rama nueva

    return base / slug(materia)


def escribir_nodo(data: dict, mover: bool) -> Path:
    """Valida, construye la nota y la coloca en WIKI. Idempotente."""
    meta = data["meta"]
    out = data["output"]
    fm = construir_frontmatter(
        {"anio_sem": meta.get("anio_semestre", "y1/s1"), "materia": meta["materia"],
         "tipo": meta["tipo"], "fase": meta.get("fase_spivak", FASE_POR_TIPO[meta["tipo"]])},
        meta.get("tags_previos", []), out["title"],
    )
    cuerpo = _cuerpo_desde_nodo(data)
    rama = meta.get("rama") or meta["materia"]           # rama wiki_* destino
    carpeta = destino_para(meta["tipo"], rama, int(meta.get("anio_semestre", "y1/s1").split("/")[0][1:]))
    sub = meta.get("subcarpeta", "").strip("/")          # ej. mathematics/calculus
    if sub:
        carpeta = carpeta / sub
    carpeta.mkdir(parents=True, exist_ok=True)
    destino = carpeta / f"{slug(out['title'])}.md"
    if destino.exists():
        destino = carpeta / f"{slug(out['title'])}-2.md"
    if mover:
        destino.write_text(fm + cuerpo, encoding="utf-8")
    return destino


def _cuerpo_desde_nodo(data: dict) -> str:
    out = data["output"]
    partes = [f"# {out['title']}\n"]
    if "fase_1_intuicion" in out:
        f = out["fase_1_intuicion"]
        partes.append("## Fase 1 · Intuición\n")
        partes.append(f"- **Concepto central:** {f.get('concepto_central', '')}")
        partes.append(f"- **Analogía:** {f.get('analogia', '')}")
        partes.append(f"- **Visualización:** {f.get('visualizacion', '')}\n")
    if "fase_2_demostracion" in out:
        f = out["fase_2_demostracion"]
        partes.append("## Fase 2 · Demostración\n")
        partes.append(f"**Enunciado.** {f.get('enunciado', '')}\n")
        partes.append(f"{f.get('prueba_latex', '')}\n")
    if "verificacion_codigo" in out:
        f = out["verificacion_codigo"]
        partes.append(f"## Verificación en código ({f.get('lenguaje', '')})\n")
        partes.append(f"```{f.get('lenguaje', 'text')}\n{f.get('codigo', '')}\n```\n")
        partes.append("> El código verifica casos; la prueba demuestra todos.\n")
    if "fase_3_examen" in out:
        f = out["fase_3_examen"]
        partes.append("## Fase 3 · Examen Socrático\n")
        partes.append(f"- **Pregunta:** {f.get('pregunta_socratica', '')}")
        partes.append(f"- **Respuesta esperada:** {f.get('respuesta_esperada', '')}\n")
    return "\n".join(partes)


# ── Paso plomería: RAW -> WIKI ───────────────────────────────────────────
def procesar_raw(archivo: Path, anio: int, sem: int, tipo: str, fase: str, mover: bool,
                 filtro: str = "") -> str | None:
    """Escanea un .md de RAW, detecta materia, fusiona frontmatter, mueve a WIKI.
    Devuelve None si el filtro de materia (ENV_MATERIA) lo descarta."""
    rel = archivo.relative_to(RAW_ROOT)
    area, materia = area_y_materia(rel)
    if area == "_incoming" and (materia == "_incoming" or materia == archivo.stem):
        materia = filtro or materia            # archivo suelto en _incoming: ENV_MATERIA manda
    elif filtro and slug(filtro) not in slug(materia):
        return None                            # filtro activo y no coincide: skip
    texto = archivo.read_text(encoding="utf-8")
    if fase == "auto":                       # enrutador: decide sin gastar tokens
        fase = inferir_fase(texto)
    campos, cuerpo = leer_frontmatter(texto)
    previos = tags_existentes(campos)
    fm = construir_frontmatter(
        {"anio_sem": f"y{anio}/s{sem}", "materia": materia, "tipo": tipo, "fase": fase},
        previos, titulo_de(archivo),
    )
    carpeta = destino_para(tipo, materia, anio)
    carpeta.mkdir(parents=True, exist_ok=True)
    destino = carpeta / archivo.name
    if destino.exists():
        destino = carpeta / f"{archivo.stem}-2{archivo.suffix}"
    if mover:
        destino.write_text(fm + cuerpo, encoding="utf-8")
        archivo.unlink()
    return f"{rel} -> {destino.relative_to(VAULT)} [{area} | {materia} | {len(previos)} tags previos]"


# ── CLI ──────────────────────────────────────────────────────────────────
def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description="Pipeline Académico LANÏAKEA v2")
    p.add_argument("--scan", action="store_true", help="plomería: escanear RAW")
    p.add_argument("--dir", type=Path, default=None, help="carpeta a escanear (default: _incoming o RAW completo)")
    p.add_argument("--anio", type=int, default=None, help="año (default: ENV_YEAR, luego 1)")
    p.add_argument("--semestre", type=int, default=None, help="semestre (default: ENV_SEMESTRE, luego 1)")
    p.add_argument("--materia", type=str, default=None, help="filtro: solo esta materia (default: ENV_MATERIA)")
    p.add_argument("--tipo", choices=sorted(TIPOS), default="concepto")
    p.add_argument("--fase", choices=sorted(FASES_AUTO), default=None,
                   help="fase Spivak o 'auto' (enrutador determinista por contenido)")
    p.add_argument("--nodo", type=Path, help="integrar un nodo JSON del contrato")
    p.add_argument("--validar", type=Path, help="solo validar contrato JSON")
    p.add_argument("--mover", action="store_true", help="escribir/mover de verdad (default: dry-run)")
    args = p.parse_args(argv)

    if args.validar:
        data = json.loads(args.validar.read_text(encoding="utf-8"))
        errores = validar_nodo(data)
        print("OK: contrato válido" if not errores else "RECHAZADO:\n  " + "\n  ".join(errores))
        return 0 if not errores else 1

    if args.nodo:
        data = json.loads(args.nodo.read_text(encoding="utf-8"))
        errores = validar_nodo(data)
        if errores:
            print("RECHAZADO (filtro en el borde):\n  " + "\n  ".join(errores), file=sys.stderr)
            return 1
        destino = escribir_nodo(data, args.mover)
        print(f"{'ESCRITO' if args.mover else 'DRY-RUN'} -> {destino.relative_to(VAULT)}")
        return 0

    if args.scan:
        raiz = (args.dir or (INCOMING if INCOMING.exists() else RAW_ROOT)).resolve()
        if not raiz.exists():
            print(f"ERROR: no existe {raiz}", file=sys.stderr)
            return 1
        anio = args.anio if args.anio is not None else (_periodo_env("ENV_YEAR") or 1)
        sem = args.semestre if args.semestre is not None else (_periodo_env("ENV_SEMESTER") or 1)
        filtro = (args.materia or os.environ.get("ENV_MATERIA") or "").strip().lower()
        fase = args.fase or FASE_POR_TIPO[args.tipo]
        n = skip = 0
        for archivo in sorted(raiz.rglob("*.md")):
            if archivo.suffix.lower() not in EXT_OK:
                continue
            if archivo.stem.startswith("_"):   # notas de sistema (_LEEME, _index…)
                skip += 1
                continue
            try:
                resultado = procesar_raw(archivo, anio, sem, args.tipo, fase, args.mover, filtro)
            except UnicodeDecodeError:
                print(f"SKIP (no UTF-8): {archivo}", file=sys.stderr)
                continue
            if resultado is None:
                skip += 1
                continue
            print(resultado)
            n += 1
        print(f"TOTAL: {n} procesados, {skip} filtrados ({'MOVIDOS' if args.mover else 'DRY-RUN'})")
        return 0

    p.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
