# pessoas.py
from dados import OperadorArquivo

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
        self.ocorrencias_gerais = []

    def notificar_ocorrencia(self,conteudo) -> None:
        self.ocorrencias_gerais.append(conteudo)
        

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

        dados_atualizados = []
        usuario_encontrado = False
        
        if linhas:
            for l in linhas:
                if l['nome'] == self.nome:
                    l['senha'] = self.get_senha()
                    usuario_encontrado = True
                dados_atualizados.append(l)

        # Se o usuário não existia no CSV por algum motivo, nós o adicionamos agora
        if not usuario_encontrado:
            dados_atualizados.append({'nome': self.nome, 'senha': self.get_senha()})
                
        operador.escrever_csv(dados_atualizados, 'usuarios.csv', ['nome', 'senha'])
        return "Senha alterada e sincronizada no CSV com sucesso!"
        


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

        
class Pessoa_admin(Pessoa):

    """
    Representa um funcionário habilitado a utilizar o administrador.
        Como uma extensão de classe pessoa, esta classe adiciona a responsabilidade
        de operação do sistema geral, onde o mesmo pode cumprir as funcionalidades dos metodos da classe Gerenciador.
    """
    def __init__(self, nome, senha):
        super().__init__(nome, senha)
