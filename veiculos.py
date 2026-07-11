# veiculos.py
import abc


class Veiculo(abc.ABC):
    """Classe abstrata base para todos os veiculos gerenciados"""
    def __init__(self,placa : str,capacidade : int,motorista : str,funcionando : bool,passageiros: int):
        self._placa=placa
        self.capacidade=capacidade
        self.motorista=motorista
        self.funcionando=funcionando
        self.passageiros=passageiros

    def entrada_passageiros(self, numero: int):
        nome_veiculo = self.__class__.__name__ # Deixa o nome dinâmico (Onibus, Van, etc.)

        if numero <= 0:
            return "Quantidade de passageiros inexistente"
            
        elif self.passageiros >= self.capacidade:
            return f"{nome_veiculo} lotado"
            
        elif self.passageiros + numero > self.capacidade:
            # Correção do cálculo para mostrar quanto ultrapassou de forma limpa
            vagas_restantes = self.capacidade - self.passageiros
            superior = numero - vagas_restantes
            return f"Numero de passageiros superior em {superior} da capacidade maxima"
            
        else:
            # Caminho de sucesso: adiciona e mostra os lugares vagos que restaram
            self.passageiros += numero
            lugares_vagos = self.capacidade - self.passageiros
            return f"Passageiros alocados. O {nome_veiculo} tem agora {lugares_vagos} lugares vagos"

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
