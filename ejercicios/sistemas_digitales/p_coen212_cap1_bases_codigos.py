"""COEN 212 · Mano 5.ª ed. · Cap. 1 · Práctica: bases, códigos y lógica binaria.

Pieza 4 del paquete estándar del capítulo 1 (script de práctica, parte Python).
Los casos salen de un caso empresarial (una ferretería) que acompaña el capítulo.
La parte de complemento a 2 y desbordamiento está en C++: c_coen212_cap1_complemento2.cpp

POR QUÉ PYTHON Y NO C++ (para ESTA parte)
  Cambiar de base, armar BCD, ASCII con paridad o código Gray es trabajar con dígitos y
  cadenas de texto: dividir, juntar residuos, agrupar de 3 en 3 o de 4 en 4.
  - Python maneja cadenas y enteros de cualquier tamaño sin declarar tipos, y el código
    se lee casi igual que el algoritmo del libro (divisiones sucesivas, multiplicar por 2).
  - C++ obligaría a pensar en tamaños de `int` y en `std::string` sin ganar nada: aquí
    no hay desbordamiento que estudiar. Para el complemento a 2, en cambio, C++ SÍ gana
    (ver el otro script): Python no tiene enteros de 8 bits y nunca «da la vuelta».

CÓMO SE USA
  1. Completa cada TODO (cambia `return None` por tu código).
     ⚠️ No uses int(texto, base), bin(), oct(), hex() ni format(..., 'b') DENTRO de tus
     funciones: la gracia es hacerlo tú con divisiones y agrupaciones, como en el libro.
  2a. En CURSOR: abre este archivo, abre la terminal integrada (Ctrl + `) y escribe
        python3 p_coen212_cap1_bases_codigos.py
      (si la terminal no está en esta carpeta, haz primero el `cd` de 2b).
  2b. En la TERMINAL del Mac:
        cd ejercicios/sistemas_digitales
        python3 p_coen212_cap1_bases_codigos.py
  3. El revisor imprime ✅ (bien), ❌ (error) o ⏳ (TODO sin completar) por caso.
  4. Postgres, pgAdmin 4 y Neon: no aplica en este capítulo.

REGLAS (del log)
  - Escríbelo tú. La IA de Cursor solo para EXPLICAR errores, no para completar el archivo.
  - Ciclo Controlado: si al 3.er intento no corre, para y anota el error en el log.

Esto verifica un caso, no demuestra para todos.
"""

DIGITOS = "0123456789ABCDEF"   # puedes usar esta cadena para leer y escribir dígitos


# ─────────────────────────────────────────────────────────────
# PARTE 1 · Bases numéricas (Mano §1.2–1.3) · actos 1 y 2 del cuento
# ─────────────────────────────────────────────────────────────

def a_decimal(texto, base):
    """'3A5', 12 -> 557.  Pista: N = suma de (dígito · base^posición)."""
    # TODO
    return None


def decimal_a_base(n, base):
    """557, 2 -> '1000101101'.  Pista: divide entre la base, guarda residuos, léelos al revés."""
    # TODO
    return None


def fraccion_a_binario(x, bits):
    """0.375, 3 -> '011'.  Pista: multiplica por 2, anota la parte entera, quédate con el resto."""
    # TODO
    return None


# ─────────────────────────────────────────────────────────────
# PARTE 2 · Octal y hexadecimal (Mano §1.4) · acto 3 del cuento
# ─────────────────────────────────────────────────────────────

def hex_a_binario(h):
    """'2F6C' -> '0010111101101100'.  Pista: cada dígito hex son exactamente 4 bits."""
    # TODO
    return None


def binario_a_octal(b):
    """'0010111101101100' -> '27554'.  Pista: agrupa de 3 en 3 DESDE LA DERECHA; quita ceros a la izquierda."""
    # TODO
    return None


# ─────────────────────────────────────────────────────────────
# PARTE 3 · Códigos binarios (Mano §1.7) · acto 5 del cuento
# ─────────────────────────────────────────────────────────────

def a_bcd(n):
    """849 -> '1000 0100 1001'.  Pista: cada dígito decimal en su propio grupo de 4 bits."""
    # TODO
    return None


def ascii_con_paridad(caracter, par=True):
    """'M', par=True -> '01001101'.  Pista: ord() da el código; 7 bits + bit de paridad a la izquierda."""
    # TODO
    return None


def gray(i, bits):
    """3, 3 -> '010'.  Pista: el bit de Gray k es (bit k) XOR (bit k+1) del binario; en Python: i ^ (i >> 1)."""
    # TODO
    return None


# ─────────────────────────────────────────────────────────────
# PARTE 4 · Lógica binaria (Mano §1.9) · acto 7 del cuento
#   La alarma suena si el sistema está armado (S) Y (puerta abierta (P) O movimiento (M)).
# ─────────────────────────────────────────────────────────────

def alarma(s, p, m):
    # TODO
    return None


# ═════════════════════════════════════════════════════════════
# REVISOR · no hace falta tocar nada de aquí para abajo
# Los valores esperados salen del cuento y del libro (Mano pp. 17–33).
# ═════════════════════════════════════════════════════════════

CASOS = [
    ("1.2", "a_decimal('10101101', 2)", lambda: a_decimal("10101101", 2), 173),
    ("1.3", "a_decimal('3A5', 12)", lambda: a_decimal("3A5", 12), 557),
    ("1.3", "a_decimal('01011010', 2)", lambda: a_decimal("01011010", 2), 90),
    ("1.3", "decimal_a_base(557, 2)", lambda: decimal_a_base(557, 2), "1000101101"),
    ("1.3", "decimal_a_base(173, 2)", lambda: decimal_a_base(173, 2), "10101101"),
    ("1.3", "decimal_a_base(144, 12)", lambda: decimal_a_base(144, 12), "100"),
    ("1.3", "fraccion_a_binario(0.375, 3)", lambda: fraccion_a_binario(0.375, 3), "011"),
    ("1.3", "fraccion_a_binario(0.10, 12)", lambda: fraccion_a_binario(0.10, 12), "000110011001"),
    ("1.4", "hex_a_binario('2F6C')", lambda: hex_a_binario("2F6C"), "0010111101101100"),
    ("1.4", "binario_a_octal('0010111101101100')", lambda: binario_a_octal("0010111101101100"), "27554"),
    ("1.4", "a_decimal('2F6C', 16)", lambda: a_decimal("2F6C", 16), 12140),
    ("1.7", "a_bcd(849)", lambda: a_bcd(849), "1000 0100 1001"),
    ("1.7", "a_bcd(1224)", lambda: a_bcd(1224), "0001 0010 0010 0100"),
    ("1.7", "ascii_con_paridad('M', par=True)", lambda: ascii_con_paridad("M", True), "01001101"),
    ("1.7", "ascii_con_paridad('8', par=True)", lambda: ascii_con_paridad("8", True), "10111000"),
    ("1.7", "gray(3, 3)", lambda: gray(3, 3), "010"),
    ("1.7", "gray(4, 3)", lambda: gray(4, 3), "110"),
    ("1.7", "[gray(i, 3) for i in range(8)]", lambda: [gray(i, 3) for i in range(8)],
     ["000", "001", "011", "010", "110", "111", "101", "100"]),
]
for _s in (0, 1):
    for _p in (0, 1):
        for _m in (0, 1):
            CASOS.append(("1.9", f"alarma({_s}, {_p}, {_m})",
                          (lambda s=_s, p=_p, m=_m: alarma(s, p, m)),
                          int(_s and (_p or _m))))


def _normal(v):
    if isinstance(v, bool):
        return int(v)
    return v


def _pendiente(v):
    return v is None or (isinstance(v, list) and None in v)


if __name__ == "__main__":
    fallos = pendientes = 0
    print(" §    | caso                                     | resultado")
    for seccion, texto, fn, esperado in CASOS:
        try:
            valor = _normal(fn())
        except Exception as e:  # un error en tu código cuenta como ❌ con su mensaje
            valor = f"ERROR: {type(e).__name__}: {e}"
        if _pendiente(valor):
            marca = "⏳"
            pendientes += 1
        elif valor == esperado:
            marca = "✅"
        else:
            marca = f"❌  obtuve {valor!r}, se esperaba {esperado!r}"
            fallos += 1
        print(f" {seccion:<4} | {texto:<40} | {marca}")
    print("\nRESUMEN")
    print(f"  ❌ casos con error: {fallos}")
    print(f"  ⏳ casos pendientes (TODO sin completar): {pendientes}")
    if fallos == 0 and pendientes == 0:
        print("  ✅ Todo coincide con el libro y el cuento.")
    print("\nEsto verifica un caso, no demuestra para todos.")
