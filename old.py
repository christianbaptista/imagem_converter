def salvar_bmp_em_cinza(caminho_saida, matriz_cinza):
    altura = len(matriz_cinza)
    largura = len(matriz_cinza[0]) if altura > 0 else 0

    # Tamanho do padding por linha (as linhas devem ser múltiplas de 4 bytes)
    padding = (4 - (largura % 4)) % 4

    # Cabeçalho do arquivo BMP
    tamanho_arquivo = 54 + (largura + padding) * altura
    cabecalho = bytearray(54)

    # Assinatura 'BM'
    cabecalho[0:2] = b'BM'

    # Tamanho do arquivo
    cabecalho[2:6] = tamanho_arquivo.to_bytes(4, byteorder='little')

    # Offset para os dados da imagem
    cabecalho[10:14] = (54).to_bytes(4, byteorder='little')

    # Tamanho do cabeçalho DIB
    cabecalho[14:18] = (40).to_bytes(4, byteorder='little')

    # Largura e altura
    cabecalho[18:22] = largura.to_bytes(4, byteorder='little')
    cabecalho[22:26] = altura.to_bytes(4, byteorder='little')

    # Planos e bits por pixel (8 bits para escala de cinza)
    cabecalho[26:28] = (1).to_bytes(2, byteorder='little')  # 1 plano
    cabecalho[28:30] = (8).to_bytes(2, byteorder='little')  # 8 bits por pixel

    # Compressão e tamanho dos dados da imagem
    cabecalho[30:34] = (0).to_bytes(4, byteorder='little')  # Sem compressão
    cabecalho[34:38] = ((largura + padding) * altura).to_bytes(4, byteorder='little')

    # Resolução horizontal e vertical (pixels por metro, opcional)
    cabecalho[38:42] = (2835).to_bytes(4, byteorder='little')  # 72 DPI
    cabecalho[42:46] = (2835).to_bytes(4, byteorder='little')  # 72 DPI

    # Número de cores na paleta (256 para escala de cinza)
    cabecalho[46:50] = (256).to_bytes(4, byteorder='little')

    # Número de cores importantes
    cabecalho[50:54] = (256).to_bytes(4, byteorder='little')

    # Paleta de cores (0-255, escala de cinza)
    paleta = bytearray()
    for i in range(256):
        paleta.extend((i, i, i, 0))  # RGB + reservado (4 bytes por cor)

    # Dados da imagem
    dados_imagem = bytearray()
    for linha in reversed(matriz_cinza):  # As linhas são armazenadas de baixo para cima
        for pixel in linha:
            dados_imagem.append(pixel)
        dados_imagem.extend([0] * padding)  # Adicionar padding

    # Escrever o arquivo BMP
    with open(caminho_saida, 'wb') as arquivo:
        arquivo.write(cabecalho)
        arquivo.write(paleta)
        arquivo.write(dados_imagem)


# Exemplo de uso
caminho_saida = "imagem_cinza.bmp"
salvar_bmp_em_cinza(caminho_saida, matriz_cinza)
print(f"Imagem salva como {caminho_saida}")




# Função para transformar a matriz de cinza em preto e branco
def binarizar_imagem(matriz_cinza, limiar=128):
    altura = len(matriz_cinza)
    largura = len(matriz_cinza[0])

    matriz_pb = [[0 for _ in range(largura)] for _ in range(altura)]  # Inicializa a matriz PB

    for y in range(altura):
        for x in range(largura):
            # Aplica o limiar para determinar preto ou branco
            if matriz_cinza[y][x] >= limiar:
                matriz_pb[y][x] = 255  # Branco
            else:
                matriz_pb[y][x] = 0    # Preto

    return matriz_pb


# Exemplo de matriz em escala de cinza
matriz_cinza = [
    [100, 150, 200],
    [50, 125, 175],
    [25, 75, 250]
]

# Binarizar a imagem com limiar fixo (ex.: 128)
matriz_pb = binarizar_imagem(matriz_cinza, limiar=128)

# Resultado
for linha in matriz_pb:
    print(linha)
