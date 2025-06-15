import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class FolderContentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de Conteúdo de Pastas")
        self.root.geometry("900x700")
        
        # Conjunto para armazenar itens selecionados
        self.selected_items = set()
        self.folder_path = tk.StringVar()
        
        # Frame superior para seleção de pasta
        top_frame = ttk.Frame(root, padding=10)
        top_frame.pack(fill=tk.X)
        
        ttk.Label(top_frame, text="Pasta selecionada:").pack(anchor=tk.W)
        entry_frame = ttk.Frame(top_frame)
        entry_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Entry(entry_frame, textvariable=self.folder_path, width=70).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(entry_frame, text="Selecionar Pasta", command=self.select_folder).pack(side=tk.LEFT, padx=(5, 0))
        
        # Frame para instruções
        instruction_frame = ttk.Frame(root, padding=(10, 0, 10, 10))
        instruction_frame.pack(fill=tk.X)
        
        ttk.Label(instruction_frame, text="Marque as pastas e arquivos que deseja INCLUIR no relatório:", 
                 font=('TkDefaultFont', 9, 'bold')).pack(anchor=tk.W)
        ttk.Label(instruction_frame, text="• Clique nos itens para marcar/desmarcar", 
                 font=('TkDefaultFont', 8)).pack(anchor=tk.W, padx=(10, 0))
        ttk.Label(instruction_frame, text="• Marcar uma pasta inclui todo seu conteúdo", 
                 font=('TkDefaultFont', 8)).pack(anchor=tk.W, padx=(10, 0))
        
        # Frame para TreeView com scrollbar
        tree_frame = ttk.Frame(root)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10)
        
        # Criar TreeView com scrollbars
        self.tree = ttk.Treeview(tree_frame, selectmode='none')
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Layout das scrollbars e treeview
        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)
        
        self.tree.heading("#0", text="Estrutura de Pastas e Arquivos (clique para marcar/desmarcar)")
        
        # Bind events
        self.tree.bind("<<TreeviewOpen>>", self.on_open)
        self.tree.bind("<Button-1>", self.on_click)
        
        # Frame inferior com controles
        bottom_frame = ttk.Frame(root, padding=10)
        bottom_frame.pack(fill=tk.X)
        
        # Frame para controles de seleção
        control_frame = ttk.Frame(bottom_frame)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.select_all_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(control_frame, text="Selecionar Tudo", 
                       variable=self.select_all_var, command=self.toggle_all).pack(side=tk.LEFT)
        
        ttk.Button(control_frame, text="Expandir Tudo", command=self.expand_all).pack(side=tk.LEFT, padx=(10, 0))
        ttk.Button(control_frame, text="Recolher Tudo", command=self.collapse_all).pack(side=tk.LEFT, padx=(5, 0))
        
        # Botão de gerar arquivo
        ttk.Button(control_frame, text="Gerar Arquivo .txt", 
                  command=self.generate_file, style='Accent.TButton').pack(side=tk.RIGHT)
        
        # Label de status
        self.status_label = ttk.Label(bottom_frame, text="Selecione uma pasta para começar", 
                                     font=('TkDefaultFont', 8))
        self.status_label.pack(fill=tk.X)
        
        # Variável para controlar expansão automática
        self.auto_expanding = False

    def select_folder(self):
        """Seleciona uma pasta e carrega sua estrutura na TreeView"""
        folder = filedialog.askdirectory()
        if not folder:
            return
        
        self.folder_path.set(folder)
        self.tree.delete(*self.tree.get_children())
        self.selected_items.clear()
        self.select_all_var.set(False)
        
        # Criar nó raiz
        root_name = os.path.basename(folder)
        root_node = self.tree.insert("", "end", text=f"☐ {root_name}", 
                                    open=False, values=[folder, "folder"])
        
        # Adicionar placeholder para permitir expansão
        self.tree.insert(root_node, "end", text="Carregando...", values=["DUMMY"])
        
        self.update_status(f"Pasta carregada: {folder}")

    def on_open(self, event):
        """Evento quando um nó é expandido"""
        if self.auto_expanding:
            return
            
        node = self.tree.focus()
        if not node:
            return
            
        values = self.tree.item(node, "values")
        if not values or len(values) < 1:
            return
            
        path = values[0]
        
        # Verificar se já foi carregado (tem apenas o placeholder)
        children = self.tree.get_children(node)
        if len(children) == 1:
            child_values = self.tree.item(children[0], "values")
            if child_values and child_values[0] == "DUMMY":
                self.tree.delete(children[0])
                self.populate_node(node, path)

    def populate_node(self, parent_node, path):
        """Popula um nó com seus filhos (pastas e arquivos)"""
        try:
            if not os.path.isdir(path):
                return
                
            entries = []
            # Listar conteúdo da pasta
            for entry in os.listdir(path):
                full_path = os.path.join(path, entry)
                if os.path.isdir(full_path):
                    entries.append((entry, full_path, "folder"))
                else:
                    # Adicionar informação de tamanho para arquivos
                    try:
                        size = os.path.getsize(full_path)
                        size_str = self.format_size(size)
                        entries.append((f"{entry} ({size_str})", full_path, "file"))
                    except:
                        entries.append((entry, full_path, "file"))
            
            # Ordenar: pastas primeiro, depois arquivos
            entries.sort(key=lambda x: (x[2] == "file", x[0].lower()))
            
            for display_name, full_path, item_type in entries:
                node = self.tree.insert(parent_node, "end", 
                                      text=f"☐ {display_name}", 
                                      values=[full_path, item_type])
                
                # Se for pasta, adicionar placeholder para permitir expansão
                if item_type == "folder":
                    self.tree.insert(node, "end", text="Carregando...", values=["DUMMY"])
                    
        except PermissionError:
            self.tree.insert(parent_node, "end", 
                           text="❌ Acesso negado", 
                           values=[])
        except Exception as e:
            self.tree.insert(parent_node, "end", 
                           text=f"❌ Erro: {str(e)}", 
                           values=[])

    def format_size(self, size_bytes):
        """Formata o tamanho do arquivo em uma string legível"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"

    def on_click(self, event):
        """Evento de clique na TreeView"""
        region = self.tree.identify("region", event.x, event.y)
        if region != "tree":
            return
        
        node = self.tree.identify_row(event.y)
        if not node:
            return
        
        values = self.tree.item(node, "values")
        if not values or values[0] == "DUMMY":
            return
            
        path = values[0]
        text = self.tree.item(node, "text")
        
        if text.startswith("☐"):
            # Marcar item
            self.tree.item(node, text=f"☑ {text[2:]}")
            self.selected_items.add(path)
            self.mark_children(node, True)
        elif text.startswith("☑"):
            # Desmarcar item
            self.tree.item(node, text=f"☐ {text[2:]}")
            self.selected_items.discard(path)
            self.mark_children(node, False)
        
        self.update_selection_count()

    def mark_children(self, node, select):
        """Marca/desmarca todos os filhos de um nó recursivamente"""
        # Primeiro, garantir que o nó esteja expandido se tiver filhos
        if select and not self.tree.item(node, "open"):
            children = self.tree.get_children(node)
            if children:
                child_values = self.tree.item(children[0], "values")
                if child_values and child_values[0] == "DUMMY":
                    # Expandir automaticamente
                    self.auto_expanding = True
                    self.tree.item(node, open=True)
                    self.auto_expanding = False
        
        for child in self.tree.get_children(node):
            values = self.tree.item(child, "values")
            if not values or values[0] == "DUMMY":
                continue
                
            path = values[0]
            text = self.tree.item(child, "text")
            
            if select:
                if text.startswith("☐"):
                    self.tree.item(child, text=f"☑ {text[2:]}")
                self.selected_items.add(path)
            else:
                if text.startswith("☑"):
                    self.tree.item(child, text=f"☐ {text[2:]}")
                self.selected_items.discard(path)
            
            # Recursão para filhos
            self.mark_children(child, select)

    def toggle_all(self):
        """Marca/desmarca todos os itens"""
        select_all = self.select_all_var.get()
        
        for root_node in self.tree.get_children():
            values = self.tree.item(root_node, "values")
            if not values or values[0] == "DUMMY":
                continue
                
            path = values[0]
            text = self.tree.item(root_node, "text")
            
            if select_all:
                if text.startswith("☐"):
                    self.tree.item(root_node, text=f"☑ {text[2:]}")
                self.selected_items.add(path)
            else:
                if text.startswith("☑"):
                    self.tree.item(root_node, text=f"☐ {text[2:]}")
                self.selected_items.discard(path)
            
            self.mark_children(root_node, select_all)
        
        self.update_selection_count()

    def expand_all(self):
        """Expande todos os nós da árvore"""
        def expand_node(node):
            self.tree.item(node, open=True)
            for child in self.tree.get_children(node):
                expand_node(child)
        
        for root_node in self.tree.get_children():
            expand_node(root_node)

    def collapse_all(self):
        """Recolhe todos os nós da árvore"""
        def collapse_node(node):
            self.tree.item(node, open=False)
            for child in self.tree.get_children(node):
                collapse_node(child)
        
        for root_node in self.tree.get_children():
            collapse_node(root_node)

    def update_selection_count(self):
        """Atualiza o contador de itens selecionados"""
        count = len(self.selected_items)
        if count == 0:
            self.update_status("Nenhum item selecionado")
        else:
            self.update_status(f"{count} item(s) selecionado(s)")

    def update_status(self, message):
        """Atualiza a mensagem de status"""
        self.status_label.config(text=message)

    def generate_file(self):
        """Gera o arquivo .txt com o conteúdo selecionado"""
        if not self.selected_items:
            messagebox.showwarning("Aviso", "Nenhum item foi selecionado.\nMarque as pastas e arquivos que deseja incluir no relatório.")
            return
        
        root_path = self.folder_path.get()
        if not root_path:
            messagebox.showerror("Erro", "Nenhuma pasta foi selecionada.")
            return
        
        # Gerar conteúdo do arquivo
        lines = []
        processed_paths = set()
        
        # Ordenar itens selecionados por caminho
        sorted_items = sorted(self.selected_items)
        
        for item_path in sorted_items:
            if not os.path.exists(item_path) or item_path in processed_paths:
                continue
            
            # Calcular caminho relativo
            rel_path = os.path.relpath(item_path, os.path.dirname(root_path)).replace(os.sep, '/')
            
            if os.path.isdir(item_path):
                lines.append(f"// {rel_path}/")
                processed_paths.add(item_path)
                
                # Se a pasta foi selecionada, incluir todo seu conteúdo
                self.add_folder_contents(item_path, lines, processed_paths, os.path.dirname(root_path))
            else:
                lines.append(f"// {rel_path}")
                try:
                    with open(item_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        lines.append("  // Conteúdo:")
                        if content.strip():
                            indented_content = content.replace('\n', '\n  ')
                            lines.append(f"  {indented_content}")
                        else:
                            lines.append("  [Arquivo vazio]")
                except Exception as e:
                    lines.append(f"  // Erro ao ler o arquivo: {e}")
                lines.append("")  # Linha em branco após cada arquivo
                processed_paths.add(item_path)
        
        # Salvar arquivo
        default_name = f"{os.path.basename(root_path)}_conteudo.txt"
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Arquivos de Texto", "*.txt"), ("Todos os Arquivos", "*.*")],
            initialfile=default_name,
            initialdir=os.path.dirname(root_path)
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))
            
            messagebox.showinfo("Sucesso", f"Arquivo gerado com sucesso!\n\nLocal: {file_path}\nItens incluídos: {len(processed_paths)}")
            self.update_status(f"Arquivo salvo: {os.path.basename(file_path)} ({len(processed_paths)} itens)")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar o arquivo:\n{e}")
            self.update_status(f"Erro ao salvar: {e}")

    def add_folder_contents(self, folder_path, lines, processed_paths, base_path):
        """Adiciona recursivamente o conteúdo de uma pasta às linhas do arquivo"""
        try:
            for root, dirs, files in os.walk(folder_path):
                # Ordenar diretórios e arquivos
                dirs.sort()
                files.sort()
                
                # Adicionar arquivos
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    if file_path in processed_paths:
                        continue
                    
                    rel_path = os.path.relpath(file_path, base_path).replace(os.sep, '/')
                    lines.append(f"// {rel_path}")
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            lines.append("  // Conteúdo:")
                            if content.strip():
                                indented_content = content.replace('\n', '\n  ')
                                lines.append(f"  {indented_content}")
                            else:
                                lines.append("  [Arquivo vazio]")
                    except Exception as e:
                        lines.append(f"  // Erro ao ler o arquivo: {e}")
                    
                    lines.append("")  # Linha em branco após cada arquivo
                    processed_paths.add(file_path)
                
        except Exception as e:
            lines.append(f"// Erro ao processar pasta {folder_path}: {e}")

def main():
    root = tk.Tk()
    
    # Configurar estilo se disponível
    try:
        style = ttk.Style()
        style.theme_use('clam')
    except:
        pass
    
    app = FolderContentApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()