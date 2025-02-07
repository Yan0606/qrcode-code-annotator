# QR Code Code Annotator

Este script automatiza o processo de adicionar os códigos correspondentes (baseados no nome do arquivo) ao lado das imagens de QR Codes. Ele é útil para organizar e identificar QR Codes de forma visual, com o código sendo exibido verticalmente ao lado da imagem.

## Funcionalidades

- Processa automaticamente todas as imagens `.png` em um diretório.
- Adiciona o código extraído do nome do arquivo ao lado do QR Code.
- O texto do código é centralizado horizontalmente e exibido na vertical.
- Gera novas imagens com o prefixo `com_codigo_`.

## Requisitos

- Python 3.7 ou superior.
- Biblioteca `Pillow`.

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/SEU_USUARIO/qrcode-code-annotator.git
