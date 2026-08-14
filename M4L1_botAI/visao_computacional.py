import os
os.environ["TF_USE_LEGACY_KERAS"] = "1"

from tensorflow.keras.models import load_model
from PIL import Image, ImageOps
import numpy as np

def classificar_imagem(caminho_da_imagem):
    # Desativa a notação científica para ficar mais amigável
    np.set_printoptions(suppress=True)

    # Carrega o modelo (lembre-se de subir o keras_model.h5)
    import os
    dir_atual = os.path.dirname(os.path.abspath(__file__))
    modelo = load_model(os.path.join(dir_atual, "keras_model.h5"), compile=False)

    # Carrega os nomes das classes que vocês criaram no teachable machine
    nomes_classes = open(os.path.join(dir_atual, "labels.txt"), "r", encoding="utf-8", errors="ignore").readlines()


    # Prepara a estrutura de dados para a IA
    dados = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    
    # Abre a imagem salva pelo bot
    imagem = Image.open(caminho_da_imagem).convert("RGB")

    # Redimensiona a imagem (importante para não dar erro)
    tamanho = (224, 224)
    imagem = ImageOps.fit(imagem, tamanho, Image.Resampling.LANCZOS)

    # Transforma a imagem em números para a IA conseguir ler
    array_imagem = np.asarray(imagem)
    array_imagem_normalizada = (array_imagem.astype(np.float32) / 127.5) - 1
    dados[0] = array_imagem_normalizada

    # A IA faz a previsão
    previsao = modelo.predict(dados)
    
    # Pega o resultado com a maior chance de acerto
    indice = np.argmax(previsao)
    nome_classe = nomes_classes[indice]
    pontuacao_confianca = previsao[0][indice]

    # Vamos entender isso no labels:  retorna o nome da classe (limpando a quebra de linha) e a confiança
    return nome_classe[2:].strip(), pontuacao_confianca