import datetime
from dados import OperadorArquivo
from pessoas import Pessoa_admin, Motorista, Passageiro
from veiculos import Onibus, Van, Micro_onibus, Bicicleta

class Ponto_parada:
    """
    Cria um ponto de parada com o endereço e o tipo de veiculo que para nele.
        Essa classe é usada para armazenar os pontos de parada no sistema.
    """
    def __init__(self, endereco, tipo_veiculo):
        self.endereco = endereco
        self.tipo_veiculo = tipo_veiculo

class Aviso:
    """
    Cria uma mensagem que contem o conteudo a ser avisado
        Essa classe é usada para armazenar informacoes de alertas e avisos gerais 
        emitidos pela administração do sistema.
    """
    def __init__(self, conteudo):
        self.conteudo = conteudo

class FrotaVeiculos:
    """
    Variavel que armazena as listas dos veiculos e retorna a quantidade especifica de cada veiculo
        Essa classe é usada para organizar e gerenciar a frota de veículos do sistema,
        permitindo o acesso rápido às listas de ônibus, vans, micro-ônibus e bicicletas.
    """
    def __init__(self, onibus=None, vans=None, micro_onibus=None, bicicleta=None):
        self.onibus = onibus or []
        self.vans = vans or []
        self.micro_onibus = micro_onibus or []
        self.bicicletas = bicicleta or []

    def get_onibus(self): return self.onibus
    def get_vans(self): return self.vans
    def get_micro_onibus(self): return self.micro_onibus
    def get_bicicletas(self): return self.bicicletas

    def __str__(self):
        return f"Ônibus: {len(self.onibus)} | Vans: {len(self.vans)} | Micro: {len(self.micro_onibus)} | Bikes: {len(self.bicicletas)}"

class Gerenciador:
    """
    Classe que contem todas as funções que administram o csv.
        Essa classe é usada para gerenciar o sistema de transporte, incluindo a autenticação de usuários,
        cadastro e gerenciamento de veículos, pontos de parada, avisos e notificações.
    """
    def __init__(self, nome="Expresso Central"):
        self.nome = nome
        self.op_usuarios = OperadorArquivo("usuarios.csv")
        self.op_veiculos = OperadorArquivo("veiculos.csv")
        self.op_bicicletas = OperadorArquivo("bicicletas.csv")
        self.op_pontos = OperadorArquivo("pontos_parada.csv")
        self.op_avisos = OperadorArquivo("avisos.csv")
        self.op_notificacoes = OperadorArquivo("notificacoes.csv")

    def validar_motorista(self, nome_motorista):
        usuarios_csv = self.op_usuarios.ler_csv(self.op_usuarios.arquivo) or []
        for u in usuarios_csv:
            if u.get("nome", "").strip() == nome_motorista and u.get("tipo", "").strip() == "Motorista":
                return True
        return False

    def cadastrar_usuario(self, nome, senha, tipo):
        usuarios_csv = self.op_usuarios.ler_csv(self.op_usuarios.arquivo) or []
        for u in usuarios_csv:
            if u.get("nome", "").strip() == nome:
                return False, "Já existe um usuário com esse nome."
        usuarios_csv.append({"nome": nome, "senha": senha, "tipo": tipo})
        self.op_usuarios.escrever_csv(usuarios_csv, self.op_usuarios.arquivo, ["nome", "senha", "tipo"])
        return True, f"Usuário '{nome}' cadastrado !"
        
    def carregar_frota(self):
        onibus_list, vans_list, micro_list, bike_list = [], [], [], []
        linhas_v = self.op_veiculos.ler_csv(self.op_veiculos.arquivo) or []
        
        for row in linhas_v:
            tipo = row.get("tipo", "").strip()
            placa = row.get("placa", "").strip()
            cap = int(row.get("capacidade", 0)) if row.get("capacidade") else 0
            mot = row.get("motorista", "Sem Motorista").strip()
            func = row.get("funcionando", "True").strip() == "True"
            rota = row.get("rota", "Geral").strip()
            passageiro = int(row.get("passageiros", 0)) if row.get("passageiros") else 0
            
            if tipo == "Ônibus": onibus_list.append(Onibus(placa, cap, mot, func, rota, passageiro))
            elif tipo == "Van": vans_list.append(Van(placa, cap, mot, func, rota, passageiro))
            elif tipo == "Micro-ônibus": micro_list.append(Micro_onibus(placa, cap, mot, func, rota, passageiro))
        
        linhas_b = self.op_bicicletas.ler_csv(self.op_bicicletas.arquivo) or []
        for row in linhas_b:
            bike_list.append(Bicicleta(
                row.get("numero", "").strip(),
                funcionando=(row.get("funcionamento", "True").strip() == "True"),
                disponivel=(row.get("disponivel", "True").strip() == "True")
            ))
            
        return FrotaVeiculos(onibus_list, vans_list, micro_list, bike_list)

    def cadastrar_veiculo(self, placa, tipo, capacidade, motorista):
        if motorista and not self.validar_motorista(motorista):
            return False, f"Motorista '{motorista}' não existe no sistema!"
        linhas = self.op_veiculos.ler_csv(self.op_veiculos.arquivo) or []
        linhas.append({"placa": placa, "tipo": tipo, "capacidade": capacidade, "passageiros": "0", "motorista": motorista, "funcionando": "True", "rota": "Geral"})
        self.op_veiculos.escrever_csv(linhas, self.op_veiculos.arquivo, ["placa", "tipo", "capacidade", "passageiros", "motorista", "funcionando", "rota"])
        return True, "Veículo cadastrado com sucesso!"

    def alterar_motorista_veiculo(self, placa, novo_motorista):
        if novo_motorista and not self.validar_motorista(novo_motorista):
            return False, f"Motorista '{novo_motorista}' não existe no sistema!"
        linhas = self.op_veiculos.ler_csv(self.op_veiculos.arquivo) or []
        alterou = False
        for v in linhas:
            if v.get("placa", "").strip().upper() == placa.upper():
                v["motorista"] = novo_motorista
                alterou = True
                break
        if alterou:
            self.op_veiculos.escrever_csv(linhas, self.op_veiculos.arquivo, ["placa", "tipo", "capacidade", "passageiros", "motorista", "funcionando", "rota"])
            return True, "Veículo atualizado com sucesso!"
        return False, "Veículo não encontrado!"

    def alterar_lotacao(self, placa, qtd, operacao):
        linhas = self.op_veiculos.ler_csv(self.op_veiculos.arquivo) or []
        for v in linhas:
            if v.get("placa", "").strip().upper() == placa.upper():
                atual = int(v.get("passageiros", 0))
                capacidade = int(v.get("capacidade", 0))
                if operacao == "subir":
                    novo_total = atual + qtd
                    if novo_total > capacidade:
                        return False, f"Capacidade excedida! Máximo: {capacidade}, tentou adicionar: {novo_total}"
                    v["passageiros"] = str(novo_total)
                else:
                    v["passageiros"] = str(max(0, atual - qtd))
                self.op_veiculos.escrever_csv(linhas, self.op_veiculos.arquivo, ["placa", "tipo", "capacidade", "passageiros", "motorista", "funcionando", "rota"])
                return True, "Lotação atualizada com sucesso!"
        return False, "Veículo não encontrado!"


    def cadastrar_bike(self, numero):
        linhas = self.op_bicicletas.ler_csv(self.op_bicicletas.arquivo) or []
        linhas.append({"numero": numero, "funcionamento": "True", "disponivel": "True"})
        self.op_bicicletas.escrever_csv(linhas, self.op_bicicletas.arquivo, ["numero", "funcionamento", "disponivel"])
        return True, "Bicicleta adicionada!"

    def acao_bike(self, numero, acao):
        linhas = self.op_bicicletas.ler_csv(self.op_bicicletas.arquivo) or []
        for b in linhas:
            if b.get("numero", "").strip() == numero:
                b["disponivel"] = "False" if acao == "emp" else "True"
                self.op_bicicletas.escrever_csv(linhas, self.op_bicicletas.arquivo, ["numero", "funcionamento", "disponivel"])
                return True, "Ação realizada com sucesso!"
        return False, "Bicicleta não encontrada!"


    def obter_pontos(self):
        return self.op_pontos.ler_csv(self.op_pontos.arquivo) or []

    def cadastrar_ponto(self, endereco, tipo_veiculo):
        linhas = self.obter_pontos()
        linhas.append({"endereco": endereco, "tipo_veiculo": tipo_veiculo})
        self.op_pontos.escrever_csv(linhas, self.op_pontos.arquivo, ["endereco", "tipo_veiculo"])
        return True, "Ponto cadastrado!"

    def alterar_ponto(self, index, novo_endereco, novo_tipo):
        linhas = self.obter_pontos()
        try:
            linhas[index] = {"endereco": novo_endereco, "tipo_veiculo": novo_tipo}
            self.op_pontos.escrever_csv(linhas, self.op_pontos.arquivo, ["endereco", "tipo_veiculo"])
            return True, "Ponto alterado com sucesso!"
        except IndexError:
            return False, "Ponto não encontrado!"

    def excluir_ponto(self, index):
        linhas = self.obter_pontos()
        try:
            linhas.pop(index)
            self.op_pontos.escrever_csv(linhas, self.op_pontos.arquivo, ["endereco", "tipo_veiculo"])
            return True, "Ponto excluído com sucesso!"
        except IndexError:
            return False, "Ponto não encontrado!"


    def obter_avisos(self):
        return self.op_avisos.ler_csv(self.op_avisos.arquivo) or []

    def publicar_aviso(self,conteudo):
        linhas = self.obter_avisos()
        linhas.append({"conteudo": conteudo})
        self.op_avisos.escrever_csv(linhas, self.op_avisos.arquivo, ["conteudo"])
        return True, "Aviso publicado!"

    def excluir_aviso(self, index):
        linhas = self.obter_avisos()
        try:
            linhas.pop(index)
            cabecalhos = list(linhas[0].keys()) if linhas else ["conteudo"]
            self.op_avisos.escrever_csv(linhas, self.op_avisos.arquivo, cabecalhos)
            return True, "Aviso excluído!"
        except Exception as e:
            return False, f"Erro ao excluir: {e}"

    def obter_notificacoes(self):
        return self.op_notificacoes.ler_csv(self.op_notificacoes.arquivo) or []

    def enviar_notificacao(self, usuario, mensagem):
        linhas = self.obter_notificacoes()
        dt = datetime.date.today().strftime('%d/%m/%Y')
        linhas.append({"usuario": usuario, "mensagem": mensagem, "data": dt})
        self.op_notificacoes.escrever_csv(linhas, self.op_notificacoes.arquivo, ["usuario", "mensagem", "data"])
        return True, "Notificação enviada!"

    def excluir_notificacao(self, index):
        linhas = self.obter_notificacoes()
        try:
            linhas.pop(index)
            self.op_notificacoes.escrever_csv(linhas, self.op_notificacoes.arquivo, ["usuario", "mensagem", "data"])
            return True, "Notificação excluída!"
        except IndexError:
            return False, "Notificação não encontrada!"

    def autenticar(self, nome, senha, perfil_acesso):
        usuarios_csv = self.op_usuarios.ler_csv(self.op_usuarios.arquivo) or []
        for row in usuarios_csv:
            if row.get("nome", "").strip() == nome and row.get("senha", "").strip() == senha:
                tipo_csv = row.get("tipo", "Usuário").strip()
                
                if perfil_acesso == "Gerenciador" and tipo_csv in ["Gerenciador", "Admin"]:
                    u = Pessoa_admin(nome, senha)
                    u.tipo_csv = tipo_csv
                    return True, u, "Sucesso"
                elif perfil_acesso == "Usuário" and tipo_csv in ["Usuário", "Passageiro", "Motorista"]:
                    u = Passageiro(nome, senha)
                    u.tipo_csv = tipo_csv
                    return True, u, "Sucesso"
                else:
                    return False, None, f"Seu tipo no sistema é '{tipo_csv}'. Você não pode entrar como '{perfil_acesso}'."
        return False, None, "Nome de usuário ou senha incorretos."
