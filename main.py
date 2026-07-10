import abc
import datetime
import csv
from dados import OperadorArquivo

class Veiculo(abc.ABC):
    """Classe abstrata base para todos os veiculos gerenciados"""
    def __init__(self,placa : str,capacidade : int,motorista : str,funcionando : bool,passageiros: int):
        self._placa=placa
        self.capacidade=capacidade
        self.motorista=motorista
        self.funcionando=funcionando
        self.passageiros=passageiros

    def entrada_passageiros(self,numero : int):

        if self.passageiros  > self.capacidade :
            return("Onibus lotado")
        elif self.passageiros + numero > self.capacidade :
            superior = self.capacidade - self.passageiros + numero
            self.passageiros += numero
            return (f"Numero de passageiros superior em {superior} da capacidade maxima") 
        else:
            self.passageiros += numero 

    def saida_passageiros(self,numero :int):
        self.passageiros -= numero
        lugares_vagos=self.capacidade- self.passageiros
        print(f"O onibus tem agora {lugares_vagos} lugares vagos")




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

        # Salva utilizando o atributo correto da bicicleta (_placa) para a coluna 'numero'
        dados = [
            {'numero': b._placa, 'funcionamento': b.funcionamento, 'disponivel': b.disponivel} 
            for b in self.get_bicicletas()
        ]
        operador.escrever_csv(dados, 'bicicletas.csv', ['numero', 'funcionamento', 'disponivel'])
        return True

        
    def devolver_bicicleta(self, placa):
        """Lê o CSV, valida, devolve a bicicleta e salva no CSV"""
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
            # Busca baseada no atributo herdado _placa
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

        dados = [
            {'numero': b._placa, 'funcionamento': b.funcionamento, 'disponivel': b.disponivel} 
            for b in self.get_bicicletas()
        ]
        operador.escrever_csv(dados, 'bicicletas.csv', ['numero', 'funcionamento', 'disponivel'])
        return True


class Onibus(Veiculo):
    def __init__(self, placa, capacidade, motorista, funcionando, rota,passageiros):
        super().__init__(placa, capacidade, motorista, funcionando,passageiros)
        
        self.rota = rota

class Van(Veiculo):
    def __init__(self, placa, capacidade, motorista, funcionando, rota,passageiros):
        super().__init__(placa, capacidade, motorista, funcionando,passageiros)
        
        self.rota = rota
            
class Micro_onibus(Onibus):
    def __init__(self, placa, capacidade, motorista, funcionando, rota,passageiros):
        super().__init__(placa, capacidade, motorista, funcionando, rota,passageiros)
        

class Pessoa:
    """
    Representa uma pessoa genérica dentro do sistema de transporte.
        Esta classe serve como base para a identificação de usuários, armazenando
    informações essenciais como nome e credenciais de acesso (senha). Além disso,
    permite que o indivíduo interaja com o sistema enviando notificações e relatórios
    de ocorrências diretamente ao gerenciador, bem como realize a manutenção e
    atualização de seus dados de segurança.
    """
    def __init__(self, nome : str, senha : str):
        self.nome = nome
        self.__senha = senha

    def notificar_ocorrencia(self,conteudo) -> str:
        Gerenciador._ocorrencias.append(conteudo)
        

    def get_senha(self):
        return self.__senha
    
    def set_senha(self, nova_senha):
        if isinstance(nova_senha, str):
            self.__senha = nova_senha 
            return "senha alterada com sucesso"
        
        else:
            return "tipo de senha errado, digite outro"

    def mudar_senha(self,nova_senha):
        resultado = self.set_senha(nova_senha)
        if "errado" in resultado:
            return resultado  
        operador = OperadorArquivo('usuarios.csv')
        linhas = operador.ler_csv('usuarios.csv')
        
        if linhas:
            dados_atualizados = []
            for l in linhas:
                if l['nome'] == self.nome:
                    l['senha'] = self.get_senha()
                dados_atualizados.append(l)
                
            operador.escrever_csv(dados_atualizados, 'usuarios.csv', ['nome', 'senha'])
            return "Senha alterada e sincronizada no CSV com sucesso!"
        
        return "Erro: Arquivo de usuários não encontrado para atualização."

            
        

class Motorista(Pessoa):
    """
    Representa um funcionário habilitado a conduzir os veículos da frota.
        Como uma extensão de classe pessoa, esta classe adiciona a responsabilidade
        de operação do sistema de transportes, mantendo  um registro atualizado de quais 
        veículos específicos (como ônibus, vans ou micro-ônibus) estão sob a sua
        condução ou autorizados para a sua escala de trabalho.
    """
    def __init__(self, nome, senha, veiculos_dirigidos: list):
        super().__init__(nome, senha)
        
        self.veiculos_dirigidos = veiculos_dirigidos
    
class Passageiro(Pessoa):
    """
    Representa o usuário final dos serviços de transportes oferecios pela frota.
        Herdando as características básicas de identificação e autenticação da classe Pessoa,
        esta classe individualiza o papel do cidadão ou colaborador que utiliza os 
        veículos para deslocamento urbano ou corporativo, permitindo sua integração com os 
        módulos de rotas, embarques e controle de capacidade.
    """
    def __init__(self, nome, senha):
        super().__init__(nome, senha)

class Bicicleta(Veiculo):
    """
    Representa uma unidade de bicicleta disponível para compartilhamento na frota.
        Esta controla os dados individuas de identificação de cada ciclomotor, 
        rastreando seu número de registro e seu estado atual de funcionamento (manutenção).
        Ela atua diretamente integração com o gerenciador para viabilizar as rotas alternativas 
        e o fluxo de empréstimos rápidos e devoluções pelos usuários do sistema.
    """
    def __init__(self, placa, capacidade, motorista, funcionando, rota,passageiros,em_uso):
        super().__init__(placa, capacidade, motorista, funcionando,passageiros)
        
        self.em_uso = em_uso
        
    def __str__(self)-> str:
        return str(self.numero)

    

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
    def mostrar_Aviso():
        return(f"{Gerenciador.nome} notifica, no dia {datetime.date.today()}, que {Aviso.conteudo}")

class Gerenciador():
    """Classe principal do sistema, gerencia o frota veiculos , os usuarios do sistema, pontos de parada e as bicicletas"""
    
    def __init__(self,usuarios: list ,frota_veiculos : FrotaVeiculos,nome : str, pontos_parada : list):
        self.nome= nome
        self.__usuarios=usuarios
        self.frota_veiculos=frota_veiculos
        self._ocorrencias=[]
        self.pontos_parada=pontos_parada
        self.operador_usuarios = OperadorArquivo('usuarios.csv')
        dados_carregados = self.sincronizar_usuarios("carregar")

        if dados_carregados:
            self.__usuarios = dados_carregados
        else:
            self.__usuarios = usuarios
            if usuarios:  # Se a lista inicial não for vazia, já persiste no arquivo
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
       Notificar.mostrar_Aviso(aviso)
        
        

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

        def criar_conta(self)-> list:
            passageiro = Passageiro(self.nome, self.__senha)
            self.gerenciador.cadastrar_usuario(passageiro)
            print(f"Conta criada com sucesso para {self.nome}!")
            

        def entrar(self):
            for usuario in self.gerenciador.get_usuarios():
                if usuario.nome == self.nome and usuario.get_senha() == self.__senha:
                    print(f"Login bem-sucedido! Bem-vindo {self.nome}.")
                    return True
            print("Erro: Usuário ou senha incorretos.")
            return False
            

        def get_senha(self):
            return self.__senha

        def set_senha(self, senha):
            if isinstance(senha, str):
                self.__senha = senha

