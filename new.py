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
