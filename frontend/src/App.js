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

  //Envia as tarefas para o backend
  const handleSubmit = (e) => {
    e.preventDefault();
    if (!data || tarefas.length === 0){
      setMessage("Data e tarefas são obrigatórios.");
      return;
    }
    
    fetch("http://127.0.0.1:5000/tarefas",{
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({data, tarefas}),
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

  )



}

export default App;