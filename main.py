from PIL import Image, ImageDraw, ImageFont
import os

# Diretório onde os QR codes estão localizados
qr_dir = './qrcodes'  # Ajuste para o seu diretório correto

# Função para adicionar o código ao lado do QR Code
def adicionar_codigo_na_imagem(qr_image_path, codigo):
    qr_image = Image.open(qr_image_path)
    
    # Criar uma nova imagem com largura extra para o código
    largura, altura = qr_image.size
    largura_extra = 100  # Espaço extra para o código
    nova_imagem = Image.new('RGB', (largura + largura_extra, altura), (255, 255, 255))  # Fundo branco
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
    print(f"Imagem salva como {novo_nome}")

# Processar os QR Codes
for nome_arquivo in os.listdir(qr_dir):
    if nome_arquivo.endswith('.png') and not nome_arquivo.startswith('com_codigo_'):  
        codigo = os.path.splitext(nome_arquivo)[0]  # Código é o nome do arquivo sem extensão
        qr_image_path = os.path.join(qr_dir, nome_arquivo)
        adicionar_codigo_na_imagem(qr_image_path, codigo)

# Verificação das imagens processadas
original_images = [f for f in os.listdir(qr_dir) if f.endswith('.png') and not f.startswith('com_codigo_')]
processed_images = [f for f in os.listdir(qr_dir) if f.startswith('com_codigo_') and f.endswith('.png')]

# Comparar os números de arquivos
print("\n--- Verificação Final ---")
print(f"Total de imagens originais: {len(original_images)}")
print(f"Total de imagens processadas: {len(processed_images)}")

if len(original_images) == len(processed_images):
    print("✅ Todas as imagens foram processadas com sucesso!")
else:
    faltantes = len(original_images) - len(processed_images)
    print(f"⚠️ {faltantes} imagens ainda não foram processadas.")
