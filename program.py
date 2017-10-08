import os
import cv2
import copy as cp
from tqdm import tqdm

# o menos um é para carregar a imagem com transparencia
logo = cv2.imread('./src/fundo.png', -1)
offset = 10

def insertLogo(img, logo, id):
    x_offset = y_offset = 10
    y1, y2 = y_offset, y_offset + logo.shape[0]
    x1, x2 = x_offset, x_offset + logo.shape[1]

    alpha_s = logo[:, :, 3] / 255.0
    alpha_l = 1.0 - alpha_s

    for c in range(0, 3):
        img[y1:y2, x1:x2, c] = (alpha_s * logo[:, :, c] +
                                alpha_l * img[y1:y2, x1:x2, c])

    # Salva a imagem com o logo
    cv2.imwrite(f"./dist/img/OPN-{id}.png", img)

images = [cv2.imread(f"./src/img/{x}") for x in os.listdir('./src/img/')]
# O step no range é de seis porque é o número de cartões por página
counter = 0
for img in tqdm(images):
    insertLogo(img, logo.copy(), counter)
    counter += 1
