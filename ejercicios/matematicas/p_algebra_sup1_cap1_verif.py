"""Gómez Laveaga · Álgebra Superior: Curso Completo · Cap. 1 (Conjuntos, relaciones y funciones)
Verificación de casos concretos — ejercicios secciones 1.1, 1.2, 1.5, 1.6 (pág. 81-128).

Esto verifica casos concretos, no demuestra para todos.
Notas: [[Conjuntos_ elementos, extensión, vacío y pares]] · [[Teoría de conjuntos (operaciones)]] ·
[[Funciones: inyectiva, suprayectiva y biyectiva]] · [[Relaciones de equivalencia y particiones]]
Ejecutar: python3 p_algebra_sup1_cap1_verif.py
"""
from itertools import chain, combinations, product


def powerset(s):
    s = list(s)
    return list(chain.from_iterable(combinations(s, r) for r in range(len(s) + 1)))


def simdiff(x, y):
    return (x - y) | (y - x)


def es_inyectiva(f, dominio):
    vals = [f[x] for x in dominio]
    return len(vals) == len(set(vals))


def es_suprayectiva(f, dominio, codominio):
    return set(f[x] for x in dominio) == set(codominio)


def es_equivalencia(rel, universo):
    reflexiva = all((x, x) in rel for x in universo)
    simetrica = all((y, x) in rel for (x, y) in rel)
    transitiva = all((x, z) in rel for (x, y) in rel for (y2, z) in rel if y == y2)
    return reflexiva and simetrica and transitiva


def clases(rel, universo):
    vistos, partes = set(), []
    for x in universo:
        if x in vistos:
            continue
        clase = {y for y in universo if (x, y) in rel}
        partes.append(clase)
        vistos |= clase
    return partes


# --- 1.1.12: |P(A)| = 2^n y subconjuntos propios, A={1,2,3,4} ---
A = {1, 2, 3, 4}
P_A = powerset(A)
print('1.1.12 |P(A)|', len(P_A), '== 2^4', 2 ** len(A), len(P_A) == 2 ** len(A))
print('1.1.12 subconjuntos propios', len(P_A) - 1)

# --- 1.2.20: leyes de De Morgan sobre conjuntos concretos ---
Ad = {'a', 'b', 'c', 'd', 1, 2, 5}
Bd = {'a', 'c', 1, 3}
X = Ad | Bd  # universo relativo
Ac, Bc = X - Ad, X - Bd
print('1.2.20 (A∩B)^c == A^c∪B^c', X - (Ad & Bd) == Ac | Bc)
print('1.2.20 (A∪B)^c == A^c∩B^c', X - (Ad | Bd) == Ac & Bc)
print('1.2.26 A∆B == (A∪B)-(A∩B)', simdiff(Ad, Bd) == (Ad | Bd) - (Ad & Bd))

# --- 2026-09-26 Fase 2: A∖(B∪C) = (A∖B)∩(A∖C) — caso Droguería (A=P, B=N, C=S) ---
# [[Algebra_Cap1_Demostracion_DeMorgan_Diferencia]]
Pd, Nd, Sd = set('aixloscnj'), set('aixos'), set('alocn')
izq, der = Pd - (Nd | Sd), (Pd - Nd) & (Pd - Sd)
print('26-sep P∖(N∪S)', sorted(izq), '| (P∖N)∩(P∖S)', sorted(der), '| iguales', izq == der)
print('26-sep compañera P∖(N∩S) == (P∖N)∪(P∖S)', Pd - (Nd & Sd) == (Pd - Nd) | (Pd - Sd))
print('26-sep falsa P∖(N∩S) == (P∖N)∩(P∖S)', Pd - (Nd & Sd) == (Pd - Nd) & (Pd - Sd))
U3 = [frozenset(s) for s in powerset({1, 2, 3})]
ternas = list(product(U3, repeat=3))
print('26-sep todas las ternas A,B,C ⊆ {1,2,3}:', len(ternas),
      all(a - (b | c) == (a - b) & (a - c) for a, b, c in ternas))

# --- 1.2.27 / 1.2.28: diferencia simétrica con los conjuntos del libro ---
A2, B2 = {1, 2, 3, 4}, {2, 4, 'a', 'b'}
C2 = {'a', frozenset({'c'}), 1, 5}
print('1.2.27 A∆B', simdiff(A2, B2))
print('1.2.27 B∆C', simdiff(B2, C2))
print('1.2.28 A∆(B∆C) == (A∆B)∆C', simdiff(A2, simdiff(B2, C2)) == simdiff(simdiff(A2, B2), C2))

# --- 1.5.x: inyectividad / suprayectividad de funciones finitas ---
f = {1: 'a', 2: 'b', 3: 'c'}
print('f (1-1-1) inyectiva', es_inyectiva(f, f.keys()))
print('f (1-1-1) suprayectiva sobre {a,b,c}', es_suprayectiva(f, f.keys(), {'a', 'b', 'c'}))

g = {1: 'a', 2: 'a', 3: 'b'}
print('g (2->a repetida) inyectiva', es_inyectiva(g, g.keys()))
print('g suprayectiva sobre {a,b,c}', es_suprayectiva(g, g.keys(), {'a', 'b', 'c'}))

# --- 1.6.x: relación de equivalencia -> clases -> partición, U={0..8}, mod 3 ---
U = set(range(9))
rel_mod3 = {(a, b) for a in U for b in U if (a - b) % 3 == 0}
print('a~b si a≡b (mod 3) es equivalencia', es_equivalencia(rel_mod3, U))

partes = clases(rel_mod3, U)
print('clases mod 3', partes)
print('partición cubre U', set.union(*partes) == U)
print('partición es disjunta', sum(len(c) for c in partes) == len(U))
