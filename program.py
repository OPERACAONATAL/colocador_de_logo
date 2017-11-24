import os
import cv2
import copy as cp
from tqdm import tqdm

# o menos um é para carregar a imagem com transparencia
logo = cv2.imread('./src/fundo.png', -1)

def insertLogo(img, logo, id):
    #   Redimenciona o logo para ficar proporcional a imagem
    ratio = (img.shape[0] / img.shape[1])
    #   Já viu, né?
    if ratio > 1.0:
        ratio = ratio * 0.6
    logo = cv2.resize(logo, (0, 0), fx=ratio, fy=ratio)

    #   Caso mesmo após o redimencionamento o logo ainda fique maior que a imagem, redimensionar novamente.
    while img.shape[0] < logo.shape[0] or img.shape[1] < logo.shape[1]:
        logo = cv2.resize(logo, (0, 0), fx=ratio, fy=ratio)
    
    offset = 10
    x1, x2 = offset, offset + logo.shape[0]
    y1, y2 = offset, offset + logo.shape[1]

    alpha_s = logo[:, :, 3] / 255.0
    alpha_l = 1.0 - alpha_s

    for c in range(0, 3):
        img[y1:y2, x1:x2, c] = (alpha_s * logo[:, :, c] + alpha_l * img[y1:y2, x1:x2, c])

    # Salva a imagem com o logo
    cv2.imwrite(f"./dist/img/OPN-{id}.png", img)

images = [cv2.imread(f"./src/img/{x}") for x in os.listdir('./src/img/')]
# O step no range é de seis porque é o número de cartões por página
counter = 0
for img in tqdm(images):
    insertLogo(img, logo.copy(), counter)
    counter += 1
