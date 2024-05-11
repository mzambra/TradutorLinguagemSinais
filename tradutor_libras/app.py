from flask import Flask, render_template, request, redirect, url_for
import requests
import numpy as np
from scipy.spatial.distance import cosine
import bpy  # Importa a API do Blender

app = Flask(__name__)

# --- CONFIGURAÇÕES DA API GEMINI ---
chave_magica = 'SUA_CHAVE_MAGICA'  # Substitua pela sua chave mágica da Gemini API
endereco_gemini = "https://api.gemini.google.com/v1"  # Endereço base da Gemini API

# --- BANCO DE DADOS DE SINAIS ---
banco_de_sinais = {
    "menino": ["Fazer o sinal de 'pessoa' e depois apontar para baixo, indicando 'pequeno'"],
    "gosta": ["Tocar o peito com a mão aberta e fazer um movimento circular"],
    "jogar": ["Imitar o movimento de arremessar uma bola"],
    "bola": ["Fazer um círculo com as mãos"],
    # Adicione mais palavras-chave e sinais aqui!
}

# --- FUNÇÕES PARA INTERAGIR COM A GEMINI API ---

def separar_palavras(frase):
    """Pede para a Gemini separar as palavras da frase."""
    carta = {"text": frase}  # Corpo da requisição (texto a ser processado)
    envelope = {
        "Authorization": f"Bearer {chave_magica}",  # Autorização com a API Key
        "Content-Type": "application/json"  # Tipo de conteúdo da requisição
    }
    destino = f"{endereco_gemini}/separarPalavras"  # Endpoint da Gemini para tokenização (substitua pelo correto)
    resposta = requests.post(destino, headers=envelope, json=carta) # Envia a requisição POST
    if resposta.status_code == 200:  # Verifica se a requisição foi bem-sucedida
        palavras_separadas = resposta.json().get('palavras', [])  # Extrai os tokens da resposta (ajuste o nome do campo se necessário)
        return palavras_separadas
    else:
        print("Ops, a Gemini não entendeu a carta!", resposta.status_code)  # Imprime mensagem de erro
        return []

def achar_palavras_chave(frase):
    """Pede para a Gemini encontrar as palavras-chave da frase."""
    carta = {"text": frase}  # Corpo da requisição (texto a ser processado)
    envelope = {
        "Authorization": f"Bearer {chave_magica}",  # Autorização com a API Key
        "Content-Type": "application/json"  # Tipo de conteúdo da requisição
    }
    destino = f"{endereco_gemini}/acharPalavrasChave"  # Endpoint da Gemini para extração de palavras-chave (substitua pelo correto)
    resposta = requests.post(destino, headers=envelope, json=carta)  # Envia a requisição POST
    if resposta.status_code == 200:  # Verifica se a requisição foi bem-sucedida
        palavras_chave = resposta.json().get('palavrasChave', [])  # Extrai as palavras-chave da resposta (ajuste o nome do campo se necessário)
        return palavras_chave
    else:
        print("Ops, a Gemini não entendeu a carta!", resposta.status_code)  # Imprime mensagem de erro
        return []

def gerar_embedding(texto):
    """Pede para a Gemini gerar um embedding para o texto."""
    carta = {"text": texto}  # Corpo da requisição (texto para gerar embedding)
    envelope = {
        "Authorization": f"Bearer {chave_magica}",  # Autorização com a API Key
        "Content-Type": "application/json"  # Tipo de conteúdo da requisição
    }
    destino = f"{endereco_gemini}/gerarEmbedding"  # Endpoint da Gemini para geração de embeddings (substitua pelo correto)
    resposta = requests.post(destino, headers=envelope, json=carta)  # Envia a requisição POST
    if resposta.status_code == 200:  # Verifica se a requisição foi bem-sucedida
        embedding = resposta.json().get('embedding', [])  # Extrai o embedding da resposta (ajuste o nome do campo se necessário)
        return embedding
    else:
        print("Ops, a Gemini não entendeu a carta!", resposta.status_code)  # Imprime mensagem de erro
        return []

# --- FUNÇÕES AUXILIARES PARA BUSCA DE SINAIS ---

def encontrar_sinal_semelhante(embedding_palavra_chave, embeddings_sinais):
    """Encontra o sinal mais semelhante à palavra-chave, com base na distância cosseno."""
    distancias = [cosine(embedding_palavra_chave, embedding_sinal) for embedding_sinal in embeddings_sinais]  # Calcula a distância cosseno entre os embeddings
    indice_sinal_semelhante = np.argmin(distancias)  # Encontra o índice do sinal com menor distância
    return indice_sinal_semelhante

# --- ROTAS DO FLASK ---

@app.route('/', methods=['GET', 'POST'])  # Rota da página inicial
def index():
    if request.method == 'POST':  # Se o formulário foi enviado
        texto_input = request.form['texto']  # Obtém o texto do formulário
        return redirect(url_for('traducao', texto=texto_input))  # Redireciona para a rota '/traducao' com o texto
    else:
        return render_template('index.html')  # Renderiza o template 'index.html'

@app.route('/traducao', methods=['GET'])  # Rota da página de tradução
def traducao():
    texto_input = request.args.get('texto', '')  # Obtém o texto da URL

    # --- PROCESSAMENTO DA TRADUÇÃO ---

    tokens = separar_palavras(texto_input)  # Tokeniza o texto com a Gemini
    palavras_chave = achar_palavras_chave(texto_input)  # Extrai as palavras-chave com a Gemini
    
    # Gerar embeddings para as palavras-chave e sinais (mesmo código da Fase 3)
    embeddings_palavras_chave = {palavra: gerar_embedding(palavra) for palavra in banco_de_sinais}
    embeddings_sinais = {}
    for palavra, sinais in banco_de_sinais.items():
        embeddings_sinais[palavra] = [gerar_embedding(sinal) for sinal in sinais]

    # --- LÓGICA PARA ENCONTRAR OS SINAIS ---

    traducao_libras = []  # Lista para armazenar os sinais encontrados
    for palavra in palavras_chave:  # Itera sobre as palavras-chave
        if palavra in banco_de_sinais:  # Verifica se a palavra está no banco de dados
            indice_sinal = encontrar_sinal_semelhante(embeddings_palavras_chave[palavra], embeddings_sinais[palavra])  # Busca o sinal mais semelhante
            sinal = banco_de_sinais[palavra][indice_sinal]  # Obtém o sinal pelo índice
            traducao_libras.append(sinal)  # Adiciona o sinal à lista de tradução

    # --- ANIMAÇÃO 3D COM BLENDER ---

    bpy.ops.wm.open_mainfile(filepath="/tradutor_libras/padrao.blend")  # Carrega o arquivo .blend
    avatar = bpy.data.objects["NomeDoAvatar"]  # Encontra o objeto avatar

    for sinal in traducao_libras:
        acao = bpy.data.actions[sinal]  # Encontra a ação pelo nome
        avatar.animation_data.action = acao  # Define a ação do avatar
        # (Opcional) Ajustar o frame inicial e final da animação

    # --- SIMULAÇÃO DA ANIMAÇÃO (imprimir frames) ---
    inicio_frame = 1
    fim_frame = 250  # Ajuste para o número de frames da sua animação
    for frame in range(inicio_frame, fim_frame):
        bpy.context.scene.frame_set(frame)  # Define o frame atual no Blender
        print(f"Frame: {frame}")  # Imprime o número do frame

    return render_template('traducao.html', texto=texto_input, traducao_libras=traducao_libras)  # Renderiza o template 'traducao.html' com os dados da tradução

if __name__ == '__main__':
    app.run(debug=True)  # Inicia o servidor Flask em modo de depuração