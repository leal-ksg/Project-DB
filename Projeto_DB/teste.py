from PIL import Image

def transformar_cor_para_preto(caminho_entrada, caminho_saida, cor_alvo=(31, 76, 145)):
    # Abre a imagem usando a biblioteca PIL
    imagem = Image.open(caminho_entrada)

    # Converte a imagem para o modo RGBA (Red, Green, Blue, Alpha)
    imagem = imagem.convert('RGBA')

    # Obtém os dados da imagem
    dados = imagem.getdata()

    # Cria uma nova lista para armazenar os pixels transformados
    novos_dados = []

    # Itera sobre os pixels e transforma a cor alvo para preto
    for item in dados:
        # Se o pixel for da cor alvo, substitui por preto
        if item[0] == cor_alvo[0] and item[1] == cor_alvo[1] and item[2] == cor_alvo[2]:
            novos_dados.append((0, 0, 0, item[3]))  # Transforma a cor alvo para preto
        else:
            novos_dados.append(item)

    # Atualiza os dados da imagem
    imagem.putdata(novos_dados)

    # Salva a imagem transformada
    imagem.save(caminho_saida, "PNG")

if __name__ == "__main__":
    caminho_entrada = "logo.png"
    caminho_saida = "logo2.png"

    transformar_cor_para_preto(caminho_entrada, caminho_saida, cor_alvo=(31, 76, 145))
