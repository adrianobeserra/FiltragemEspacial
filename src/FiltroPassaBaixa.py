'''
Este código imprime no console as coordenadas x,y e a intensidade do
pixel de uma imagem aberta utilizando openCV
'''

import cv2
import numpy as np

def getFiltro(tamanhoJanela):
    filtro = np.zeros((tamanhoJanela, tamanhoJanela))
    for y in range(0, tamanhoJanela):
        for x in range(0, tamanhoJanela):
            filtro[x,y] = 1/(tamanhoJanela**2)
    return filtro

def getMedia(img, tamFiltro):
    filtro = getFiltro(tamFiltro)
    media = 0
    filtro_sum = filtro.sum()
    imgDest = np.zeros_like(img)

    width, height =  img.shape[1], img.shape[0]
    filter_width, filter_height = filtro.shape[0], filtro.shape[1]

    for y in range(height):
        for x in range(width):
            weighted_pixel_sum = 0
            for filterY in range(-(filter_height // 2), filter_height - 1):
                for filterX in range(-(filter_width // 2), filter_width - 1):
                    pixel = 0
                    pixel_y = y - filterY
                    pixel_x = x - filterX

                    # boundary check: all values outside the image are treated as zero.
                    # This is a definition and implementation dependent, it's not a property of the convolution itself.
                    if (pixel_y >= 0) and (pixel_y < height) and (pixel_x >= 0) and (pixel_x < width):
                        pixel = img[pixel_y, pixel_x]

                    # get the weight at the current kernel position
                    # (also un-shift the kernel coordinates into the valid range for the array.)
                    weight = filtro[filterY + (filter_height // 2), filterX + (filter_width // 2)]

                    # weigh the pixel value and sum
                    weighted_pixel_sum += pixel * weight

            # finally, the pixel at location (x,y) is the sum of the weighed neighborhood
            imgDest[y, x] = weighted_pixel_sum / filtro_sum
    return imgDest

'''
for m in range(1, tamFiltro):
        for n in range(1, tamFiltro):
            media += img[m,n] * filtro[m,n]
    return media
'''



img = cv2.imread("Suavizar_(1).jpg", cv2.IMREAD_GRAYSCALE)
height, width = img.shape[:2]
imgDest = np.zeros_like(img)
tamFiltro = 3
print('Using filter [{0},{0}]'.format(tamFiltro))
print("Processing image...")
imgDest = getMedia(img, tamFiltro)
print("Done.")

#cv2.imwrite('teste.jpg', imgDest)
cv2.imshow('teste.jpg', imgDest)
cv2.waitKey(0)
cv2.destroyAllWindows()