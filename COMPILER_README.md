# MichiScript - Compilador e Intérprete

Implementación completa de un compilador/intérprete para el lenguaje de programación **MichiScript** escrito en Python.

## 📁 Estructura del Proyecto

```
michiscript/
├── michiscript_lexer.py          # Análisis léxico (tokenización)
├── michiscript_ast.py            # Definición del árbol de sintaxis abstracta
├── michiscript_parser.py         # Análisis sintáctico (parsing)
├── michiscript_evaluator.py      # Evaluador/Intérprete
├── michiscript.py                # Interfaz CLI (REPL + ejecutor de archivos)
├── test_michiscript.py           # Suite de pruebas unitarias
└── ejemplos/                      # Archivos de ejemplo
    ├── hola_mundo.michis
    ├── calculadora.michis
    ├── fibonacci.michis
    └── ...
```

## 🛠️ Componentes

### 1. **Lexer** (`michiscript_lexer.py`)
- Tokeniza el código fuente en tokens
- Reconoce palabras clave, operadores, literales
- Maneja comentarios (`miau`)
- Soporte para strings con escape

**Características:**
- 50+ tipos de tokens
- Seguimiento de línea y columna
- Manejo de errores léxicos

### 2. **AST** (`michiscript_ast.py`)
- Define todas las estructuras del árbol de sintaxis abstracta
- Patrón Visitor para evaluación
- Nodos para:
  - Expresiones: literales, binarias, llamadas, listas, diccionarios
  - Sentencias: asignación, bloques, control de flujo
  - Definiciones: funciones, clases

### 3. **Parser** (`michiscript_parser.py`)
- Análisis sintáctico recursivo descendente
- Precedencia correcta de operadores
- Manejo de:
  - Expresiones con precedencia
  - Sentencias de control (si/sino, mientras, para)
  - Definiciones de funciones y clases
  - Asignaciones simples y múltiples

**Características:**
- Precedencia de operadores correcta
- Recuperación de errores básica
- Soporte para lambdas y funciones anónimas

### 4. **Evaluador** (`michiscript_evaluator.py`)
- Ejecuta el AST usando el patrón Visitor
- Entornos para gestionar variables
- Funciones integradas (50+)
- Soporte para:
  - Funciones recursivas
  - Clases y objetos
  - Métodos vinculados
  - Módulos (math, tiempo, aleatorio)

**Características:**
- Tipado dinámico
- Llamadas a funciones del usuario y integradas
- Manejo de excepciones especiales (break, continue, return)
- Conversión de tipos automática

### 5. **CLI** (`michiscript.py`)
- REPL interactivo
- Ejecutor de archivos .michis
- Comandos especiales (ayuda, variables, funciones)

## 🚀 Instalación

### Requisitos
- Python 3.8+
- Sin dependencias externas

### Instalación

```bash
# Clonar o descargar el proyecto
git clone https://github.com/michiscript/michiscript.git
cd michiscript

# Hacer el script ejecutable (en Linux/macOS)
chmod +x michiscript.py
```

## 💻 Uso

### 1. REPL Interactivo

```bash
python3 michiscript.py
```

```
╔══════════════════════════════════════════╗
║       MichiScript v1.0.0 - REPL          ║
║     Bienvenido al mundo de los michis 🐱 ║
╚══════════════════════════════════════════╝

michis> traer "¡Hola Michis!"
¡Hola Michis!

michis> x = 5 + 3
michis> traer x
8

michis> funcion sumar(a, b) {
  retorna a + b
}
michis> traer sumar(3, 4)
7
```

### 2. Ejecutar archivo

```bash
python3 michiscript.py archivo.michis
```

**archivo.michis:**
```michiscript
funcion fibonacci(n) {
    si n <= 1 {
        retorna n
    }
    retorna fibonacci(n - 1) + fibonacci(n - 2)
}

para i en rango(10) {
    traer fibonacci(i)
}
```

### 3. Importar como módulo Python

```python
from michiscript_parser import parse
from michiscript_evaluator import Evaluator

source = """
funcion multiplicar(a, b) {
    retorna a * b
}
resultado = multiplicar(6, 7)
"""

ast = parse(source)
evaluator = Evaluator()
evaluator.evaluate(ast)

print(evaluator.current_env.get('resultado'))  # 42
```

## 📚 Ejemplos

### Ejemplo 1: Operaciones Matemáticas

```michiscript
x = 10
y = 3

traer "Suma: " + (x + y)
traer "Resta: " + (x - y)
traer "Multiplicación: " + (x * y)
traer "División: " + (x / y)
traer "Módulo: " + (x % y)
traer "Potencia: " + (x ^ y)
```

### Ejemplo 2: Bucles

```michiscript
miau Tabla de multiplicar
para i en rango(1, 11) {
    resultado = 7 * i
    traer "7 x " + i + " = " + resultado
}
```

### Ejemplo 3: Funciones

```michiscript
funcion es_par(numero) {
    retorna numero % 2 == 0
}

para i en rango(1, 11) {
    si es_par(i) {
        traer i + " es PAR"
    } sino {
        traer i + " es IMPAR"
    }
}
```

### Ejemplo 4: Listas y Diccionarios

```michiscript
numeros = [10, 20, 30, 40, 50]
gato = {nombre: "Michi", edad: 5, raza: "Persa"}

miau Procesar lista
suma = 0
para num en numeros {
    suma = suma + num
}
traer "Suma: " + suma

miau Acceder diccionario
traer "Nombre: " + gato["nombre"]
traer "Edad: " + gato["edad"]
```

### Ejemplo 5: Clases (POO)

```michiscript
gatito Gato {
    funcion __inicializar(nombre, edad) {
        esto.nombre = nombre
        esto.edad = edad
        esto.energia = 100
    }
    
    funcion ronronear() {
        traer esto.nombre + ": Prrr... 😸"
    }
    
    funcion dormir(horas) {
        esto.energia = min(100, esto.energia + horas * 15)
        traer esto.nombre + " durmió " + horas + " horas"
    }
}

michi = Gato("Whiskers", 5)
michi.ronronear()
michi.dormir(8)
```

## 🧪 Pruebas

Ejecutar la suite de pruebas:

```bash
python3 -m unittest test_michiscript
```

Ejecutar una prueba específica:

```bash
python3 -m unittest test_michiscript.TestEvaluator.test_function_definition
```

Pruebas incluidas:
- Análisis léxico (tokens)
- Análisis sintáctico (AST)
- Evaluación de expresiones
- Control de flujo
- Funciones y recursión
- Listas y diccionarios
- Conversión de tipos
- Asignación múltiple
- Integración

## 🔍 Características Implementadas

### Expresiones
- ✅ Literales (números, strings, booleanos, nulo)
- ✅ Operadores binarios (aritméticos, comparación, lógicos)
- ✅ Operadores unarios (negación, NOT)
- ✅ Llamadas a función
- ✅ Acceso a índice y miembro
- ✅ Slicing
- ✅ Ternario
- ✅ Funciones anónimas (lambda)

### Sentencias
- ✅ Asignación simple y múltiple
- ✅ Asignación compuesta (+=, -=, etc)
- ✅ Bloque de código
- ✅ If/Else/Elif
- ✅ While loop
- ✅ For loop
- ✅ Break/Continue
- ✅ Print (traer)
- ✅ Input (pedir)
- ✅ Return

### Definiciones
- ✅ Funciones con parámetros por defecto
- ✅ Clases y métodos
- ✅ Constructores (__inicializar)
- ✅ Métodos vinculados
- ✅ Declaración de variables

### Funciones Integradas (50+)
- ✅ Conversión: numero(), texto(), booleano(), lista()
- ✅ Matemáticas: abs(), max(), min(), sqrt(), pow(), etc
- ✅ Secuencias: longitud(), rango(), suma(), promedio()
- ✅ Tipos: tipo(), es_numero(), es_texto(), etc
- ✅ Especiales: aleatorio(), espera()
- ✅ E/S: traer(), pedir()

### Módulos
- ✅ math (funciones matemáticas)
- ✅ tiempo (fecha/hora)
- ✅ aleatorio (números aleatorios)

## 📊 Estadísticas del Código

```
Lexer:       ~400 líneas
AST:         ~250 líneas
Parser:      ~800 líneas
Evaluator:   ~900 líneas
CLI:         ~200 líneas
Tests:       ~600 líneas
─────────────────────────
Total:       ~3150 líneas de código Python
```

## 🐛 Limitaciones Conocidas

1. **Rendimiento**: El intérprete es lento para código complejo (no usa optimizaciones)
2. **Módulos**: Sistema de módulos muy simplificado
3. **Tipos**: Sin tipado estático (dinámico solamente)
4. **Errores**: Recuperación de errores básica
5. **Concurrencia**: No hay soporte para concurrencia
6. **Comentarios**: Solo comentarios de una línea (`miau`)

## 🔮 Roadmap Futuro

- [ ] Compilación a bytecode
- [ ] Máquina virtual para ejecutar bytecode
- [ ] Optimización de llamadas de cola
- [ ] Decoradores
- [ ] Generadores
- [ ] Context managers
- [ ] Manejo excepciones (try/except)
- [ ] Type hints
- [ ] Mejor sistema de módulos
- [ ] Estándar library más completa
- [ ] Debugging (breakpoints, stepping)
- [ ] Documentación integrada

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu característica
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📝 Licencia

MIT License - Ver LICENSE para más detalles

## 👨‍💻 Autor

Creado con ❤️ para los michis 🐱

## 📞 Soporte

- GitHub Issues: https://github.com/michiscript/issues
- Documentación: https://michiscript.dev/docs
- Comunidad: https://michiscript-forum.dev

---

**¡Feliz programación con MichiScript! 🐱✨**
