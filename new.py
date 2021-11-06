'''
Bubble sort
Selection sort
Insertion sort
Quick sort
Merge sort
'''
import pygame as pg
import sys
import random
import math

screen = None
screenSize = (800, 600)
reference = 600
mouse = {
    "pos": (0, 0),
    "up": False,
    "down": False
}
dropdown_open = False
sorting_titles = ['Métodos',
                  'Bubble sort',
                  'Selection sort',
                  'Insertion sort',
                  'Quick sort',
                  'Merge sort']
current_sorting_method = 0

listSize = 30
floatList = [0]
delay = 30  # em dezenas de ms
old_pointer = []

TOP_BAR_COLOR = (50, 168, 151)
DROPDOWN_MARGIN_COLOR = (255, 255, 255)
DROPDOWN_FONT_COLOR = (255, 255, 255)
DROPDOWN_BACKGROUND_COLOR = (100, 100, 100)
DROPDOWN_BACKGROUND_HOVERED_COLOR = (90, 90, 90)
DROPDOWN_BACKGROUND_CLICKED_COLOR = (80, 80, 80)
BAR_COLOR = (255, 255, 255)
BAR_MARGIN_COLOR = (0, 0, 0)
BACKGROUND_COLOR = (0, 0, 30)
POINTER_COLOR = (255, 0, 0)


def clamp(n, smallest, largest): return max(smallest, min(n, largest))


def GetTextSurface(text, size=30, color=(255, 255, 255)):
    font = pg.font.SysFont('Futura', int(size))
    return font.render(text, True, color)


def mouseOverlaps(rect):
    return rect[0] < mouse['pos'][0] < rect[0] + rect[2] and rect[1] < mouse['pos'][1] < rect[1] + rect[3]


def DrawButton(surface, rect, defaultColor, hoverColor, clickColor, *args, **kwargs):
    if mouseOverlaps(rect):
        if mouse['down']:
            pg.draw.rect(surface, clickColor, rect)
        else:
            pg.draw.rect(surface, hoverColor, rect)
            onClickMethod = kwargs.get('onClick')
            onClickArgs = kwargs.get('onClickArgs')
            if onClickMethod and mouse['up']:
                if onClickArgs:
                    onClickMethod(*onClickArgs)
                else:
                    onClickMethod()
                return True
    else:
        pg.draw.rect(surface, defaultColor, rect)
    return False


def activateDropdownMenu():
    global dropdown_open
    dropdown_open = not dropdown_open


def setSortingMethod(i):
    global dropdown_open
    global current_sorting_method
    current_sorting_method = i
    dropdown_open = False


def generateFloatList():
    global floatList
    floatList = [0] * listSize
    for i in range(listSize):
        floatList[i] = random.uniform(0.0, 1.0)


def UpDownValue(Surface, pos, height, text, value):
    leftColor = (200, 0, 0)
    rightColor = (0, 200, 0)
    tint = (40, 40, 40)

    labelSurface = GetTextSurface(text, height / 2, (255, 255, 255))
    valueSurface = GetTextSurface(str(value), height / 2, (255, 255, 255))

    if mouseOverlaps((pos[0], pos[1], labelSurface.get_height() * 2, labelSurface.get_height() * 2)):
        leftColor = (clamp(leftColor[0] - tint[0], 0, 255), clamp(leftColor[1] - tint[1], 0, 255),
                     clamp(leftColor[2] - tint[2], 0, 255))
        if mouse['up']:
            value -= 1
    elif mouseOverlaps((pos[0] + labelSurface.get_height() * 2 + labelSurface.get_width(), pos[1],
                        labelSurface.get_height() * 2, labelSurface.get_height() * 2)):
        rightColor = (clamp(rightColor[0] - tint[0], 0, 255), clamp(rightColor[1] - tint[1], 0, 255),
                      clamp(rightColor[2] - tint[2], 0, 255))
        if mouse['up']:
            value += 1

    Surface.blit(labelSurface, (pos[0] + 2 * labelSurface.get_height(), pos[1]))
    Surface.blit(valueSurface, (
        pos[0] + labelSurface.get_width() * 0.5 + labelSurface.get_height() * 2 - valueSurface.get_width() * 0.5,
        pos[1] + labelSurface.get_height()))

    # seta esquerda
    pg.draw.polygon(Surface, color=leftColor,
                    points=[(pos[0], pos[1] + labelSurface.get_height()),
                            (pos[0] + 2 * labelSurface.get_height(), pos[1] + labelSurface.get_height()),
                            (pos[0] + labelSurface.get_height(), pos[1] + 2 * labelSurface.get_height())])
    pg.draw.rect(Surface, leftColor, (
        pos[0] + 0.6 * labelSurface.get_height(), pos[1],
        0.99 * labelSurface.get_height(), labelSurface.get_height()))

    # seta direita
    pg.draw.polygon(Surface, color=rightColor,
                    points=[(pos[0] + labelSurface.get_width() + labelSurface.get_height() * 2,
                             pos[1] + labelSurface.get_height()),
                            (pos[0] + labelSurface.get_width() + labelSurface.get_height() * 3,
                             pos[1]),
                            (pos[0] + labelSurface.get_width() + labelSurface.get_height() * 4,
                             pos[1] + labelSurface.get_height())
                            ])
    pg.draw.rect(Surface, rightColor, (
        pos[0] + 2.6 * labelSurface.get_height() + labelSurface.get_width(), pos[1] + labelSurface.get_height(),
        0.99 * labelSurface.get_height(), labelSurface.get_height()))

    return value


def Dropdown():
    global dropdown_open

    foi_interagido = False

    if dropdown_open:
        areaRect = (
            0.01 * reference, 0.01 * reference, 0.3 * reference, 0.051 + (0.041 * len(sorting_titles)) * reference)
        pg.draw.rect(screen, DROPDOWN_BACKGROUND_COLOR, areaRect)
        dropdown_open = mouseOverlaps(areaRect)
        drawnTitles = 1
        for i in range(len(sorting_titles)):
            if i != current_sorting_method:
                textSurface = GetTextSurface(sorting_titles[i], int(0.04 * reference))
                foi_interagido = foi_interagido or DrawButton(screen,
                                                              (
                                                                  0.01 * reference,
                                                                  (0.02 + drawnTitles * 0.04) * reference,
                                                                  0.3 * reference, 0.04 * reference),
                                                              DROPDOWN_BACKGROUND_COLOR,
                                                              DROPDOWN_BACKGROUND_HOVERED_COLOR,
                                                              DROPDOWN_BACKGROUND_CLICKED_COLOR,
                                                              onClick=setSortingMethod,
                                                              onClickArgs=[i])
                screen.blit(textSurface, (0.02 * reference, (0.03 + drawnTitles * 0.04) * reference))
                drawnTitles += 1
    # DropDown button
    areaRect = (0.01 * reference, 0.01 * reference, 0.3 * reference, 0.05 * reference)
    DrawButton(screen, areaRect, DROPDOWN_BACKGROUND_COLOR, DROPDOWN_BACKGROUND_HOVERED_COLOR,
               DROPDOWN_BACKGROUND_CLICKED_COLOR, onClick=activateDropdownMenu)

    pg.draw.rect(screen, DROPDOWN_MARGIN_COLOR,
                 (int(0.01 * reference), int(0.01 * reference), int(0.3 * reference), int(0.05 * reference)),
                 width=max(int(0.005 * reference), 1))
    pg.draw.polygon(screen, DROPDOWN_FONT_COLOR,
                    ([(0.28 * reference, 0.025 * reference), (0.265 * reference, 0.041 * reference),
                      (0.295 * reference, 0.041 * reference)] if dropdown_open
                     else [(0.28 * reference, 0.046 * reference), (0.265 * reference, 0.03 * reference),
                           (0.295 * reference, 0.03 * reference)]))
    screen.blit(GetTextSurface(sorting_titles[current_sorting_method], int(reference * 0.05)),
                (0.02 * reference, 0.02 * reference))
    return foi_interagido


def basicUI(swap=None, pointer=[], animatedPointerTransition=True):
    global screenSize
    global mouse
    global dropdown_open
    global delay
    global reference
    global old_pointer
    global listSize
    startTime = pg.time.get_ticks()
    progress = 0.0
    while progress < 1:

        mouse['up'] = False
        for e in pg.event.get():
            if e.type == pg.QUIT or (e.type == pg.KEYUP and e.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif e.type == pg.WINDOWRESIZED:
                screenSize = e.x, e.y
            elif e.type == pg.MOUSEMOTION:
                mouse['pos'] = e.pos
            elif e.type == pg.MOUSEBUTTONDOWN:
                if e.button == 1:
                    mouse['down'] = True
            elif e.type == pg.MOUSEBUTTONUP:
                if e.button == 1:
                    mouse['down'] = False
                    mouse['up'] = True

        reference = screenSize[1]

        areaRect = (0, 0, screenSize[0], screenSize[1] * 0.1)
        # top bar
        pg.draw.rect(screen, TOP_BAR_COLOR, areaRect)

        # bot area
        pg.draw.rect(screen, BACKGROUND_COLOR, (0, 0.1 * reference, screenSize[0], screenSize[1] * 0.9))

        bar_width = screenSize[0] / len(floatList)
        pointer_width = max(10, 0.01 * screenSize[0])

        # desenha o pointer
        for i in range(len(pointer)):
            if len(old_pointer) > i and animatedPointerTransition:
                lastPos = old_pointer[i]
            else:
                lastPos = pointer[i]
            pg.draw.rect(screen, POINTER_COLOR, (
                (bar_width * (lastPos + 0.5) - pointer_width * 0.5) * (1 - progress) + (
                        bar_width * (pointer[i] + 0.5) - pointer_width * 0.5) * progress,
                0.1 * reference, pointer_width, 0.9 * reference))

        # desenha as barras
        for i in range(len(floatList)):
            if swap is not None and i == swap[0]:
                xPos = (screenSize[0] / len(floatList)) * swap[0] * (1 - progress) + (screenSize[0] / len(floatList)) * \
                       swap[1] * progress
            elif swap is not None and i == swap[1]:
                xPos = (screenSize[0] / len(floatList)) * swap[0] * progress + (screenSize[0] / len(floatList)) * \
                       swap[1] * (1 - progress)
            else:
                xPos = (screenSize[0] / len(floatList)) * i

            rect = (xPos,
                    screenSize[1] - (0.9 * reference * floatList[i]),
                    screenSize[0] / len(floatList),
                    0.9 * reference * floatList[i])

            pg.draw.rect(screen, BAR_COLOR, rect)
            pg.draw.rect(screen, BAR_MARGIN_COLOR, rect, 1)

        # dropdown menu
        if Dropdown():
            return False

        # delay selector
        delay = UpDownValue(screen, (0.4 * reference, 0.01 * reference), 0.1 * reference, "delay (x10ms)", delay)

        # list size selector
        listSize = UpDownValue(screen, (0.8 * reference, 0.01 * reference), 0.1 * reference, "tamanho", listSize)

        pg.display.flip()
        progress = (pg.time.get_ticks() - startTime) / (delay * 10)

    old_pointer = pointer
    if swap is not None:
        floatList[swap[0]], floatList[swap[1]] = floatList[swap[1]], floatList[swap[0]]
    return True


def BubbleSort(V):
    deve_continuar = basicUI(pointer=[0])
    i = 0
    while i < (len(V) - 1) and deve_continuar:
        j = 0
        while j < (len(V) - 1 - i) and deve_continuar:
            swap = None
            if V[j] > V[j + 1]:
                swap = j, j + 1
            deve_continuar = basicUI(swap, pointer=[j + 1])
            j += 1
        i += 1
    if deve_continuar: deve_continuar = basicUI(pointer=[-1])
    return deve_continuar


def SelectionSort(v):
    deve_continuar = True
    i = 0
    while i < (len(v) - 1) and deve_continuar:
        menor = i
        j = i
        while j < len(v) and deve_continuar:
            if v[j] < v[menor]:
                menor = j
            deve_continuar = basicUI(pointer=[j])
            j += 1
        if deve_continuar:
            deve_continuar = basicUI(swap=(i, menor), pointer=[i])
            i += 1
    if deve_continuar: deve_continuar = basicUI(pointer=[len(v)])
    return deve_continuar


def InsertionSort(v):
    deve_continuar = basicUI(pointer=[0])
    # ainda não chegou ao final?
    i = 1
    while i < len(v) and deve_continuar:
        j = i - 1
        while j >= 0 and v[j] > v[j + 1] and deve_continuar:
            deve_continuar = basicUI(swap=(j, j + 1), pointer=[i])
            j -= 1
        i += 1
        deve_continuar = basicUI(pointer=[i])
    return deve_continuar


def QS_partition(lista, inicio, fim):
    pivo = lista[fim]
    i = inicio  # barra min
    j = inicio
    deve_continuar = True
    while j < fim and deve_continuar:  # barra max
        if lista[j] <= pivo:
            # swap
            deve_continuar = basicUI(swap=(i, j), pointer=[fim, i])
            i += 1
        j += 1

    if deve_continuar:
        deve_continuar = basicUI(swap=(i, fim), pointer=[fim, i])
    return i, deve_continuar


def QuickSort(lista, inicio=0, fim=None):
    if fim is None:
        fim = len(lista) - 1
    deve_continuar = True
    if inicio < fim:
        pivo, deve_continuar = QS_partition(lista, inicio, fim)
        if deve_continuar:
            deve_continuar = QuickSort(lista, inicio, pivo - 1)
            if deve_continuar:
                deve_continuar = QuickSort(lista, pivo + 1, fim)
    return deve_continuar


MergeSortPointers = []


def Merge(lista, inicio, fim):
    meio = (inicio + fim) // 2
    esquerda = lista[inicio:meio]
    direita = lista[meio:fim]
    top_e, top_d = 0, 0
    for k in range(inicio, fim):
        if top_e >= len(esquerda):
            lista[k] = direita[top_d]
            top_d += 1
        elif top_d >= len(direita):
            lista[k] = esquerda[top_e]
            top_e += 1
        elif esquerda[top_e] < direita[top_d]:
            lista[k] = esquerda[top_e]
            top_e += 1
        elif esquerda[top_e] >= direita[top_d]:
            lista[k] = direita[top_d]
            top_d += 1


def dividir_em_2(listas):
    r = []
    for l in listas:
        if len(l) > 1:
            r.append(l[0:int(len(l) / 2)])
            r.append(l[int(len(l) / 2):len(l)])
        else:
            r.append(l)
    return r


def MergeSort(lista):
    # Divisão
    listas = [lista]
    pointers = []
    divisores = []

    deve_continuar = basicUI()
    i = 0
    while i < math.ceil(math.log(len(lista), 2)) and deve_continuar:
        listas = dividir_em_2(listas)
        total = 0
        for j in range(len(listas) - 1):
            total += len(listas[j])
            if total not in divisores:
                divisores.append(total)
                pointers.append(total - 0.5)
        deve_continuar = basicUI(pointer=pointers)
        i += 1
    sorted_divisores = divisores.copy()
    sorted_divisores.sort()

    # União
    i = len(divisores) - 1
    while i > -1 and deve_continuar:
        divisor = divisores[i]

        start = divisores[i]
        del pointers[i]
        sorted_divisores.remove(divisor)
        print('divisor:', divisor)

        upper_limit = list(x for x in sorted_divisores if x > divisor)
        if len(upper_limit) == 0:
            end = len(lista)
        else:
            end = min(upper_limit)
        bottom_limit = list(x for x in sorted_divisores if x < divisor)
        if len(bottom_limit) == 0:
            start = 0
        else:
            start = max(bottom_limit)

        h = start
        while h < end - 1 and deve_continuar:

            menor = h
            j = h
            while j < end and deve_continuar:
                if lista[j] < lista[menor]:
                    menor = j
                j += 1
            deve_continuar = basicUI(swap=(h, menor), pointer=pointers)
            h += 1
        i -= 1
    return deve_continuar


def main():
    global screen
    global current_sorting_method
    pg.init()
    screen = pg.display.set_mode(screenSize, pg.RESIZABLE)
    pg.display.set_caption("Sort")

    pg.font.init()
    generateFloatList()
    while True:

        # se o metodo selecionado não for idle, cria uma lista e depois chama ele
        if current_sorting_method != 0:
            generateFloatList()
            sucesso = [BubbleSort, SelectionSort, InsertionSort, QuickSort, MergeSort][current_sorting_method - 1](
                floatList)
            # se tiver tido sucesso, vai pro idle
            if sucesso:
                current_sorting_method = 0
        else:
            basicUI()


if __name__ == '__main__':
    main()
