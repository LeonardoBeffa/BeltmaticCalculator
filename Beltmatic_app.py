import math
import queue
import tkinter as tk
import customtkinter as ctk
import json
import os
import sqlite3

class QueueItem:
    def __init__(self, value, steps, operator, steps_list):
        self.value = value
        self.steps = steps
        self.operator = operator
        self.steps_list = steps_list

    def __lt__(self, other):
        return self.steps < other.steps

def f_value_evaluation(a, b, target):
    a_dif = (1 - abs(target - a.value) / target) * 2
    b_dif = (1 - abs(target - b.value) / target) * 2
    return a.steps - a_dif - (b.steps - b_dif)

def apply_operator(a, b, operator):
    if operator == '+':
        return a + b
    elif operator == '-':
        return a - b
    elif operator == '*':
        return a * b
    elif operator == '/':
        return a / b if b != 0 else None
    elif operator == '^':
        return math.pow(a, b)
    return None

def skip_unnecessary_operators(value, current_value, operator, target):
    if (operator in ['+', '*', '^'] and (current_value > target or value > target)) or \
        (operator in ['-', '/'] and current_value < target) or \
        (value < 0 or current_value < 0) or \
        (value == 1 and operator in ['*', '/', '^']):
        return True
    return False

def least_steps(target, max_src, allowed_operators):
    allowed_numbers = [i for i in range(1, max_src + 1) if i != 10]
    visited = set()
    pq = queue.PriorityQueue()
    pq.put((0, QueueItem(0, 0, '', [])))
    calc_count = 0

    while not pq.empty():
        _, element = pq.get()
        for num in allowed_numbers:
            for operator in allowed_operators:
                if skip_unnecessary_operators(num, element.value, operator, target):
                    continue

                new_value = apply_operator(element.value, num, operator)
                calc_count += 1

                if new_value is None or new_value > target + max_src or new_value < 0 or new_value in visited:
                    continue

                visited.add(new_value)
                new_steps_list = element.steps_list + [[element.value, num, operator, new_value]]

                if new_value == target:
                    return new_steps_list[1:]

                pq.put((element.steps + 1, QueueItem(new_value, element.steps + 1, operator, new_steps_list)))

    return []

def run_calculation():
    try:
        target = int(entry_target.get())
        max_src = int(entry_max_src.get())
        if target <= 0 or max_src <= 0:
            raise ValueError("Valores devem ser positivos e inteiros.")
        steps = least_steps(target, max_src, ['+', '-', '*', '^'])
        result_text.delete(1.0, tk.END)
        for step in steps:
            result_text.insert(tk.END, f"{step[0]} ", 'number')
            result_text.insert(tk.END, f"{step[2]} ", 'operator')
            result_text.insert(tk.END, f"{step[1]} = ", 'number')
            result_text.insert(tk.END, f"{step[3]}\n", 'result')

        save_to_history_db(target, max_src, steps)
        update_history_listbox()
    except ValueError as e:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Error: Valores devem ser positivos e inteiros.\n")

def init_db():
    conn = sqlite3.connect('calculations.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS history (
                        id INTEGER PRIMARY KEY,
                        target INTEGER NOT NULL,
                        max_src INTEGER NOT NULL,
                        steps TEXT NOT NULL
                    )''')
    conn.commit()
    conn.close()

def save_to_history_db(target, max_src, steps):
    steps_str = json.dumps(steps)
    conn = sqlite3.connect('calculations.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM history WHERE target = ? AND max_src = ?", (target, max_src))
    existing_record = cursor.fetchone()
    if existing_record is not None:
        return

    cursor.execute("INSERT INTO history (target, max_src, steps) VALUES (?, ?, ?)", (target, max_src, steps_str))
    conn.commit()
    conn.close()

def load_history_db():
    conn = sqlite3.connect('calculations.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, target, max_src, steps FROM history")
    rows = cursor.fetchall()
    history = []
    for row in rows:
        id, target, max_src, steps_str = row
        steps = json.loads(steps_str)
        history.append({"id": id, "target": target, "max_src": max_src, "steps": steps})
    conn.close()
    return history

def update_history_listbox():
    history = load_history_db()
    history_listbox.delete(0, tk.END)
    for idx, item in enumerate(history):
        history_listbox.insert(tk.END, f"{idx + 1}: {item['target']} (Extrator: {item['max_src']})")

def show_history_details(event):
    selected_index = history_listbox.curselection()
    if selected_index:
        index = selected_index[0]
        history = load_history_db()
        steps = history[index]["steps"]
        result_text.delete(1.0, tk.END)
        for step in steps:
            result_text.insert(tk.END, f"{step[0]} ", 'number')
            result_text.insert(tk.END, f"{step[2]} ", 'operator')
            result_text.insert(tk.END, f"{step[1]} = ", 'number')
            result_text.insert(tk.END, f"{step[3]}\n", 'result')
        delete_button.configure(state="normal")

def delete_history_item():
    selected_index = history_listbox.curselection()
    if selected_index:
        index = selected_index[0]
        history = load_history_db()
        item_id = history[index]["id"]
        
        confirm = tk.messagebox.askyesno("Confirmação", "Você realmente deseja excluir este item?")
        if confirm:
            conn = sqlite3.connect('calculations.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM history WHERE id = ?", (item_id,))
            conn.commit()
            conn.close()
            update_history_listbox()
            result_text.delete(1.0, tk.END)
            delete_button.configure(state="disabled")

# Configurar o tema do customtkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Configurar a janela principal
root = ctk.CTk()
root.title("Calculadora de Menor Número de Passos")
root.geometry("800x250")

# Frame para os campos de entrada e o histórico (lado a lado)
frame_top = ctk.CTkFrame(root)
frame_top.pack(pady=10)

frame_input = ctk.CTkFrame(frame_top)
frame_input.pack(side="left", padx=20)

frame_history = ctk.CTkFrame(frame_top)
frame_history.pack(side="right", padx=20)

# Widgets da interface
label_target = ctk.CTkLabel(frame_input, text="Valor Desejado:")
label_target.grid(row=0, column=0, padx=5, pady=10, sticky='e')

entry_target = ctk.CTkEntry(frame_input, placeholder_text='Exemplo - 4682')
entry_target.grid(row=0, column=1, padx=5, pady=10)

label_max_src = ctk.CTkLabel(frame_input, text="Extrator Máximo:")
label_max_src.grid(row=1, column=0, padx=5, pady=10, sticky='e')

entry_max_src = ctk.CTkEntry(frame_input, placeholder_text='Exemplo - 10')
entry_max_src.grid(row=1, column=1, padx=5, pady=10)

calculate_button = ctk.CTkButton(frame_input, text="Calcular", command=run_calculation)
calculate_button.grid(row=2, columnspan=2, pady=10)

# Frame para o resultado
frame_result = ctk.CTkFrame(frame_top)
frame_result.pack(pady=10)

result_label = ctk.CTkLabel(frame_result, text='Passos:')
result_label.pack(pady=1)

result_text = tk.Text(frame_result, wrap=tk.WORD, height=10, width=30, bg='#2B2B2B', foreground='white', font=14)
result_text.tag_config('number', foreground='white', justify='center')
result_text.tag_config('operator', foreground='red', justify='center')
result_text.tag_config('result', foreground='green', justify='center')
result_text.pack(pady=5)

# Frame para o histórico
history_label = ctk.CTkLabel(frame_history, text='Histórico de Cálculos:')
history_label.pack(pady=1)

history_listbox = tk.Listbox(frame_history, height=10, width=30, bg='#2B2B2B', foreground='white')
history_listbox.pack(pady=5)
history_listbox.bind('<<ListboxSelect>>', show_history_details)

delete_button = ctk.CTkButton(frame_history, text="Deletar", command=delete_history_item, state="disabled")
delete_button.pack(pady=5)

# Inicializar o banco de dados e carregar histórico ao iniciar o programa
init_db()
update_history_listbox()

# Iniciar o loop principal da interface
root.mainloop()
