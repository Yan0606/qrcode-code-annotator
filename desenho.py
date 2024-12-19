from PIL import Image
import os

# Diretório onde os QR codes estão localizados
qr_dir = '../qrcodes'

# Caminho da imagem overlay (formato PNG)
imagem_overlay_path = './logo.png'  # Substitua pelo caminho correto da imagem PNG

# Função para adicionar o overlay ao QR Code
def adicionar_overlay(qr_image_path, imagem_overlay):
    print(f"Processando a imagem: {qr_image_path}...")

    # Abrir a imagem do QR Code
    qr_image = Image.open(qr_image_path).convert("RGBA")

    # Adicionar um fundo branco ao redor do QR Code
    largura, altura = qr_image.size
    novo_largura = int(largura * 1.6)  # Aumenta espaço ao redor do QR Code
    novo_altura = int(altura * 1.9)

    nova_imagem = Image.new('RGBA', (novo_largura, novo_altura), (255, 255, 255, 255))
    nova_imagem.paste(qr_image, (int((novo_largura - largura) / 2), int((novo_altura - altura) / 2)))

    # Aumentar o tamanho da imagem overlay (4 vezes maior)
    overlay_largura = imagem_overlay.width * 4
    overlay_altura = imagem_overlay.height * 4
    imagem_overlay_resized = imagem_overlay.resize((overlay_largura, overlay_altura), Image.LANCZOS)

    # Centralizar o overlay sobre a nova imagem
    overlay_x = (nova_imagem.width - imagem_overlay_resized.width) // 2
    overlay_y = (nova_imagem.height - imagem_overlay_resized.height) // 2
    nova_imagem.paste(imagem_overlay_resized, (overlay_x, overlay_y), imagem_overlay_resized)

    # Salvar a imagem final
    nova_imagem.save(qr_image_path.replace('.png', '_overlay.png'))
    print(f"Imagem salva com sucesso: {qr_image_path.replace('.png', '_overlay.png')}")

# Carregar a imagem de overlay uma única vez
imagem_overlay = Image.open(imagem_overlay_path).convert("RGBA")

# Iterar pelas imagens no diretório
for nome_arquivo in os.listdir(qr_dir):
    if nome_arquivo.endswith('.png'):
        qr_image_path = os.path.join(qr_dir, nome_arquivo)
        print(f"Encontrada imagem de QR Code: {nome_arquivo}")
        
        # Adicionar o overlay na imagem do QR Code
        adicionar_overlay(qr_image_path, imagem_overlay)

print("Processamento concluído!")