from tkinter import *
from tkinter import messagebox, ttk
from banco import conectar, adicionar_aluno, listar_alunos, excluir_aluno, editar_aluno

# conectando ao banco
con, cur = conectar()

# limpa depois de adicionar e editar
def limpar_campos():
    entry_nome.delete(0, END)
    entry_nota1.delete(0, END)
    entry_nota2.delete(0, END)
    entry_simulado1.delete(0, END)
    entry_simulado2.delete(0, END)
    entry_busca.delete(0, END)

# banco
def adicionar():
    nome = entry_nome.get()
    nota1 = entry_nota1.get()
    nota2 = entry_nota2.get()
    simulado1 = entry_simulado1.get()
    simulado2 = entry_simulado2.get()
    
    if not nome or not nota1 or not nota2 or not simulado1 or not simulado2:
        messagebox.showerror("Erro ao Adicionar", "Todos os campos são obrigatórios.")
        return
    
    try:
        nota1 = float(nota1)
        nota2 = float(nota2) 
        simulado1 = float(simulado1) 
        simulado2 = float(simulado2) 
        if nota1 > 10 or nota1 < 0 or nota2 > 10 or nota2 < 0:
            messagebox.showerror("Erro na Nota", "Os campos de notas não podem ser maiores que 10 ou menores que 0.")
            return
        if simulado1 > 1 or simulado1 < 0 or simulado2 > 1 or simulado2 <0:
            messagebox.showerror("Erro no Simulado", "Os campos de simulados não podem ser maiores que 1 ou menores que 0.")
            return
    except ValueError:
        messagebox.showerror("Erro ao Adicionar", "As notas devem ser números.")
        return
    
    adicionar_aluno(cur, nome, nota1, nota2, simulado1, simulado2)
    con.commit()
    listar()
    limpar_campos()

def listar(filtro=""):
    for item in tree.get_children():
        tree.delete(item)
    for row in listar_alunos(cur, filtro):
        aluno_id, nome, nota1, nota2, simulado1, simulado2, media = row
        if media <= 9.9:
            media = media + simulado1
            if media <= 9.9:
                media = media + simulado2
                status = "Aprovado" if media >= 6 else "Reprovado"
                tag = "Aprovado" if media >= 6 else "Reprovado"
        if media >= 10:
            media = 10.0
            status = "Aprovado" if media >= 6 else "Reprovado"
            tag = "Aprovado" if media >= 6 else "Reprovado"
        tree.insert("", "end", iid=aluno_id, values=(aluno_id, nome, nota1, nota2, simulado1, simulado2, media, status), tags=(tag,))
    tree.tag_configure("Aprovado", foreground="green")
    tree.tag_configure("Reprovado", foreground="red")

def excluir():
    selected_item = tree.selection()
    if selected_item:
        aluno_id = tree.item(selected_item)["values"][0]
        excluir_aluno(cur, aluno_id)
        con.commit()
        listar()
        limpar_campos()
    else:
        messagebox.showwarning("Seleção vazia", "Por favor, selecione um aluno para excluir.")

def editar():
    selected_item = tree.selection()
    if selected_item:
        aluno_id = tree.item(selected_item)["values"][0]
        nome = entry_nome.get()
        nota1 = entry_nota1.get()
        nota2 = entry_nota2.get()
        simulado1 = entry_simulado1.get()
        simulado2 = entry_simulado2.get()
        
        if not nome or not nota1 or not nota2 or not simulado1 or not simulado2:
            messagebox.showerror("Erro ao Editar", "Todos os campos são obrigatórios.")
            return

        try:
            nota1 = float(nota1)
            nota2 = float(nota2)
            simulado1 = float(simulado1)
            simulado2 = float(simulado2)
            if nota1 > 10 or nota1 < 0 or nota2 > 10 or nota2 < 0:
                messagebox.showerror("Erro ao Editar", "Os campos de notas não podem ser maiores que 10 ou menores que 0.")
                return
            if simulado1 > 1 or simulado1 < 0 or simulado2 > 1 or simulado2 <0:
                messagebox.showerror("Erro no Simulado", "Os campos de simulados não podem ser maiores que 1 ou menores que 0.")
                return
        except ValueError:
            messagebox.showerror("Erro ao Editar", "As notas devem ser números.")
            return

        editar_aluno(cur, aluno_id, nome, nota1, nota2, simulado1, simulado2)
        con.commit()
        listar()
        limpar_campos()
    else:
        messagebox.showwarning("Seleção vazia", "Por favor, selecione um aluno para editar.")

def buscar():
    filtro = entry_busca.get()
    listar(filtro)
    entry_busca.delete(0, END)

def on_tree_select(event):
    selected_item = tree.selection()
    if selected_item:
        aluno_id = selected_item[0]
        values = tree.item(aluno_id)["values"]
        entry_nome.delete(0, END)
        entry_nome.insert(0, values[1])
        entry_nota1.delete(0, END)
        entry_nota1.insert(0, values[2])
        entry_nota2.delete(0, END)
        entry_nota2.insert(0, values[3])
        entry_simulado1.delete(0, END)
        entry_simulado1.insert(0, values[4])
        entry_simulado2.delete(0, END)
        entry_simulado2.insert(0, values[5])

# info janela
root = Tk()
root.title("Cadastro de Alunos")
root.geometry("720x450")
root.resizable(False, False)
root.configure(bg="#f0f0f0")

# logo
root.iconbitmap("logo.ico")  # precisa ser .ico

# label de entrada
Label(root, text="Nome:", bg="#f0f0f0", fg="#333333", font=("Franklin Gothic", 10)).grid(row=0, column=0, padx=(0, 2), pady=(15,5), sticky="e")
entry_nome = Entry(root, width=41, font=("Arial", 10))
entry_nome.grid(row=0, column=1, padx=2, pady=(15,5), sticky="w", columnspan=2)

Label(root, text="Nota 1:", bg="#f0f0f0", fg="#333333", font=("Franklin Gothic", 10)).grid(row=1, column=0, padx=(5, 2), pady=5, sticky="e")
entry_nota1 = Entry(root, width=10, font=("Arial", 10))
entry_nota1.grid(row=1, column=1, padx=(2, 138), pady=5, sticky="w")

Label(root, text="Nota 2:", bg="#f0f0f0", fg="#333333", font=("Franklin Gothic", 10)).grid(row=2, column=0, padx=(5, 2), pady=5, sticky="e")
entry_nota2 = Entry(root, width=10, font=("Arial", 10))
entry_nota2.grid(row=2, column=1, padx=(2, 100), pady=5, sticky="w")

Label(root, text="Simulado 1:", bg="#f0f0f0", fg="#333333", font=("Franklin Gothic", 10)).grid(row=1, column=1, padx=(5, 2), pady=5, sticky="e")
entry_simulado1 = Entry(root, width=10, font=("Arial", 10))
entry_simulado1.grid(row=1, column=2, padx=2, pady=5, sticky="w")

Label(root, text="Simulado 2:", bg="#f0f0f0", fg="#333333", font=("Franklin Gothic", 10)).grid(row=2, column=1, padx=(5, 2), pady=5, sticky="e")
entry_simulado2 = Entry(root, width=10, font=("Arial", 10))
entry_simulado2.grid(row=2, column=2, padx=2, pady=5, sticky="w")

# criando os botões
Button(root, text="Adicionar", command=adicionar, bg="#4CAF50", fg="white", font=("Franklin Gothic", 10), width=10).grid(row=0, column=2, padx=(3, 2), pady=(15,5))
Button(root, text="Excluir", command=excluir, bg="#E83B3B", fg="white", font=("Franklin Gothic", 10), width=10).grid(row=2, column=2, padx=2, pady=5)
Button(root, text="Editar", command=editar, bg="#FFC517", fg="white", font=("Franklin Gothic", 10), width=10).grid(row=1, column=2, padx=(2, 5), pady=5)

# botão de buscar
Label(root, text="Buscar:", bg="#f0f0f0", fg="#333333", font=("Franklin Gothic", 10)).grid(row=5, column=0, padx=(5, 2), pady=5, sticky="e")
entry_busca = Entry(root, width=41, font=("Franklin Gothic", 10))
entry_busca.grid(row=5, column=1, padx=2, pady=5, sticky="w", columnspan=2)
Button(root, text="Buscar", command=buscar, bg="#3B6FE8", fg="white", font=("Franklin Gothic", 10), width=10).grid(row=5, column=2, padx=(2, 5))

# descrição tabela
columns = ("ID", "Nome", "Nota 1", "Nota 2", "Simulado 1", "Simulado 2", "Média", "Status")
tree = ttk.Treeview(root, columns=columns, show="headings", height=8)
tree.heading("ID", text="ID")
tree.heading("Nome", text="Nome")
tree.heading("Nota 1", text="Nota 1")
tree.heading("Nota 2", text="Nota 2")
tree.heading("Simulado 1", text="Simulado 1")
tree.heading("Simulado 2", text="Simulado 2")
tree.heading("Média", text="Média")
tree.heading("Status", text="Status")

# tamanho tabela
tree.column("ID", width=50, anchor="center")
tree.column("Nome", width=100, anchor="center")
tree.column("Nota 1", width=80, anchor="center")
tree.column("Nota 2", width=80, anchor="center")
tree.column("Simulado 1", width=100, anchor="center")
tree.column("Simulado 2", width=100, anchor="center")
tree.column("Média", width=80, anchor="center")
tree.column("Status", width=100, anchor="center")

# style
style = ttk.Style()
style.configure("Treeview.Heading", font=("Franklin Gothic", 11, "bold"))
style.configure("Treeview", font=("Franklin Gothic", 10))

tree.grid(row=6, column=0, columnspan=3, pady=20)

# centralizando a tabela
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(2, weight=1)
listar()

# puxa dados
tree.bind("<<TreeviewSelect>>", on_tree_select)

root.mainloop()

# fechando o banco
con.close()