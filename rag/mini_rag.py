# -*- coding: utf-8 -*-
"""
mini_rag.py — Mini-RAG sobre tus notas del vault (LANÏAKEA)

Aprende la mecánica interna de Smart Connections construyendo uno tú misma:
    chunk → embed → store → retrieve

Instalar (una vez):
    pip install chromadb sentence-transformers

Ejecutar:
    python3 mini_rag.py "¿qué es el axioma del supremo?" --notas ../pipeline/demo_vault

Salida: top-5 notas más relacionadas semánticamente + distancia.
Es la parte de RECUPERACIÓN de un RAG: encuentra las notas; no genera la respuesta.
"""
import argparse, os, glob
import chromadb
from sentence_transformers import SentenceTransformer

# ── 1. CONFIG ─────────────────────────────────────────────
args = argparse.ArgumentParser(description="Mini-RAG: búsqueda semántica en notas .md")
args.add_argument("pregunta", nargs="?", default="¿Qué es el axioma del supremo?")
args.add_argument("--notas", default="../pipeline/demo_vault", help="carpeta con notas .md")
args = args.parse_args()
NOTES_DIR = args.notas                          # tu WIKI (el conocimiento)
COLLECTION = "laniakea_concepts"
MODEL = "all-MiniLM-L6-v2"                      # local, gratis, privado

# ── 2. CARGAR NOTAS (una nota = un chunk, gracias a tu diseño atómico) ──
def load_notes(path):
    docs = []
    for p in glob.glob(os.path.join(path, "**/*.md"), recursive=True):
        try:
            text = open(p, encoding="utf-8").read()
        except Exception:
            continue
        if len(text.strip()) < 50:
            continue
        docs.append((os.path.relpath(p, path), text[:5000]))
    return docs

# ── 3. EMBED + STORE (lo que hace Smart Connections por detrás) ──
print("1/3 Cargando notas...")
docs = load_notes(NOTES_DIR)
print(f"    {len(docs)} notas encontradas")

print("2/3 Vectorizando (embeddings locales)...")
embedder = SentenceTransformer(MODEL)
embeddings = embedder.encode([t for _, t in docs], show_progress_bar=False).tolist()

client = chromadb.PersistentClient(path="./chroma_db")
try:
    client.delete_collection(COLLECTION)
except Exception:
    pass
col = client.create_collection(COLLECTION, metadata={"hnsw:space": "cosine"})
col.add(
    ids=[f"n{i}" for i in range(len(docs))],
    embeddings=embeddings,
    documents=[t for _, t in docs],
    metadatas=[{"fuente": p} for p, _ in docs],
)
print("    índice vectorial construido ✓")

# ── 4. RETRIEVE (búsqueda semántica) ──
q = args.pregunta
print(f"3/3 Pregunta: {q}")
q_emb = embedder.encode([q]).tolist()
res = col.query(query_embeddings=q_emb, n_results=5)

print("\nTop-5 notas más relacionadas:\n")
for doc, meta, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0]):
    first = " ".join(doc.split())[:110]
    print(f"  • {meta['fuente']}  (distancia={dist:.3f})")
    print(f"    {first}...\n")
