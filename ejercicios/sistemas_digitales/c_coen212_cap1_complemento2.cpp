// COEN 212 · Mano 5.ª ed. · Cap. 1 · Práctica: complementos, resta y desbordamiento (8 bits).
//
// Pieza 4 del paquete estándar del capítulo 1 (script de práctica, parte C++).
// La parte de bases, códigos y lógica está en Python: p_coen212_cap1_bases_codigos.py
//
// POR QUÉ C++ Y NO PYTHON (para ESTA parte)
//   El complemento a 2 existe porque un registro tiene un número FIJO de bits (8, 16, 64…)
//   y, al pasarse, «da la vuelta» como un odómetro (Mano §1.5–1.6).
//   - En C++, std::uint8_t y std::int8_t SON registros de 8 bits: 100 + 50 en int8_t da -106,
//     igual que el hardware. std::bitset<8> te deja ver los 8 bits tal cual.
//   - En Python los enteros crecen sin límite: 100 + 50 siempre da 150 y nunca verías el
//     desbordamiento. Tendrías que simularlo a mano con % 256, que esconde justo lo que se estudia.
//   Para cambiar de base o armar BCD/ASCII, en cambio, Python es más cómodo (ver el otro script).
//
// CÓMO SE USA
//   1. Completa cada TODO (cambia `return std::nullopt;` por tu código).
//      Operadores útiles: ~x (invierte todos los bits), x + 1, static_cast<std::uint8_t>(…),
//      static_cast<std::int8_t>(…), x & 0x80 (¿bit de signo encendido?).
//   2a. En CURSOR: abre este archivo, abre la terminal integrada (Ctrl + `) y escribe
//         c++ -std=c++2b c_coen212_cap1_complemento2.cpp -o /tmp/c212cap1 && /tmp/c212cap1
//       (si la terminal no está en esta carpeta, haz primero el `cd` de 2b).
//   2b. En la TERMINAL del Mac:
//         cd ejercicios/sistemas_digitales
//         c++ -std=c++2b c_coen212_cap1_complemento2.cpp -o /tmp/c212cap1 && /tmp/c212cap1
//       (-std=c++2b es C++23 en Apple clang 16; el ejecutable va a /tmp para no ensuciar el vault).
//   3. El revisor imprime ✅ (bien), ❌ (error) o ⏳ (TODO sin completar) por caso.
//   4. Postgres, pgAdmin 4 y Neon: no aplica en este capítulo.
//
// REGLAS (del log)
//   - Escríbelo tú. La IA de Cursor solo para EXPLICAR errores, no para completar el archivo.
//   - Ciclo Controlado: si al 3.er intento no compila, para y anota el error en el log.
//
// Esto verifica un caso, no demuestra para todos.

#include <bitset>
#include <cstdint>
#include <optional>
#include <print>
#include <string>

using u8 = std::uint8_t;
using i8 = std::int8_t;

// ─────────────────────────────────────────────────────────────
// PARTE 1 · Complementos (Mano §1.5)
// ─────────────────────────────────────────────────────────────

// Complemento a 1: invertir cada bit.  01011000 -> 10100111
std::optional<u8> complemento_a1(u8 x) {
    // TODO
    return std::nullopt;
}

// Complemento a 2: complemento a 1 + 1.  01011000 -> 10101000
std::optional<u8> complemento_a2(u8 x) {
    // TODO (puedes usar tu complemento_a1)
    return std::nullopt;
}

// ─────────────────────────────────────────────────────────────
// PARTE 2 · Restar sumando (Mano §1.5–1.6) · acto 4 y reto final del cuento
// ─────────────────────────────────────────────────────────────

// a - b usando SOLO suma: a + C2(b). El acarreo que se sale del bit 7 se pierde solo en un u8.
std::optional<u8> restar_sumando(u8 a, u8 b) {
    // TODO
    return std::nullopt;
}

// Leer los mismos 8 bits como número CON signo (complemento a 2): 11100101 -> -27
std::optional<int> leer_con_signo(u8 bits) {
    // TODO (pista: si el bit 7 está encendido, el valor es bits - 256)
    return std::nullopt;
}

// ¿Desborda la suma con signo a + b en 8 bits?  100 + 50 -> true (sale -106)
// Regla del libro: dos positivos que dan negativo, o dos negativos que dan positivo.
std::optional<bool> hay_desbordamiento(i8 a, i8 b) {
    // TODO
    return std::nullopt;
}

// ═════════════════════════════════════════════════════════════
// REVISOR · no hace falta tocar nada de aquí para abajo
// Valores esperados del cuento (actos 4 y reto final) y de Mano §1.5–1.6.
// ═════════════════════════════════════════════════════════════

namespace {
int fallos = 0, pendientes = 0;

std::string bits(u8 v) { return std::bitset<8>(v).to_string(); }

template <class T, class E>
void revisar(const std::string& seccion, const std::string& caso, const std::optional<T>& obtenido,
             E esperado, const std::string& mostrar_obtenido) {
    std::string marca;
    if (!obtenido) {
        marca = "⏳";
        ++pendientes;
    } else if (*obtenido == static_cast<T>(esperado)) {
        marca = "✅";
    } else {
        marca = "❌  obtuve " + mostrar_obtenido;
        ++fallos;
    }
    std::println(" {:<5}| {:<44}| {}", seccion, caso, marca);
}
}  // namespace

int main() {
    std::println(" §    | caso                                        | resultado");

    auto c1 = complemento_a1(0b01011000);
    revisar("1.5", "C1(01011000) = 10100111", c1, u8{0b10100111}, c1 ? bits(*c1) : "");
    auto c2 = complemento_a2(0b01011000);
    revisar("1.5", "C2(01011000) = 10101000", c2, u8{0b10101000}, c2 ? bits(*c2) : "");
    auto c2z = complemento_a2(0);
    revisar("1.5", "C2(00000000) = 00000000 (un solo cero)", c2z, u8{0}, c2z ? bits(*c2z) : "");

    auto r1 = restar_sumando(45, 72);
    revisar("1.6", "45 - 72 -> 11100101", r1, u8{0b11100101}, r1 ? bits(*r1) : "");
    auto s1 = leer_con_signo(0b11100101);
    revisar("1.6", "11100101 con signo = -27", s1, -27, s1 ? std::to_string(*s1) : "");
    auto r2 = restar_sumando(173, 36);
    revisar("1.6", "173 - 36 -> 10001001 (reto final)", r2, u8{0b10001001}, r2 ? bits(*r2) : "");
    auto r3 = restar_sumando(7, 3);
    revisar("1.6", "7 - 3 -> 00000100", r3, u8{0b00000100}, r3 ? bits(*r3) : "");

    auto s2 = leer_con_signo(0b10010110);
    revisar("1.6", "10010110 con signo = -106", s2, -106, s2 ? std::to_string(*s2) : "");
    auto o1 = hay_desbordamiento(100, 50);
    revisar("1.6", "100 + 50 en 8 bits desborda", o1, true, o1 ? (*o1 ? "true" : "false") : "");
    auto o2 = hay_desbordamiento(45, -72);
    revisar("1.6", "45 + (-72) no desborda", o2, false, o2 ? (*o2 ? "true" : "false") : "");
    auto o3 = hay_desbordamiento(-100, -50);
    revisar("1.6", "-100 + (-50) desborda", o3, true, o3 ? (*o3 ? "true" : "false") : "");

    // Demostración del hardware (no hay TODO aquí): así «da la vuelta» un registro de 8 bits.
    i8 a = 100, b = 50;
    auto suma = static_cast<i8>(a + b);
    std::println("\nEl registro de 8 bits en vivo: 100 + 50 = {} ({})", static_cast<int>(suma),
                 bits(static_cast<u8>(suma)));

    std::println("\nRESUMEN");
    std::println("  ❌ casos con error: {}", fallos);
    std::println("  ⏳ casos pendientes (TODO sin completar): {}", pendientes);
    if (fallos == 0 && pendientes == 0) std::println("  ✅ Todo coincide con el libro y el cuento.");
    std::println("\nEsto verifica un caso, no demuestra para todos.");
}
