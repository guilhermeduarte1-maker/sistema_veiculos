# veiculos.py
import abc


class Veiculo(abc.ABC):
    """
    Classe abstrata base para todos os veiculos gerenciados pelo sistema.
        Esta classe define os atributos e métodos comuns a todos os tipos de veículos. 
        Ela serve como um modelo para garantir que todos os veículos compartilhem uma interface.
    """
    def __init__(self,placa : str,capacidade : int,motorista : str,funcionando : bool,passageiros: int):
        self._placa=placa
        self.capacidade=capacidade
        self.motorista=motorista
        self.funcionando=funcionando
        self.passageiros=passageiros

class Onibus(Veiculo):
    """
    Representa um ônibus na frota de veículos.
        Esta classe herda de Veiculo e adiciona o atributo rota, que indica a rota específica que o ônibus percorre.
    """
    def __init__(self, placa, capacidade, motorista, funcionando, rota,passageiros):
        super().__init__(placa, capacidade, motorista, funcionando,passageiros)
        
        self.rota = rota

class Van(Veiculo):
    """
    Representa uma van na frota de veículos.
        Esta classe herda de Veiculo e adiciona o atributo rota, que indica a rota específica que a van percorre.
    """
    def __init__(self, placa, capacidade, motorista, funcionando, rota,passageiros):
        super().__init__(placa, capacidade, motorista, funcionando,passageiros)
        
        self.rota = rota
            
class Micro_onibus(Onibus):
    """
    Representa um micro-ônibus na frota de veículos.
        Esta classe herda de Onibus e mantém o mesmo atributo rota, permitindo a diferenciação entre micro-ônibus 
        e ônibus regulares, enquanto compartilha a mesma estrutura de dados.
    """
    def __init__(self, placa, capacidade, motorista, funcionando, rota,passageiros):
        super().__init__(placa, capacidade, motorista, funcionando, rota,passageiros)

        self.rota = rota
        

class Bicicleta(Veiculo):
    """
    Representa uma unidade de bicicleta disponível para compartilhamento na frota.
        Esta controla os dados individuas de identificação de cada ciclomotor, 
        rastreando seu número de registro e seu estado atual de funcionamento (manutenção).
        Ela atua diretamente integração com o gerenciador para viabilizar as rotas alternativas 
        e o fluxo de empréstimos rápidos e devoluções pelos usuários do sistema.
    """
    def __init__(self, placa, funcionando=True, disponivel=True):
        # Passa os dados para o construtor do Veiculo
        super().__init__(placa=placa, capacidade=1, motorista="", funcionando=funcionando, passageiros=0)        
        self.__disponivel = disponivel 

    
    @property
    def disponivel(self):
        return self.__disponivel

    @disponivel.setter
    def disponivel(self, valor):
        self.__disponivel = valor
        
    def __str__(self) -> str:
        return str(self._placa)
