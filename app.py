#Importando bibliotecas
import json
import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

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
def salvar_json(tarefas,data):
    with open(arquivo_json,"w") as file:
        json.dump(tarefas,file,indent=4)


#Função para calcular a porcentagem de tarefas concluídas
def calcular_porcentagem_sucesso(tarefas, data):
    if data in tarefas and len(tarefas[data]) > 0:
        total_tarefas = len(tarefas[data])
        concluidas = sum(1 for tarefa in tarefas[data] if tarefa["concluida"]) #Conta tarefas concluídas

        porcentagem = (concluidas/total_tarefas) * 100
        return total_tarefas, concluidas, porcentagem
    return 0, 0, 0 #Retorna zero caso não haja tarefas registradas

'''#Função para os inputs do usuário
def obter_inputs():
    data_atual = input("Digite a data (YYYY-MM-DD): ")
    numero_tarefas = int(input(f"Quantas tarefas você deseja adicionar para o dia {data_atual}?"))
    return data_atual, numero_tarefas

#Função para capturar as tarefas do usuário
def capturar_tarefas(numero_tarefas,data,tarefas):
    
    #Loop para adicionar múltiplas tarefas
    for i in range(numero_tarefas):
        print(f"\nTarefa {i+1}/{numero_tarefas}: ")
        nome_tarefa = input("Digite o nome da tarefa: ")

        nova_tarefa = {"nome": nome_tarefa}

        salvar_json(tarefas,data,nova_tarefa)

#Função Buscar tarefas por data
def  buscar_tarefas_por_data(tarefas, data_busca):
    if data_busca in tarefas:
        return tarefas[data_busca]
    else:
        return []

#Função para exibir tarefas por data
def exibir_por_data(tarefas):
    data_busca = input("\nDigite a data para buscar tarefas (YYYY-MM-DD): ")
    tarefas_encontradas = buscar_tarefas_por_data(tarefas,data_busca)

    if tarefas_encontradas:
        print(f"\nTarefas encontradas para {data_busca}:")
        for tarefa in tarefas_encontradas:
            print(f"-{tarefa['nome']} (Concluída: {'Sim' if tarefa['concluida'] else 'Não'})")

        #Calcula e exibe a porcetagem de tarefas concluídas
        total_tarefas, concluidas, porcentagem = calcular_porcentagem_sucesso(tarefas,data_busca)
        print(f"Tarefas concluídas: {concluidas}/{total_tarefas} ({porcentagem:.2f}%)")
    else:
        print(f"\nNenhuma tarefa encontrada para {data_busca}.")


#Função para registrar tarefas
def registrar_tarefa(tarefas):
    #Captura os inputs iniciais
    data_atual, numero_tarefas = obter_inputs()
    #Captura as tarefas do usuário
    capturar_tarefas(numero_tarefas, data_atual, tarefas)
    #Calcula a porcentagem
    total_tarefas, concluidas, porcentagem = calcular_porcentagem_sucesso(tarefas, data_atual)
    print(f"\n{numero_tarefas} tarefas adicionadas para o dia {data_atual};")
    print(f"Tarefas concluídas: {concluidas}/{total_tarefas} ({porcentagem:.2f}%)")

#Função principal
def main():
    tarefas = ler_json()

    while True:
        print("\n--Gerenciador de Tarefas--")
        print("1. Buscar tarefas por data")
        print("2. Registrar tarefas")
        print("3. Sair")

        opcao = int(input("Digite o número da opção desejada: "))
    
    
        if opcao == 1:
            exibir_por_data(tarefas)
        elif opcao == 2:
            registrar_tarefa(tarefas)
        elif opcao == 3:
            break
        else:
            print("Opção inválida. Tente novamente.")
'''    

@app.route("/",methods=["GET","POST"])
def index():
    tarefas = ler_json()
    if request.method == "POST":
        data = request.form["dtata"]
        nome_tarefa = request.form["nome_tarefa"]
        concluida = request.form.get("concluida") == "on"

        if data not in tarefas:
            tarefas[data] = []

        tarefa_existente = next((t for t in tarefas[data] if t['nome'] == nome_tarefa),None)
        if tarefa_existente:
            return "Tarefa já existe para este dia."
    
        nova_tarefa = {'nome':nome_tarefa,"concluida":concluida}
        tarefas[data].append(nova_tarefa)
        salvar_json(tarefas)

        return redirect(url_for("index"))
    return render_template("index.html",tarefas=tarefas)

if __name__ == "__main__":
    main()