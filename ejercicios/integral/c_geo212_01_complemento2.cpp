// ╔══════════════════════════════════════════════════════════════════════════╗
// ║  Ïntegral ✦  JUEVES · Geometria A. I (T1 §1.1) + COEN 212 (Mano Cap. 1)    ║
// ║  Tema: la flecha de A a B puede tener componentes NEGATIVAS.               ║
// ║        ¿Como guarda la maquina un -3?  → complemento a 2 en 8 bits.        ║
// ║  Tiempo: 50 min (despues de 1 h 15 de Geometria: p_geo_01_ejercicios.py)   ║
// ║  Correr:  cd ejercicios/integral                                          ║
// ║           c++23 c_geo212_01_complemento2.cpp -o /tmp/j && /tmp/j           ║
// ║  Sin resolver: ❌ ❌ ❌ ⏳.   Resuelto: ✅ ✅ ✅ ✅.                           ║
// ║  Esto verifica un caso, no demuestra para todos.                           ║
// ╚══════════════════════════════════════════════════════════════════════════╝
//
// ─── LEYENDA 0 · ¿PYTHON O C++23? ───────────────────────────────────────────
//   PYTHON 3.12  cuando el tema es verificar MATEMATICA o LOGICA: condiciones,
//                conjuntos, tablas de verdad, calculos, fracciones exactas.
//                Se lee casi como el libro y no se compila.
//                Archivo p_*.py  ·  correr:  python3 archivo.py
//   C++23        cuando la materia ES C++ (COEN 243) o importan los TIPOS, los BITS
//                de ancho fijo, la MEMORIA, el desbordamiento o la rapidez
//                (ej. complemento a 2 con int8_t). Python esconderia justo eso.
//                Archivo c_*.cpp  ·  correr:  c++23 archivo.cpp -o /tmp/x && /tmp/x
//   LOS DOS      cuando el tema pide comparar: se hacen ambos y se explica la diferencia.
//   ESTE ARCHIVO: C++23, porque el tema son 8 bits FIJOS (int8_t).
//                 Python no tiene enteros de 8 bits: mostraria -3 sin 11111101.
//
// Como leer cada linea:  // [C++ PARTES] · // [MAT PARTES] arriba,  [C++] | [MAT] al lado.
//
// ─── LEYENDA 1 · NANO (teclado) ── (siempre igual) ──────────────────────────
//   ^ = Ctrl.   Esc + letra = suelta Esc y luego la letra (Alt de nano).
//   Ctrl+O, Enter  guardar          Ctrl+X  salir (Y = guardar, N = no)
//   Esc Espacio    palabra anterior            Ctrl+N / P   linea siguiente / anterior
//   Ctrl+A / E     inicio / final de linea     Ctrl+V / Y   bajar / subir pantalla
//   Esc G + numero ir a la linea N             Ctrl+C       en que linea estoy
//   Ctrl+K / U     cortar / pegar linea        Esc U / E    deshacer / rehacer
//   Ctrl+W o Ctrl+F  buscar (ej. TODO)         Esc W        siguiente resultado
//   Esc $          partir lineas largas ($ = Shift+4)       Ctrl+G  ayuda
//
// ─── LEYENDA 2 · COEN 212 (sistemas digitales, en C++) ───────────────────────
//   BIT            un 0 o un 1 (un interruptor apagado/encendido)
//   BYTE           8 bits seguidos: 0000 0011
//   int8_t         TIPO de C++: entero CON signo de exactamente 8 bits: de -128 a 127
//   uint8_t        TIPO de C++: entero SIN signo de 8 bits: de 0 a 255
//   BIT DE SIGNO   el bit de la izquierda: 0 = positivo, 1 = negativo
//   COMPLEMENTO A 1   voltear cada bit (0→1, 1→0)
//   COMPLEMENTO A 2   complemento a 1, y luego sumar 1  →  asi se guarda un negativo
//   ~  OPERADOR de bits "voltear todos"        (complemento a 1)
//   &  |  ^   OPERADORES de bits AND, OR, XOR  (aqui no se usan; vienen en Cap. 2)
//   {:08b}     en println: escribir el numero en binario con 8 cifras
//   static_cast<uint8_t>(n)   leer los mismos 8 bits como numero sin signo
//   #include <cstdint> = BIBLIOTECA que trae int8_t y uint8_t
//
// ─── LEYENDA 3 · MATEMATICAS (Geometria A. I, T1 §1.1) ───────────────────────
//   PUNTO      un lugar del plano:  A = (a_x, a_y)
//   ℝ²         el plano: todas las parejas (x, y)
//   VECTOR     la flecha de A a B:  v = B − A = (b_x − a_x, b_y − a_y)
//   COMPONENTE NEGATIVA   si B esta a la IZQUIERDA de A, v_x < 0; si esta ABAJO, v_y < 0
//   −n         el opuesto de n:  n + (−n) = 0
//   ‖v‖        la norma (largo):  √(v_x² + v_y²)
//   Pitagoras  √(3² + 4²) = √25 = 5
//
// ═════════════════════════════════════════════════════════════════════════════

// [C++ PARTES] #include = traer · <print> = BIBLIOTECA (println)
// [MAT PARTES] no aplica
#include <print>                                     // [C++] trae println                    | [MAT] mostrar el resultado

// [C++ PARTES] #include = traer · <cstdint> = BIBLIOTECA (int8_t, uint8_t)
// [MAT PARTES] enteros con un rango limitado: −128 ≤ n ≤ 127
#include <cstdint>                                   // [C++] trae los tipos de 8 bits        | [MAT] {−128, …, 127} ⊂ ℤ

// [C++ PARTES] <string> = BIBLIOTECA de texto (std::string) · <format> = BIBLIOTECA (std::format)
// [MAT PARTES] palabra = sucesion de simbolos 0 y 1
#include <string>                                    // [C++] trae std::string                | [MAT] palabra binaria
#include <format>                                    // [C++] trae std::format                | [MAT] escribir en base 2

// [C++ PARTES] struct = crear TIPO · Punto = TIPO nuevo · int = TIPO entero · x, y = CAMPOS
// [MAT PARTES] A = PUNTO · (x, y) = COORDENADAS enteras
struct Punto { int x, y; };                          // [C++] tipo con dos enteros            | [MAT] A = (x, y) ∈ ℤ² ⊂ ℝ²

// TODO 1: la flecha de A a B es B - A (resta x con x, y con y)   — igual que en c_geo243_01_flecha.cpp
// [C++ PARTES] Punto = TIPO que devuelve · flecha = FUNCION · Punto a, Punto b = PARAMETROS · return = devolver
// [MAT PARTES] f = FUNCION · B − A = VECTOR · b_x − a_x, b_y − a_y = COMPONENTES (pueden ser negativas)
Punto flecha(Punto a, Punto b) { return {0, 0}; }    // [C++] recibe 2 puntos, devuelve 1     | [MAT] f(A,B) = B − A

// TODO 2: el opuesto de n SIN usar el signo menos: complemento a 2 = voltear los bits (~) y sumar 1
// [C++ PARTES] int8_t = TIPO que devuelve · negar = FUNCION · int8_t n = PARAMETRO · ~ = OPERADOR voltear bits · + = OPERADOR sumar
// [MAT PARTES] n ↦ −n = FUNCION "opuesto" · se cumple n + (−n) = 0
int8_t negar(int8_t n) { return 0; }                 // [C++] devuelve el complemento a 2     | [MAT] g(n) = −n

int main() {                                         // [C++] aqui empieza el programa        | [MAT] el enunciado

    // [C++ PARTES] Punto = TIPO · a, b = VARIABLES · {5, 3}, {2, 7} = valores de los CAMPOS
    // [MAT PARTES] A, B = PUNTOS · B esta a la izquierda y arriba de A
    Punto a{5, 3}, b{2, 7};                          // [C++] crea dos puntos                 | [MAT] A = (5,3), B = (2,7)

    // [C++ PARTES] Punto = TIPO · v = VARIABLE · = OPERADOR guardar · flecha(a, b) = llamada con ARGUMENTOS
    // [MAT PARTES] v = VECTOR · su primera componente es negativa
    Punto v = flecha(a, b);                          // [C++] llama flecha, guarda en v       | [MAT] v = B − A = (−3, 4)
    std::println("flecha A→B = ({}, {})", v.x, v.y); // [C++] imprime las dos componentes      | [MAT] v = (v_x, v_y)

    // [C++ PARTES] int8_t = TIPO de 8 bits · c = VARIABLE · = guardar · v.x = CAMPO de v
    // [MAT PARTES] c = la componente v_x, ahora guardada en 8 bits
    int8_t c = v.x;                                  // [C++] mete v.x en una caja de 8 bits  | [MAT] c = v_x
    // [C++ PARTES] {:08b} = binario con 8 cifras · static_cast<uint8_t>(c) = ver los 8 bits sin signo
    // [MAT PARTES] la escritura en base 2 de c
    std::println("v_x = {} se guarda como {:08b}", c, static_cast<uint8_t>(c)); // [C++] imprime los bits | [MAT] (c)₂

    // TODO 3: escribe TU los 8 bits de -5 en complemento a 2, pensando, sin correr el programa.
    //         Pasos: 5 en binario (8 cifras) → voltear cada bit → sumar 1.  Cambia "????????".
    //         (Es -5 y no -3 porque la linea de arriba ya imprime los bits de -3.)
    // [C++ PARTES] const char* = TIPO texto fijo · a_mano = VARIABLE · "..." = texto
    // [MAT PARTES] (−5)₂ en complemento a 2 = tu respuesta
    const char* a_mano = "????????";                 // [C++] tu respuesta como texto         | [MAT] (−5)₂ = ?

    // ─── REVISOR ─────────────────────────────────────────────────────────────
    // [C++ PARTES] == = OPERADOR comparar · && = "y" · ? : = OPERADOR condicional (atajo del if)
    // [MAT PARTES] P ≡ (v_x = −3) ∧ (v_y = 4)  · PROPOSICION: verdadera o falsa
    std::println("{}", (v.x == -3 && v.y == 4) ? "✅ flecha" : "❌ flecha");   // [C++] revisa TODO 1 | [MAT] P
    // [MAT PARTES] Q ≡ g(3) = −3  y  g(−3) = 3   (el opuesto del opuesto vuelve)
    std::println("{}", (negar(3) == -3 && negar(-3) == 3) ? "✅ negar" : "❌ negar"); // [C++] revisa TODO 2 | [MAT] −(−n) = n
    // [MAT PARTES] R ≡ n + g(n) = 0 para n = 100
    std::println("{}", (100 + negar(100) == 0) ? "✅ suma cero" : "❌ suma cero"); // [C++] restar = sumar el negado | [MAT] n + (−n) = 0
    // [C++ PARTES] std::format = armar texto · std::string = TIPO texto · == compara textos
    // [MAT PARTES] tu escritura = la de la maquina
    std::string maquina = std::format("{:08b}", static_cast<uint8_t>(int8_t{-5}));  // [C++] los bits reales de -5 | [MAT] (−5)₂
    std::string tuyo = a_mano;                       // [C++] tu texto como string            | [MAT] tu respuesta
    std::println("{}", tuyo == "????????" ? "⏳ bits de -5 (falta)"
                     : tuyo == maquina   ? "✅ bits de -5"
                                         : "❌ bits de -5");               // [C++] revisa TODO 3 | [MAT] ¿coinciden?
}                                                    // [C++] fin del programa                | [MAT] ∎
