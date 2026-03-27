# 🐱 MichiScript v2
<p align="center">
  <img src="https://github.com/MininoSua/My-own-programming-language-MichiScript/blob/main/logo.png?raw=true" width="200">
</p>

### The first cat-themed programming language with Gemini AI integration.


🐾 MichiScript v1.1.0 (PLS the functions and variables in spanish bcz that how i programmed it sorry for my grammar)

MichiScript is a dynamic, interpreted programming language with a cat-inspired theme. It is designed to be simple, readable, and fun for developers who want to code with a "feline" touch. Built entirely in Python, it features a complete compiler/interpreter architecture including a Lexer, Parser, and AST-based Evaluator. 
(Also maybe some files are outdated bcz the project follows a fast-paced update cycle)

✨ Key Features

Thematic Syntax: Use keywords like miau for comments, traer for printing, and pedir for input.

Dynamic Typing: Variables are flexible and can change types at runtime.

Built-in 3D Engine: Native mathematical projection for 3D wireframe rendering.

File System Support: Built-in functions for reading, writing, and deleting files.

Michi-GPT Assistant: An integrated helper logic to assist with coding questions.

Modern IDE: A custom Dark Mode IDE (Catppuccin theme) built with support for touch devices.

🚀 Getting Started

Prerequisites

Python 3.10 or higher

No external dependencies are required for the core language.

Installation

Clone the repository and run the integrated IDE:

git clone [https://github.com/YOUR_USERNAME/MichiScript.git](https://github.com/YOUR_USERNAME/MichiScript.git)
cd MichiScript
python michiscript_ide_pro.py


📖 Syntax Guide

1. Variables and Types

MichiScript handles types automatically. Just assign a value:

miau This is a comment
name = "Whiskers"
fish_count = 15
is_happy = cierto


2. Control Flow

si fish_count > 10 {
    traer "Dinner time!"
} sino {
    traer "Miau... still hungry."
}

mientras fish_count > 0 {
    traer "Eating fish number " + texto(fish_count)
    fish_count = fish_count - 1
}


3. Functions

funcion greet(name) {
    traer "Miau, " + name + "!"
}

greet("Human")


🧊 Advanced Capabilities

3.D Graphics Engine

Launch a rotating 3D cube directly from your script:

renderizar_cubo_3d()


File Management

escribir_archivo("diary.txt", "Today I caught a laser pointer.")
si existe_archivo("temp.log") {
    borrar_archivo("temp.log")
}


🛠️ Project Structure

michiscript_lexer.py: Lexical analysis and token generation.

michiscript_parser.py: Syntax analysis and AST construction.

michiscript_ast.py: Abstract Syntax Tree node definitions.

michiscript_evaluator.py: The execution engine (Interpreter).

michiscript_ide_pro.py: The graphical development environment.

🤝 Contributing

Contributions are what make the feline community amazing!

Fork the Project

Create your Feature Branch (git checkout -b feature/AmazingFeature)

Commit your Changes (git commit -m 'Add some AmazingFeature')

Push to the Branch (git push origin feature/AmazingFeature)

Open a Pull Request

📜 License

Distributed under the MIT License. See LICENSE for more information.

Developed with ❤️ for cats and humans alike.
