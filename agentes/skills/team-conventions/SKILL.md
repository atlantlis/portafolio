---
name: team-conventions
description: Convenciones del equipo LANÏAKEA v2 (flujo Karpathy, Modos Kimball, Anti-Slop, topologías). Cárgala cuando la tarea toque estructura del vault, gobernanza o calidad de salida de IA.
---

# team-conventions — Convenciones de LANÏAKEA v2

> Fuente de verdad: `CLAUDE.md` en la raíz. Este skill es el resumen operativo.

## Flujo unidireccional
`10_RAW` (fuentes) → `20_AXÖN` (WIKI) → `30_OUTPUT` (entregables). Nunca al revés.

## Modos Kimball (declarar ANTES de cada tarea)
1. Auto — IA ejecuta, humano audita (formato, LaTeX, enlaces, bibliografía).
2. Asist — IA borra, humano pule (borradores, definiciones, resúmenes).
3. Idea — IA propone, humano cura (analogías, abogado del diablo).
4. Lider — humano decide, IA mapea (jerarquía, tesis, selección de fuentes).

## Protocolo Anti-Slop (obligatorio)
- **Grounding:** usa SOLO notas del vault; si no está: "Información no disponible".
- **Sustracción:** borrar adjetivos vacíos ("fundamental", "crucial") y párrafos genéricos.
- **Trazabilidad:** toda afirmación enlaza a su fuente en `10_RAW/`.

## Topologías de procesamiento
- Cadena (A→B→C solo con dependencia) · Diamante (paralelo + síntesis)
- Enrutador (determinista = código 0 tokens; conceptual = agente)
- Ciclo controlado (máx 3 intentos → intervención humana)

## Reglas de escritura del vault
- Conceptos SOLO en `20_AXÖN/23_Wiki-Academic/wiki_<materia>/` con `[[enlaces]]`.
- Actualizar `_master-index.md` y `_MOC_<rama>` al crear notas.
- No duplicar conceptos; borradores van a `30_OUTPUT/31_Projects/`.
- Código verifica casos, NO demuestra (C++23 `std::print`, Python 3.12+).
- LaTeX estricto: `$...$`, `$$...$$`, `\mathbb{R}`, `\varepsilon`, `\delta`.
