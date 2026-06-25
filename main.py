import abc
import datetime

class Veiculo(abc.ABC):
    def __init__(self,placa : str,capacidade : int,motorista : str,funcionando : bool,passageiros: int):
        self._placa=placa
        self.capacidade=capacidade
        self.mototorista=motorista
        self.funcionando=funcionando
        self.passageiros=passageiros

    def entrada_passageiros(self,numero : int):

        if self.passageiros >self.capacidade :
            return("Não deixe ninguem entrar")
        elif self.passageiros + numero > self.capacidade :
            superior = self.capacidade - self.passageiros + numero
            self.passageiros += numero
            return (f"Numero de passageiros superior em {superior} da capacidade maxima") 
        else:
            self.passageiros += numero 

    def saida_passageiros(self,numero :int):
        self.passageiros -= numero

    def começar_rota(self):
        pass



class FrotaVeiculos:

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
    def __init__(self, nome : str, senha : str):
        self.nome = nome
        self.__senha =senha

    def notificar_ocorrencia(self,conteudo) -> str:
        Gerenciador._ocorrencia.append(conteudo)
        

    def get_senha(self):
        return self.__senha
    
    def set_senha(self, nova_senha):
        self.__senha = nova_senha       

    def mudar_senha(self,nova_senha):
        self.set_senha(nova_senha)
        

class Motorista(Pessoa):
    def __init__(self, nome, senha, veiculos_dirigidos: list):
        super().__init__(nome, senha)
        
        self.veiculos_dirigidos = veiculos_dirigidos
    
class Passageiro(Pessoa):
    def __init__(self, nome, senha):
        super().__init__(nome, senha)

class Bicicleta:
    def __init__(self, numero : int, funcionamento : bool):
        self.numero = numero
        self.funcionamento = funcionamento
        
    def __str__(self)-> str :
        pass

    def usar(self):
        pass
    
    def emprestar(self, numero, quantidade, novo_numero):
        quantidade = int(input("Quantas bicicletas serão emprestadas?"))

        novo_numero = numero - quantidade

        return(f"{quantidade} bicicleta(s) foram emprestadas, restam {novo_numero}.")
    
    def devolver(self):
        pass
        

class Ponto_parada():
    def __init__(self, endereco:str, tipo_veiculo:str):
        self.endereco = endereco
        self.tipo_veiculo = tipo_veiculo

class Aviso():
    def __init__(self, conteudo:str):
        self.conteudo = conteudo

class Notificar():
    
    def mostrar_Aviso():
        return(f"{Gerenciador.nome} notifica, no dia {datetime.date.today()}, que {Aviso.conteudo}")

class Gerenciador():
    
    def __init__(self,usuarios: list ,frota_veiculos : FrotaVeiculos,nome):
        self.nome= nome
        self.__usuarios=usuarios
        self.frota_veiculos=frota_veiculos
        self._ocorrencias=[]

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
        
    def relatorio_geral(self):
        pass

    def consultar_usuario(self,nome):
        
        if nome in self.get_usuarios() :
            return True
        
        else:
            return False
    
    def get_usuarios(self):
        return self.__usuarios

    def set_usuario(self,lista_usuarios):
        self.__usuarios=lista_usuarios         