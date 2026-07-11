import tkinter as tk
from tkinter import ttk, messagebox
import datetime

# 1. IMPORTAÇÃO DOS COMPONENTES DO SEU PROJETO
from dados import OperadorArquivo
from veiculos import Onibus, Van, Micro_onibus, Bicicleta
from pessoas import Motorista, Passageiro, Pessoa_admin

# Classes de apoio para unificar o comportamento com o seu backend
class Gerenciador:
    def __init__(self, usuarios, frota_veiculos, nome, pontos_parada):
        self._usuarios = usuarios
        self.frota_veiculos = frota_veiculos
        self.nome = nome
        self.pontos_parada = pontos_parada

    def get_usuarios(self):
        return self._usuarios

class FrotaVeiculos:
    def __init__(self, onibus, vans, micro_onibus, bicicleta):
        self._onibus = onibus
        self._vans = vans
        self._micro_onibus = micro_onibus
        self._bicicletas = bicicleta

    def get_onibus(self): return self._onibus
    def get_vans(self): return self._vans
    def get_micro_onibus(self): return self._micro_onibus
    def get_bicicletas(self): return self._bicicletas

    def emprestar_bicicleta(self, placa):
        for b in self._bicicletas:
            if b._placa == placa and b.disponivel:
                b.disponivel = False
                return True
        return False

    def devolver_bicicleta(self, placa):
        for b in self._bicicletas:
            if b._placa == placa and not b.disponivel:
                b.disponivel = True
                return True
        return False

    def __str__(self):
        total = len(self._onibus) + len(self._vans) + len(self._micro_onibus) + len(self._bicicletas)
        return f"{total} veículo(s) mapeado(s) no total de registros."


class AppTransporte(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Expresso Central - Painel de Controle Integrado")
        self.geometry("850x650")
        self.configure(bg="#f4f6f9")
        
        # INSTANCIAÇÃO DOS OPERADORES COM OS SEUS ARQUIVOS REAIS
        self.op_veiculos = OperadorArquivo("veiculos.csv")
        self.op_usuarios = OperadorArquivo("usuarios.csv")
        self.op_avisos = OperadorArquivo("avisos.csv")
        
        self.gerenciador = Gerenciador(
            usuarios=self.carregar_usuarios_do_operador(),
            frota_veiculos=self.carregar_frota_do_operador(),
            nome="Expresso Central",
            pontos_parada=[]
        )
        
        self.usuario_atual = None  
        self.perfil_acesso = "Passageiro"

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

    # ==================== TRATAMENTO DE DADOS (ALINHADO COM SEUS ARQUIVOS) ====================

    def carregar_frota_do_operador(self):
        onibus_list, vans_list, micro_list, bike_list = [], [], [], []
        linhas = self.op_veiculos.ler_csv(self.op_veiculos.arquivo)
        
        for row in linhas:
            tipo = row.get("tipo", "").strip()
            placa = row.get("placa", "").strip()
            cap = int(row.get("capacidade", 0)) if row.get("capacidade") else 0
            mot = row.get("motorista", "Sem Motorista").strip()
            func = row.get("funcionando", "True").strip() == "True"
            rota = row.get("rota", "Geral").strip()
            passag = int(row.get("passageiros", 0)) if row.get("passageiros") else 0
            
            if tipo == "Ônibus":
                onibus_list.append(Onibus(placa, cap, mot, func, rota, passag))
            elif tipo == "Van":
                vans_list.append(Van(placa, cap, mot, func, rota, passag))
            elif tipo == "Micro-ônibus":
                micro_list.append(Micro_onibus(placa, cap, mot, func, rota, passag))
            elif tipo == "Bicicleta":
                bike_list.append(Bicicleta(placa, funcionando=func, disponivel=True))
                
        return FrotaVeiculos(onibus=onibus_list, vans=vans_list, micro_onibus=micro_list, bicicleta=bike_list)

    def carregar_usuarios_do_operador(self):
        usuarios = []
        linhas = self.op_usuarios.ler_csv(self.op_usuarios.arquivo)
        for row in linhas:
            nome = row.get("nome", "").strip()
            senha = row.get("senha", "").strip()
            tipo = row.get("tipo", "Passageiro").strip()
            
            if not nome:
                continue
                
            if tipo == "Gerenciador" or tipo == "Admin":
                usuarios.append(Pessoa_admin(nome, senha))
            elif tipo == "Motorista":
                usuarios.append(Motorista(nome, senha, []))
            else:
                usuarios.append(Passageiro(nome, senha))
        return usuarios

    def salvar_frota_pelo_operador(self):
        dados_salvar = []
        fv = self.gerenciador.frota_veiculos
        
        for v in fv.get_onibus():
            dados_salvar.append({"placa": v._placa, "tipo": "Ônibus", "capacidade": v.capacidade, "motorista": v.motorista, "funcionando": str(v.funcionando), "rota": v.rota, "passageiros": v.passageiros})
        for v in fv.get_vans():
            dados_salvar.append({"placa": v._placa, "tipo": "Van", "capacidade": v.capacidade, "motorista": v.motorista, "funcionando": str(v.funcionando), "rota": v.rota, "passageiros": v.passageiros})
        for v in fv.get_micro_onibus():
            dados_salvar.append({"placa": v._placa, "tipo": "Micro-ônibus", "capacidade": v.capacidade, "motorista": v.motorista, "funcionando": str(v.funcionando), "rota": v.rota, "passageiros": v.passageiros})
        for v in fv.get_bicicletas():
            dados_salvar.append({"placa": v._placa, "tipo": "Bicicleta", "capacidade": "1", "motorista": "Livre", "funcionando": str(v.funcionando), "rota": "Geral", "passageiros": "0"})
            
        fieldnames = ["placa", "tipo", "capacidade", "passageiros", "motorista", "funcionando", "rota"]
        self.op_veiculos.escrever_csv(dados_salvar, self.op_veiculos.arquivo, fieldnames=fieldnames)

    # ==================== FLUXOS DE TELAS ====================

    def mostrar_tela_login(self):
        self.limpar_container()
        card = tk.Frame(self.container, bg="white", highlightbackground="#e2e8f0", highlightthickness=1, padx=30, pady=25)
        card.place(relx=0.5, rely=0.5, anchor="center", width=440, height=520)

        tk.Label(card, text="🚌 Expresso Central", bg="white", fg="#1a365d", font=("Segoe UI", 20, "bold")).pack(pady=(5, 2))
        tk.Label(card, text="Acesso Gerenciado via Operador CSV", bg="white", fg="#718096", font=("Segoe UI", 9)).pack(pady=(0, 15))

        tk.Label(card, text="Selecione seu Perfil:", bg="white", fg="#4a5568", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        var_perfil = tk.StringVar(value="Passageiro")
        frame_perfis = tk.Frame(card, bg="white")
        frame_perfis.pack(fill="x", pady=(5, 15))
        tk.Radiobutton(frame_perfis, text="Passageiro", variable=var_perfil, value="Passageiro", bg="white").pack(side="left", padx=(0, 10))
        tk.Radiobutton(frame_perfis, text="Gerenciador (Admin)", variable=var_perfil, value="Gerenciador", bg="white").pack(side="left")

        tk.Label(card, text="Nome de Usuário", bg="white", fg="#4a5568", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        ent_nome = tk.Entry(card, font=("Segoe UI", 11), bg="#f7fafc", relief="solid", bd=1)
        ent_nome.pack(fill="x", ipady=5, pady=(2, 12))

        tk.Label(card, text="Senha", bg="white", fg="#4a5568", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        ent_senha = tk.Entry(card, show="*", font=("Segoe UI", 11), bg="#f7fafc", relief="solid", bd=1)
        ent_senha.pack(fill="x", ipady=5, pady=(2, 20))

        def acao_login():
            nome = ent_nome.get().strip()
            senha = ent_senha.get().strip()
            self.perfil_acesso = var_perfil.get()

            self.gerenciador._usuarios = self.carregar_usuarios_do_operador()
            
            usuario_encontrado = None
            for u in self.gerenciador.get_usuarios():
                if u.nome == nome and u.get_senha() == senha:
                    usuario_encontrado = u
                    break
            
            if usuario_encontrado:
                self.usuario_atual = usuario_encontrado
                self.mostrar_painel_principal()
            else:
                messagebox.showerror("Erro de Autenticação", "Usuário não cadastrado ou senha incorreta no seu arquivo CSV.")

        def acao_cadastro():
            nome = ent_nome.get().strip()
            senha = ent_senha.get().strip()
            if not nome or not senha:
                messagebox.showwarning("Aviso", "Preencha todos os campos para cadastrar!")
                return
            
            linhas_atuais = self.op_usuarios.ler_csv(self.op_usuarios.arquivo)
            linhas_atuais.append({"nome": nome, "senha": senha, "tipo": self.perfil_acesso})
            
            self.op_usuarios.escrever_csv(linhas_atuais, self.op_usuarios.arquivo, fieldnames=["nome", "senha", "tipo"])
            messagebox.showinfo("Sucesso", "Usuário gravado via OperadorArquivo com sucesso!")

        tk.Button(card, text="Entrar no Sistema", command=acao_login, bg="#1a365d", fg="white", font=("Segoe UI", 11, "bold"), relief="flat").pack(fill="x", ipady=6, pady=(0, 10))
        tk.Button(card, text="Cadastrar Novo Perfil", command=acao_cadastro, bg="white", fg="#4a5568", font=("Segoe UI", 10, "underline"), relief="flat", bd=0).pack(pady=5)

    def mostrar_painel_principal(self):
        self.limpar_container()
        header = tk.Frame(self.container, bg="#1a365d", height=65)
        header.pack(fill="x", side="top")
        
        tk.Label(header, text=f"👤 {self.usuario_atual.nome} ({self.perfil_acesso})", bg="#1a365d", fg="white", font=("Segoe UI", 11, "bold")).pack(side="left", padx=20, pady=18)
        tk.Button(header, text="Sair ➔", command=self.mostrar_tela_login, bg="#e53e3e", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", padx=12).pack(side="right", padx=20, pady=15)

        notebook = ttk.Notebook(self.container)
        notebook.pack(fill="both", expand=True, padx=15, pady=15)

        if self.perfil_acesso == "Gerenciador":
            self.criar_aba_dashboard_geral(notebook)
            self.criar_aba_controle_frota(notebook)
            self.criar_aba_bikes(notebook)
            self.criar_aba_acoes_gerenciador(notebook)
        else:
            self.criar_aba_quadro_avisos(notebook)

    def criar_aba_dashboard_geral(self, notebook):
        aba = tk.Frame(notebook, bg="#f4f6f9")
        notebook.add(aba, text=" 📊 Dashboard ")
        card = tk.Frame(aba, bg="white", highlightbackground="#e2e8f0", highlightthickness=1, padx=20, pady=20)
        card.pack(fill="x", padx=20, pady=15)
        tk.Label(card, text="Resumo da Frota Atualizado por OperadorArquivo", font=("Segoe UI", 11, "bold"), bg="white").pack(anchor="w")
        tk.Label(card, text=str(self.gerenciador.frota_veiculos), font=("Segoe UI", 14, "bold"), fg="#1a365d", bg="white").pack(anchor="w", pady=5)

    def criar_aba_controle_frota(self, notebook):
        aba = tk.Frame(notebook, bg="#f4f6f9")
        notebook.add(aba, text=" 🚌 Frota ")

        frame_tabela = tk.Frame(aba, bg="white")
        frame_tabela.pack(fill="both", expand=True, padx=20, pady=10)

        colunas = ("placa", "tipo", "capacidade", "passageiros", "motorista")
        tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings")
        tree.pack(side="left", fill="both", expand=True)

        for col in colunas: tree.heading(col, text=col.title())

        def recarregar_tabela():
            for i in tree.get_children(): tree.delete(i)
            self.gerenciador.frota_veiculos = self.carregar_frota_do_operador()
            f = self.gerenciador.frota_veiculos
            cats = [(f.get_onibus(), "Ônibus"), (f.get_vans(), "Van"), (f.get_micro_onibus(), "Micro-ônibus")]
            for lista, nome_cat in cats:
                for v in lista:
                    tree.insert("", "end", values=(v._placa, nome_cat, v.capacidade, v.passageiros, v.motorista))

        recarregar_tabela()

        frame_fluxo = tk.LabelFrame(aba, text=" Alterar Lotação de Passageiros ", bg="white", padx=15, pady=15)
        frame_fluxo.pack(fill="x", padx=20, pady=15)

        ent_qtd = tk.Entry(frame_fluxo, width=10, relief="solid")
        ent_qtd.grid(row=0, column=0, padx=5)

        def alterar_passageiros(operacao):
            sel = tree.selection()
            if not sel: return
            try: 
                qtd = int(ent_qtd.get().strip())
            except: 
                return

            placa, tipo = tree.item(sel, "values")[0], tree.item(sel, "values")[1]
            fv = self.gerenciador.frota_veiculos
            lista = fv.get_onibus() if tipo == "Ônibus" else (fv.get_vans() if tipo == "Van" else fv.get_micro_onibus())

            for v in lista:
                if v._placa == placa:
                    if operacao == "subir":
                        resultado = v.entrada_passageiros(qtd)
                        messagebox.showinfo("Log do Veículo", resultado)
                    else:
                        if v.passageiros - qtd < 0:
                            v.passageiros = 0
                        else:
                            v.passageiros -= qtd
                        messagebox.showinfo("Log do Veículo", f"Passageiros removidos. Lotação atual do {tipo}: {v.passageiros}")
                    break
            
            self.salvar_frota_pelo_operador()
            recarregar_tabela()
            ent_qtd.delete(0, tk.END)

        tk.Button(frame_fluxo, text="📥 Entrada (+)", command=lambda: alterar_passageiros("subir"), bg="#2f855a", fg="white").grid(row=0, column=1, padx=5)
        tk.Button(frame_fluxo, text="📤 Saída (-)", command=lambda: alterar_passageiros("descer"), bg="#c53030", fg="white").grid(row=0, column=2, padx=5)

    def criar_aba_bikes(self, notebook):
        aba = tk.Frame(notebook, bg="#f4f6f9")
        notebook.add(aba, text=" 🚲 Compartilhamento ")

        card = tk.Frame(aba, bg="white", padx=25, pady=25)
        card.place(relx=0.5, rely=0.4, anchor="center", width=400, height=200)

        tk.Label(card, text="Inserir Identificador da Bike:", bg="white").pack(anchor="w")
        ent_id = tk.Entry(card, font=("Segoe UI", 12), relief="solid")
        ent_id.pack(fill="x", pady=10)

        def bike_action(acao):
            p = ent_id.get().strip()
            res = self.gerenciador.frota_veiculos.emprestar_bicicleta(p) if acao == "emp" else self.gerenciador.frota_veiculos.devolver_bicicleta(p)
            if res:
                self.salvar_frota_pelo_operador()
                messagebox.showinfo("Sucesso", f"Estado da Bike {p} persistido no arquivo CSV!")
                ent_id.delete(0, tk.END)
            else:
                messagebox.showwarning("Erro", "Bike não encontrada ou estado indisponível.")

        tk.Button(card, text="🚲 Liberar Empréstimo", command=lambda: bike_action("emp"), bg="#2b6cb0", fg="white").pack(side="left", fill="x", expand=True, padx=5)
        tk.Button(card, text="🔄 Trancar / Devolver", command=lambda: bike_action("dev"), bg="#dd6b20", fg="white").pack(side="right", fill="x", expand=True, padx=5)

    def criar_aba_acoes_gerenciador(self, notebook):
        aba = tk.Frame(notebook, bg="#f4f6f9")
        notebook.add(aba, text=" 📢 Avisos ")

        frame_aviso = tk.LabelFrame(aba, text=" Publicar Informativo no Arquivo ", bg="white", padx=15, pady=10)
        frame_aviso.pack(fill="x", padx=20, pady=10)

        ent_aviso = tk.Entry(frame_aviso, relief="solid")
        ent_aviso.pack(side="left", fill="x", expand=True, padx=(0, 10))

        def publicar_aviso():
            txt = ent_aviso.get().strip()
            if not txt: return
            dt = datetime.date.today().strftime('%d/%m/%Y')
            
            linhas_antigas = self.op_avisos.ler_csv(self.op_avisos.arquivo)
            linhas_antigas.append({"data": dt, "conteudo": txt})
            
            self.op_avisos.escrever_csv(linhas_antigas, self.op_avisos.arquivo, fieldnames=["data", "conteudo"])
            messagebox.showinfo("Sucesso", "Aviso adicionado usando OperadorArquivo!")
            ent_aviso.delete(0, tk.END)

        tk.Button(frame_aviso, text="Gravar Aviso", command=publicar_aviso, bg="#1a365d", fg="white").pack(side="right")

    def criar_aba_quadro_avisos(self, notebook):
        aba = tk.Frame(notebook, bg="#f4f6f9")
        notebook.add(aba, text=" 📢 Quadro de Avisos ")

        txt = tk.Text(aba, bg="white", padx=15, pady=15)
        txt.pack(fill="both", expand=True, padx=20, pady=20)

        linhas = self.op_avisos.ler_csv(self.op_avisos.arquivo)
        if linhas:
            for row in reversed(linhas):
                txt.insert(tk.END, f"📍 NOTIFICAÇÃO ({row.get('data')}):\n{row.get('conteudo')}\n\n-------------------\n\n")
        else:
            txt.insert(tk.END, "Nenhum informativo registrado no momento no arquivo avisos.csv.")
        txt.config(state="disabled")


if __name__ == "__main__":
    app = AppTransporte()
    app.mainloop()