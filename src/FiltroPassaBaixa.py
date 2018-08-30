'''
Este programa contem implementações de filtros espaciais de mediana, máximo e aguçamento via Laplaciano a fim de
processar imagens removendo pixels indesejados e melhorando a qualidade de imagens.
'''

import cv2
import numpy as np
import time
import sys
import os

'''Implementação do filtro de mediana.'''
def get_median(list):
    list = sorted(list)
    tamanhoLista = len(list)
    meio = int(tamanhoLista / 2)
    if tamanhoLista % 2 == 0:
        medianA = list[meio]
        medianB = list[meio-1]
        median = (medianA + medianB) / 2
    else:
        median = list[meio + 1]
    return median

def getFiltro(tamanhoJanela):
    filtro = np.zeros((tamanhoJanela, tamanhoJanela), int)
    return filtro

'''Determina se a imagem possui algum quadrante com uma com pixels mais escuros que outros ou se contém distancia 
da média em todos os quadrantes'''
def get_quadrant_lower_intensity(img):
    width, height = img.shape[1], img.shape[0]
    metade_altura = int(height / 2)
    metade_largura = int(width / 2)
    min_pixel_primeiro_quadrante = 0
    min_pixel_segundo_quadrante = 0
    min_pixel_terceiro_quadrante = 0
    min_pixel_quarto_quadrante = 0
    min_pixel = 0
    for y in range(height):
        for x in range(width):
            atual_intensity = img[y,x]

            if(y < metade_altura and x < metade_largura):
                min_pixel_segundo_quadrante += atual_intensity

            if(y < metade_altura and x >= metade_largura):
                min_pixel_primeiro_quadrante += atual_intensity

            if(y > metade_altura and x < metade_largura):
                min_pixel_terceiro_quadrante += atual_intensity

            if(y > metade_altura and x >= metade_largura):
                min_pixel_quarto_quadrante += atual_intensity

            atual_intensity = 0
    lista = [min_pixel_segundo_quadrante, min_pixel_primeiro_quadrante, min_pixel_terceiro_quadrante, min_pixel_quarto_quadrante]
    minor = min(lista)
    media = round(min_pixel_primeiro_quadrante + min_pixel_segundo_quadrante + min_pixel_terceiro_quadrante + min_pixel_quarto_quadrante) / 4
    peso1 = round(media/min_pixel_primeiro_quadrante)
    peso2 = round(media/min_pixel_segundo_quadrante)
    peso3 = round(media/min_pixel_terceiro_quadrante)
    peso4 = round(media/min_pixel_quarto_quadrante)
    if (peso1 + peso2 + peso3 + peso4) == 4:
        return 0

    switcher = {
        min_pixel_primeiro_quadrante: 1,
        min_pixel_segundo_quadrante: 2,
        min_pixel_terceiro_quadrante: 3,
        min_pixel_quarto_quadrante: 4
    }
    return switcher.get(minor)

'''Implementa o filtro baseado na mediada.'''
def median_filter(img, tamFiltro, min_quadrant):
    filtro = getFiltro(tamFiltro)
    imgDest = np.zeros_like(img)
    filtro = getFiltro(tamFiltro)
    width, height = img.shape[1], img.shape[0]
    filter_width, filter_height = filtro.shape[0], filtro.shape[1]
    intensidades = []
    metade_altura = int(height / 2)
    metade_largura = int(width / 2)

    for y in range(height):
        for x in range(width):

            for filterY in range(int(-(filter_height / 2)), filter_height - 1):
                for filterX in range(int(-(filter_width / 2)), filter_width - 1):

                    pixel_y = y - filterY
                    pixel_x = x - filterX
                    pixel = img[filterY, filterX]

                    if (pixel_y >= 0) and (pixel_y < height) and (pixel_x >= 0) and (pixel_x < width):
                        pixel = img[pixel_y, pixel_x]

                    intensidades.append(pixel)

            mediana = get_median(intensidades)
            imgDest[y, x] = mediana

            if min_quadrant == 1:
                if(y < metade_altura and x >= metade_largura):
                    imgDest[y, x] = img[y,x]

            if min_quadrant == 2:
                if(y < metade_altura and x < metade_largura):
                    imgDest[y, x] = img[y,x]

            if min_quadrant == 3:
                if(y > metade_altura and x < metade_largura):
                    imgDest[y, x] = img[y,x]

            if min_quadrant == 4:
                if(y > metade_altura and x >= metade_largura):
                    imgDest[y, x] = img[y,x]

            intensidades = []
    return imgDest

'''Implementação do filtro de máximo. Além do filtro há uma lógica no código para determinar em quais quadrantes
o filtro deverá ser aplicado, baseado na retorno da função get_quadrant_lower_intensity'''
def max_filter(img, tamFiltro, min_quadrant):
    filtro = getFiltro(tamFiltro)
    imgDest = np.zeros_like(img)
    filtro = getFiltro(tamFiltro)
    width, height = img.shape[1], img.shape[0]
    filter_width, filter_height = filtro.shape[0], filtro.shape[1]
    max_pixel = 0
    metade_altura = int(height / 2)
    metade_largura = int(width / 2)

    for y in range(height):
        for x in range(width):

            for filterY in range(int(-(filter_height / 2)), filter_height - 1):
                for filterX in range(int(-(filter_width / 2)), filter_width - 1):

                    pixel_y = y - filterY
                    pixel_x = x - filterX
                    pixel = img[filterY, filterX]

                    #Defini a ação a ser realizada quando o pixel atual fizer parte das bordas da imagem.
                    if (pixel_y >= 0) and (pixel_y < height) and (pixel_x >= 0) and (pixel_x < width):
                        pixel = img[pixel_y, pixel_x]

                    if (pixel > max_pixel):
                        max_pixel = pixel

            imgDest[y, x] = max_pixel

            #A partir daqui, determina em qual quadrante será aplicado o filtro espacial.
            if min_quadrant == 1:
                if(y < metade_altura and x >= metade_largura):
                    imgDest[y, x] = img[y,x]


            if min_quadrant == 2:
                if(y < metade_altura and x < metade_largura):
                    imgDest[y, x] = img[y,x]

            if min_quadrant == 3:
                if(y > metade_altura and x < metade_largura):
                    imgDest[y, x] = img[y,x]

            if min_quadrant == 4:
                if(y > metade_altura and x >= metade_largura):
                    imgDest[y, x] = img[y,x]

            max_pixel = 0

    return imgDest

'''Implementação do filtro laplaciano que se baseia na segunda derivada'''
def lapaclaciano_filter(img, tamFiltro):
    filtro = getFiltro(tamFiltro)
    imgDest = np.zeros_like(img)
    filtro = getFiltro(tamFiltro)
    width, height = img.shape[1], img.shape[0]
    filter_width, filter_height = filtro.shape[0], filtro.shape[1]

    filtro[0,0] = 1
    filtro[0,1] = 1
    filtro[0,2] = 1
    filtro[1,0] = 1
    filtro[1,1] = 8
    filtro[1,2] = 1
    filtro[2,0] = 1
    filtro[2,1] = 1
    filtro[2,2] = 1

    for y in range(height):
        for x in range(width):
            sum_pixels = 0
            for filterY in range(int(-(filter_height / 2)), filter_height - 1):
                for filterX in range(int(-(filter_width / 2)), filter_width - 1):

                    pixel_y = y - filterY
                    pixel_x = x - filterX
                    pixel = img[filterY, filterX]

                    #Defini a ação a ser realizada quando o pixel atual fizer parte das bordas da imagem.
                    if (pixel_y >= 0) and (pixel_y < height) and (pixel_x >= 0) and (pixel_x < width):
                        pixel = img[pixel_y, pixel_x]

                    sum_pixels += pixel

            sum_pixels = ((sum_pixels - 9*img[y,x]) * -1) + img[y,x]
            imgDest[y, x] = sum_pixels
            sum_pixels = 0

    return imgDest

def process_image(imgName, tamFiltro):
    start_time = time.time()
    desImgName = imgName
    imgName = sys.path[0] + '\\' + imgName
    processedFolder = sys.path[0] + '\\' + 'processed'

    if not os.path.exists(processedFolder):
        os.makedirs(processedFolder)

    img = cv2.imread(imgName, cv2.IMREAD_GRAYSCALE)
    print('Using filter [{0},{0}]'.format(tamFiltro))
    print("Processing image '{0}'...".format(imgName))
    min_quadrant = get_quadrant_lower_intensity(img)
    imgDest = median_filter(img, tamFiltro, min_quadrant)
    imgDest = max_filter(imgDest, tamFiltro, min_quadrant)
    cv2.imwrite(processedFolder + "\\" + desImgName, imgDest)
    elapsed_time = time.time() - start_time
    print("Done.")
    print("Done! Elapsed Time: {0}".format(time.strftime("%H:%M:%S", time.gmtime(elapsed_time))))

    ''' Caso queira exibir a imagem na tela
    cv2.imshow(imgName, imgDest)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''

def process_image_laplace(imgName, tamFiltro):
    start_time = time.time()
    desImgName = imgName
    imgName = sys.path[0] + '\\' + imgName
    processedFolder = sys.path[0] + '\\' + 'processed'

    if not os.path.exists(processedFolder):
        os.makedirs(processedFolder)

    img = cv2.imread(imgName, cv2.IMREAD_GRAYSCALE)
    print('Using filter [{0},{0}]'.format(tamFiltro))
    print("Processing image '{0}'...".format(imgName))
    min_quadrant = get_quadrant_lower_intensity(img)
    imgDest = lapaclaciano_filter(img, tamFiltro)
    cv2.imwrite(processedFolder + "\\" + desImgName, imgDest)
    elapsed_time = time.time() - start_time
    print("Done.")
    print("Done! Elapsed Time: {0}".format(time.strftime("%H:%M:%S", time.gmtime(elapsed_time))))

    ''' Caso queira exibir a imagem na tela 
    cv2.imshow(imgName, imgDest)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''

'''Programa Principal'''
process_image("Suavizar_(1).jpg", 11)
process_image("Suavizar_(2).jpg", 11)
process_image_laplace('Agucar_(1).jpg', 3)
process_image_laplace('Agucar_(2).jpg', 3)