import os
import subprocess
import sys
from tkinter import filedialog
import tkinter as tk
import whisper
import ollama

model = whisper.load_model("base", device="cpu")

def transcribe_audio(selected_file: str):
    try:
        label_file_explorer.config(text="Processing...", foreground="orange")
        window.update()

        file_dir = os.path.dirname(selected_file)
        file_name = os.path.splitext(os.path.basename(selected_file))[0]

        result = model.transcribe(selected_file)
        text = extract_medical_context(result['text'])
        parts = text.split(",")
        final = "\n".join(parts)
        print(final)

        tex_file_path = os.path.join(file_dir, f"{file_name}.tex")

        with open(tex_file_path, 'w', encoding="utf-8") as f:
            f.write('\\documentclass{article}\n')
            f.write('\\usepackage[english,romanian]{babel}\n')
            f.write('\\usepackage{graphicx}\n')
            f.write('\\usepackage[margin=2cm]{geometry}\n')
            f.write('\\usepackage{parskip}\n')
            f.write('\\begin{document}\n')

            f.write('\\begin{center}\n')
            f.write('\\includegraphics[width=3cm]{/home/raulpuscas/ai/proj/logo.jpg}\\\\[0.5cm]\n')
            f.write('{\\LARGE\\bfseries Fisa medicala}\\\\[0.2cm]\n')
            f.write('{\\normalsize Dr. Echipa AI-VROS}\\\\[0.3cm]\n')
            f.write('\\end{center}\n')

            for line in parts:
                f.write(line.strip() + "\\\\\n")

            f.write('\\vspace{0.8cm}\n')
            f.write('\\begin{center}\n')
            f.write('\\small Multumim pentru increderea acordata in clinica LAB AI 2025!\n')
            f.write('\\end{center}\n')
            f.write('\\end{document}\n')

        if sys.platform == 'linux':
            pid = os.fork()
            if pid == 0:  
                try:
                    subprocess.run(
                        ['pdflatex', '-interaction=nonstopmode', tex_file_path],
                        check=True,
                        cwd=file_dir
                    )
                    os._exit(0)  
                except Exception as e:
                    print(f"Child process error: {e}")
                    os._exit(1)
        else:
            subprocess.run([
                r'C:\Users\ioana\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe',
                tex_file_path
            ], check=True, cwd=file_dir)

        label_file_explorer.config(text=f"Success! PDF generated: {file_name}.pdf", foreground="green")

        pdf_path = os.path.join(file_dir, f"{file_name}.pdf")

        if sys.platform == 'linux':
            if 'pid' in locals():
                os.waitpid(pid, 0)

        os.startfile(pdf_path) if sys.platform == 'win32' else subprocess.run(['xdg-open', pdf_path])

    except Exception as e:
        label_file_explorer.config(text=f"Error: {str(e)}", foreground="red")
        print(f"An error occurred: {e}")

def extract_medical_context(text: str):
    prompt = (
        "You are a medical scribe. Your task is to extract all medically relevant information from the transcript below.\n\n"
        "Focus on:\n"
        "- Diagnoses\n"
        "- Findings\n"
        "- Measurements\n"
        "- Clinical impressions\n"
        "- Anatomical references\n"
        "- Procedures\n\n"
        "Do not include any formatting, categories, or explanations. Simply list the extracted terms and phrases line by line, as plain text.\n"
        "Avoid any additional comments or reasoning.\n\n"
        f"Transcript:\n{text}\n\n"
        "Extracted medical content:"
    )

    response = ollama.chat(
        model='llama3-chatqa',
        messages=[{
            'role': 'user',
            'content': prompt
        }]
    )
    return response['message']['content']

def browseFiles():
    global selected_file
    selected_file = filedialog.askopenfilename(initialdir="/",
                                               title="Select a File",
                                               filetypes=(("Audio files", "*.wav;*.m4a;*.flac;*.mp3;*.ogg"), ("All files", "*.*")))
    if selected_file:
        label_file_explorer.configure(text="File Opened: " + selected_file)
        print("Selected file path:", selected_file)
        transcribe_audio(selected_file)


import tkinter as tk
from tkinter import ttk



def exit():
    window.destroy()

window = tk.Tk()
window.title("File Explorer")
window.geometry("600x400")
window.config(background="#f0f0f0")

style = ttk.Style()
style.theme_use('clam')


style.configure('TLabel', background="#f0f0f0", font=('Helvetica', 12))
style.configure('TButton', font=('Helvetica', 10), padding=6)
style.configure('Title.TLabel', font=('Helvetica', 14, 'bold'))

header_frame = ttk.Frame(window, style='TFrame')
header_frame.grid(column=0, row=0, columnspan=2, pady=10, padx=10, sticky="ew")

label_title = ttk.Label(header_frame,
                       text="File Explorer",
                       style='Title.TLabel',
                       foreground="#2c3e50")
label_title.pack()

content_frame = ttk.Frame(window, style='TFrame')
content_frame.grid(column=0, row=1, padx=20, pady=20, sticky="nsew")

label_file_explorer = ttk.Label(content_frame,
                               text="Select a file to explore",
                               style='TLabel',
                               foreground="#3498db")
label_file_explorer.grid(column=0, row=0, pady=(0, 20))

button_frame = ttk.Frame(content_frame)
button_frame.grid(column=0, row=1, pady=10)

button_explore = ttk.Button(button_frame,
                           text="Browse Files",
                           command=browseFiles,
                           style='Accent.TButton')
button_explore.grid(column=0, row=0, padx=5)

button_exit = ttk.Button(button_frame,
                        text="Exit",
                        command=exit,
                        style='TButton')
button_exit.grid(column=1, row=0, padx=5)


window.columnconfigure(0, weight=1)
window.rowconfigure(1, weight=1)
content_frame.columnconfigure(0, weight=1)

separator = ttk.Separator(window, orient='horizontal')
separator.grid(column=0, row=2, sticky="ew", pady=5)

status_bar = ttk.Label(window,
                      text="Ready",
                      relief='sunken',
                      anchor='w',
                      font=('Helvetica', 8))
status_bar.grid(column=0, row=3, sticky="ew", padx=5, pady=5)

style.configure('Accent.TButton',
               foreground='white',
               background='#3498db',
               font=('Helvetica', 10, 'bold'))
style.map('Accent.TButton',
         foreground=[('pressed', 'white'), ('active', 'white')],
         background=[('pressed', '#2980b9'), ('active', '#2980b9')])

window.mainloop()
