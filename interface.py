import tkinter as tk
from tkinter import ttk, messagebox
from main import Gerenciador
from pessoas import Pessoa_admin

class AppTransporte(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Expresso Central - Painel de Controle Integrado")
        self.geometry("950x750")
        self.configure(bg="#f4f6f9")
        
    
        self.gerenciador = Gerenciador()
        self.usuario_atual = None  
        self.perfil_acesso = "Usuário"
        self.configurar_estilos()
        self.container = tk.Frame(self, bg="#f4f6f9")
        self.container.pack(fill="both", expand=True)
        self.mostrar_tela_login()

    def configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background="#f4f6f9", borderwidth=0)
        style.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"), padding=[12, 5], background="#e2e8f0", foreground="#4a5568")
        style.map("TNotebook.Tab", background=[("selected", "#1a365d")], foreground=[("selected", "white")])

    def limpar_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()


    def mostrar_tela_login(self):
        self.limpar_container()
        card = tk.Frame(self.container, bg="white", highlightbackground="#e2e8f0", highlightthickness=1, padx=30, pady=25)
        card.place(relx=0.5, rely=0.5, anchor="center", width=460, height=540)

        tk.Label(card, text="🚌 Expresso Central", bg="white", fg="#1a365d", font=("Segoe UI", 20, "bold")).pack(pady=(5, 2))
        tk.Label(card, text="Selecione seu Perfil:", bg="white", fg="#4a5568", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        
        self.var_perfil = tk.StringVar(value="Usuário")
        frame_perfis = tk.Frame(card, bg="white")
        frame_perfis.pack(fill="x", pady=(5, 15))
        tk.Radiobutton(frame_perfis, text="Usuário (Comum)", variable=self.var_perfil, value="Usuário", bg="white").pack(side="left", padx=(0, 20))
        tk.Radiobutton(frame_perfis, text="Gerenciador", variable=self.var_perfil, value="Gerenciador", bg="white").pack(side="left")

        tk.Label(card, text="Nome de Usuário", bg="white", fg="#4a5568", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.ent_nome = tk.Entry(card, font=("Segoe UI", 11), bg="#f7fafc", relief="solid", bd=1)
        self.ent_nome.pack(fill="x", ipady=5, pady=(2, 12))

        tk.Label(card, text="Senha", bg="white", fg="#4a5568", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.ent_senha = tk.Entry(card, show="*", font=("Segoe UI", 11), bg="#f7fafc", relief="solid", bd=1)
        self.ent_senha.pack(fill="x", ipady=5, pady=(2, 20))

        tk.Button(card, text="Entrar", command=self.acao_login, bg="#1a365d", fg="white", font=("Segoe UI", 11, "bold")).pack(fill="x", ipady=6, pady=(0, 10))
        tk.Button(card, text="Criar Conta / Registrar", command=self.acao_cadastro, bg="white", fg="#4a5568", bd=0).pack(pady=5)

    def acao_login(self):
        nome = self.ent_nome.get().strip()
        senha = self.ent_senha.get().strip()
        self.perfil_acesso = self.var_perfil.get()

        sucesso, user_obj, msg = self.gerenciador.autenticar(nome, senha, self.perfil_acesso)
        
        if sucesso:
            self.usuario_atual = user_obj
            self.mostrar_painel_principal()
        else:
            messagebox.showerror("Erro de Autenticação", msg)

    def acao_cadastro(self):
        nome = self.ent_nome.get().strip()
        senha = self.ent_senha.get().strip()
        if not nome or not senha: 
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return
        
        sucesso, msg = self.gerenciador.cadastrar_usuario(nome, senha, self.var_perfil.get())
        if sucesso:
            messagebox.showinfo("Sucesso", msg)
        else:
            messagebox.showerror("Erro", msg)

    def mostrar_painel_principal(self):
        self.limpar_container()
        header = tk.Frame(self.container, bg="#1a365d", height=65)
        header.pack(fill="x", side="top")
        
        tipo_display = "(Gerenciador)" if isinstance(self.usuario_atual, Pessoa_admin) else "(Usuário)"
        tk.Label(header, text=f"👤 {self.usuario_atual.nome} {tipo_display}", bg="#1a365d", fg="white", font=("Segoe UI", 11, "bold")).pack(side="left", padx=20, pady=18)
        tk.Button(header, text="Sair ➔", command=self.mostrar_tela_login, bg="#e53e3e", fg="white", font=("Segoe UI", 9, "bold"), padx=12).pack(side="right", padx=20, pady=15)

        notebook = ttk.Notebook(self.container)
        notebook.pack(fill="both", expand=True, padx=15, pady=15)

        if self.perfil_acesso == "Gerenciador":
            self.criar_aba_dashboard_geral(notebook)
            self.criar_aba_controle_frota(notebook)
            self.criar_aba_bikes(notebook)
            self.criar_aba_gestao_admin(notebook)
            self.criar_aba_acoes_gerenciador(notebook)
            self.criar_aba_pontos(notebook)
        else:
            self.criar_aba_quadro_avisos(notebook)
            self.criar_aba_pontos(notebook)
            self.criar_aba_notificar_admin(notebook)

        notebook.bind("<<NotebookTabChanged>>", self.ao_mudar_aba)

    def ao_mudar_aba(self, event):
        self.recarregar_tabela_frota()
        self.recarregar_tabela_bikes()
        self.recarregar_tabela_pontos()
        self.carregar_notificacoes()

    def recarregar_tabela_frota(self):
        if hasattr(self, 'tree_frota') and self.tree_frota.winfo_exists():
            for i in self.tree_frota.get_children(): self.tree_frota.delete(i)
            
            frota = self.gerenciador.carregar_frota()
            if hasattr(self, 'lbl_resumo_frota'):
                self.lbl_resumo_frota.config(text=str(frota))

            cats = [(frota.get_onibus(), "Ônibus"), (frota.get_vans(), "Van"), (frota.get_micro_onibus(), "Micro-ônibus")]
            for lista, nome_cat in cats:
                for v in lista:
                    self.tree_frota.insert("", "end", values=(v._placa, nome_cat, v.capacidade, v.passageiros, v.motorista, "Sim" if v.funcionando else "Não"))

    def recarregar_tabela_bikes(self):
        if hasattr(self, 'tree_bike') and self.tree_bike.winfo_exists():
            for i in self.tree_bike.get_children(): self.tree_bike.delete(i)
            frota = self.gerenciador.carregar_frota()
            for b in frota.get_bicicletas():
                self.tree_bike.insert("", "end", values=(b._placa, "Sim" if b.funcionando else "Não", "Sim" if b.disponivel else "Emprestada"))

    def recarregar_tabela_pontos(self):
        if hasattr(self, 'tree_pontos') and self.tree_pontos.winfo_exists():
            for i in self.tree_pontos.get_children():
                self.tree_pontos.delete(i)
            pontos = self.gerenciador.obter_pontos()
            for row in pontos:
                self.tree_pontos.insert("", "end", values=(row.get("endereco", ""), row.get("tipo_veiculo", "")))

    def carregar_notificacoes(self):
        if hasattr(self, 'txt_notif') and self.txt_notif.winfo_exists():
            self.txt_notif.config(state="normal")
            self.txt_notif.delete("1.0", tk.END)
            notificacoes = self.gerenciador.obter_notificacoes()
            for row in reversed(notificacoes):
                self.txt_notif.insert(tk.END, f"📩 {row.get('usuario')} ({row.get('data')}):\n{row.get('mensagem')}\n\n---\n")
            self.txt_notif.config(state="disabled")

    def criar_aba_dashboard_geral(self, notebook):
        aba = tk.Frame(notebook, bg="#f4f6f9")
        notebook.add(aba, text=" 📊 Dashboard ")
        card = tk.Frame(aba, bg="white", highlightthickness=1, padx=20, pady=20)
        card.pack(fill="x", padx=20, pady=15)
        tk.Label(card, text="Resumo da Frota", font=("Segoe UI", 11, "bold"), bg="white").pack(anchor="w")
        self.lbl_resumo_frota = tk.Label(card, text="", font=("Segoe UI", 14, "bold"), fg="#1a365d", bg="white", justify="left")
        self.lbl_resumo_frota.pack(anchor="w", pady=5)

    def criar_aba_controle_frota(self, notebook):
        aba = tk.Frame(notebook, bg="#f4f6f9")
        notebook.add(aba, text=" 🚌 Frota Pesada ")
        frame_tabela = tk.Frame(aba, bg="white")
        frame_tabela.pack(fill="both", expand=True, padx=20, pady=10)

        self.tree_frota = ttk.Treeview(frame_tabela, columns=("placa", "tipo", "capacidade", "passageiros", "motorista", "funcionando"), show="headings")
        self.tree_frota.pack(fill="both", expand=True)
        for col in self.tree_frota["columns"]: self.tree_frota.heading(col, text=col.title())
        self.recarregar_tabela_frota()

        frame_fluxo = tk.LabelFrame(aba, text=" Controle de Lotação ", bg="white", padx=15, pady=15)
        frame_fluxo.pack(fill="x", padx=20, pady=15)
        self.ent_qtd = tk.Entry(frame_fluxo, width=10, relief="solid")
        self.ent_qtd.grid(row=0, column=0, padx=5)
        tk.Button(frame_fluxo, text="📥 Entrada (+)", command=lambda: self.alterar_passageiros("subir"), bg="#2f855a", fg="white").grid(row=0, column=1, padx=5)
        tk.Button(frame_fluxo, text="📤 Saída (-)", command=lambda: self.alterar_passageiros("descer"), bg="#c53030", fg="white").grid(row=0, column=2, padx=5)

    def criar_aba_bikes(self, notebook):
        aba = tk.Frame(notebook, bg="#f4f6f9")
        notebook.add(aba, text=" 🚲 Bikes ")
        frame_tabela = tk.Frame(aba, bg="white", padx=10, pady=10)
        frame_tabela.pack(fill="both", expand=True, padx=20, pady=10)
        self.tree_bike = ttk.Treeview(frame_tabela, columns=("numero", "funcionamento", "disponivel"), show="headings", height=6)
        self.tree_bike.pack(fill="both", expand=True)
        for col, nome in zip(self.tree_bike["columns"], ["Placa", "Funcionando", "Disponível"]): self.tree_bike.heading(col, text=nome)
        self.recarregar_tabela_bikes()

        frame_acoes = tk.LabelFrame(aba, text=" Gerenciar Bikes ", bg="white", padx=15, pady=10)
        frame_acoes.pack(fill="x", padx=20, pady=10)
        self.ent_nova_bike = tk.Entry(frame_acoes, relief="solid", width=12)
        self.ent_nova_bike.grid(row=0, column=0, padx=5)
        tk.Button(frame_acoes, text="➕ Adicionar", command=self.add_bike, bg="#2f855a", fg="white").grid(row=0, column=1, padx=10)
        
        self.ent_id_bike = tk.Entry(frame_acoes, relief="solid", width=12)
        self.ent_id_bike.grid(row=0, column=2, padx=5)
        tk.Button(frame_acoes, text="🚲 Emprestar", command=lambda: self.bike_action("emp"), bg="#2b6cb0", fg="white").grid(row=0, column=3, padx=5)
        tk.Button(frame_acoes, text="🔄 Devolver", command=lambda: self.bike_action("dev"), bg="#dd6b20", fg="white").grid(row=0, column=4, padx=5)

    def criar_aba_gestao_admin(self, notebook):
        aba = tk.Frame(notebook, bg="#f4f6f9")
        notebook.add(aba, text=" ⚙️ Cadastros ")
        canvas = tk.Canvas(aba, bg="#f4f6f9", highlightthickness=0)
        scrollbar = ttk.Scrollbar(aba, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f4f6f9")
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True, padx=10)
        scrollbar.pack(side="right", fill="y")

        frame_cad = tk.LabelFrame(scrollable_frame, text=" Cadastrar Veículo ", bg="white", padx=15, pady=15)
        frame_cad.pack(fill="x", padx=10, pady=10)
        self.ent_placa_c = tk.Entry(frame_cad, relief="solid", width=15)
        self.ent_placa_c.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(frame_cad, text="Placa:", bg="white").grid(row=0, column=0)
        self.var_tipo_c = tk.StringVar(value="Ônibus")
        ttk.Combobox(frame_cad, textvariable=self.var_tipo_c, values=["Ônibus", "Van", "Micro-ônibus"], state="readonly", width=12).grid(row=0, column=3)
        tk.Label(frame_cad, text="Tipo:", bg="white").grid(row=0, column=2)
        self.ent_cap_c = tk.Entry(frame_cad, relief="solid", width=15)
        self.ent_cap_c.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(frame_cad, text="Capacidade:", bg="white").grid(row=1, column=0)
        self.ent_mot_c = tk.Entry(frame_cad, relief="solid", width=15)
        self.ent_mot_c.grid(row=1, column=3, padx=5, pady=5)
        tk.Label(frame_cad, text="Motorista:", bg="white").grid(row=1, column=2)
        tk.Button(frame_cad, text="Salvar Veículo", command=self.cadastrar_novo_veiculo, bg="#2f855a", fg="white").grid(row=2, column=0, columnspan=4, pady=10)

        frame_alt = tk.LabelFrame(scrollable_frame, text=" Alterar Veículo (Motorista) ", bg="white", padx=15, pady=15)
        frame_alt.pack(fill="x", padx=10, pady=10)
        tk.Label(frame_alt, text="Placa:", bg="white").grid(row=0, column=0, padx=5, pady=5)
        self.ent_placa_alt = tk.Entry(frame_alt, relief="solid", width=15)
        self.ent_placa_alt.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(frame_alt, text="Novo Mot.:", bg="white").grid(row=0, column=2, padx=5, pady=5)
        self.ent_mot_alt = tk.Entry(frame_alt, relief="solid", width=15)
        self.ent_mot_alt.grid(row=0, column=3, padx=5, pady=5)
        tk.Button(frame_alt, text="Atualizar", command=self.acao_alterar_veiculo, bg="#d69e2e", fg="white").grid(row=1, column=0, columnspan=4, pady=10)

        frame_mot = tk.LabelFrame(scrollable_frame, text=" Cadastrar Novo Motorista ", bg="white", padx=15, pady=15)
        frame_mot.pack(fill="x", padx=10, pady=10)
        tk.Label(frame_mot, text="Nome:", bg="white").grid(row=0, column=0, padx=5, pady=5)
        self.ent_nome_mot = tk.Entry(frame_mot, relief="solid", width=15)
        self.ent_nome_mot.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(frame_mot, text="Senha:", bg="white").grid(row=0, column=2, padx=5, pady=5)
        self.ent_senha_mot = tk.Entry(frame_mot, relief="solid", width=15, show="*")
        self.ent_senha_mot.grid(row=0, column=3, padx=5, pady=5)
        tk.Button(frame_mot, text="Cadastrar", command=self.acao_cadastrar_motorista, bg="#3182ce", fg="white").grid(row=1, column=0, columnspan=4, pady=10)

        frame_ponto = tk.LabelFrame(scrollable_frame, text=" Cadastrar Pontos ", bg="white", padx=15, pady=15)
        frame_ponto.pack(fill="x", padx=10, pady=10)
        self.ent_end_ponto = tk.Entry(frame_ponto, relief="solid", width=25)
        self.ent_end_ponto.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(frame_ponto, text="Endereço:", bg="white").grid(row=0, column=0)
        self.ent_tipo_ponto = tk.Entry(frame_ponto, relief="solid", width=15)
        self.ent_tipo_ponto.grid(row=0, column=3, padx=5, pady=5)
        tk.Label(frame_ponto, text="Tipos perm.:", bg="white").grid(row=0, column=2)
        tk.Button(frame_ponto, text="Cadastrar Ponto", command=self.add_ponto, bg="#2b6cb0", fg="white").grid(row=1, column=0, columnspan=4, pady=10)

    def criar_aba_acoes_gerenciador(self, notebook):
        aba = tk.Frame(notebook, bg="#f4f6f9")
        notebook.add(aba, text=" 📢 Comunicação ")
        frame_aviso = tk.LabelFrame(aba, text=" Publicar Informativo ", bg="white", padx=15, pady=10)
        frame_aviso.pack(fill="x", padx=20, pady=10)
        self.ent_aviso = tk.Entry(frame_aviso, relief="solid")
        self.ent_aviso.pack(side="left", fill="x", expand=True, padx=(0, 10), ipady=3)
        tk.Button(frame_aviso, text="Gravar", command=self.publicar_aviso, bg="#1a365d", fg="white").pack(side="left", padx=5)
        tk.Button(frame_aviso, text="Excluir 🗑️", command=self.janela_excluir_avisos, bg="#c53030", fg="white").pack(side="right")
        
        frame_notif = tk.LabelFrame(aba, text=" Notificações Recebidas ", bg="white", padx=15, pady=10)
        frame_notif.pack(fill="both", expand=True, padx=20, pady=10)
        self.txt_notif = tk.Text(frame_notif, bg="#f7fafc", padx=10, pady=10, relief="solid")
        self.txt_notif.pack(fill="both", expand=True)
        tk.Button(frame_notif, text="Excluir Notificações", command=self.janela_excluir_notificacoes, bg="#c53030", fg="white").pack(anchor="e", pady=(10, 0))

    def criar_aba_quadro_avisos(self, notebook):
        aba = tk.Frame(notebook, bg="#f4f6f9")
        notebook.add(aba, text=" 📢 Mural ")
        txt = tk.Text(aba, bg="white", padx=15, pady=15, relief="solid")
        txt.pack(fill="both", expand=True, padx=20, pady=20)
        avisos = self.gerenciador.obter_avisos()
        for row in reversed(avisos):
            txt.insert(tk.END, f"📍 {row.get('conteudo', '')}\n\n-------------------\n\n")
        txt.config(state="disabled")

    def criar_aba_pontos(self, notebook):
        aba = tk.Frame(notebook, bg="#f4f6f9")
        notebook.add(aba, text=" 🚏 Pontos de Parada ")
        
        if self.perfil_acesso == "Gerenciador":
            frame_btn = tk.Frame(aba, bg="#f4f6f9")
            frame_btn.pack(fill="x", padx=20, pady=10)
            tk.Button(frame_btn, text="⚙️ Gerenciar Pontos", command=self.janela_gerenciar_pontos, bg="#3182ce", fg="white").pack(side="left", padx=5)
        
        frame_tabela = tk.Frame(aba, bg="white")
        frame_tabela.pack(fill="both", expand=True, padx=20, pady=20)
        self.tree_pontos = ttk.Treeview(frame_tabela, columns=("endereco", "tipo_veiculo"), show="headings")
        self.tree_pontos.pack(fill="both", expand=True)
        self.tree_pontos.heading("endereco", text="Endereço / Localização")
        self.tree_pontos.heading("tipo_veiculo", text="Veículos autorizados")
        self.recarregar_tabela_pontos()

    def criar_aba_notificar_admin(self, notebook):
        aba = tk.Frame(notebook, bg="#f4f6f9")
        notebook.add(aba, text=" ✉️ Notificar ")
        card = tk.LabelFrame(aba, text=" Falar com a Gerência ", bg="white", padx=20, pady=20)
        card.pack(fill="x", padx=30, pady=30)
        self.txt_msg = tk.Text(card, height=5, relief="solid", bg="#f7fafc")
        self.txt_msg.pack(fill="x", pady=10)
        tk.Button(card, text="Enviar Notificação", command=self.enviar_notificacao, bg="#1a365d", fg="white").pack(anchor="e")

    def janela_gerenciar_pontos(self):
        janela = tk.Toplevel(self)
        janela.title("Gerenciar Pontos de Parada")
        janela.geometry("700x450")
        
        lista_visual = tk.Listbox(janela, font=("Segoe UI", 10), selectmode="single")
        lista_visual.pack(fill="both", expand=True, padx=20, pady=10)

        def carregar_lista():
            lista_visual.delete(0, tk.END)
            for i, ponto in enumerate(self.gerenciador.obter_pontos()):
                lista_visual.insert(tk.END, f"{i + 1}. {ponto.get('endereco', '')} - {ponto.get('tipo_veiculo', '')}")
        carregar_lista()

        frame_add = tk.Frame(janela, bg="white", padx=15, pady=10)
        frame_add.pack(fill="x", padx=20, pady=(0, 10))

        tk.Label(frame_add, text="Endereço:", bg="white").grid(row=0, column=0, padx=5, pady=5)
        ent_end_add = tk.Entry(frame_add, relief="solid", width=30)
        ent_end_add.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(frame_add, text="Tipo de Veículo:", bg="white").grid(row=0, column=2, padx=5, pady=5)
        ent_tipo_add = tk.Entry(frame_add, relief="solid", width=25)
        ent_tipo_add.grid(row=0, column=3, padx=5, pady=5)
        tk.Button(frame_add, text="➕ Adicionar Ponto", command=lambda: acao_adicionar_ponto(), bg="#2f855a", fg="white").grid(row=1, column=0, columnspan=4, pady=10)

        frame_acoes = tk.Frame(janela, bg="white", padx=15, pady=10)
        frame_acoes.pack(fill="x", padx=20, pady=10)

        def acao_adicionar_ponto():
            endereco = ent_end_add.get().strip()
            tipo = ent_tipo_add.get().strip()
            if not endereco or not tipo:
                messagebox.showwarning("Atenção", "Preencha o endereço e o tipo do ponto!", parent=janela)
                return
            sucesso, msg = self.gerenciador.cadastrar_ponto(endereco, tipo)
            if sucesso:
                messagebox.showinfo("Sucesso", msg, parent=janela)
                ent_end_add.delete(0, tk.END)
                ent_tipo_add.delete(0, tk.END)
                carregar_lista()
            else:
                messagebox.showerror("Erro", msg, parent=janela)

        def acao_alterar():
            sel = lista_visual.curselection()
            if not sel: 
                messagebox.showwarning("Atenção", "Selecione um ponto", parent=janela)
                return
            
            ponto_idx = sel[0]
            ponto = self.gerenciador.obter_pontos()[ponto_idx]
            
            janela_alt = tk.Toplevel(janela)
            janela_alt.title("Alterar Ponto")
            janela_alt.geometry("400x200")
            
            tk.Label(janela_alt, text="Endereço:", font=("Segoe UI", 10)).pack(pady=(10, 0))
            ent_end = tk.Entry(janela_alt, relief="solid", width=40)
            ent_end.insert(0, ponto.get('endereco', ''))
            ent_end.pack(pady=5)
            
            tk.Label(janela_alt, text="Tipo de Veículo:", font=("Segoe UI", 10)).pack(pady=(10, 0))
            ent_tipo = tk.Entry(janela_alt, relief="solid", width=40)
            ent_tipo.insert(0, ponto.get('tipo_veiculo', ''))
            ent_tipo.pack(pady=5)
            
            def salvar():
                sucesso, msg = self.gerenciador.alterar_ponto(ponto_idx, ent_end.get().strip(), ent_tipo.get().strip())
                if sucesso:
                    messagebox.showinfo("Sucesso", msg, parent=janela_alt)
                    janela_alt.destroy()
                    carregar_lista()
                else:
                    messagebox.showerror("Erro", msg, parent=janela_alt)
            
            tk.Button(janela_alt, text="Salvar", command=salvar, bg="#2f855a", fg="white").pack(pady=10)

        def acao_excluir():
            sel = lista_visual.curselection()
            if not sel: 
                messagebox.showwarning("Atenção", "Selecione um ponto!", parent=janela)
                return
            
            if messagebox.askyesno("Confirmar", "Tem certeza que quer excluir este ponto?", parent=janela):
                sucesso, msg = self.gerenciador.excluir_ponto(sel[0])
                if sucesso:
                    messagebox.showinfo("Sucesso", msg, parent=janela)
                    carregar_lista()
                else:
                    messagebox.showerror("Erro", msg, parent=janela)

        tk.Button(frame_acoes, text="✏️ Alterar", command=acao_alterar, bg="#d69e2e", fg="white").pack(side="left", padx=5)
        tk.Button(frame_acoes, text="🗑️ Excluir", command=acao_excluir, bg="#c53030", fg="white").pack(side="left", padx=5)



    def janela_excluir_avisos(self):
        janela = tk.Toplevel(self)
        janela.title("Gerenciar Avisos")
        janela.geometry("600x400")
        
        lista_visual = tk.Listbox(janela, font=("Segoe UI", 10), selectmode="single")
        lista_visual.pack(fill="both", expand=True, padx=20, pady=10)

        def carregar_lista():
            lista_visual.delete(0, tk.END)
            for i, av in enumerate(self.gerenciador.obter_avisos()):
                lista_visual.insert(tk.END, f"{i + 1}. {av.get('conteudo', '')[:45]}...")
        carregar_lista()

        def acao_excluir():
            sel = lista_visual.curselection()
            if not sel: return messagebox.showwarning("Atenção", "Selecione um aviso!", parent=janela)
            sucesso, msg = self.gerenciador.excluir_aviso(sel[0])
            if sucesso:
                messagebox.showinfo("Sucesso", msg, parent=janela)
                carregar_lista()
            else:
                messagebox.showerror("Erro", msg, parent=janela)

        tk.Button(janela, text="🗑️ Apagar Selecionado", command=acao_excluir, bg="#c53030", fg="white").pack(pady=10)

    def janela_excluir_notificacoes(self):
        janela = tk.Toplevel(self)
        janela.title("Gerenciar Notificações")
        janela.geometry("700x450")
        
        lista_visual = tk.Listbox(janela, font=("Segoe UI", 10), selectmode="single")
        lista_visual.pack(fill="both", expand=True, padx=20, pady=10)

        def carregar_lista():
            lista_visual.delete(0, tk.END)
            for i, notif in enumerate(self.gerenciador.obter_notificacoes()):
                lista_visual.insert(tk.END, f"{i + 1}. {notif.get('usuario', '')} ({notif.get('data', '')}): {notif.get('mensagem', '')[:50]}")
        carregar_lista()

        def acao_excluir():
            sel = lista_visual.curselection()
            if not sel:
                return messagebox.showwarning("Atenção", "Selecione uma notificação!", parent=janela)
            sucesso, msg = self.gerenciador.excluir_notificacao(sel[0])
            if sucesso:
                messagebox.showinfo("Sucesso", msg, parent=janela)
                carregar_lista()
                self.carregar_notificacoes()
            else:
                messagebox.showerror("Erro", msg, parent=janela)

        tk.Button(janela, text="🗑️ Apagar Selecionado", command=acao_excluir, bg="#c53030", fg="white").pack(pady=10)

    def alterar_passageiros(self, operacao):
        sel = self.tree_frota.selection()
        if not sel: 
            messagebox.showwarning("Atenção", "Selecione um veículo!")
            return
        placa = self.tree_frota.item(sel, "values")[0]
        try:
            qtd = int(self.ent_qtd.get().strip() or 0)
        except ValueError:
            messagebox.showerror("Erro", "Digite uma quantidade válida!")
            return
        
        sucesso, msg = self.gerenciador.alterar_lotacao(placa, qtd, operacao)
        if sucesso:
            self.recarregar_tabela_frota()
            messagebox.showinfo("Sucesso", msg)
        else:
            messagebox.showerror("Erro", msg)

    def add_bike(self):
        sucesso, msg = self.gerenciador.cadastrar_bike(self.ent_nova_bike.get().strip())
        if sucesso: self.recarregar_tabela_bikes()

    def bike_action(self, acao):
        sucesso, msg = self.gerenciador.acao_bike(self.ent_id_bike.get().strip(), acao)
        if sucesso: self.recarregar_tabela_bikes()

    def cadastrar_novo_veiculo(self):
        placa = self.ent_placa_c.get().strip()
        capacidade = self.ent_cap_c.get().strip()
        motorista = self.ent_mot_c.get().strip()

        if not placa or not capacidade:
            messagebox.showwarning("Atenção", "Informe placa e capacidade do veículo!")
            return
        if not capacidade.isdigit():
            messagebox.showwarning("Atenção", "Capacidade deve ser um número inteiro!")
            return

        sucesso, msg = self.gerenciador.cadastrar_veiculo(
            placa,
            self.var_tipo_c.get(),
            capacidade,
            motorista
        )
        if sucesso:
            self.recarregar_tabela_frota()
            messagebox.showinfo("Sucesso", msg)
            self.ent_placa_c.delete(0, tk.END)
            self.ent_cap_c.delete(0, tk.END)
            self.ent_mot_c.delete(0, tk.END)
        else:
            messagebox.showerror("Erro", msg)

    def acao_alterar_veiculo(self):
        sucesso, msg = self.gerenciador.alterar_motorista_veiculo(self.ent_placa_alt.get().strip(), self.ent_mot_alt.get().strip())
        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.recarregar_tabela_frota()
        else:
            messagebox.showerror("Erro", msg)

    def acao_cadastrar_motorista(self):
        sucesso, msg = self.gerenciador.cadastrar_usuario(self.ent_nome_mot.get().strip(), self.ent_senha_mot.get().strip(), "Motorista")
        if sucesso: messagebox.showinfo("Sucesso", msg)
        else: messagebox.showerror("Erro", msg)

    def add_ponto(self):
        endereco = self.ent_end_ponto.get().strip()
        tipo = self.ent_tipo_ponto.get().strip()
        if not endereco or not tipo:
            messagebox.showwarning("Atenção", "Preencha o endereço e o tipo do ponto!")
            return
        sucesso, msg = self.gerenciador.cadastrar_ponto(endereco, tipo)
        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.ent_end_ponto.delete(0, tk.END)
            self.ent_tipo_ponto.delete(0, tk.END)
            self.recarregar_tabela_pontos()
        else:
            messagebox.showerror("Erro", msg)

    def publicar_aviso(self):
        sucesso, msg = self.gerenciador.publicar_aviso(self.ent_aviso.get().strip())
        if sucesso:
            self.ent_aviso.delete(0, tk.END)

    def enviar_notificacao(self):
        sucesso, msg = self.gerenciador.enviar_notificacao(self.usuario_atual.nome, self.txt_msg.get("1.0", tk.END).strip())
        if sucesso: self.txt_msg.delete("1.0", tk.END)

if __name__ == "__main__":
    app = AppTransporte()
    app.mainloop()