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

    #Verifica se já existe uma tarefa com o mesmo nome na lista
    if not any(tarefa["nome"] == nova_tarefa["nome"] for tarefa in tarefas[data]):
        #Adiciona a nova tarefa à lista correspondente à data
        tarefas[data].append(nova_tarefa)
        with open(arquivo_json,"w") as file:
            json.dump(tarefas,file,indent=4) #Salva com identação para melhor legibilidade
    else:
        print(f"A tarefa '{nova_tarefa["nome"]}' já existe para o dia {data}.")

#Função para calcular a porcentagem de tarefas concluídas
def calcular_porcentagem_sucesso(tarefas, data):
    if data in tarefas and len(tarefas[data]) > 0:
        total_tarefas = len(tarefas[data])
        concluidas = sum(1 for tarefa in tarefas[data] if tarefa["concluida"]) #Conta tarefas concluídas

        porcentagem = (concluidas/total_tarefas) * 100
        return total_tarefas, concluidas, porcentagem
    return 0, 0, 0 #Retorna zero caso não haja tarefas registradas

#Função para os inputs do usuário
def obter_inputs():
    data_atual = input("Digite a data (YYYY-MM-DD): ")
    numero_tarefas = int(input(f"Quantas tarefas você deseja adicionar para o dia {data_atual}?"))
    return data_atual, numero_tarefas

#Função para capturar as tarefas do usuário
def capturar_tarefas(numero_tarefas):
    lista_tarefas = []
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
        
        lista_tarefas.append({"nome": nome_tarefa, "concluida": concluida}) #Criando o dicionário da nova tarefa

    return lista_tarefas

#Função principal
def main():
    tarefas = ler_json()

    #Captura os inputs iniciais
    data_atual, numero_tarefas = obter_inputs()

    #Captura as tarefas do usuário
    novas_tarefas = capturar_tarefas(numero_tarefas)
    
    #Adiciona todas as tarefas à data correspondente
    for tarefa in novas_tarefas:
        salvar_json(tarefas, data_atual, tarefa)

    #Calcula a porcentagem
    total_tarefas, concluidas, porcentagem = calcular_porcentagem_sucesso(tarefas, data_atual)


    print(f"\n{numero_tarefas} tarefas adicionadas para o dia {data_atual};")
    print(f"Tarefas concluídas: {concluidas}/{total_tarefas} ({porcentagem:.2f}%)")
    '''print("Tarefas atuais:",json.dumps(tarefas,indent=4))'''


if __name__ == "__main__":
    main()