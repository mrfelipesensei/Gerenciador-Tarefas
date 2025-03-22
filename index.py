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

'''#Exemplo de uso
tarefas = ler_json()
data_atual = "2025-03-22"
nova_tarefa = {"nome":"Reunião","concluida":False}
#Salva a nova tarefa no arquivo
salvar_json(tarefas,data_atual,nova_tarefa)
#Exibe o conteúdo atual das tarefas
print(tarefas)'''

#Função principal
def main():
    tarefas = ler_json()

    #Inserção de data pelo usuário
    data_atual = input("Digite a data (YYY-MM-DD): ")
    
    #Define o número de tarefas a serem adicionadas
    numero_tarefas = int(input(f"Quantas tarefas você deseja adicionar para o dia {data_atual}?"))

    #Loop para adicionar múltiplas tarefas
    for i in range(numero_tarefas):
        print(f"\nTarefa {i+1}/{numero_tarefas}: ")
        nome_tarefa = input("Digite o nome da tarefa: ")

        while True:
            concluida_input = input("A tarefa está concluída? ").strip().lower()

        #Conversão "Sim" para True e "Não" para False
            if concluida_input == "sim":
                concluida = True
                break
            elif concluida_input == "não":
                concluida = False
                break
            else:
                print("Entrada inválida. Responda com 'Sim' ou 'Não'.")
        

    nova_tarefa = {"nome": nome_tarefa, "concluida": concluida} #Criando o dicionário da nova tarefa

    salvar_json(tarefas,data_atual,nova_tarefa)

    print(f"\n{numero_tarefas} tarefas adicionadas para o dia {data_atual};")
    print("Tarefas atuais:",json.dumps(tarefas,indent=4))


if __name__ == "__main__":
    main()