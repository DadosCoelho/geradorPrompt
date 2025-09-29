import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import datetime

class ModernFolderContentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de Conteúdo - Documentação de Projetos")
        self.root.geometry("1100x700")
        self.root.minsize(800, 600)
        
        # Centralizar janela na tela
        self.center_window()
        
        # Configurar cores e estilos modernos
        self.setup_modern_style()
        
        # Variáveis de estado
        self.selected_items = set()
        self.folder_path = tk.StringVar()
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search_change)
        
        # Criar interface
        self.create_interface()
        
        # Configurar atalhos de teclado
        self.setup_keyboard_shortcuts()

    def center_window(self):
        """Centraliza a janela na tela"""
        self.root.update_idletasks()
        
        # Obter dimensões da tela
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Obter dimensões da janela
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        
        # Se a janela ainda não foi renderizada, usar valores padrão
        if window_width == 1:
            window_width = 1100
        if window_height == 1:
            window_height = 750
        
        # Calcular posição para centralizar
        pos_x = (screen_width // 2) - (window_width // 2)
        pos_y = (screen_height // 2) - (window_height // 2)
        
        # Garantir que a janela não fique fora da tela
        pos_x = max(0, pos_x)
        pos_y = max(0, pos_y)
        
        # Definir posição da janela
        self.root.geometry(f"{window_width}x{window_height}+{pos_x}+{pos_y}")

    def setup_modern_style(self):
        """Configura um estilo moderno para a aplicação"""
        style = ttk.Style()
        
        # Usar tema moderno se disponível
        available_themes = style.theme_names()
        if 'vista' in available_themes:
            style.theme_use('vista')
        elif 'clam' in available_themes:
            style.theme_use('clam')
        
        # Cores modernas
        self.colors = {
            'primary': '#2563eb',      # Azul moderno
            'primary_light': '#dbeafe',
            'secondary': '#64748b',    # Cinza azulado
            'success': '#10b981',      # Verde
            'warning': '#f59e0b',      # Amarelo
            'danger': '#ef4444',       # Vermelho
            'light': '#f8fafc',        # Cinza muito claro
            'dark': '#1e293b',         # Cinza escuro
            'white': '#ffffff'
        }
        
        # Configurar estilos personalizados
        style.configure('Title.TLabel', font=('Segoe UI', 16, 'bold'), foreground=self.colors['dark'])
        style.configure('Subtitle.TLabel', font=('Segoe UI', 10), foreground=self.colors['secondary'])
        style.configure('Primary.TButton', font=('Segoe UI', 9, 'bold'))
        style.configure('Secondary.TButton', font=('Segoe UI', 9))
        style.configure('Card.TFrame', relief='flat', borderwidth=1)

    def create_interface(self):
        """Cria a interface principal com layout moderno"""
        # Container principal com padding
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header com título e descrição
        self.create_header(main_container)
        
        # Seção de seleção de pasta
        self.create_folder_selection_section(main_container)
        
        # Seção principal com árvore de arquivos
        self.create_main_content_section(main_container)
        
        # Footer com controles e ações
        self.create_footer_section(main_container)

    def create_header(self, parent):
        """Cria o cabeçalho da aplicação"""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Título principal
        title_label = ttk.Label(
            header_frame, 
            text="Gerador de Conteúdo", 
            style='Title.TLabel'
        )
        title_label.pack(anchor=tk.W)
        
        # Subtítulo
        subtitle_label = ttk.Label(
            header_frame,
            text="Documente a estrutura e conteúdo de seus projetos de forma inteligente",
            style='Subtitle.TLabel'
        )
        subtitle_label.pack(anchor=tk.W, pady=(2, 0))

    def create_folder_selection_section(self, parent):
        """Cria a seção de seleção de pasta"""
        # Frame principal da seção
        section_frame = ttk.LabelFrame(parent, text="📂 Selecionar Projeto", padding=15)
        section_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Frame para o campo de entrada e botão
        input_frame = ttk.Frame(section_frame)
        input_frame.pack(fill=tk.X)
        
        # Campo de pasta selecionada
        self.folder_entry = ttk.Entry(
            input_frame, 
            textvariable=self.folder_path,
            font=('Segoe UI', 10),
            state='readonly'
        )
        self.folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Botão de seleção
        select_btn = ttk.Button(
            input_frame,
            text="📁 Selecionar Pasta",
            command=self.select_folder,
            style='Primary.TButton'
        )
        select_btn.pack(side=tk.LEFT, padx=(10, 0))
        
        # Informações da pasta (oculta inicialmente)
        self.folder_info_frame = ttk.Frame(section_frame)
        self.folder_info_label = ttk.Label(
            self.folder_info_frame,
            text="",
            style='Subtitle.TLabel'
        )
        self.folder_info_label.pack(anchor=tk.W)

    def create_main_content_section(self, parent):
        """Cria a seção principal com árvore de arquivos e controles"""
        # Frame principal
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Configurar colunas
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Barra de ferramentas
        self.create_toolbar(main_frame)
        
        # Área da árvore de arquivos
        self.create_tree_area(main_frame)

    def create_toolbar(self, parent):
        """Cria a barra de ferramentas"""
        toolbar = ttk.Frame(parent)
        toolbar.grid(row=0, column=0, sticky='ew', pady=(0, 10))
        toolbar.columnconfigure(1, weight=1)
        
        # Frame esquerdo - controles de seleção
        left_controls = ttk.Frame(toolbar)
        left_controls.grid(row=0, column=0, sticky='w')
        
        # Título da seção
        ttk.Label(left_controls, text="🎯 Seleção:", font=('Segoe UI', 9, 'bold')).pack(side=tk.LEFT)
        
        # Checkbox selecionar tudo
        self.select_all_var = tk.BooleanVar(value=False)
        select_all_cb = ttk.Checkbutton(
            left_controls,
            text="Selecionar Tudo",
            variable=self.select_all_var,
            command=self.toggle_all
        )
        select_all_cb.pack(side=tk.LEFT, padx=(10, 0))
        
        # Separador
        ttk.Separator(left_controls, orient='vertical').pack(side=tk.LEFT, fill='y', padx=(10, 10))
        
        # Botões de expansão
        expand_btn = ttk.Button(
            left_controls,
            text="⊞ Expandir",
            command=self.expand_all,
            style='Secondary.TButton'
        )
        expand_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        collapse_btn = ttk.Button(
            left_controls,
            text="⊟ Recolher",
            command=self.collapse_all,
            style='Secondary.TButton'
        )
        collapse_btn.pack(side=tk.LEFT)
        
    def create_tree_area(self, parent):
        """Cria a área da árvore de arquivos"""
        # Frame container
        tree_container = ttk.LabelFrame(parent, text="📋 Estrutura do Projeto", padding=10)
        tree_container.grid(row=1, column=0, sticky='nsew')
        tree_container.columnconfigure(0, weight=1)
        tree_container.rowconfigure(0, weight=1)
        
        # Frame para árvore com scrollbars
        tree_frame = ttk.Frame(tree_container)
        tree_frame.grid(row=0, column=0, sticky='nsew')
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        # TreeView melhorado
        self.tree = ttk.Treeview(
            tree_frame,
            selectmode='none',
            show='tree',
            height=15
        )
        
        # Configurar colunas
        self.tree.heading("#0", text="✓ Nome do Arquivo/Pasta")
        
        # Scrollbars modernas
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Layout
        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        # Bind eventos
        self.tree.bind("<<TreeviewOpen>>", self.on_open)
        self.tree.bind("<Button-1>", self.on_click)
        self.tree.bind("<Double-1>", self.on_double_click)
        
        # Estado vazio inicial
        self.show_empty_state()

    def create_footer_section(self, parent):
        """Cria a seção do rodapé com informações e ações"""
        # Frame principal do rodapé
        footer = ttk.Frame(parent)
        footer.pack(fill=tk.X)
        footer.columnconfigure(0, weight=1)
        
        # Barra de status
        status_frame = ttk.Frame(footer)
        status_frame.grid(row=0, column=0, sticky='ew', pady=(0, 10))
        status_frame.columnconfigure(1, weight=1)
        
        # Ícone de status
        self.status_icon = ttk.Label(status_frame, text="ℹ️", font=('Segoe UI', 11))
        self.status_icon.grid(row=0, column=0, padx=(0, 8))
        
        # Mensagem de status
        self.status_label = ttk.Label(
            status_frame,
            text="Selecione uma pasta para começar a documentação",
            font=('Segoe UI', 9),
            foreground=self.colors['secondary']
        )
        self.status_label.grid(row=0, column=1, sticky='w')
        
        # Contador de seleção
        self.selection_label = ttk.Label(
            status_frame,
            text="",
            font=('Segoe UI', 9, 'bold'),
            foreground=self.colors['primary']
        )
        self.selection_label.grid(row=0, column=2, sticky='e')
        
        # Barra de ações
        actions_frame = ttk.Frame(footer)
        actions_frame.grid(row=1, column=0, sticky='ew')
        
        # Botão principal de gerar
        self.generate_btn = ttk.Button(
            actions_frame,
            text="📄 Gerar Documentação",
            command=self.generate_file,
            style='Primary.TButton'
        )
        self.generate_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Informações adicionais
        info_text = "💡 Dica: Marque as pastas e arquivos que deseja incluir na documentação"
        ttk.Label(
            actions_frame,
            text=info_text,
            font=('Segoe UI', 8),
            foreground=self.colors['secondary']
        ).pack(side=tk.LEFT, anchor='w')

    def show_empty_state(self):
        """Mostra estado vazio na árvore"""
        self.tree.delete(*self.tree.get_children())
        empty_node = self.tree.insert("", "end", text="📂 Nenhuma pasta selecionada")
        self.tree.item(empty_node, tags=('empty',))
        
    def select_folder(self):
        """Seleciona uma pasta e carrega sua estrutura"""
        folder = filedialog.askdirectory(
            title="Selecionar pasta do projeto"
        )
        if not folder:
            return
        
        self.folder_path.set(folder)
        self.tree.delete(*self.tree.get_children())
        self.selected_items.clear()
        self.select_all_var.set(False)
        
        # Mostrar informações da pasta
        self.show_folder_info(folder)
        
        # Criar nó raiz
        folder_name = os.path.basename(folder) or folder
        root_node = self.tree.insert("", "end", 
            text=f"☐ 📁 {folder_name}",
            open=False, 
            values=[folder, "folder"]
        )
        
        # Adicionar placeholder
        self.tree.insert(root_node, "end", text="⏳ Carregando...", values=["DUMMY"])
        
        self.update_status("📁 Projeto carregado! Expanda as pastas e selecione os itens desejados.", "info")

    def show_folder_info(self, folder):
        """Mostra informações sobre a pasta selecionada"""
        try:
            # Contar arquivos e pastas
            total_files = 0
            total_dirs = 0
            for root, dirs, files in os.walk(folder):
                total_files += len(files)
                total_dirs += len(dirs)
            
            info_text = f"📊 {total_dirs} pastas • {total_files} arquivos • {Path(folder).name}"
            self.folder_info_label.config(text=info_text)
            self.folder_info_frame.pack(fill=tk.X, pady=(10, 0))
            
        except Exception:
            self.folder_info_frame.pack_forget()

    def on_open(self, event):
        """Evento quando um nó é expandido"""
        node = self.tree.focus()
        if not node:
            return
        
        values = self.tree.item(node, "values")
        if not values or len(values) < 1:
            return
        
        path = values[0]
        
        # Verificar se precisa carregar
        children = self.tree.get_children(node)
        if len(children) == 1:
            child_values = self.tree.item(children[0], "values")
            if child_values and child_values[0] == "DUMMY":
                self.tree.delete(children[0])
                self.populate_node(node, path)

    def populate_node(self, parent_node, path):
        """Popula um nó com seus filhos"""
        try:
            if not os.path.isdir(path):
                return
            
            entries = []
            for entry in os.listdir(path):
                full_path = os.path.join(path, entry)
                if os.path.isdir(full_path):
                    entries.append((f"📁 {entry}", full_path, "folder"))
                else:
                    size = self.get_file_size(full_path)
                    icon = self.get_file_icon(entry)
                    entries.append((f"{icon} {entry} ({size})", full_path, "file"))
            
            # Ordenar: pastas primeiro, depois arquivos
            entries.sort(key=lambda x: (x[2] == "file", x[0].lower()))
            
            for display_name, full_path, item_type in entries:
                node = self.tree.insert(parent_node, "end",
                    text=f"☐ {display_name}",
                    values=[full_path, item_type]
                )
                
                if item_type == "folder":
                    self.tree.insert(node, "end", text="⏳ Carregando...", values=["DUMMY"])
                    
        except PermissionError:
            self.tree.insert(parent_node, "end", text="🔒 Acesso negado", values=[])
        except Exception as e:
            self.tree.insert(parent_node, "end", text=f"⚠️ Erro: {str(e)}", values=[])

    def get_file_icon(self, filename):
        """Retorna um ícone baseado na extensão do arquivo"""
        ext = os.path.splitext(filename)[1].lower()
        icons = {
            '.py': '🐍', '.js': '🟨', '.html': '🌐', '.css': '🎨',
            '.md': '📝', '.txt': '📄', '.json': '📋', '.xml': '📄',
            '.jpg': '🖼️', '.png': '🖼️', '.gif': '🖼️', '.svg': '🖼️',
            '.pdf': '📕', '.doc': '📘', '.docx': '📘',
            '.zip': '📦', '.rar': '📦', '.7z': '📦',
            '.exe': '⚙️', '.bat': '⚙️', '.sh': '⚙️'
        }
        return icons.get(ext, '📄')

    def get_file_size(self, file_path):
        """Obtém o tamanho formatado do arquivo"""
        try:
            size = os.path.getsize(file_path)
            if size < 1024:
                return f"{size} B"
            elif size < 1024 * 1024:
                return f"{size / 1024:.1f} KB"
            elif size < 1024 * 1024 * 1024:
                return f"{size / (1024 * 1024):.1f} MB"
            else:
                return f"{size / (1024 * 1024 * 1024):.1f} GB"
        except:
            return "0 B"

    def on_click(self, event):
        """Manipula cliques na árvore.

        Evita alternar a seleção quando o usuário clica no indicador de
        expandir/recolher (triângulo). Apenas cliques sobre o texto/imagem
        do item irão alternar seleção.
        """
        region = self.tree.identify("region", event.x, event.y)
        if region != "tree":
            return

        # Tentar identificar o elemento exato sob o cursor (ex: indicator, padding, image, text)
        element = None
        try:
            # API mais comum
            element = self.tree.identify("element", event.x, event.y)
        except Exception:
            try:
                # Alternativa disponível em algumas versões
                element = self.tree.identify_element(event.x, event.y)
            except Exception:
                element = None

        # Se o clique foi no indicador (área do triângulo) ou padding à esquerda, não alternar seleção
        if element and ("indicator" in element or "padding" in element):
            return

        node = self.tree.identify_row(event.y)
        if not node:
            return

        values = self.tree.item(node, "values")
        if not values or values[0] == "DUMMY":
            return

        self.toggle_selection(node)

    def on_double_click(self, event):
        """Manipula duplo clique para expandir/recolher"""
        node = self.tree.identify_row(event.y)
        if not node:
            return
        
        values = self.tree.item(node, "values")
        if values and len(values) >= 2 and values[1] == "folder":
            current_state = self.tree.item(node, "open")
            self.tree.item(node, open=not current_state)

    def toggle_selection(self, node):
        """Alterna seleção de um nó com propagação hierárquica"""
        values = self.tree.item(node, "values")
        if not values or values[0] == "DUMMY":
            return
        
        path = values[0]
        text = self.tree.item(node, "text")
        
        if text.startswith("☐"):
            # Marcar
            new_text = text.replace("☐", "☑️", 1)
            self.tree.item(node, text=new_text)
            self.selected_items.add(path)
            self.mark_children(node, True)

            # 🔥 NOVO: Atualizar nós pais também ao marcar
            self.update_parent_selection(node)

        elif text.startswith("☑️"):
            # Desmarcar
            new_text = text.replace("☑️", "☐", 1)
            self.tree.item(node, text=new_text)
            self.selected_items.discard(path)
            self.mark_children(node, False)

            # Atualizar nós pais quando um item é desmarcado
            self.update_parent_selection(node)

        
        self.update_selection_display()

    def update_parent_selection(self, node):
        """Atualiza o estado de seleção dos nós pais baseado nos filhos"""
        parent = self.tree.parent(node)
        if not parent:
            return

        parent_values = self.tree.item(parent, "values")
        if not parent_values or parent_values[0] == "DUMMY":
            return

        # Verificar se todos os filhos estão selecionados
        all_children_selected = True
        any_child_selected = False
        for child in self.tree.get_children(parent):
            child_values = self.tree.item(child, "values")
            if child_values and child_values[0] != "DUMMY":
                child_path = child_values[0]
                if child_path in self.selected_items:
                    any_child_selected = True
                else:
                    all_children_selected = False

        parent_path = parent_values[0]
        parent_text = self.tree.item(parent, "text")

        # Caso todos os filhos estejam selecionados → marca o pai
        if all_children_selected and parent_text.startswith("☐"):
            new_text = parent_text.replace("☐", "☑️", 1)
            self.tree.item(parent, text=new_text)
            self.selected_items.add(parent_path)
            self.update_parent_selection(parent)

        # Caso nenhum ou só alguns filhos estejam selecionados → desmarca o pai
        elif not all_children_selected and parent_text.startswith("☑️"):
            new_text = parent_text.replace("☑️", "☐", 1)
            self.tree.item(parent, text=new_text)
            self.selected_items.discard(parent_path)
            self.update_parent_selection(parent)

    def mark_children(self, node, select):
        """Marca/desmarca filhos recursivamente"""
        for child in self.tree.get_children(node):
            values = self.tree.item(child, "values")
            if not values or values[0] == "DUMMY":
                continue
            
            path = values[0]
            text = self.tree.item(child, "text")
            
            if select and text.startswith("☐"):
                new_text = text.replace("☐", "☑️", 1)
                self.tree.item(child, text=new_text)
                self.selected_items.add(path)
            elif not select and text.startswith("☑️"):
                new_text = text.replace("☑️", "☐", 1)
                self.tree.item(child, text=new_text)
                self.selected_items.discard(path)
            
            self.mark_children(child, select)

    def toggle_all(self):
        """Marca/desmarca todos os itens"""
        select_all = self.select_all_var.get()
        
        for root_node in self.tree.get_children():
            values = self.tree.item(root_node, "values")
            if not values or values[0] == "DUMMY":
                continue
            
            text = self.tree.item(root_node, "text")
            path = values[0]
            
            if select_all and text.startswith("☐"):
                new_text = text.replace("☐", "☑️", 1)
                self.tree.item(root_node, text=new_text)
                self.selected_items.add(path)
            elif not select_all and text.startswith("☑️"):
                new_text = text.replace("☑️", "☐", 1)
                self.tree.item(root_node, text=new_text)
                self.selected_items.discard(path)
            
            self.mark_children(root_node, select_all)
        
        self.update_selection_display()

    def expand_all(self):
        """Expande toda a árvore"""
        def expand_recursive(node):
            self.tree.item(node, open=True)
            for child in self.tree.get_children(node):
                expand_recursive(child)
        
        for root_node in self.tree.get_children():
            expand_recursive(root_node)
        
        self.update_status("🔍 Estrutura expandida completamente", "info")

    def collapse_all(self):
        """Recolhe toda a árvore"""
        def collapse_recursive(node):
            self.tree.item(node, open=False)
            for child in self.tree.get_children(node):
                collapse_recursive(child)
        
        for root_node in self.tree.get_children():
            collapse_recursive(root_node)
        
        self.update_status("📁 Estrutura recolhida", "info")

    def update_selection_display(self):
        """Atualiza a exibição de seleção"""
        count = len(self.selected_items)
        if count == 0:
            self.selection_label.config(text="")
            self.update_status("Selecione itens para incluir na documentação", "info")
        else:
            self.selection_label.config(text=f"✓ {count} itens selecionados")
            self.update_status(f"✅ {count} item(s) prontos para documentação", "success")

    def update_status(self, message, status_type="info"):
        """Atualiza status com ícones apropriados"""
        icons = {
            "info": "ℹ️",
            "success": "✅",
            "warning": "⚠️",
            "error": "❌"
        }
        
        colors = {
            "info": self.colors['secondary'],
            "success": self.colors['success'],
            "warning": self.colors['warning'],
            "error": self.colors['danger']
        }
        
        self.status_icon.config(text=icons.get(status_type, "ℹ️"))
        self.status_label.config(text=message, foreground=colors.get(status_type, self.colors['secondary']))

    def on_search_focus_in(self, event):
        """Evento de foco no campo de busca"""
        if event.widget.get() == "Buscar arquivos...":
            event.widget.delete(0, tk.END)
            event.widget.config(foreground='black')

    def on_search_focus_out(self, event):
        """Evento de perda de foco no campo de busca"""
        if not event.widget.get():
            event.widget.insert(0, "Buscar arquivos...")
            event.widget.config(foreground='gray')

    def on_search_change(self, *args):
        """Manipula mudanças na busca"""
        search_term = self.search_var.get().lower()
        if search_term and search_term != "buscar arquivos...":
            self.highlight_search_results(search_term)

    def highlight_search_results(self, search_term):
        """Destaca resultados da busca"""
        # Implementação básica - pode ser expandida
        pass

    def generate_file(self):
        """Gera o arquivo de documentação"""
        if not self.selected_items:
            messagebox.showwarning(
                "Nenhum item selecionado",
                "Por favor, selecione pelo menos um arquivo ou pasta para incluir na documentação."
            )
            return
        
        root_path = self.folder_path.get()
        if not root_path:
            messagebox.showerror("Erro", "Nenhuma pasta foi selecionada.")
            return
        
        # Gerar nome padrão mais descritivo
        folder_name = os.path.basename(root_path)
        default_name = f"{folder_name}_documentacao.txt"
        
        # Dialog de salvamento
        file_path = filedialog.asksaveasfilename(
            title="Salvar documentação como...",
            defaultextension=".txt",
            filetypes=[
                ("Arquivos de Texto", "*.txt"),
                ("Arquivos Markdown", "*.md"),
                ("Todos os Arquivos", "*.*")
            ],
            initialfile=default_name,
            initialdir=os.path.dirname(root_path)
        )
        
        if not file_path:
            return
        
        try:
            self.update_status("📝 Gerando documentação...", "info")
            self.root.update()  # Atualizar interface
            
            # Gerar conteúdo
            content = self.generate_content()
            
            # Salvar arquivo
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Sucesso
            item_count = len(self.selected_items)
            success_msg = (f"📄 Documentação gerada com sucesso!\n\n"
                          f"📂 Local: {file_path}\n"
                          f"📊 Itens incluídos: {item_count}\n"
                          f"📏 Tamanho: {self.get_file_size(file_path)}")
            
            messagebox.showinfo("Sucesso", success_msg)
            self.update_status(f"✅ Documentação salva: {os.path.basename(file_path)}", "success")
            
        except Exception as e:
            error_msg = f"Erro ao gerar documentação:\n{str(e)}"
            messagebox.showerror("Erro", error_msg)
            self.update_status(f"❌ Erro ao salvar: {str(e)}", "error")

    def generate_content(self):
        """Gera o conteúdo do arquivo de documentação"""
        root_path = self.folder_path.get()
        folder_name = os.path.basename(root_path)
        
        lines = [
            f"# Documentação do Projeto: {folder_name}",
            f"Gerado automaticamente pelo Gerador de Conteúdo",
            f"Data: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
            f"Caminho base: {root_path}",
            "",
            "=" * 60,
            ""
        ]
        
        processed_paths = set()
        sorted_items = sorted(self.selected_items)
        
        for item_path in sorted_items:
            if not os.path.exists(item_path) or item_path in processed_paths:
                continue
            
            rel_path = os.path.relpath(item_path, os.path.dirname(root_path)).replace(os.sep, '/')
            
            if os.path.isdir(item_path):
                lines.append(f"## 📁 {rel_path}/")
                lines.append("")
                processed_paths.add(item_path)
                
                # Incluir conteúdo da pasta se selecionada
                self.add_folder_contents(item_path, lines, processed_paths, os.path.dirname(root_path))
            else:
                lines.append(f"### 📄 {rel_path}")
                lines.append("```")
                try:
                    with open(item_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if content.strip():
                            lines.append(content)
                        else:
                            lines.append("[Arquivo vazio]")
                except Exception as e:
                    lines.append(f"[Erro ao ler arquivo: {e}]")
                lines.append("```")
                lines.append("")
                processed_paths.add(item_path)
        
        return '\n'.join(lines)

    def add_folder_contents(self, folder_path, lines, processed_paths, base_path):
        """Adiciona conteúdo de uma pasta recursivamente"""
        try:
            for root, dirs, files in os.walk(folder_path):
                dirs.sort()
                files.sort()
                
                # Adicionar arquivos
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    if file_path in processed_paths:
                        continue
                    
                    rel_path = os.path.relpath(file_path, base_path).replace(os.sep, '/')
                    lines.append(f"### 📄 {rel_path}")
                    lines.append("```")
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if content.strip():
                                lines.append(content)
                            else:
                                lines.append("[Arquivo vazio]")
                    except Exception as e:
                        lines.append(f"[Erro ao ler arquivo: {e}]")
                    
                    lines.append("```")
                    lines.append("")
                    processed_paths.add(file_path)
                    
        except Exception as e:
            lines.append(f"[Erro ao processar pasta {folder_path}: {e}]")
            lines.append("")

    def setup_keyboard_shortcuts(self):
        """Configura atalhos de teclado"""
        self.root.bind('<Control-o>', lambda e: self.select_folder())
        self.root.bind('<Control-g>', lambda e: self.generate_file())
        self.root.bind('<Control-a>', lambda e: self.select_all_var.set(not self.select_all_var.get()) or self.toggle_all())
        self.root.bind('<F5>', lambda e: self.refresh_tree())
        self.root.bind('<Control-f>', lambda e: self.focus_search())

    def refresh_tree(self):
        """Atualiza a árvore de arquivos"""
        if self.folder_path.get():
            current_folder = self.folder_path.get()
            self.folder_path.set("")  # Limpar temporariamente
            self.folder_path.set(current_folder)  # Recarregar
            self.select_folder()

    def focus_search(self):
        """Foca no campo de busca"""
        # Encontrar o widget de busca e focar nele
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Entry) and widget.cget('textvariable') == str(self.search_var):
                widget.focus_set()
                break

def main():
    """Função principal da aplicação"""
    root = tk.Tk()
    
    # Tentar carregar ícone personalizado do diretório da aplicação
    try:
        # Obter diretório do script atual
        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_dir, 'icon.ico')
        
        # Verificar se o arquivo icon.ico existe
        if os.path.exists(icon_path):
            root.iconbitmap(icon_path)
        else:
            print(f"⚠️  Arquivo icon.ico não encontrado em: {icon_path}")
            print("💡 Dica: Coloque o arquivo 'icon.ico' no mesmo diretório do programa")
    except Exception as e:
        print(f"❌ Erro ao carregar ícone: {e}")
        # Se houver erro, continuar sem ícone personalizado
    
    # Configurar tema do sistema
    try:
        import tkinter.ttk as ttk
        style = ttk.Style()
        # Usar tema nativo do sistema se disponível
        if 'winnative' in style.theme_names():
            style.theme_use('winnative')
        elif 'aqua' in style.theme_names():
            style.theme_use('aqua')
    except:
        pass
    
    # Criar aplicação
    app = ModernFolderContentApp(root)
    
    # Configurar fechamento da aplicação
    def on_closing():
        if messagebox.askokcancel("Sair", "Deseja realmente sair da aplicação?"):
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Mostrar mensagem de boas-vindas
    root.after(100, lambda: app.update_status("👋 Bem-vindo! Selecione uma pasta para começar", "info"))
    
    # Iniciar loop principal
    root.mainloop()

if __name__ == "__main__":
    main()