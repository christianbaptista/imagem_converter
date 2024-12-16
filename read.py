def resolution(caminho_imagem):
    with open(caminho_imagem, 'rb') as arquivo:
        arquivo.seek(18)
        largura = int.from_bytes(arquivo.read(4), byteorder='little')
        altura = int.from_bytes(arquivo.read(4), byteorder='little')

        print(f"Largura: {largura} e Altura: {altura}")

        cabecalho = bytearray(54)

        cabecalho[18:22] = largura.to_bytes(4, byteorder='little')
        cabecalho[22:26] = altura.to_bytes(4, byteorder='little')

        print(cabecalho[18:22])
        print(cabecalho[22:26])




caminho_imagem = 'sua_imagem.bmp'
resolution(caminho_imagem)
