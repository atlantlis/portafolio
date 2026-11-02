# Lanïakea · portafolio

Soy Diana Arrubla, cofundadora de ECOALMA SAS (mobiliario a medida, más de 1.000 proyectos). Desde 2025 sigo un plan propio de estudio en computación, IA y matemáticas, con los temarios oficiales de la UNAM, la Universidad de Antioquia y la Universidad Nacional de Colombia.

Este repositorio muestra **cómo trabajo con agentes de IA** y **cómo estudio con código**. Es una selección: mi base de conocimiento completa es privada.

## Qué hay aquí

| Carpeta | Qué es |
|---|---|
| [`agentes/`](agentes/) | Las reglas con que trabajan los agentes de IA (Claude Code) sobre mi base de conocimiento: 4 modos humano-IA, protocolo anti-relleno, 4 topologías y un límite de 3 intentos. Incluye mi skill propia [`team-conventions`](agentes/skills/team-conventions/SKILL.md). |
| [`pipeline/`](pipeline/) | `pipeline_academico.py`: clasifica las fuentes por materia, decide la fase de estudio sin usar IA (enrutador determinista) y valida un **contrato JSON** antes de escribir en la wiki. Solo usa la biblioteca estándar de Python. |
| [`rag/`](rag/) | `mini_rag.py`: búsqueda semántica sobre mis notas con *embeddings* locales (la parte de recuperación de un RAG). |
| [`ejercicios/`](ejercicios/) | Plantillas de práctica por capítulo con revisor automático: muestran ❌ o ⏳ hasta que se completan los TODO, y ✅ cuando el resultado coincide con el libro. Incluyen conjuntos y funciones en Python, bases numéricas y complemento a 2 en Python y C++23, y ejercicios que unen geometría o lógica con programación. |

## Cómo probarlo

Python 3.12+ y un compilador con C++23.

```bash
# Pipeline: valida el contrato de ejemplo
python3 pipeline/pipeline_academico.py --validar pipeline/ejemplos/nodo_desigualdad_triangular.json

# Pipeline: simula clasificar las fuentes del vault de ejemplo (no mueve nada)
python3 pipeline/pipeline_academico.py --scan --fase auto

# Álgebra: verifica casos de conjuntos, funciones y relaciones de equivalencia
python3 ejercicios/matematicas/p_algebra_sup1_cap1_verif.py

# Sistemas digitales: plantilla de práctica (muestra ⏳ hasta completar los TODO)
python3 ejercicios/sistemas_digitales/p_coen212_cap1_bases_codigos.py

# RAG (instala dependencias primero)
pip install -r rag/requirements.txt
cd rag && python3 mini_rag.py "¿qué es el supremo?"
```

Los archivos `c_*.cpp` usan `std::println` (`<print>`), que pide un compilador con C++23 completo (por ejemplo, clang 17+ o GCC 14+):

```bash
c++ -std=c++23 ejercicios/integral/c_geo212_01_complemento2.cpp -o /tmp/x && /tmp/x
```

## Cómo se hizo

Diseño las reglas, el método y los criterios de calidad. Escribo y pruebo el código con ayuda de Claude Code, siguiendo las reglas de [`agentes/`](agentes/). Cada archivo de código verifica casos concretos: **esto verifica un caso, no demuestra para todos.**
