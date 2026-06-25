
import csv

class LeitorCsvMixing():
    def ler_csv(arquivo):
        '''
        Lê um arquivo CSV e retorna os dados como uma lista de dicionários.
        '''
        dados = []
        try:
            with open(arquivo, mode='r', newline='', encoding='utf-8') as file:
                leitor = csv.DictReader(file)
                for linha in leitor:
                    dados.append(linha)
        except FileNotFoundError:
            # se não for possivel retorne o print
            print(' Dado não encontrado.')
            pass
        return dados
class EscritorCsvMixing():

    def escrever_csv(dados, arquivo, fieldnames):
        '''
        Escreve uma lista de dicionários em um arquivo CSV.
        '''
        with open(arquivo, mode='w', newline='', encoding='utf-8') as file:
            escritor = csv.DictWriter(file, fieldnames=fieldnames)
            escritor.writeheader()
            escritor.writerows(dados)

class OperadorArquivo(LeitorCsvMixing,EscritorCsvMixing):
    def __init__(self,arquivo):
        self.arquivo=arquivo
