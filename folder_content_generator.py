import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

def get_folder_contents(folder_path, ignore_items):
    """Obtém informações sobre pastas, arquivos e seus conteúdos com caminhos relativos, ignorando itens especificados."""
    output = []
    
    # Verifica se o caminho existe e é uma pasta
    if not os.path.isdir(folder_path):
        return ["Erro: O caminho especificado não é uma pasta válida."]
    
    # Obtém o nome da pasta principal
    folder_name = os.path.basename(folder_path)
    
    # Adiciona o nome da pasta principal com o prefixo //
    output.append(f"// {folder_name}")
    
    # Percorre a estrutura de diretórios
    for root, dirs, files in os.walk(folder_path):
        # Calcula o caminho relativo a partir da pasta base
        rel_path = os.path.relpath(root, os.path.dirname(folder_path))
        if rel_path == ".":
            rel_path = folder_name
        
        # Remove pastas ignoradas da lista de diretórios a serem processados
        dirs[:] = [d for d in dirs if os.path.basename(os.path.join(root, d)) not in ignore_items]
        
        # Adiciona subpastas com caminho relativo
        for dir_name in sorted(dirs):
            dir_rel_path = os.path.join(rel_path, dir_name).replace(os.sep, '/')
            output.append(f"// {dir_rel_path}/")
        
        # Adiciona arquivos e seus conteúdos com caminho relativo, exceto os ignorados
        for file_name in sorted(files):
            if file_name in ignore_items:
                continue
            file_rel_path = os.path.join(rel_path, file_name).replace(os.sep, '/')
            output.append(f"// {file_rel_path}")
            
            file_path = os.path.join(root, file_name)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    output.append(f"  // Conteúdo:")
                    output.append(f"  {content.replace('\n', '\n  ')}")
            except Exception as e:
                output.append(f"  // Erro ao ler o arquivo: {str(e)}")
            output.append("")  # Linha em branco após cada arquivo
    
    return output

def save_to_txt(content, output_path):
    """Salva o conteúdo em um arquivo .txt."""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(content))
        return True, f"Arquivo gerado com sucesso: {output_path}"
    except Exception as e:
        return False, f"Erro ao salvar o arquivo: {str(e)}"

class FolderContentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de Conteúdo de Pastas")
        self.root.geometry("700x500")
        
        # Lista para armazenar Checkbuttons e seus estados
        self.check_vars = {}
        self.items = []
        
        # Frame principal
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Campo e botão para selecionar a pasta
        self.folder_path = tk.StringVar()
        ttk.Label(self.main_frame, text="Pasta a analisar:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.folder_entry = ttk.Entry(self.main_frame, textvariable=self.folder_path, width=60)
        self.folder_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        ttk.Button(self.main_frame, text="Selecionar Pasta", command=self.select_folder).grid(row=1, column=1, padx=5)
        
        # Frame para a lista com rolagem
        ttk.Label(self.main_frame, text="Marque as caixas para IGNORAR pastas e arquivos:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.list_frame = ttk.Frame(self.main_frame)
        self.list_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Canvas e Scrollbar para rolagem
        self.canvas = tk.Canvas(self.list_frame)
        self.scrollbar = ttk.Scrollbar(self.list_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Botão para gerar o arquivo
        ttk.Button(self.main_frame, text="Gerar Arquivo .txt", command=self.generate_file).grid(row=4, column=0, columnspan=2, pady=10)
        
        # Área de status
        self.status_label = ttk.Label(self.main_frame, text="")
        self.status_label.grid(row=5, column=0, columnspan=2, pady=5)
        
        # Configurar redimensionamento
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(3, weight=1)
        self.list_frame.columnconfigure(0, weight=1)
        self.list_frame.rowconfigure(0, weight=1)
        
        self.folder_selected = False
    
    def select_folder(self):
        """Abre um diálogo para selecionar a pasta e lista seus conteúdos."""
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)
            self.status_label.config(text="Pasta selecionada: " + folder)
            self.folder_selected = True
            self.populate_list(folder)
    
    def populate_list(self, folder):
        """Popula a lista com Checkbuttons para pastas e arquivos."""
        # Limpa a lista anterior
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.check_vars.clear()
        self.items = []
        
        # Lista pastas e arquivos do primeiro nível
        try:
            items = os.listdir(folder)
            self.items = sorted(items)
            for i, item in enumerate(self.items):
                item_path = os.path.join(folder, item)
                size = ""
                if os.path.isfile(item_path):
                    size = f"{os.path.getsize(item_path) / 1024:.2f} KB"
                else:
                    size = "[Pasta]"
                
                # Cria variável para o Checkbutton
                var = tk.BooleanVar(value=False)
                self.check_vars[item] = var
                
                # Cria frame para alinhar Checkbutton e Label
                item_frame = ttk.Frame(self.scrollable_frame)
                item_frame.grid(row=i, column=0, sticky=tk.W, pady=2)
                
                # Checkbutton
                ttk.Checkbutton(item_frame, variable=var).grid(row=0, column=0, padx=5)
                
                # Label com nome e tamanho
                ttk.Label(item_frame, text=f"{item} ({size})").grid(row=0, column=1, sticky=tk.W)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar conteúdos: {str(e)}")
            self.folder_selected = False
    
    def reset_form(self):
        """Reseta todas as informações preenchidas."""
        self.folder_path.set("")
        self.folder_selected = False
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.check_vars.clear()
        self.items = []
        self.status_label.config(text="")
    
    def generate_file(self):
        """Gera o arquivo .txt com base nas entradas."""
        if not self.folder_selected:
            messagebox.showerror("Erro", "Por favor, selecione uma pasta.")
            return
        
        folder_path = self.folder_path.get().strip()
        if not folder_path:
            messagebox.showerror("Erro", "Por favor, selecione uma pasta.")
            return
        
        # Obtém itens a ignorar (Checkbuttons marcados)
        ignore_items = [item for item, var in self.check_vars.items() if var.get()]
        
        # Gera o conteúdo
        content = get_folder_contents(folder_path, ignore_items)
        
        # Abre diálogo de "Salvar como"
        default_filename = f"{os.path.basename(folder_path)}.txt"
        output_file = filedialog.asksaveasfilename(
            initialfile=default_filename,
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        # Verifica se o usuário cancelou o diálogo
        if not output_file:
            messagebox.showerror("Erro", "Nenhum arquivo selecionado para salvar.")
            return
        
        # Salva o conteúdo
        success, message = save_to_txt(content, output_file)
        self.status_label.config(text=message)
        if success:
            messagebox.showinfo("Sucesso", message)
            self.reset_form()  # Reseta o formulário após salvar com sucesso
        else:
            messagebox.showerror("Erro", message)

def main():
    root = tk.Tk()
    app = FolderContentApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()