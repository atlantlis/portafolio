# Reglas para trabajar con agentes de IA

Estas son las reglas con que los agentes de IA (Claude Code) trabajan sobre mi base de conocimiento. El agente las lee al empezar cada sesión. La versión resumida está en [`skills/team-conventions/SKILL.md`](skills/team-conventions/SKILL.md).

## 1. Flujo de la información

```
10_RAW (fuentes) → 20_AXÖN (wiki: una nota por concepto) → 30_OUTPUT (proyectos y entregables)
```

Siempre en un solo sentido. Las fuentes no se editan. Los borradores no entran a la wiki.

## 2. Cuatro modos de colaboración humano-IA

Antes de cada tarea declaro el modo, es decir, quién decide:

| Modo | Nombre | Quién decide | Uso típico |
|---|---|---|---|
| 1 | Auto | la IA ejecuta, yo audito | formato, LaTeX, enlaces, bibliografía |
| 2 | Asistente | la IA hace el borrador, yo pulo | resúmenes, definiciones |
| 3 | Ideas | la IA propone, yo elijo | analogías, abogado del diablo |
| 4 | Líder | yo decido, la IA organiza | estructura, selección de fuentes |

## 3. Protocolo anti-relleno (obligatorio en todo modo)

1. **Solo con fuente:** la IA usa únicamente mis notas. Si la información no está, responde «Información no disponible».
2. **Sustracción:** se borran los adjetivos vacíos («fundamental», «crucial») y los párrafos de introducción genéricos.
3. **Trazabilidad:** cada afirmación enlaza a su fuente.

## 4. Cuatro topologías de trabajo

- **Cadena:** A → B → C, solo cuando un paso necesita el resultado del anterior.
- **Diamante:** las tareas independientes se hacen en paralelo y se unen en una síntesis final.
- **Enrutador:** si la tarea se resuelve con lógica determinista, se ejecuta código (0 llamadas a la IA). Solo lo que pide juicio conceptual va al agente. Ejemplo: [`pipeline/pipeline_academico.py --fase auto`](../pipeline/pipeline_academico.py).
- **Ciclo controlado:** generar → validar → corregir, **con un máximo de 3 intentos**. Al tercer fallo, el agente se detiene y pide intervención humana. El pipeline lo aplica con el campo `meta.intento` del contrato JSON.

## 5. Código como verificación

El código verifica casos concretos; **no demuestra**. Por eso cada archivo dice: *«Esto verifica un caso, no demuestra para todos»*.

- **Python 3.12** para verificar matemática o lógica (conjuntos, tablas de verdad, conversiones).
- **C++23** cuando importan los tipos, los bits de ancho fijo o el desbordamiento (por ejemplo, el complemento a 2 con `int8_t`).
- Guías de estilo: PEP 8 (Python) y C++ Core Guidelines (C++).

## 6. Método de estudio «problema primero»

1. Intentar un problema del capítulo antes de leer, como diagnóstico.
2. Resolver los problemas del libro (la mayor parte del tiempo).
3. Demostrar sin el libro y verificar casos con código.
4. Evaluación con un problema nuevo, sin ayuda.

La IA no entrega analogías ni resúmenes de un capítulo antes de que yo termine el paso 2.
