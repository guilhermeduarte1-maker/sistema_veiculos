import abc
import datetime

class Veiculo(abc.ABC):
    """
    Representa um veículo genérico dentro do sistema de transporte escolar.
        Essa classe serve como base para os outros tipos de veículo, 
    tendo caractéristicas como: a placa, a capacidade máxima de passageiros,
    o motorista que vai dirigir ele, o estado que o ônibus se encontra(funcionando ou não)
    e a quantidade de passageiros presentes.
        Além disso, tem os metodos da entrada de passageiros, da saída deles e começar a rota.
    """
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

    def comecar_rota(self):
        pass



class FrotaVeiculos:
    """
    Gerencia uma frota diversificada de veículos corporativos ou urbanos.
        Esta classe centraliza o controle de diferentes categorias de transporte 
    (ônibus, vans, micro-ônibus e bicicletas), permitindo monitorar a quantidade 
    total de itens cadastrados, visualizar os componentes da frota e gerenciar 
    o fluxo específico de empréstimo e devolução de bicicletas.
    """

    def __init__(self, onibus : list, vans : list, micro_onibus : list, bicicleta: list):
        self._onibus = onibus
        self._vans = vans
        self._micro_onibus = micro_onibus
        self._bicicletas = bicicleta

    def mostrar_frota(self):
        print(f"{self.get_onibus()},  {self.get_vans()},  {self.get_micro_onibus()},  {self.get_bicicletas()}")
              
    def get_onibus(self):
        return self._onibus

    def set_onibus(self, onibus):
        self._onibus = onibus
        
    def get_vans(self):
        return self._vans

    def set_vans(self, vans):
        self._vans = vans

    def get_bicicletas(self):
        return self._bicicletas
    
    def set_bicicletas(self, bicicletas):
        self._bicicletas = bicicletas

    def get_micro_onibus(self):
        return self._micro_onibus
    
    def set_micro_onibus(self, micro_onibus):
        self._micro_onibus = micro_onibus

    def __str__(self) -> str:
        total_veiculos = len(self._onibus) + len(self._vans) + len(self._micro_onibus) + len(self._bicicletas)
        return f"FrotaVeiculos: {total_veiculos} veículos registrados."
    
    def emprestar_bicicleta(self):

        pass

    def devolver_bicicleta(self):
        pass

    def modificar_onibus_por_indice(self, indice: int, novo_onibus: Onibus):
        """ Altera um ônibus específico pelo índice e atualiza apenas o CSV de ônibus """
        if 0 <= indice < len(self._onibus):
            self._onibus[indice] = novo_onibus
            self.salvar_onibus()
        else:
            print("Erro: Índice de ônibus inválido.")

    def modificar_van_por_indice(self, indice: int, nova_van: Van):
        """ Altera uma van específica pelo índice e atualiza apenas o CSV de vans """
        if 0 <= indice < len(self._vans):
            self._vans[indice] = nova_van
            self.salvar_vans()
        else:
            print("Erro: Índice de van inválido.")

    def modificar_micro_onibus_por_indice(self, indice: int, novo_micro: Micro_onibus):
        """ Altera um micro-ônibus específico pelo índice e atualiza apenas o CSV de micro-ônibus """
        if 0 <= indice < len(self._micro_onibus):
            self._micro_onibus[indice] = novo_micro
            self.salvar_micro_onibus()
        else:
            print("Erro: Índice de micro-ônibus inválido.")

    def modificar_bicicleta_por_indice(self, indice: int, nova_bike: Bicicleta):
        """ Altera uma bicicleta específica pelo índice e atualiza apenas o CSV de bicicletas """
        if 0 <= indice < len(self._bicicletas):
            self._bicicletas[indice] = nova_bike
            self.salvar_bicicletas()
        else:
            print("Erro: Índice de bicicleta inválido.")


    def salvar_onibus(self):
        dados = [{'placa': o._placa, 'capacidade': o.capacidade, 'motorista': o.motorista, 'funcionando': str(o.funcionando), 'rota': o.rota, 'passageiros': o.passageiros} for o in self._onibus]
        self.escrever_csv(dados, 'onibus.csv', ['placa', 'capacidade', 'motorista', 'funcionando', 'rota', 'passageiros'])

    def salvar_vans(self):
        dados = [{'placa': v._placa, 'capacidade': v.capacidade, 'motorista': v.motorista, 'funcionando': str(v.funcionando), 'rota': v.rota, 'passageiros': v.passageiros} for v in self._vans]
        self.escrever_csv(dados, 'vans.csv', ['placa', 'capacidade', 'motorista', 'funcionando', 'rota', 'passageiros'])

    def salvar_micro_onibus(self):
        dados = [{'placa': m._placa, 'capacidade': m.capacidade, 'motorista': m.motorista, 'funcionando': str(m.funcionando), 'rota': m.rota, 'passageiros': m.passageiros} for m in self._micro_onibus]
        self.escrever_csv(dados, 'micro_onibus.csv', ['placa', 'capacidade', 'motorista', 'funcionando', 'rota', 'passageiros'])

    def salvar_bicicletas(self):
        dados = [{'numero': b.numero, 'funcionando': str(b.funcionando)} for b in self._bicicletas]
        self.escrever_csv(dados, 'bicicletas.csv', ['numero', 'funcionando'])

    def carregar_toda_frota(self):
        # Carrega Ônibus
        self._onibus = [Onibus(l['placa'], int(l['capacidade']), l['motorista'], l['funcionando'] == 'True', l['rota'], int(l['passageiros'])) for l in self.ler_csv('onibus.csv')]
        # Carrega Vans
        self._vans = [Van(l['placa'], int(l['capacidade']), l['motorista'], l['funcionando'] == 'True', l['rota'], int(l['passageiros'])) for l in self.ler_csv('vans.csv')]
        # Carrega Micro-ônibus
        self._micro_onibus = [Micro_onibus(l['placa'], int(l['capacidade']), l['motorista'], l['funcionando'] == 'True', l['rota'], int(l['passageiros'])) for l in self.ler_csv('micro_onibus.csv')]
        # Carrega Bicicletas
        self._bicicletas = [Bicicleta(int(l['numero']), l['funcionando'] == 'True') for l in self.ler_csv('bicicletas.csv')]

class Onibus(Veiculo):
    """
    Simplesmente herda as caractéristicas da classe veículo.
    """
    def __init__(self, placa, capacidade, motorista, funcionando, rota,passageiros):
        super().__init__(placa, capacidade, motorista, funcionando,passageiros)
        
        self.rota = rota

class Van(Veiculo):
    """
    Herda as caractéristicas da classe veículo, mas recebe de forma diferente 
    o método de receber passageiros(tem uma capacidade menor do que o ônibus)
    """
    def __init__(self, placa, capacidade, motorista, funcionando, rota,passageiros):
        super().__init__(placa, capacidade, motorista, funcionando,passageiros)
        
        self.rota = rota
            
class Micro_onibus(Onibus):
    """
    Herda as caractéristicas da classe veículo, mas recebe de forma diferente 
    o método de receber passageiros(tem uma capacidade menor do que o ônibus)
    """
    def __init__(self, placa, capacidade, motorista, funcionando, rota,passageiros):
        super().__init__(placa, capacidade, motorista, funcionando, rota,passageiros)
        

class Pessoa:
    """
    Representa uma pessoa genérica dentro do sistema de trasponte escolar. 
        Essa classe serve como base para identificação de usuários, armazenando informações
    essenciais como nome e credenciais de acesso (senha).
        Além disso, permite que o indivíduo interaja com o sistema enviando notificações e
    relatórios de ocorrência diretamente ao gerenciador, bem como realizar a manutenção e
    atualização de seus dados de segurança
    """
    def __init__(self, nome : str, senha : str):
        self.nome = nome
        self.__senha = senha

    def notificar_ocorrencia(self,conteudo) -> str:
        Gerenciador._ocorrencias.append(conteudo)
        

    def get_senha(self):
        return self.__senha
    
    def set_senha(self, nova_senha):
        if nova_senha == str:
            self.__senha = nova_senha 
            return "senha alterada com sucesso"
        
        else:
            return "tipo de senha errado, digite outro"

    def mudar_senha(self,nova_senha):
        self.set_senha(nova_senha)
        

class Motorista(Pessoa):
    """
    Representa um motorista, herda todas as caractéristicas da classe pessoa, 
    mas com a peculiaridade da lista de veículos que ele pode dirigir.
    """
    def __init__(self, nome, senha, veiculos_dirigidos: list):
        super().__init__(nome, senha)
        
        self.veiculos_dirigidos = veiculos_dirigidos
    
class Passageiro(Pessoa):
    """
    Simplesmente herda todas as caractéristicas e métodos da classe pessoa.
    """
    def __init__(self, nome, senha):
        super().__init__(nome, senha)

class Bicicleta:
    """
    Representa uma bicicleta dentro do sistema de transporte escolar.
    """
    def __init__(self, numero : int, funcionamento : bool):
        self.numero = numero
        self.funcionamento = funcionamento
        
    def __str__(self)-> str :
        pass

    def comecar_rota(self):
        pass
    

class Ponto_parada():
    """
    Representa um ponto de parada dentro do sistema de transporte escolar.
    """
    def __init__(self, endereco:str, tipo_veiculo:str):
        self.endereco = endereco
        self.tipo_veiculo = tipo_veiculo

class Aviso():
    """
    Representa um aviso dentro do sistema de transporte escolar.
    """
    def __init__(self, conteudo:str):
        self.conteudo = conteudo

class Notificar():
    """
    Classe responsável por notificar os usuários do sistema sobre avisos e ocorrências.
    """
    
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

    def criar_aviso(self,conteudo):
       aviso=Aviso(conteudo)
       Notificar.mostrar_aviso(aviso)
        
        

    def mudar_ponto_parada(self,endereco,tipo_veiculo,velho_ponto):
        velho_ponto.endereco=endereco
        velho_ponto.tipo_veiculo=tipo_veiculo
        
    def mudar_motorista(self,novos_veiculos,motorista):
        motorista.veiculos_dirigidos= novos_veiculos
        
        
    def cadastrar_usuario(self,novo_usuario):
        lista_usuarios= self.get_usuarios()
        lista_usuarios.append(novo_usuario)
        self.set_usuario(lista_usuarios)
        

    def consultar_usuario(self,nome):
        
        usuarios=self.get_usuarios()
        v=0
        for n in range(len(usuarios)):
            if nome == usuarios[n] :
                return True
                v+=1
        if v==0 :
            return False
             
    def get_usuarios(self):
        return self.__usuarios

    def set_usuario(self,lista_usuarios):
        if lista_usuarios == list:
            self.__usuarios = lista_usuarios
            return "lista atualizada"

        else:
            return "tipo de usuarios errado, digite outro"    


    def salvar_usuarios(self):
        dados = []
        for u in self.__usuarios:
            tipo = 'Motorista' if isinstance(u, Motorista) else 'Passageiro'
            veiculos = ";".join(u.veiculos_dirigidos) if isinstance(u, Motorista) else ""
            dados.append({'nome': u.nome, 'senha': u.get_senha(), 'tipo': tipo, 'veiculos_dirigidos': veiculos})
        self.escrever_csv(dados, 'usuarios.csv', ['nome', 'senha', 'tipo', 'veiculos_dirigidos'])

    def salvar_pontos_parada(self):
        dados = [{'endereco': p.endereco, 'tipo_veiculo': p.tipo_veiculo} for p in self.pontos_parada]
        self.escrever_csv(dados, 'pontos_parada.csv', ['endereco', 'tipo_veiculo'])

    def salvar_ocorrencias(self):
        dados = [{'conteudo': o} for o in Gerenciador._ocorrencias]
        self.escrever_csv(dados, 'ocorrencias.csv', ['conteudo'])

    def carregar_dados_gerenciador(self):
        # Carrega Usuários descobrindo se era Motorista ou Passageiro
        self.__usuarios = []
        for l in self.ler_csv('usuarios.csv'):
            if l['tipo'] == 'Motorista':
                veiculos = l['veiculos_dirigidos'].split(';') if l['veiculos_dirigidos'] else []
                self.__usuarios.append(Motorista(l['nome'], l['senha'], veiculos))
            else:
                self.__usuarios.append(Passageiro(l['nome'], l['senha']))
        
        # Carrega Pontos de Parada
        self.pontos_parada = [Ponto_parada(l['endereco'], l['tipo_veiculo']) for l in self.ler_csv('pontos_parada.csv')]
        
        # Carrega Ocorrências globais
        Gerenciador._ocorrencias = [l['conteudo'] for l in self.ler_csv('ocorrencias.csv')]    

    class Login():
        """Verifica se um usuario possui o cadastro no sistema, permitindo que ele o acesse, ou cadastra-o"""
        def __init__(self,nome,senha):
            self.nome=nome
            self.__senha=senha

        def criar_conta(self)-> list:
            passageiro=Passageiro(self.nome,self.__senha)
            Gerenciador.cadastrar_usuario(passageiro)
            

        def entrar(self):
            for i in range(len(Gerenciador.usuarios)):
                if self.nome[i] ==  Gerenciador.get_usuarios[i].nome and self.get_senha() == Gerenciador.get_usuarios[i].get_senha():

                    return True
                
                else: 
                    return False
            

        def get_senha(self):
            return self.__senha

        def set_senha(self,senha):
            if senha == str:
                self.__senha= senha


