# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  Ïntegral ✦  JUEVES · Geometria A. I (T1 §1.1) + Logica (Cap. 1, reconoc.) ║
# ║  Tema: "el punto esta en el primer cuadrante" es una PROPOSICION:          ║
# ║        P ∧ Q,  con P ≡ x > 0  y  Q ≡ y > 0.  Su tabla de verdad.           ║
# ║  Tiempo: 25 min (despues de COEN 212) · todo en nano, sin papel            ║
# ║  Correr:  cd ejercicios/integral                                          ║
# ║           python3 p_geolog_01_cuadrantes.py                                ║
# ║  Sin resolver: ❌ ❌ ❌ ⏳ ⏳.   Resuelto: ✅ en todo  (⭐ el reto es opcional) ║
# ║  Esto verifica un caso, no demuestra para todos.                           ║
# ╚══════════════════════════════════════════════════════════════════════════╝
#
# ─── LEYENDA 0 · ¿PYTHON O C++23? ───────────────────────────────────────────
#   PYTHON 3.12  cuando el tema es verificar MATEMATICA o LOGICA: condiciones,
#                conjuntos, tablas de verdad, calculos, fracciones exactas.
#                Se lee casi como el libro y no se compila.
#                Archivo p_*.py  ·  correr:  python3 archivo.py
#   C++23        cuando la materia ES C++ (COEN 243) o importan los TIPOS, los BITS
#                de ancho fijo, la MEMORIA, el desbordamiento o la rapidez
#                (ej. complemento a 2 con int8_t). Python esconderia justo eso.
#                Archivo c_*.cpp  ·  correr:  c++23 archivo.cpp -o /tmp/x && /tmp/x
#   LOS DOS      cuando el tema pide comparar: se hacen ambos y se explica la diferencia.
#   ESTE ARCHIVO: Python, porque el tema es LOGICA (tablas de verdad):
#                 and/or/not como en el libro, e itertools.product da todas las filas.
#
# Como leer cada linea:  # [PY PARTES] · # [MAT PARTES] arriba,  [PY] | [MAT] al lado.
#
# ─── LEYENDA 1 · NANO (teclado) ── (siempre igual) ──────────────────────────
#   ^ = Ctrl.   Esc + letra = suelta Esc y luego la letra (Alt de nano).
#   Ctrl+O, Enter  guardar          Ctrl+X  salir (Y = guardar, N = no)
#   Esc Espacio    palabra anterior            Ctrl+N / P   linea siguiente / anterior
#   Ctrl+A / E     inicio / final de linea     Ctrl+V / Y   bajar / subir pantalla
#   Esc G + numero ir a la linea N             Ctrl+C       en que linea estoy
#   Ctrl+K / U     cortar / pegar linea        Esc U / E    deshacer / rehacer
#   Ctrl+W o Ctrl+F  buscar (ej. TODO)         Esc W        siguiente resultado
#   Esc $          partir lineas largas ($ = Shift+4)       Ctrl+G  ayuda
#
# ─── LEYENDA 2 · LOGICA en PYTHON ────────────────────────────────────────────
#   #            comentario (Python lo ignora; en C++ era //)
#   True/False   los dos valores de verdad: V y F      (TIPO bool)
#   and or not   OPERADORES logicos: "y", "o", "no"
#   >  ==        OPERADORES comparar: devuelven True o False
#   def f(x):    define una FUNCION; lo de adentro va con 4 espacios (sangria, no llaves)
#   return       devuelve el resultado
#   lista = [..] ESTRUCTURA DE DATOS: varios valores en orden; se cuentan desde 0
#   for p, q in ...:   BUCLE: repite para cada fila
#   import / from ... import   traer una BIBLIOTECA
#   product([True, False], repeat=2)   todas las parejas (V,V) (V,F) (F,V) (F,F)
#   print(...)   imprimir      f"...{x}..."   texto con huecos (como {} en println)
#
# ─── LEYENDA 3 · MATEMATICAS (Logica + Geometria) ────────────────────────────
#   PROPOSICION  frase que es verdadera (V) o falsa (F):  "x > 0"
#   ¬P           "no P"        P ∧ Q   "P y Q" (V solo si las dos son V)
#   P ∨ Q        "P o Q" (V si al menos una es V)
#   ≡            "es equivalente / se define como"
#   TABLA DE VERDAD  todas las combinaciones de V/F; con 2 letras hay 2² = 4 filas
#   CUADRANTE    los ejes cortan el plano en 4: I (x>0, y>0) · II (x<0, y>0) · III · IV
#   EJE          la recta x = 0 o y = 0: un punto sobre un eje NO esta en ningun cuadrante
#
# ═════════════════════════════════════════════════════════════════════════════

# [PY PARTES] from/import = traer · itertools = BIBLIOTECA · product = FUNCION
# [MAT PARTES] {V, F} × {V, F} = las 4 filas de la tabla
from itertools import product                       # [PY] trae product                    | [MAT] {V,F}²


# TODO 1: devuelve si el punto (x, y) esta en el primer cuadrante: x mayor que 0 Y y mayor que 0
# [PY PARTES] def = definir FUNCION · primer_cuadrante = nombre · x, y = PARAMETROS · return = devolver
# [MAT PARTES] P ≡ x > 0 · Q ≡ y > 0 · resultado = P ∧ Q
def primer_cuadrante(x, y):                         # [PY] recibe 2 numeros                | [MAT] (x, y) ∈ ℝ²
    return False                                    # [PY] devuelve True o False           | [MAT] P ∧ Q


# TODO 2: llena TU la columna P ∧ Q, pensando, sin correr el programa.  Cambia cada None por True o False.
#         Filas en orden:  P=V,Q=V · P=V,Q=F · P=F,Q=V · P=F,Q=F
# [PY PARTES] tabla_a_mano = VARIABLE · [ ] = lista · None = "todavia nada"
# [MAT PARTES] la columna P ∧ Q de la tabla de verdad
tabla_a_mano = [None, None, None, None]             # [PY] tu respuesta, fila por fila     | [MAT] P ∧ Q = ?


# ⭐ TODO 3 (reto opcional): "fuera del primer cuadrante" ≡ ¬(P ∧ Q).
#         Escribelo usando SOLO not y or (sin and).
# [PY PARTES] def = FUNCION · p, q = PARAMETROS (True/False)
# [MAT PARTES] ¬(P ∧ Q) ≡ ?   (busca la ley de De Morgan en tu libro de Logica)
def fuera(p, q):                                    # [PY] recibe 2 valores de verdad      | [MAT] P, Q
    return None                                     # [PY] tu expresion con not y or       | [MAT] ¬(P ∧ Q)


# ─── REVISOR ─────────────────────────────────────────────────────────────────
# [PY PARTES] print = imprimir · ... if ... else ... = OPERADOR condicional
# [MAT PARTES] puntos de la flecha de hoy: A = (5,3), B = (2,7), v = (−3,4), y un punto en el eje
print("✅ A en I" if primer_cuadrante(5, 3) is True else "❌ A en I")          # [PY] A = (5,3)  | [MAT] 5>0 ∧ 3>0
print("✅ v no en I" if primer_cuadrante(-3, 4) is False and primer_cuadrante(5, 3) else "❌ v no en I")  # [MAT] −3>0 es F
print("✅ eje no es cuadrante" if primer_cuadrante(0, 2) is False and primer_cuadrante(5, 3) else "❌ eje no es cuadrante")  # [MAT] 0>0 es F

# [PY PARTES] list(...) = convertir a lista · for = BUCLE · and = OPERADOR
# [MAT PARTES] la columna correcta de P ∧ Q, calculada fila por fila
filas = list(product([True, False], repeat=2))      # [PY] (V,V) (V,F) (F,V) (F,F)         | [MAT] {V,F}²
correcta = [p and q for p, q in filas]              # [PY] P y Q en cada fila              | [MAT] P ∧ Q
if None in tabla_a_mano:
    print("⏳ tabla de P ∧ Q (falta)")
else:
    print("✅ tabla de P ∧ Q" if tabla_a_mano == correcta else "❌ tabla de P ∧ Q")

# [MAT PARTES] comparar tu ¬(P ∧ Q) con la de la maquina en las 4 filas
if fuera(True, True) is None:
    print("⏳ ⭐ reto De Morgan (opcional)")
else:
    ok = all(fuera(p, q) == (not (p and q)) for p, q in filas)
    print("✅ ⭐ reto De Morgan" if ok else "❌ ⭐ reto De Morgan")
