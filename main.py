from PIL import Image, ImageDraw, ImageFont
import os
from tqdm import tqdm

# Diretório onde os QR codes estão localizados
qr_dir = './qrcodes'  # Ajuste para o seu diretório correto
tamanho_padrao = (480, 460)  # Defina o tamanho padrão para todas as imagens

# Função para adicionar o código ao lado do QR Code
def adicionar_codigo_na_imagem(qr_image_path, codigo):
    qr_image = Image.open(qr_image_path).convert("RGBA")
    qr_image = qr_image.resize(tamanho_padrao, Image.LANCZOS)
    
    # Criar uma nova imagem com largura extra para o código
    largura, altura = qr_image.size
    largura_extra = 100  # Espaço extra para o código
    nova_imagem = Image.new('RGBA', (largura + largura_extra, altura), (255, 255, 255, 255))  # Fundo branco
    nova_imagem.paste(qr_image, (0, 0))
    
    # Criar o objeto para desenhar
    draw = ImageDraw.Draw(nova_imagem)
    
    # Definir a fonte e o tamanho do código
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        font = ImageFont.load_default()
    
    # Calcular dimensões do texto
    espaco_entre_letras = 45  # Espaçamento entre letras
    altura_total_texto = len(codigo) * espaco_entre_letras  # Altura total do texto vertical
    
    # Calcular a posição X para centralizar o texto horizontalmente
    texto_bounding_box = draw.textbbox((0, 0), codigo[0], font=font)  # Apenas 1 caractere para largura
    texto_largura = texto_bounding_box[2] - texto_bounding_box[0]
    x = largura + (largura_extra - texto_largura) // 2
    
    # Calcular a posição inicial Y para centralizar o texto verticalmente
    y_inicial = (altura - altura_total_texto) // 2
    
    # Desenhar o código na vertical
    y = y_inicial
    for char in codigo:
        draw.text((x, y), char, font=font, fill=(0, 0, 0))  # Cor preta
        y += espaco_entre_letras  # Avançar para desenhar o próximo caractere
    
    # Salvar a nova imagem
    novo_nome = os.path.join(qr_dir, f"com_codigo_{os.path.basename(qr_image_path)}")
    nova_imagem.save(novo_nome)
    
    # Fechar a imagem antes de excluir
    qr_image.close()
    nova_imagem.close()
    
    # Excluir a imagem original
    os.remove(qr_image_path)

# Função para adicionar o overlay ao QR Code
def adicionar_overlay(qr_image_path, imagem_overlay):
    try:
        # Abrir a imagem do QR Code
        qr_image = Image.open(qr_image_path).convert("RGBA")
        qr_image = qr_image.resize(tamanho_padrao, Image.LANCZOS)

        # Adicionar um fundo branco ao redor do QR Code
        largura, altura = qr_image.size
        novo_largura = int(largura * 2.0)
        novo_altura = int(altura * 2.0)

        nova_imagem = Image.new('RGBA', (novo_largura, novo_altura), (255, 255, 255, 255))
        nova_imagem.paste(qr_image, (int((novo_largura - largura) / 2), int((novo_altura - altura) / 2)))

        # Redimensionar o overlay para caber no QR Code (ajustável)
        overlay_largura = int(imagem_overlay.width * 1.4)  # Ajuste proporcional (40% do tamanho original da logo)
        overlay_altura = int(imagem_overlay.height * 1.4)
        imagem_overlay_resized = imagem_overlay.resize((overlay_largura, overlay_altura), Image.LANCZOS)

        # Centralizar o overlay sobre a nova imagem
        overlay_x = (nova_imagem.width - imagem_overlay_resized.width) // 2
        overlay_y = (nova_imagem.height - imagem_overlay_resized.height) // 2
        nova_imagem.paste(imagem_overlay_resized, (overlay_x, overlay_y), imagem_overlay_resized)

        # Salvar a imagem final
        nova_imagem.save(qr_image_path.replace('.png', '_overlay.png'))

        # Fechar a imagem antes de excluir
        qr_image.close()
        nova_imagem.close()

        # Excluir a imagem com código
        os.remove(qr_image_path)

    except Exception as e:
        print(f"Erro ao processar a imagem {qr_image_path}: {e}")

# Caminho da imagem overlay (formato PNG)
imagem_overlay_path = './logoQrc.png'  # Atualize para o caminho correto da nova imagem

# Carregar a nova imagem de overlay
try:
    imagem_overlay = Image.open(imagem_overlay_path).convert("RGBA")
    print(f"Imagem overlay carregada com sucesso: {imagem_overlay_path}")
except Exception as e:
    print(f"Erro ao carregar a imagem overlay: {e}")
    exit()

# Processar os QR Codes
total_imagens = len([f for f in os.listdir(qr_dir) if f.endswith('.png') and not f.startswith('com_codigo_')])
total_imagens_overlay = len([f for f in os.listdir(qr_dir) if f.endswith('.png') and f.startswith('com_codigo_')])
total_imagens += total_imagens_overlay

with tqdm(total=total_imagens, desc="Processando imagens") as pbar:
    for nome_arquivo in os.listdir(qr_dir):
        if nome_arquivo.endswith('.png') and not nome_arquivo.startswith('com_codigo_'):
            codigo = os.path.splitext(nome_arquivo)[0]  # Código é o nome do arquivo sem extensão
            qr_image_path = os.path.join(qr_dir, nome_arquivo)
            adicionar_codigo_na_imagem(qr_image_path, codigo)
            pbar.update(1)

    for nome_arquivo in os.listdir(qr_dir):
        if nome_arquivo.endswith('.png') and nome_arquivo.startswith('com_codigo_'):
            qr_image_path = os.path.join(qr_dir, nome_arquivo)
            adicionar_overlay(qr_image_path, imagem_overlay)
            pbar.update(1)

print("\nProcessamento concluído!")
