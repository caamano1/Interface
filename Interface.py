import json
import os
import tkinter as tk
from tkinter import messagebox

ARQUIVO_JSON = "tarefas.json"

def carregar_tarefas():
    if os.path.exists(ARQUIVO_JSON):
        with open(ARQUIVO_JSON, "r") as arquivo:
            return json.load(arquivo)
    return []

def salvar_tarefas(tarefas):
    with open(ARQUIVO_JSON, "w") as arquivo:
        json.dump(tarefas, arquivo, indent=4)

def adicionar_tarefa():
    titulo = entrada_tarefa.get().strip()
    if titulo:
        tarefas = carregar_tarefas()
        tarefas.append({"titulo": titulo, "status": "Pendente"})
        salvar_tarefas(tarefas)
        atualizar_lista()
        entrada_tarefa.delete(0, tk.END)
    else:
        messagebox.showwarning("Aviso", "Digite um título para a tarefa.")

def listar_tarefas():
    tarefas = carregar_tarefas()
    texto_tarefas.delete(1.0, tk.END)
    for tarefa in tarefas:
        texto_tarefas.insert(tk.END, f"{tarefa['titulo']} - {tarefa['status']}\n")

def atualizar_lista():
    for widget in frame_tarefas.winfo_children():
        widget.destroy()
    tarefas = carregar_tarefas()
    for idx, tarefa in enumerate(tarefas):
        var = tk.StringVar(value=tarefa["status"])
        frame_tarefa = tk.Frame(frame_tarefas)
        frame_tarefa.pack(anchor='w', pady=2)

        titulo_label = tk.Label(frame_tarefa, text=tarefa['titulo'])
        titulo_label.pack(side=tk.LEFT)

        radio_pendente = tk.Radiobutton(frame_tarefa, text="Pendente", variable=var, value="Pendente", command=lambda i=idx, v=var: marcar_status(i, v.get()))
        radio_pendente.pack(side=tk.LEFT)

        radio_em_progresso = tk.Radiobutton(frame_tarefa, text="Em Progresso", variable=var, value="Em Progresso", command=lambda i=idx, v=var: marcar_status(i, v.get()))
        radio_em_progresso.pack(side=tk.LEFT)

        radio_concluida = tk.Radiobutton(frame_tarefa, text="Concluída", variable=var, value="Concluída", command=lambda i=idx, v=var: marcar_status(i, v.get()))
        radio_concluida.pack(side=tk.LEFT)

def marcar_status(indice, status):
    tarefas = carregar_tarefas()
    tarefas[indice]["status"] = status
    salvar_tarefas(tarefas)
    atualizar_lista()

def excluir_tarefa():
    tarefas = carregar_tarefas()
    tarefas = [tarefa for tarefa in tarefas if tarefa["status"] != "Concluída"]
    salvar_tarefas(tarefas)
    atualizar_lista()

janela = tk.Tk()
janela.title("Gerenciador de Tarefas")
janela.configure(bg="white")

frame_topo = tk.Frame(janela)
frame_topo.pack(pady=10)

entrada_tarefa = tk.Entry(frame_topo, width=40)
entrada_tarefa.pack(side=tk.LEFT, padx=5)

botao_adicionar = tk.Button(frame_topo, text="Adicionar", command=adicionar_tarefa)
botao_adicionar.pack(side=tk.LEFT)

frame_tarefas = tk.Frame(janela)
frame_tarefas.pack(pady=10)

texto_tarefas = tk.Text(janela, width=50, height=10)
texto_tarefas.pack(pady=5)

botao_listar = tk.Button(janela, text="Listar Tarefas", command=listar_tarefas)
botao_listar.pack(pady=5)

botao_excluir = tk.Button(janela, text="Excluir Concluídas", command=excluir_tarefa)
botao_excluir.pack(pady=5)

atualizar_lista()

janela.mainloop()
