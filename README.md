### Compiler Based Secure Programming Language

## Project Description

Secure C Compiler is a security-enhanced compilation system developed to analyse C programs for selected potentially unsafe coding practices before compilation.

The project integrates security analysis with lexical analysis, syntax analysis and GCC compilation. It provides a graphical user interface developed using Python Tkinter.

## Technologies Used

- C Programming
- Python
- Flex
- GNU Bison
- GCC
- Python Tkinter
- Visual Studio Code
- MSYS2

## Main Features

- C source code input through a graphical interface.
- Detection of selected potentially unsafe coding practices.
- Identification of gets(), strcpy(), sprintf(), unsafe printf() format strings and possible hardcoded credentials.
- Lexical analysis using Flex.
- Syntax analysis using GNU Bison.
- Compilation using GCC.
- Display of security warnings and compilation results.

## Project Structure

- compiler/ – Lexer and parser files.
- security/ – Security analysis module.
- gui/ – Python graphical interface.
- examples/ – Sample C programs.
- screenshots/ – Project output screenshots.

## Requirements

- Windows 10 or Windows 11
- Python 3
- GCC
- Flex
- GNU Bison
- Visual Studio Code
- MSYS2

## How to Run

1. Install the required software.
2. Open the project folder in Visual Studio Code.
3. Open the terminal in the project directory.
4. Generate the parser using GNU Bison.
5. Generate the lexical analyser using Flex.
6. Compile the secure compiler using GCC.
7. Run the Python GUI.

## Limitations

The current implementation uses predefined pattern-based security checks and supports a limited subset of C grammar. It is an educational project and does not guarantee complete vulnerability detection.

## Future Enhancements

- Advanced security analysis.
- Automatic code correction.
- Complete C grammar support.
- Detailed security reports.
- Multi-language support.
