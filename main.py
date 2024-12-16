def ler_bmp_para_matriz(caminho_imagem):
    with open(caminho_imagem, 'rb') as arquivo:
        # Ler o cabeçalho do BMP
        arquivo.seek(18)  # O cabeçalho BMP começa com informações da imagem no byte 18
        largura = int.from_bytes(arquivo.read(4), byteorder='little')
        altura = int.from_bytes(arquivo.read(4), byteorder='little')

        # Pular outras informações do cabeçalho até os dados da imagem
        arquivo.seek(54)  # Offset para os dados da imagem no formato BMP (54 bytes)

        # Ler os dados da imagem (supondo BMP de 24 bits sem compressão)
        bytes_por_linha = (largura * 3 + 3) // 4 * 4  # Linhas são alinhadas em múltiplos de 4 bytes
        matriz = []

        for _ in range(altura):
            linha = []
            for x in range(largura):
                # Cada pixel é composto por 3 bytes: Blue, Green, Red
                blue = int.from_bytes(arquivo.read(1), byteorder='little')
                green = int.from_bytes(arquivo.read(1), byteorder='little')
                red = int.from_bytes(arquivo.read(1), byteorder='little')
                linha.append((red, green, blue))
            # Ignorar bytes de preenchimento (padding)
            arquivo.read(bytes_por_linha - largura * 3)
            matriz.insert(0, linha)  # BMP armazena as linhas de baixo para cima

        return matriz

# Exemplo de uso
caminho_imagem = 'sua_imagem.bmp'
matriz = ler_bmp_para_matriz(caminho_imagem)
#print(matriz)

def rgb_para_cinza(matriz_rgb):
    matriz_cinza = []
    for linha in matriz_rgb:
        linha_cinza = []
        for r, g, b in linha:
            # Conversão para escala de cinza com ponderação
            cinza = int(0.299 * r + 0.587 * g + 0.114 * b)
            linha_cinza.append(cinza)
        matriz_cinza.append(linha_cinza)
    return matriz_cinza

# Exemplo de uso
matriz_cinza = rgb_para_cinza(matriz)
for linha in matriz_cinza:
    print(linha)

def salvar_bmp_em_cinza(caminho_saida, matriz_cinza):
    altura = len(matriz_cinza)
    largura = len(matriz_cinza[0]) if altura > 0 else 0

    # Tamanho do padding por linha (linhas precisam ser múltiplos de 4 bytes)
    padding = (4 - (largura % 4)) % 4

    # Cabeçalho do arquivo BMP
    tamanho_arquivo = 54 + (largura + padding) * altura
    cabecalho = bytearray(54)

    # Assinatura 'BM'
    cabecalho[0:2] = b'BM'

    # Tamanho do arquivo
    cabecalho[2:6] = tamanho_arquivo.to_bytes(4, byteorder='little')

    # Offset para os dados da imagem
    cabecalho[10:14] = (54 + 256 * 4).to_bytes(4, byteorder='little')  # 54 bytes cabeçalho + paleta

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
    cabecalho[50:54] = (0).to_bytes(4, byteorder='little')  # Todas as cores são importantes

    # Paleta de cores (0-255, escala de cinza)
    paleta = bytearray()
    for i in range(256):
        paleta.extend((i, i, i, 0))  # RGB + reservado (4 bytes por cor)

    # Dados da imagem
    dados_imagem = bytearray()
    for linha in reversed(matriz_cinza):  # As linhas são armazenadas de baixo para cima no formato BMP
        for pixel in linha:
            dados_imagem.append(pixel)
        dados_imagem.extend([0] * padding)  # Adicionar padding para alinhamento

    # Escrever o arquivo BMP
    with open(caminho_saida, 'wb') as arquivo:
        arquivo.write(cabecalho)
        arquivo.write(paleta)
        arquivo.write(dados_imagem)


# Exemplo de uso
caminho_saida = "imagem_cinza_revisada.bmp"
salvar_bmp_em_cinza(caminho_saida, matriz_cinza)
print(f"Imagem salva como {caminho_saida}")



def cinza_para_binaria(matriz_cinza, limiar=128):
    matriz_binaria = []
    for linha in matriz_cinza:
        linha_binaria = []
        for valor in linha:
            linha_binaria.append(255 if valor >= limiar else 0)
        matriz_binaria.append(linha_binaria)
    return matriz_binaria


matriz_binaria = cinza_para_binaria(matriz_cinza, limiar=120)

def salvar_bmp_pb(matriz_binaria, nome_arquivo):
    altura = len(matriz_binaria)
    largura = len(matriz_binaria[0])

    # Tamanho da paleta de 2 cores: preto e branco
    tamanho_paleta = 8  # 2 cores × 4 bytes cada (RGB + reservado)

    # Calcular o padding
    padding = (4 - (largura % 4)) % 4

    # Tamanho total do arquivo
    tamanho_cabecalho = 54
    tamanho_imagem = (largura + padding) * altura
    tamanho_arquivo = tamanho_cabecalho + tamanho_paleta + tamanho_imagem

    # Criar o cabeçalho BMP
    cabecalho = bytearray(54)
    cabecalho[0:2] = b'BM'                             # Assinatura do BMP
    cabecalho[2:6] = tamanho_arquivo.to_bytes(4, 'little')  # Tamanho do arquivo
    cabecalho[10:14] = (tamanho_cabecalho + tamanho_paleta).to_bytes(4, 'little')  # Offset para os dados de pixel
    cabecalho[14:18] = (40).to_bytes(4, 'little')      # Tamanho do cabeçalho DIB
    cabecalho[18:22] = largura.to_bytes(4, 'little')   # Largura da imagem
    cabecalho[22:26] = altura.to_bytes(4, 'little')    # Altura da imagem
    cabecalho[26:28] = (1).to_bytes(2, 'little')       # Planos de cor (sempre 1)
    cabecalho[28:30] = (8).to_bytes(2, 'little')       # Bits por pixel (8 = paleta de cores)
    cabecalho[30:34] = (0).to_bytes(4, 'little')       # Sem compressão
    cabecalho[34:38] = tamanho_imagem.to_bytes(4, 'little')  # Tamanho da imagem
    cabecalho[38:42] = (2835).to_bytes(4, 'little')    # Resolução horizontal (72 DPI)
    cabecalho[42:46] = (2835).to_bytes(4, 'little')    # Resolução vertical (72 DPI)
    cabecalho[46:50] = (2).to_bytes(4, 'little')       # Número de cores na paleta
    cabecalho[50:54] = (0).to_bytes(4, 'little')       # Todas as cores são importantes

    # Criar a paleta de 2 cores (preto e branco)
    paleta = bytearray([
        255, 255, 255, 0,   # Branco (valor 0)
        0, 0, 0, 0          # Preto (valor 1)
    ])

    # Criar os dados de pixel com padding
    dados_pixel = bytearray()
    for linha in reversed(matriz_binaria):  # BMP armazena linhas de baixo para cima
        dados_pixel.extend(linha)      # Adiciona a linha
        dados_pixel.extend([0] * padding)  # Adiciona o padding necessário

    # Escrever no arquivo
    with open(nome_arquivo, 'wb') as f:
        f.write(cabecalho)  # Escreve o cabeçalho
        f.write(paleta)     # Escreve a paleta
        f.write(dados_pixel)  # Escreve os dados dos pixels



# Salvar como arquivo BMP
salvar_bmp_pb(matriz_binaria, "imagem_preto_branco.bmp")

# Exemplo de uso
for linha in matriz_binaria:
    print(linha)
