#main.py
import abc
import csv
from dados import OperadorArquivo
from veiculos import Onibus, Van, Micro_onibus, Bicicleta
from pessoas import Passageiro,Motorista,Pessoa_admin

class FrotaVeiculos:
    """
    Gerencia uma frota diversificada de veículos corporativos ou urbanos.
        Esta classe centraliza o controle de diferentes categorias de transporte 
    (ônibus, vans, micro-ônibus e bicicletas), permitindo monitorar a quantidade 
    total de itens cadastrados, visualizar os componentes da frota e gerenciar
    o fluxo específico de empréstimo e devolução de bicicletas.
    """

    def __init__(self, onibus : list, vans : list, micro_onibus : list, bicicleta: list):
        self.__onibus = onibus
        self.__vans = vans
        self.__micro_onibus = micro_onibus
        self.__bicicletas = bicicleta

    def mostrar_frota(self):
        print(f"{self.get_onibus()},  {self.get_vans()},  {self.get_micro_onibus()},  {self.get_bicicletas()}")
              
    def get_onibus(self):
        return self.__onibus

    def set_onibus(self, onibus):
        self.__onibus = onibus
        
    def get_vans(self):
        return self.__vans

    def set_vans(self, vans):
        self.__vans = vans

    def get_bicicletas(self):
        return self.__bicicletas
    
    def set_bicicletas(self, bicicletas):
        self.__bicicletas = bicicletas

    def get_micro_onibus(self):
        return self.__micro_onibus
    
    def set_micro_onibus(self, micro_onibus):
        self.__micro_onibus = micro_onibus

    def __str__(self) -> str:
        total_veiculos = len(self.__onibus) + len(self.__vans) + len(self.__micro_onibus) + len(self.__bicicletas)
        return f"FrotaVeiculos: {total_veiculos} veículos registrados."
    
    def emprestar_bicicleta(self, placa):

        operador = OperadorArquivo('bicicletas.csv')
        
        linhas = operador.ler_csv('bicicletas.csv')
        if linhas:
            bikes_atualizadas = [
                Bicicleta(l['numero'], l['funcionamento'] == 'True', l['disponivel'] == 'True') 
                for l in linhas 
            ]
            self.set_bicicletas(bikes_atualizadas)

        sucesso = False
        for bike in self.get_bicicletas():
            if str(bike._placa) == str(placa):
                if not bike.funcionando:
                    print(f"Erro: A bicicleta {placa} está em manutenção.")
                    return False
                if not bike.disponivel:
                    print(f"Erro: A bicicleta {placa} já está emprestada.")
                    return False
                
                bike.disponivel = False  
                sucesso = True
                print(f"Sucesso: Bicicleta {placa} emprestada!")
                break
        
        if not sucesso:
            print(f"Erro: Bicicleta {placa} não encontrada.")
            return False

        dados = [{'numero': b._placa, 'funcionamento': str(b.funcionamento), 'disponivel': str(b.disponivel)} for b in self.get_bicicletas()]
        operador.escrever_csv(dados, 'bicicletas.csv', ['numero', 'funcionamento', 'disponivel'])
        return True

        
    def devolver_bicicleta(self, placa):
        operador = OperadorArquivo('bicicletas.csv')
        
        linhas = operador.ler_csv('bicicletas.csv')
        if linhas:
            bicicletas_atualizadas = [
                Bicicleta(l['numero'], l['funcionamento'] == 'True', l['disponivel'] == 'True') 
                for l in linhas
            ]
            self.set_bicicletas(bicicletas_atualizadas)

        sucesso = False
        for bike in self.get_bicicletas():
            if str(bike._placa) == str(placa):
                if bike.disponivel:
                    print(f"Erro: A bicicleta {placa} já consta como disponível.")
                    return False
                
                bike.disponivel = True  
                sucesso = True
                print(f"Sucesso: Bicicleta {placa} devolvida com sucesso!")
                break
        
        if not sucesso:
            print(f"Erro: Bicicleta {placa} não pertence a esta frota.")
            return False

        dados = [{'numero': b._placa, 'funcionamento': str(b.funcionamento), 'disponivel': str(b.disponivel)} for b in self.get_bicicletas()]
        operador.escrever_csv(dados, 'bicicletas.csv', ['numero', 'funcionamento', 'disponivel'])
        return True

class Ponto_parada():
        """Classe responsavel por criar os locacis onde o onibus para com a informação do tipo de veiculo que passa na localidade"""
        def __init__(self, endereco:str, tipo_veiculo:str):
            self.endereco = endereco
            self.tipo_veiculo = tipo_veiculo


class Aviso():
        """Cria o conteudo-chave da notificação"""
        def __init__(self, conteudo:str):
            self.conteudo = conteudo


class Notificar():
        """Mostra aos usuario os avisos , cujo conteudo advem da classe Aviso"""
        @staticmethod
        def mostrar_aviso(Aviso, notificador):
                texto_aviso = f"{notificador.nome} notifica que : {Aviso.conteudo}"

                operador=OperadorArquivo("avisos.csv")
                dados_aviso = [{"autor": notificador.nome,"conteudo" : Aviso.conteudo     }]
                operador.escrever_csv(dados_aviso,"avisos.csv",fieldnames=["autor","conteudo"  ])

                return texto_aviso
                


class Gerenciador():
    """Classe principal do sistema, gerencia o frota veiculos , os usuarios do sistema, pontos de parada e as bicicletas"""
    
    def __init__(self,usuarios: list ,frota_veiculos : FrotaVeiculos,nome : str, pontos_parada : list):
        self.nome= nome
        self.__usuarios=usuarios
        self.frota_veiculos=frota_veiculos
        self.ocorrencias=[]
        self.pontos_parada=pontos_parada
        self.operador_usuarios = OperadorArquivo('usuarios.csv')
        dados_carregados = self.sincronizar_usuarios("carregar")

        if dados_carregados:
            self.__usuarios = dados_carregados
        else:
            self.__usuarios = usuarios
            if usuarios:  
                self.sincronizar_usuarios("salvar")

    def sincronizar_usuarios(self, acao="carregar"):
        if acao == "carregar":

            dados_csv = self.operador_usuarios.ler_csv(self.operador_usuarios.arquivo)
            if dados_csv:
                return [Passageiro(l['nome'], l['senha']) for l in dados_csv]
            return []
                
        elif acao == "salvar":
            dados = [{'nome': u.nome, 'senha': u.get_senha()} for u in self.get_usuarios()]
            self.operador_usuarios.escrever_csv(dados, self.operador_usuarios.arquivo, fieldnames=['nome', 'senha'])

    def criar_aviso(self,conteudo):
        
       aviso=Aviso(conteudo)
       return Notificar.mostrar_aviso(aviso, self)
        
        

    def mudar_ponto_parada(self,endereco,tipo_veiculo,velho_ponto):
        velho_ponto.endereco=endereco
        velho_ponto.tipo_veiculo=tipo_veiculo
        
    def mudar_motorista(self,novos_veiculos,motorista):
        motorista.veiculos_dirigidos= novos_veiculos
        
        
    def cadastrar_usuario(self,novo_usuario):
        lista_atual = self.get_usuarios()
        lista_atual.append(novo_usuario)
        self.set_usuario(lista_atual)
        return "Usuário cadastrado com sucesso"
        

    def consultar_usuario(self,nome):
        for usuario in self.get_usuarios():
            if usuario.nome == nome:
                return True
        return False
             
    def get_usuarios(self):
        return self.__usuarios

    def set_usuario(self,lista_usuarios):
        if isinstance(lista_usuarios, list):
            self.__usuarios = lista_usuarios
            self.sincronizar_usuarios("salvar")
            return "lista atualizada"
        else:
            return "tipo de usuarios errado, digite outro"  


class Login():
    """Verifica se um usuario possui o cadastro no sistema, permitindo que ele o acesse, ou cadastra-o"""

    def __init__(self,nome,senha, gerenciador_instancia):
        self.nome=nome
        self.__senha=senha
        self.gerenciador = gerenciador_instancia

    def criar_conta(self)-> str:

        passageiro = Passageiro(self.nome, self.get_senha())
        self.gerenciador.cadastrar_usuario(passageiro)

        return "Conta criada com sucesso!"
        

    def entrar(self):
        if not self.gerenciador.consultar_usuario(self.nome):
            return "Usuário não encontrado."
        


        for usuario in self.gerenciador.get_usuarios():
            if usuario.nome == self.nome and usuario.get_senha() == self.get_senha():

                return "Login bem sucedido."

        return "Senha incorreta."
        

    def get_senha(self):
        return self.__senha

    def set_senha(self, senha):
        if isinstance(senha, str):
            self.__senha = senha