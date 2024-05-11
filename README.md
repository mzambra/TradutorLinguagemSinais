# Tradutor de Linguagem de Sinais


Este projeto tem como objetivo traduzir frases em português para a Língua Brasileira de Sinais (Libras), utilizando inteligência artificial e animação 3D para apresentar os sinais correspondentes com a ajuda de um avatar 3D.

**Observação:** Por questões de segurança, a chave da API do Google Gemini foi removida deste código. Você precisará obter sua própria chave e adicioná-la ao arquivo `app.py` para que o projeto funcione corretamente. 

## 💻 Tecnologias Utilizadas

* **Linguagem de Programação:** [Python](https://www.python.org/)
* **Framework Web:** [Flask](https://flask.palletsprojects.com/en/2.2.x/)
* **Bibliotecas Python:**
    * [requests](https://docs.python-requests.org/en/latest/)
    * [NumPy](https://numpy.org/)
    * [SciPy](https://scipy.org/)
    * [bpy](https://docs.blender.org/api/current/bpy.ops.html) (API do Blender)
* **Software de Animação 3D:** [Blender](https://www.blender.org/)
* **API de Inteligência Artificial:** Google Gemini API (Hipotética)
* **Modelo 3D:** Hugo, do site do VLIBRAS ([https://vlibras.gov.br/](https://vlibras.gov.br/))

## 🚀 Pré-requisitos

* **Python 3:** Faça o download e instale a versão mais recente do Python em [https://www.python.org/](https://www.python.org/).
* **Visual Studio Code (Recomendado):** Utilize o VS Code como editor de código-fonte, disponível em [https://code.visualstudio.com/](https://code.visualstudio.com/).
* **Blender:** Baixe e instale o Blender em [https://www.blender.org/](https://www.blender.org/).
* **API Key do Google Gemini:** Obtenha sua própria chave da API do Google Gemini (instruções serão fornecidas quando a API estiver disponível).
* **Bibliotecas Python:** Instale as bibliotecas necessárias dentro do seu ambiente virtual:
  ```bash
  pip install flask requests numpy scipy

## 📂 Estrutura do Projeto

tradutor-libras/

├── app.py

└── templates/

    ├── index.html
    └── traducao.html
    └── padrao.blend

* `app.py`: Código principal da aplicação Flask, com rotas, processamento da tradução e integração com o Blender.
* `templates/index.html`: Página inicial, onde o usuário digita a frase para tradução.
* `templates/traducao.html`: Página de exibição da animação 3D do avatar em Libras.
* `padrao.blend`: Arquivo do Blender com o modelo 3D do avatar (Hugo) e as animações dos sinais.

## ⚙️ Implementação

O projeto é dividido em cinco fases:

* **Fase 1: Interface do Usuário:** Uma interface web simples criada com Flask, com um formulário para o usuário inserir a frase. O formulário envia a frase via método POST para a rota `/traducao`.

* **Fase 2: Processamento de Texto:** A API do Google Gemini é utilizada para:
    * Tokenizar o texto: Separar o texto em palavras individuais.
    * Extrair as palavras-chave: Identificar as palavras mais relevantes da frase.
* Requisições HTTP são enviadas à API do Gemini através da biblioteca requests. Os tokens e palavras-chave são armazenados para uso posterior.

* **Fase 3: Banco de Dados de Sinais e Embeddings:** Um dicionário em Python serve como banco de dados, relacionando palavras-chave com sinais em Libras. A API do Google Gemini gera embeddings (representações numéricas) para cada palavra-chave e sinal. Uma função calcula a distância cosseno entre embeddings para encontrar o sinal mais similar a uma palavra-chave.

* **Fase 4: Animação 3D no Blender:** O modelo 3D do avatar (Hugo) é importado do VLIBRAS para o Blender. Animações são criadas para cada sinal no banco de dados, definindo os movimentos do avatar com keyframes. Cada animação é exportada como um arquivo separado (ex: `.fbx` ou `.glb`).

* **Fase 5: Integração e Exibição:** A lógica de tradução é integrada ao Blender usando a API `bpy`. O arquivo `.blend` é carregado no `app.py`, e o objeto do avatar é acessado. Para cada sinal encontrado, a ação do avatar é definida para a animação correspondente. A animação é renderizada como um vídeo (ex: `.mp4`) pelas funções do Blender. O vídeo é incorporado na página `traducao.html` para exibição.

## 📝 Observações


* O projeto pode ser expandido com:
    * Suporte a mais palavras-chave e sinais.
    * Animação 3D mais realista e com expressões faciais.
    * Reconhecimento de fala para entrada de texto.

## 🎉 Conclusão

Este projeto demonstra como IA e animação 3D podem criar aplicações inovadoras para comunicação e inclusão de pessoas surdas.

## ▶️ Como Executar

* Clone o repositório.
* Instale as dependências: `pip install -r requirements.txt`.
* Insira sua API Key do Google Gemini no arquivo `app.py`.
* Abra o Blender com o arquivo `.blend` do avatar.
* Execute o `app.py`.
* Acesse a aplicação em `http://127.0.0.1:5000/` no seu navegador.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

## 📄 Licença

MIT
