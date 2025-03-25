import React, {useState, useEffect} from "react";

function App() {
  const [data, setData] = useState("");
  const [quantidade, setQuantidade] = useState(0);
  const [tarefas, setTarefas] = useState([]);
  const [tarefasSalvas, setTarefasSalvas] = useState({});
  const [message, setMessage] = useState("");

  //Carrega todas as tarefas do backend
  const carregarTarefas = () => {
    fetch("http://127.0.0.1:5000/tarefas")
    .then((res) => res.json())
    .then((data) => setTarefasSalvas(data))
    .catch((error) => console.error("Erro ao carregar tarefas:",console.error));
  };

  useEffect(() => {
    carregarTarefas();
  },[]);

  //Gera os campos para a quantidade de tarefas especificada
  const gerarCampos = () => {
    const novosCampos = Array.from({length:Number(quantidade)}, () =>({
      nome: "",
      concluida: false,
    }));
    setTarefas(novosCampos);
  };

  //Atualiza os dados de cada tarefa
  const handleTarefaChange = (index, campo, valor) => {
    const novasTarefas = [...tarefas];
    novasTarefas[index][campo] = valor;
    setTarefas(novasTarefas);
  };
  //Formatar data
  const formatarData = (data) => {
    const [dia, mes, ano] = data.split("-");
    return `${ano}-${mes}-${dia}`; //Converte para DD-MM-YYYY
  };

  //Envia as tarefas para o backend
  const handleSubmit = (e) => {
    e.preventDefault();
    if (!data || tarefas.length === 0){
      setMessage("Data e tarefas são obrigatórios.");
      return;
    }
    
    const dataFormatada = formatarData(data);

    fetch("http://127.0.0.1:5000/tarefas",{
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({data: dataFormatada, tarefas}),
    })
      .then((res) => res.json())
      .then((result) => {
        if (result.message){
          setMessage(result.message);
        }else if (result.error) {
          setMessage(result.error);
        }
        carregarTarefas();
        //Limpa os campos do formulário
        setData("");
        setQuantidade(0);
        setTarefas([]);
      })
      .catch((error) => {
        console.error("Erro:", error);
        setMessage("Erro ao salvar tarefas.")
      });
  };

  return (
    
    <div style={{ padding: "20px" }}>
      <h1>Gerenciador de Tarefas</h1>
      {message && <p>{message}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <label>Data (YYYY-MM-DD): </label>
          <input
            type="date"
            value={data}
            onChange={(e) => setData(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Quantidade de Tarefas: </label>
          <input
            type="number"
            value={quantidade}
            onChange={(e) => setQuantidade(e.target.value)}
            min="1"
            required
          />
          <button type="button" onClick={gerarCampos}>
            Gerar Campos
          </button>
        </div>
        {tarefas.length > 0 && (
          <div>
            {tarefas.map((tarefa, index) => (
              <div key={index}>
                <label>Tarefa {index + 1}: </label>
                <input
                  type="text"
                  value={tarefa.nome}
                  onChange={(e) =>
                    handleTarefaChange(index, "nome", e.target.value)
                  }
                  required
                />
                <label> Concluída: </label>
                <input
                  type="checkbox"
                  checked={tarefa.concluida}
                  onChange={(e) =>
                    handleTarefaChange(index, "concluida", e.target.checked)
                  }
                />
              </div>
            ))}
          </div>
        )}
        <button type="submit">Salvar Tarefas</button>
      </form>

      <hr />
      <h2>Lista de Tarefas</h2>
      {Object.keys(tarefasSalvas).length === 0 ? (
        <p>Nenhuma tarefa cadastrada.</p>
      ) : (
        Object.entries(tarefasSalvas).map(([dataKey, lista]) => (
          <div key={dataKey}>
            <h3>{dataKey}</h3>
            <ul>
              {lista.map((tarefa, index) => (
                <li key={index}>
                  {tarefa.nome} - {tarefa.concluida ? "Concluída" : "Pendente"}
                </li>
              ))}
            </ul>
          </div>
        ))
      )}
    </div>
  );
}

export default App;