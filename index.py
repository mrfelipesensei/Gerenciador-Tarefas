#Importando bibliotecas
import json
import os

#Definindo arquivo JSON
arquivo_json = "tarefas.json"

#Função para ler o JSON
def ler_json():
    if os.path.exists(arquivo_json):
        with open(arquivo_json,"r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                print("Erro ao decodificar o arquivo JSON.")
                return {}
    return {}

#Função para salvar tarefas no arquivo JSON
def salvar_json(tarefas,data,nova_tarefa):
    #Verifica se a data já existe no dicionário, caso contrário, cria uma lista vazia para essa data
    if data not in tarefas:
        tarefas[data] = []
    
    #Adiciona a nova tarefa à lista correspondente à data
    tarefas[data].append(nova_tarefa)


    with open(arquivo_json,"w") as file:
        json.dump(tarefas,file,indent=4) #Salva com identação para melhor legibilidade

#Exemplo de uso
tarefas = ler_json()
data_atual = "2025-03-22"
nova_tarefa = {"nome":"Reunião","concluida":False}
#Salva a nova tarefa no arquivo
salvar_json(tarefas,data_atual,nova_tarefa)
#Exibe o conteúdo atual das tarefas
print(tarefas)
