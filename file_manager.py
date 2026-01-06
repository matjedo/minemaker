import os
import shutil
import tkinter as tk
from tkinter import messagebox, filedialog

def abrir_gerenciador(pasta_servidor):
    root = tk.Tk()
    root.title(f"Mine Maker - Arquivos ({os.path.basename(pasta_servidor)})")
    root.geometry("650x420")

    path_atual = tk.StringVar(value=pasta_servidor)

    lista = tk.Listbox(root)
    lista.pack(fill=tk.BOTH, expand=True)

    def atualizar():
        lista.delete(0, tk.END)
        for item in os.listdir(path_atual.get()):
            lista.insert(tk.END, item)

    def abrir():
        sel = lista.curselection()
        if not sel:
            return
        nome = lista.get(sel)
        caminho = os.path.join(path_atual.get(), nome)

        if os.path.isdir(caminho):
            path_atual.set(caminho)
            atualizar()
        else:
            with open(caminho, "r", errors="ignore") as f:
                conteudo = f.read()

            editor = tk.Toplevel(root)
            editor.title(nome)

            txt = tk.Text(editor)
            txt.pack(fill=tk.BOTH, expand=True)
            txt.insert("1.0", conteudo)

            def salvar():
                with open(caminho, "w") as f:
                    f.write(txt.get("1.0", tk.END))
                messagebox.showinfo("Salvo", "Arquivo salvo com sucesso.")

            tk.Button(editor, text="Salvar", command=salvar).pack()

    def deletar():
        sel = lista.curselection()
        if not sel:
            return
        nome = lista.get(sel)
        caminho = os.path.join(path_atual.get(), nome)

        if messagebox.askyesno("Confirmar", f"Deletar {nome}?"):
            try:
                if os.path.isdir(caminho):
                    shutil.rmtree(caminho)
                else:
                    os.remove(caminho)
                atualizar()
            except Exception as e:
                messagebox.showerror("Erro", str(e))

    def voltar():
        pai = os.path.dirname(path_atual.get())
        if pai.startswith(pasta_servidor):
            path_atual.set(pai)
            atualizar()

    def upload():
        arquivo = filedialog.askopenfilename()
        if not arquivo:
            return
        try:
            shutil.copy(arquivo, path_atual.get())
            atualizar()
            messagebox.showinfo("Upload", "Arquivo enviado com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def download():
        sel = lista.curselection()
        if not sel:
            return
        nome = lista.get(sel)
        caminho = os.path.join(path_atual.get(), nome)

        if os.path.isdir(caminho):
            messagebox.showwarning("Aviso", "Download de pastas não suportado.")
            return

        destino = filedialog.asksaveasfilename(initialfile=nome)
        if not destino:
            return

        try:
            shutil.copy(caminho, destino)
            messagebox.showinfo("Download", "Arquivo baixado com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    botoes = tk.Frame(root)
    botoes.pack(fill=tk.X)

    tk.Button(botoes, text="Abrir", command=abrir).pack(side=tk.LEFT)
    tk.Button(botoes, text="Voltar", command=voltar).pack(side=tk.LEFT)
    tk.Button(botoes, text="Enviar arquivo", command=upload).pack(side=tk.LEFT)
    tk.Button(botoes, text="Baixar arquivo", command=download).pack(side=tk.LEFT)
    tk.Button(botoes, text="Deletar", command=deletar).pack(side=tk.LEFT)

    atualizar()
    root.mainloop()
