🏗️ MichiScript: Technical Architecture & Design

This document outlines the internal structure, design patterns, and execution pipeline of the MichiScript programming language.

1. Execution Pipeline

MichiScript is a tree-walking interpreted language. The lifecycle of a script follows a traditional compiler frontend architecture:

Source Code: Raw .michis text file.

Lexical Analysis (Lexer): Converts characters into a stream of Tokens.

Syntactic Analysis (Parser): Consumes tokens and builds an Abstract Syntax Tree (AST).

Evaluation (Interpreter): Recursively traverses the AST and executes the logic using the Visitor Pattern.

2. Core Modules Breakdown

🐾 Lexer (michiscript_lexer.py)

The Lexer uses Regular Expressions and a stateful scanner to categorize code into tokens.

Keywords: Maps feline-themed words to internal types (e.g., miau -> COMMENT, traer -> PRINT).

Error Handling: Tracks line and column numbers to provide precise feedback during lexical failures.

🧩 Parser (michiscript_parser.py)

A Recursive Descent Parser that enforces the MichiScript grammar.

Precedence: Implements the "Shunting-yard" logic implicitly through recursive calls to handle math operations (PEMDAS).

Grammar: Handles complex structures like nested si/sino blocks, mientras loops, and gatito class definitions.

⚙️ Evaluator (michiscript_evaluator.py)

The "Engine" of the language. It manages the runtime state.

Environment & Scoping: Uses a linked-list of dictionaries to handle global and local scopes (closures).

Object Model: Implements MichiClass and MichiInstance to support Object-Oriented Programming.

Native Bridge: Connects MichiScript calls to Python's underlying math, time, and random libraries.

3. Language Specifications

Type System

MichiScript is Dynamically Typed. Types are checked at runtime during the evaluation phase.

Primitives: Numbers (float/int), Strings, Booleans (verdadero/falso), and nulo.

Collections: Native support for dynamic Lists ([]) and Dictionaries ({}).

Object-Oriented Programming (OOP)

The language implements a class-based model:

gatito: Defines a blueprint for objects.

__inicializar: The constructor method called during instantiation.

esto: Reference to the current instance (equivalent to self in Python).

4. Advanced Components

Mathematical 3D Engine

Integrated directly into the standard library, the 3D engine uses orthographic and perspective projection matrices implemented from scratch.

Workflow: 3D Vertices $\rightarrow$ Rotation Matrices $\rightarrow$ 2D Projection $\rightarrow$ GUI Rendering.

IDE Environment

Built with Tkinter, the IDE provides:

Syntax Highlighting: Visual cues for keywords and strings.

Integrated Terminal: Captures the stdout of the evaluator to display output in real-time.

Filesystem Integration: Direct I/O operations to save and load .michis files.

5. Technical Requirements

Core: Python 3.10+ (utilizes dataclasses and match statements where applicable).

GUI: tkinter module (Standard Library).

Architecture: Modular and decoupled (Lexer and Parser can be used independently).

"A well-structured language is the first step towards a happy developer." 🐱✨
