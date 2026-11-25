import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from pathlib import Path
import subprocess
import re

# =====================================
# PROJECT CONFIGURATION
# =====================================

PROJECT_DIR = Path(__file__).resolve().parent.parent
COMPILER = PROJECT_DIR / "compiler" / "secure_compiler.exe"
SOURCE_FILE = PROJECT_DIR / "gui" / "current_input.c"

BG = "#0F172A"
PANEL = "#1E293B"
EDITOR_BG = "#111827"
OUTPUT_BG = "#080E19"
BLUE = "#2563EB"
GREEN = "#22C55E"
RED = "#EF4444"
ORANGE = "#F59E0B"
WHITE = "#F8FAFC"
MUTED = "#94A3B8"

# =====================================
# MAIN WINDOW
# =====================================

root = tk.Tk()
root.title("Secure C Compiler")
root.geometry("1400x820")
root.minsize(1000, 650)
root.configure(bg=BG)

# =====================================
# HEADER
# =====================================

header = tk.Frame(root, bg=PANEL, height=80)
header.pack(fill="x")
header.pack_propagate(False)

tk.Label(
    header,
    text="🛡  SECURE C COMPILER",
    font=("Arial", 21, "bold"),
    bg=PANEL,
    fg=WHITE
).pack(side="left", padx=25, pady=15)

tk.Label(
    header,
    text="SECURE CODE ANALYSIS & COMPILATION",
    font=("Arial", 9, "bold"),
    bg=PANEL,
    fg=MUTED
).pack(side="left", padx=10)

tk.Label(
    header,
    text="● COMPILER READY",
    font=("Arial", 10, "bold"),
    bg=PANEL,
    fg=GREEN
).pack(side="right", padx=25)

# =====================================
# TOOLBAR
# =====================================

toolbar = tk.Frame(root, bg=BG)
toolbar.pack(fill="x", padx=18, pady=12)


def make_button(text, command, color=PANEL):
    return tk.Button(
        toolbar,
        text=text,
        command=command,
        bg=color,
        fg=WHITE,
        activebackground=BLUE,
        activeforeground=WHITE,
        font=("Arial", 10, "bold"),
        relief="flat",
        padx=15,
        pady=9,
        cursor="hand2"
    )


# =====================================
# MAIN TWO-PANEL AREA
# =====================================

main = tk.PanedWindow(
    root,
    orient=tk.HORIZONTAL,
    bg="#334155",
    sashwidth=7,
    sashrelief="flat",
    bd=0
)

main.pack(
    fill="both",
    expand=True,
    padx=18,
    pady=(0, 12)
)

# =====================================
# LEFT PANEL - PROGRAM EDITOR
# =====================================

editor_panel = tk.Frame(main, bg=PANEL)

main.add(editor_panel, minsize=400)

editor_header = tk.Frame(editor_panel, bg=PANEL)
editor_header.pack(fill="x", padx=15, pady=13)

tk.Label(
    editor_header,
    text="</>  SOURCE CODE EDITOR",
    font=("Arial", 12, "bold"),
    bg=PANEL,
    fg=WHITE
).pack(side="left")

tk.Label(
    editor_header,
    text="C PROGRAM",
    font=("Arial", 9, "bold"),
    bg=PANEL,
    fg=BLUE
).pack(side="right")

# Editor container

editor_container = tk.Frame(
    editor_panel,
    bg=EDITOR_BG
)
editor_container.pack(
    fill="both",
    expand=True,
    padx=12,
    pady=(0, 12)
)

# Line numbers

line_numbers = tk.Text(
    editor_container,
    width=4,
    bg="#1E293B",
    fg="#64748B",
    font=("Consolas", 12),
    relief="flat",
    padx=8,
    pady=12,
    state="disabled",
    takefocus=0,
    wrap="none"
)

line_numbers.pack(side="left", fill="y")

# Source code editor

code_editor = tk.Text(
    editor_container,
    bg=EDITOR_BG,
    fg=WHITE,
    insertbackground=WHITE,
    font=("Consolas", 12),
    relief="flat",
    padx=12,
    pady=12,
    wrap="none",
    undo=True
)

code_editor.pack(
    side="left",
    fill="both",
    expand=True
)

editor_scroll = ttk.Scrollbar(
    editor_container,
    orient="vertical",
    command=code_editor.yview
)

editor_scroll.pack(side="right", fill="y")

code_editor.configure(
    yscrollcommand=editor_scroll.set
)


# =====================================
# LINE NUMBERS
# =====================================

def update_line_numbers(event=None):

    total = int(
        code_editor.index("end-1c").split(".")[0]
    )

    numbers = "\n".join(
        str(i) for i in range(1, total + 1)
    )

    line_numbers.configure(state="normal")
    line_numbers.delete("1.0", tk.END)
    line_numbers.insert("1.0", numbers)
    line_numbers.configure(state="disabled")


# =====================================
# SYNTAX HIGHLIGHTING
# =====================================

def highlight_code(event=None):

    content = code_editor.get("1.0", "end-1c")

    for tag in [
        "keyword", "string", "comment",
        "number", "function"
    ]:
        code_editor.tag_remove(tag, "1.0", tk.END)

    patterns = {
        "keyword": (
            r"\b(int|char|float|double|void|return|"
            r"if|else|for|while|do|switch|case|"
            r"break|continue|struct|const|static|"
            r"long|short|unsigned|sizeof)\b"
        ),
        "string": r'"(?:\\.|[^"\\])*"',
        "comment": r"//.*|/\*[\s\S]*?\*/",
        "number": r"\b\d+\b",
        "function": r"\b[A-Za-z_]\w*(?=\s*\()"
    }

    for tag, pattern in patterns.items():

        for match in re.finditer(pattern, content):

            start = "1.0+" + str(match.start()) + "c"
            end = "1.0+" + str(match.end()) + "c"

            code_editor.tag_add(tag, start, end)

    code_editor.tag_config(
        "keyword", foreground="#60A5FA"
    )
    code_editor.tag_config(
        "string", foreground="#A3E635"
    )
    code_editor.tag_config(
        "comment", foreground="#64748B"
    )
    code_editor.tag_config(
        "number", foreground="#FBBF24"
    )
    code_editor.tag_config(
        "function", foreground="#C084FC"
    )

    update_line_numbers()


code_editor.bind("<KeyRelease>", highlight_code)


# =====================================
# RIGHT PANEL - OUTPUT
# =====================================

output_panel = tk.Frame(main, bg=PANEL)

main.add(output_panel, minsize=400)

output_header = tk.Frame(output_panel, bg=PANEL)
output_header.pack(fill="x", padx=15, pady=13)

tk.Label(
    output_header,
    text="▣  COMPILER OUTPUT",
    font=("Arial", 12, "bold"),
    bg=PANEL,
    fg=WHITE
).pack(side="left")

tk.Label(
    output_header,
    text="LIVE RESULTS",
    font=("Arial", 9, "bold"),
    bg=PANEL,
    fg=GREEN
).pack(side="right")

# Compilation status

status_frame = tk.Frame(output_panel, bg="#293548")
status_frame.pack(fill="x", padx=12, pady=(0, 10))

status_labels = {}

for name in ["Security", "Syntax", "GCC"]:

    row = tk.Frame(status_frame, bg="#293548")
    row.pack(fill="x", padx=10, pady=5)

    tk.Label(
        row,
        text=name,
        font=("Arial", 10, "bold"),
        bg="#293548",
        fg=WHITE
    ).pack(side="left")

    label = tk.Label(
        row,
        text="WAITING",
        font=("Arial", 9, "bold"),
        bg="#293548",
        fg=MUTED
    )

    label.pack(side="right")

    status_labels[name] = label

# Output console

output_container = tk.Frame(
    output_panel,
    bg=OUTPUT_BG
)

output_container.pack(
    fill="both",
    expand=True,
    padx=12,
    pady=(0, 12)
)

output_area = ScrolledText(
    output_container,
    bg=OUTPUT_BG,
    fg=GREEN,
    insertbackground=WHITE,
    font=("Consolas", 10),
    relief="flat",
    padx=12,
    pady=12,
    wrap="word"
)

output_area.pack(
    fill="both",
    expand=True
)

output_area.tag_config(
    "success", foreground=GREEN
)
output_area.tag_config(
    "warning", foreground=ORANGE
)
output_area.tag_config(
    "error", foreground=RED
)
output_area.tag_config(
    "heading", foreground="#38BDF8"
)
output_area.tag_config(
    "normal", foreground=WHITE
)


# =====================================
# OUTPUT DISPLAY
# =====================================

def show_colored_output(text):

    output_area.delete("1.0", tk.END)

    for line in text.splitlines():

        lower = line.lower()

        if "[warning]" in lower or "recommendation:" in lower:
            tag = "warning"

        elif (
            "error" in lower
            or "failed" in lower
            or "failure" in lower
        ):
            tag = "error"

        elif "=====" in line:
            tag = "heading"

        elif (
            "successful" in lower
            or "successfully" in lower
            or "no security issues detected" in lower
        ):
            tag = "success"

        else:
            tag = "normal"

        output_area.insert(
            tk.END,
            line + "\n",
            tag
        )

    output_area.see(tk.END)


def reset_status():

    for label in status_labels.values():
        label.config(
            text="WAITING",
            fg=MUTED
        )


# =====================================
# UPDATE STATUS
# =====================================

def update_status(output):

    lower = output.lower()

    # Security

    if (
        "total security warnings: 0" in lower
        or "no security issues detected" in lower
    ):
        status_labels["Security"].config(
            text="PASSED",
            fg=GREEN
        )

    elif "[warning]" in lower:
        status_labels["Security"].config(
            text="WARNING",
            fg=ORANGE
        )

    # Syntax

    if "syntax analysis successfully" in lower:

        status_labels["Syntax"].config(
            text="VALID",
            fg=GREEN
        )

    elif (
        "syntax error" in lower
        or "program contains syntax errors" in lower
    ):
        status_labels["Syntax"].config(
            text="INVALID",
            fg=RED
        )

    # GCC

    if "compilation successful" in lower:

        status_labels["GCC"].config(
            text="SUCCESS",
            fg=GREEN
        )

    elif "compilation skipped" in lower:

        status_labels["GCC"].config(
            text="SKIPPED",
            fg=ORANGE
        )

    elif "gcc compilation failed" in lower:

        status_labels["GCC"].config(
            text="FAILED",
            fg=RED
        )


# =====================================
# OPEN FILE
# =====================================

def open_file():

    filename = filedialog.askopenfilename(
        filetypes=[("C Files", "*.c")]
    )

    if filename:

        try:
            with open(
                filename, "r", encoding="utf-8"
            ) as file:
                code = file.read()

            code_editor.delete("1.0", tk.END)
            code_editor.insert("1.0", code)

            highlight_code()

        except Exception as error:
            messagebox.showerror(
                "File Error", str(error)
            )


# =====================================
# SAVE FILE
# =====================================

def save_file():

    filename = filedialog.asksaveasfilename(
        defaultextension=".c",
        filetypes=[("C Files", "*.c")]
    )

    if filename:

        try:
            with open(
                filename, "w", encoding="utf-8"
            ) as file:

                file.write(
                    code_editor.get("1.0", "end-1c")
                )

            messagebox.showinfo(
                "Success",
                "C program saved successfully!"
            )

        except Exception as error:
            messagebox.showerror(
                "Save Error", str(error)
            )


# =====================================
# NEW FILE
# =====================================

def new_file():

    if code_editor.get("1.0", "end-1c").strip():

        answer = messagebox.askyesno(
            "New File",
            "Clear the current program?"
        )

        if not answer:
            return

    code_editor.delete("1.0", tk.END)
    output_area.delete("1.0", tk.END)

    reset_status()
    update_line_numbers()


# =====================================
# CLEAR OUTPUT
# =====================================

def clear_output():

    output_area.delete("1.0", tk.END)


# =====================================
# ANALYZE AND COMPILE
# =====================================

def analyze_code():

    if not COMPILER.exists():

        messagebox.showerror(
            "Compiler Error",
            "Secure compiler executable not found!\n\n"
            + str(COMPILER)
        )
        return

    code = code_editor.get(
        "1.0", "end-1c"
    )

    if not code.strip():

        messagebox.showwarning(
            "Warning",
            "Please enter a C program first!"
        )
        return

    try:

        SOURCE_FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        SOURCE_FILE.write_text(
            code,
            encoding="utf-8"
        )

        output_area.delete("1.0", tk.END)

        output_area.insert(
            tk.END,
            "STARTING SECURE C COMPILER...\n\n",
            "heading"
        )

        reset_status()
        root.update_idletasks()

        result = subprocess.run(
            [str(COMPILER), str(SOURCE_FILE)],
            cwd=str(PROJECT_DIR),
            capture_output=True,
            text=True,
            timeout=30
        )

        combined_output = result.stdout

        if result.stderr:
            combined_output += "\n" + result.stderr

        if not combined_output.strip():
            combined_output = (
                "Compiler returned no output.\n"
                f"Exit code: {result.returncode}"
            )

        show_colored_output(combined_output)
        update_status(combined_output)

    except subprocess.TimeoutExpired:

        output_area.insert(
            tk.END,
            "\nERROR: Compiler execution timed out.\n",
            "error"
        )

    except Exception as error:

        messagebox.showerror(
            "Execution Error",
            str(error)
        )


# =====================================
# TOOLBAR BUTTONS
# =====================================

make_button(
    "＋ New",
    new_file
).pack(side="left", padx=4)

make_button(
    "📂 Open",
    open_file
).pack(side="left", padx=4)

make_button(
    "💾 Save",
    save_file
).pack(side="left", padx=4)

make_button(
    "Clear Output",
    clear_output
).pack(side="left", padx=4)

make_button(
    "▶ Analyze & Compile",
    analyze_code,
    BLUE
).pack(side="right", padx=4)


# =====================================
# FOOTER
# =====================================

footer = tk.Frame(root, bg=PANEL, height=30)
footer.pack(fill="x", side="bottom")

tk.Label(
    footer,
    text="Secure C Compiler | Flex + Bison + GCC + Python",
    font=("Arial", 8),
    bg=PANEL,
    fg=MUTED
).pack(side="left", padx=15, pady=7)

tk.Label(
    footer,
    text="VERSION 1.0",
    font=("Arial", 8, "bold"),
    bg=PANEL,
    fg=BLUE
).pack(side="right", padx=15)


# =====================================
# START APPLICATION
# =====================================

update_line_numbers()

# Set initial panel proportions
root.update_idletasks()
main.sash_place(0, 690, 0)

root.mainloop()

# python gui/app.py