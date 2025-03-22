#Importando bibliotecas
import json
import os
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "chave_secreta"

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

    

@app.route("/",methods=["GET","POST"])
def index():
    tarefas = ler_json()
    if request.method == "POST":
        data = request.form["data"]
        nome_tarefa = request.form["nome_tarefa"]
        concluida = request.form.get("concluida") == "on"

        if not data or not nome_tarefa:
            flash("Data e nome da tarefa são obrigatórios.","error")
            return redirect(url_for("index"))

        if data not in tarefas:
            tarefas[data] = []

        if any(tarefa["nome"] == nome_tarefa for tarefa in tarefas[data]):
            flash("Tarefa já existe para este dia.","error")
            return redirect(url_for("index"))
    
        nova_tarefa = {'nome':nome_tarefa,"concluida":concluida}
        tarefas[data].append(nova_tarefa)
        
        if salvar_json(tarefas):
            flash("Tarefa adicionada com sucesso!","success")
        else:
            flash("Erro ao salvar tarefa.","error")

        return redirect(url_for("index"))
    return render_template("index.html",tarefas=tarefas)


@app.route("/tarefas/<data>")
def exibir_tarefas(data):
    tarefas = ler_json()
    tarefas_data = tarefas.get(data,[])
    total_tarefas,concluidas,porcentagem = calcular_porcentagem_sucesso(tarefas,data)
    return render_template("tarefas.html",data=data, tarefas=tarefas_data, total_tarefas=total_tarefas, concluidas=concluidas, porcentagem=porcentagem)

if __name__ == "__main__":
    app.run(debug=True)