#Importando bibliotecas
import json
import os
from flask import Flask, request, jsonify
from flask_cors import CORS #Necessário para permitir que o React acessa a API

app = Flask(__name__)
CORS(app)

#Definindo arquivo JSON
arquivo_json = "tarefas.json"

#Função para ler o JSON
def ler_json():
    try:
        if os.path.exists(arquivo_json):
            with open(arquivo_json,"r") as file:
                    return json.load(file)
            return {}
    except (FileNotFoundError,json.JSONDecodeError):
        return {}

#Função para salvar tarefas no arquivo JSON
def salvar_json(tarefas):
    try:
        with open(arquivo_json,"w") as file:
            json.dump(tarefas,file,indent=4)
        return True
    except IOError:
        return False


#Função para calcular a porcentagem de tarefas concluídas
def calcular_porcentagem_sucesso(tarefas, data):
    if data in tarefas and len(tarefas[data]) > 0:
        total_tarefas = len(tarefas[data])
        concluidas = sum(1 for tarefa in tarefas[data] if tarefa["concluida"]) #Conta tarefas concluídas

        porcentagem = (concluidas/total_tarefas) * 100
        return total_tarefas, concluidas, porcentagem
    return 0, 0, 0 #Retorna zero caso não haja tarefas registradas

#Endpoint para adicionar tarefas
#O playload deve ter o seguinte formato:
#{"data": "YYYY-MM-DD","tarefas":[{"nome": "Tarefa 1","concluida": false},{...} ] }
@app.route("/tarefas",methods=["POST"])
def adicionar_tarefas():
    content = request.json
    if not content:
        return jsonify({"error":"Playload JSON não fornecido."}),400
    
    data = content.get("data")
    tarefas_novas = content.get("tarefas")
    if not data or not tarefas_novas:
        return jsonify({"error","Os campos 'data' e 'tarefas' são obrigatórios"}),400

    tarefas = ler_json()
    if data not in tarefas:
        tarefas[data] = []

    #Adiciona cada tarefa, evitando duplicatas (pelo nome)
    for nova in tarefas_novas:
        nome_tarefa = nova.get("nome")
        concluida = nova.get("concluida",False)
        if not nome_tarefa:
            continue #Ignora se não houver nome
        if any(tarefa["nome"] == nome_tarefa for tarefa in tarefas[data]):
            continue #Pula se já existir essa tarefa
        tarefas[data].append({"nome": nome_tarefa,"concluida": concluida})

    if salvar_json(tarefas):
        return jsonify({"message":"Tarefas adicionadas com sucesso!"}), 201
    else:
        return jsonify({"error":"Erro ao salvar tarefas."}),500


#Endpoint para obter todas tarefas (agrupadas por data)
@app.route("/tarefas/<data>",methods=["GET"])
def exibir_tarefas(data):
    tarefas = ler_json()
    tarefas_data = tarefas.get(data, [])
    total, concluidas, porcentagem = calcular_porcentagem_sucesso(tarefas,data)
    return jsonify({
        "data": data,
        "tarefas": tarefas_data,
        "total_tarefas": total,
        "concluidas": concluidas,
        "porcentagem": porcentagem
    })


if __name__ == "__main__":
    app.run(debug=True)