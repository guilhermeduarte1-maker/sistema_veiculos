import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from main import Gerenciador, FrotaVeiculos, Passageiro, Ponto_parada


class AppTransporte(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Sistema de Gerenciamento de Frota")
        self.geometry("600x500")
        self.configure(bg="#f0f0f0")


        frota = FrotaVeiculos(
            onibus=[], vans=[], micro_onibus=[], bicicleta=[]
        )

        self.gerenciador = Gerenciador(
            usuarios=[],
            frota_veiculos=frota,
            nome="Expresso Central",
            pontos_parada=[],
        )


        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=10, expand=True, fill="both")


        self.aba_usuarios = tk.Frame(self.notebook, bg="#f0f0f0")
        self.notebook.add(self.aba_usuarios, text="👤 Usuários")
        self.configurar_aba_usuarios()

        # Aba de Bicicletas
        self.aba_bicicletas = tk.Frame(self.notebook, bg="#f0f0f0")
        self.notebook.add(self.aba_bicicletas, text="🚲 Bicicletas")
        self.configurar_aba_bicicletas()


        self.atualizar_tabela_usuarios()


    def configurar_aba_usuarios(self):
        # Frame de Cadastro
        frame_cadastro = tk.LabelFrame(
            self.aba_usuarios,
            text=" Cadastrar Novo Usuário ",
            bg="#f0f0f0",
            padx=10,
            pady=10,
        )
        frame_cadastro.pack(padx=10, pady=10, fill="x")

        tk.Label(frame_cadastro, text="Nome:", bg="#f0f0f0").grid(
            row=0, column=0, sticky="w", pady=5
        )
        self.entry_nome = tk.Entry(frame_cadastro, width=30)
        self.entry_nome.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(frame_cadastro, text="Senha:", bg="#f0f0f0").grid(
            row=1, column=0, sticky="w", pady=5
        )
        self.entry_senha = tk.Entry(frame_cadastro, show="*", width=30)
        self.entry_senha.grid(row=1, column=1, pady=5, padx=5)

        btn_cadastrar = tk.Button(
            frame_cadastro,
            text="Cadastrar e Salvar",
            command=self.acao_cadastrar_usuario,
            bg="#4CAF50",
            fg="white",
        )
        btn_cadastrar.grid(row=2, column=1, pady=10, sticky="e")


        frame_lista = tk.LabelFrame(
            self.aba_usuarios,
            text=" Usuários Cadastrados (Lidos do CSV) ",
            bg="#f0f0f0",
            padx=10,
            pady=10,
        )
        frame_lista.pack(padx=10, pady=5, fill="both", expand=True)


        self.listbox_usuarios = tk.Listbox(frame_lista, height=10)
        self.listbox_usuarios.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(frame_lista)
        scrollbar.pack(side="right", fill="y")


        self.listbox_usuarios.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox_usuarios.yview)

    def configurar_aba_bicicletas(self):
        frame_acoes = tk.LabelFrame(
            self.aba_bicicletas,
            text=" Controle de Empréstimos ",
            bg="#f0f0f0",
            padx=20,
            pady=20,
        )
        frame_acoes.pack(padx=20, pady=20, fill="x")

        tk.Label(
            frame_acoes,
            text="Número / Placa da Bicicleta:",
            bg="#f0f0f0",
            font=("Arial", 11),
        ).pack(pady=5)
        self.entry_placa_bike = tk.Entry(
            frame_acoes, font=("Arial", 12), width=20, justify="center"
        )
        self.entry_placa_bike.pack(pady=5)

        # Botões lado a lado
        frame_botoes = tk.Frame(frame_acoes, bg="#f0f0f0")
        frame_botoes.pack(pady=15)

        btn_emprestar = tk.Button(
            frame_botoes,
            text="🚲 Emprestar Bicicleta",
            command=self.acao_emprestar_bike,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=10,
            pady=5,
        )
        btn_emprestar.pack(side="left", padx=10)

        btn_devolver = tk.Button(
            frame_botoes,
            text="🔄 Devolver Bicicleta",
            command=self.acao_devolver_bike,
            bg="#FF9800",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=10,
            pady=5,
        )
        btn_devolver.pack(side="left", padx=10)

    # --- AÇÕES E INTEGRAÇÃO COM A TUA LÓGICA ---
    def acao_cadastrar_usuario(self):
        nome = self.entry_nome.get().strip()
        senha = self.entry_senha.get().strip()

        if not nome or not senha:
            messagebox.showwarning("Aviso", "Por favor, preencha todos os campos.")
            return

        # Instancia a tua classe Passageiro
        novo_passageiro = Passageiro(nome, senha)

        # Chama o teu método do Gerenciador (que já insere na lista e salva no CSV)
        mensagem = self.gerenciador.cadastrar_usuario(novo_passageiro)

        # Mostra o pop-up de sucesso
        messagebox.showinfo("Sucesso", mensagem)

        # Limpa os campos de texto
        self.entry_nome.delete(0, tk.END)
        self.entry_senha.delete(0, tk.END)

        # Atualiza a lista visual automaticamente
        self.atualizar_tabela_usuarios()

    def atualizar_tabela_usuarios(self):
        # Limpa a lista atual do ecrã
        self.listbox_usuarios.delete(0, tk.END)

        # Usa o teu método get_usuarios() para ler os dados da memória (que vieram do CSV)
        for usuario in self.gerenciador.get_usuarios():
            self.listbox_usuarios.insert(tk.END, f"  👤 {usuario.nome}")

    def acao_emprestar_bike(self):
        placa = self.entry_placa_bike.get().strip()
        if not placa:
            messagebox.showwarning("Aviso", "Introduza o número da bicicleta.")
            return

        # Executa o teu método original da FrotaVeiculos (que lê o CSV, valida e salva de volta)
        # Como o print() está dentro do teu método, adicionámos um retorno booleano lá atrás
        sucesso = self.gerenciador.frota_veiculos.emprestar_bicicleta(placa)

        if sucesso:
            messagebox.showinfo("Sucesso", f"Bicicleta {placa} emprestada!")
            self.entry_placa_bike.delete(0, tk.END)
        else:
            messagebox.showerror(
                "Erro",
                f"Não foi possível emprestar a bicicleta {placa}.\nVerifique o estado no terminal.",
            )

    def acao_devolver_bike(self):
        placa = self.entry_placa_bike.get().strip()
        if not placa:
            messagebox.showwarning("Aviso", "Introduza o número da bicicleta.")
            return

        # Executa o teu método original de devolução
        sucesso = self.gerenciador.frota_veiculos.devolver_bicicleta(placa)

        if sucesso:
            messagebox.showinfo("Sucesso", f"Bicicleta {placa} devolvida!")
            self.entry_placa_bike.delete(0, tk.END)
        else:
            messagebox.showerror(
                "Erro",
                f"Não foi possível devolver a bicicleta {placa}.\nVerifique o número no terminal.",
            )


# Inicializa o programa gráfico
if __name__ == "__main__":
    app = AppTransporte()
    app.mainloop()