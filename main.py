from PIL import Image, ImageDraw, ImageFont
import os

# Diretório onde os QR codes estão localizados
qr_dir = '../qrcodes'  

# Função para adicionar o código ao lado do QR Code
def adicionar_codigo_na_imagem(qr_image_path, codigo):
    qr_image = Image.open(qr_image_path)
    
    # Criar uma nova imagem com largura extra para o código
    largura, altura = qr_image.size
    nova_largura = largura + 100 
    nova_imagem = Image.new('RGB', (nova_largura, altura), (255, 255, 255))  # Fundo branco
    nova_imagem.paste(qr_image, (0, 0))
    
    # Criar o objeto para desenhar
    draw = ImageDraw.Draw(nova_imagem)
    
    # Definir a fonte e o tamanho do código
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        # Se não encontrar, use a fonte padrão
        font = ImageFont.load_default()
    
    # Calcular a largura do código usando textbbox
    texto_bounding_box = draw.textbbox((0, 0), codigo, font=font)
    texto_largura = texto_bounding_box[2] - texto_bounding_box[0]
    
    # Calcular a posição X para centralizar o código
    x = largura + (100 - texto_largura) // 2  # Centralizando o texto no espaço extra
    
    # Posição vertical do código (começo do texto)
    y = 10 
    
    # Desenhar o código na vertical
    for char in codigo:
        draw.text((x, y), char, font=font, fill=(0, 0, 0))  # Cor preta
        y += 45 
    
    # Salvar a nova imagem
    novo_nome = os.path.join(qr_dir, f"com_codigo_{os.path.basename(qr_image_path)}")
    nova_imagem.save(novo_nome)
    print(f"Imagem salva como {novo_nome}")

# Iterar pelas imagens no diretório
for nome_arquivo in os.listdir(qr_dir):
    if nome_arquivo.endswith('.png'):
        
        codigo = os.path.splitext(nome_arquivo)[0]
        
        qr_image_path = os.path.join(qr_dir, nome_arquivo)

        adicionar_codigo_na_imagem(qr_image_path, codigo)
