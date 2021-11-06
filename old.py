'''
Visualização de algorítmos de ordenação
Este script depende da biblioteca PyGame (S2)

Por Tito Guidotti
14/10/2021

Os comentários estão uma bagunça, parte em inglês e parte em português...
'''

import random
import pygame as pg

# Constants
METODO = 0
METODO_PROPOSTO = 1
LISTA = 2
I = 3
J = 4
SWAP = 5
INDICADOR = 6
TIME = 7
AUX = 8

LIST_SIZE = 20


def clamp(n, smallest, largest): return max(smallest, min(n, largest))


def GetTextSurface(text, size=30, color=(255, 255, 255)):
    font = pg.font.SysFont('Futura', int(size))
    return font.render(text, True, color)


def Button(surface, pos, height, text, backgroundColor, marginColor, textColor=(255, 255, 255),
           tint=(50, 50, 50), margin=0, mouseEvent=None, clickMethod=None, clickMethodArgs=None):
    textSurface = GetTextSurface(text, height, textColor)
    if mouseEvent is not None:
        if pos[0] < mouseEvent[0] < pos[0] + textSurface.get_width() and \
                pos[1] < mouseEvent[1] < pos[1] + textSurface.get_height():
            backgroundColor = clamp(backgroundColor[0] + tint[0], 0, 255), \
                              clamp(backgroundColor[1] + tint[1], 0, 255), \
                              clamp(backgroundColor[2] + tint[2], 0, 255)
            if mouseEvent[2] and clickMethod is not None:
                if clickMethodArgs is None:
                    clickMethod()
                else:
                    clickMethod(clickMethodArgs)

    pg.draw.rect(surface, marginColor,
                 (pos[0], pos[1], textSurface.get_width() + 2 * margin, textSurface.get_height() + 2 * margin))

    pg.draw.rect(surface, backgroundColor,
                 (pos[0] + margin, pos[1] + margin, textSurface.get_width(), textSurface.get_height()))
    surface.blit(textSurface, (pos[0] + margin, pos[1] + margin))


def UpDownValue(Surface, pos, height, text, value, mouseEvent):
    leftColor = (200, 0, 0)
    rightColor = (0, 200, 0)
    tint = (40, 40, 40)

    labelSurface = GetTextSurface(text, height / 2, (255, 255, 255))
    valueSurface = GetTextSurface(str(value), height / 2, (255, 255, 255))

    if pos[0] < mouseEvent[0] < pos[0] + labelSurface.get_height() * 2 and pos[1] < mouseEvent[1] < pos[
        1] + labelSurface.get_height() * 2:
        leftColor = (clamp(leftColor[0] - tint[0], 0, 255), clamp(leftColor[1] - tint[1], 0, 255),
                     clamp(leftColor[2] - tint[2], 0, 255))
        if mouseEvent[2]:
            value -= 1

    elif pos[0] + labelSurface.get_height() * 2 + labelSurface.get_width() < mouseEvent[0] < pos[
        0] + labelSurface.get_height() * 4 + labelSurface.get_width() and pos[1] < mouseEvent[1] < pos[
        1] + labelSurface.get_height() * 2:
        rightColor = (clamp(rightColor[0] - tint[0], 0, 255), clamp(rightColor[1] - tint[1], 0, 255),
                      clamp(rightColor[2] - tint[2], 0, 255))
        if mouseEvent[2]:
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


# List
def GenerateRandomFloatList(args):
    for i in range(len(args), 0, -1):
        del args[i - 1]
    for i in range(LIST_SIZE):
        args.append(random.uniform(0, 1))


def SetsortData(args):
    args[METODO] = args[METODO_PROPOSTO]
    GenerateRandomFloatList(args[LISTA])
    args[I] = 0
    args[J] = 0
    args[SWAP] = [-1, -1]
    args[INDICADOR] = 0
    args[TIME] = pg.time.get_ticks()


def BubbleSort(V, currentI, currentJ, aux):
    swap = [-1, -1]
    if currentI < len(V) - 1:
        if currentJ < len(V) - 1 - currentI:
            if V[currentJ] > V[currentJ + 1]:
                swap = [currentJ, currentJ + 1]
            currentJ += 1
            return V, currentI, currentJ, swap, currentJ, -1
        currentI += 1
        currentJ = 0

        return V, currentI, currentJ, swap, currentJ, -1
    else:
        return V, currentI, currentJ, swap, -1, -1


def SelectionSort(V, currentI, currentJ, menor):
    swap = [-1, -1]
    if currentI < (len(V) - 1):
        if currentJ < len(V):
            if V[currentJ] < V[menor]:
                menor = currentJ
            currentJ += 1
            return V, currentI, currentJ, swap, currentJ, menor
        swap = [currentI, menor]
        currentI += 1
        currentJ = currentI
        return V, currentI, currentJ, swap, currentJ, currentI
    return V, currentI, currentJ, swap, -1, -1


def InsertionSort(V, currentI, currentJ, aux):
    # Está com a lista ordenada já?
    if currentI >= len(V):
        return V, currentI, currentJ, [-1, -1], -1, -1
    else:
        # item atual ainda não chegou na primeira posicao e é menor q o anterior?
        if currentI - currentJ >= 1:
            if (V[currentI - currentJ - 1]) > (V[currentI - currentJ]):
                swap = [currentI - currentJ - 1, currentI - currentJ]
                currentJ += 1
                return V, currentI, currentJ, swap, currentI, -1
            else:
                currentI += 1
                currentJ = 0
                return V, currentI, currentJ, [-1, -1], currentI, -1
        else:
            # passa para o proximo item
            currentI += 1
            currentJ = 0
            return V, currentI, currentJ, [-1, -1], currentI, -1


def main():
    global LIST_SIZE
    screenSize = (800, 600)
    pg.init()
    screen = pg.display.set_mode(screenSize, pg.RESIZABLE)
    pg.display.set_caption("Sort")

    swapTime = 300
    floatList = [0.5] * LIST_SIZE
    # Metodo, Metodo proposto, floatList, i, j, swap, indicador, time
    sortData = [None, None, floatList, 0, 0, [-1, -1], -1, pg.time.get_ticks(), -1]
    previousIndicator = -1

    # enable font usage
    pg.font.init()

    # Colors
    buttonMarginColor = 240, 240, 240
    buttonBackgroundColor = 0, 0, 0
    selectedButtonBackground = 30, 30, 30
    white = 255, 240, 200
    black = 20, 20, 40

    mouseEvent = [0, 0, False]
    # main game loop
    done = 0
    while not done:
        mouseEvent[2] = False
        for e in pg.event.get():
            if e.type == pg.QUIT or (e.type == pg.KEYUP and e.key == pg.K_ESCAPE):
                done = 1
                break
            if e.type == pg.WINDOWRESIZED:
                screenSize = e.x, e.y
            if e.type == pg.MOUSEMOTION:
                mouseEvent[0] = e.pos[0]
                mouseEvent[1] = e.pos[1]
            if e.type == pg.MOUSEBUTTONUP:
                mouseEvent[2] = True

        screen.fill(black)
        reference = screenSize[1]

        # Button "Bubble Sort"
        sortData[1] = BubbleSort
        Button(screen, (0.01 * reference, 0.01 * reference), 0.06 * reference, "Bubble Sort",
               buttonBackgroundColor, buttonMarginColor, margin=1, mouseEvent=mouseEvent,
               clickMethod=SetsortData, clickMethodArgs=sortData)

        # Button "Selection Sort"
        sortData[1] = SelectionSort
        Button(screen, (0.255 * reference, 0.01 * reference), 0.06 * reference, "Selection Sort",
               buttonBackgroundColor, buttonMarginColor, margin=1, mouseEvent=mouseEvent,
               clickMethod=SetsortData, clickMethodArgs=sortData)

        # Button "Insertion Sort"
        sortData[1] = InsertionSort
        Button(screen, (0.547 * reference, 0.01 * reference), 0.06 * reference, "Insertion Sort",
               buttonBackgroundColor, buttonMarginColor, margin=1, mouseEvent=mouseEvent,
               clickMethod=SetsortData, clickMethodArgs=sortData)

        # Control Tamnho da Lista
        LIST_SIZE = max(UpDownValue(screen, (0.85 * reference, 0.01 * reference), 0.06 * reference, "Tamanho",
                                    LIST_SIZE, mouseEvent), 1)

        # Control Delay
        swapTime = 10 * max(
            UpDownValue(screen, (1.05 * reference, 0.01 * reference), 0.06 * reference, "Delay(em 10ms)",
                        int(swapTime / 10), mouseEvent), 0)

        if swapTime <= 0:
            progress = 1
        else:
            progress = (pg.time.get_ticks() - sortData[TIME]) / swapTime

        if progress >= 1 and sortData[0] is not None:
            previousIndicator = sortData[INDICADOR]
            floatList, sortData[3], sortData[4], sortData[5], sortData[6], sortData[AUX] = sortData[0](floatList,
                                                                                                       sortData[3],
                                                                                                       sortData[4],
                                                                                                       sortData[AUX])
            if sortData[5] != (-1, -1):
                aux = floatList[sortData[5][0]]
                floatList[sortData[5][0]] = floatList[sortData[5][1]]
                floatList[sortData[5][1]] = aux

            sortData[7] = pg.time.get_ticks()

        # Barras
        barMargin = 1  # max(0.001 * screenSize[1], 1)
        barMaxHeight = screenSize[1] * 0.9
        barWidth = (screenSize[0] - barMargin) / len(floatList) - barMargin

        pg.draw.rect(screen, (255, 0, 0, 0),
                     (int(
                         progress * ((barWidth + barMargin) * (sortData[6] + 0.5)) +
                         (1.0 - progress) * (barWidth + barMargin) * (previousIndicator + 0.5)
                     ),
                      int(screenSize[1] - barMaxHeight),
                      int(screenSize[0] * 0.01),
                      int(barMaxHeight)))

        for i in range(len(floatList)):
            if i == sortData[5][0]:
                xPos = ((barMargin + i * (barWidth + barMargin)) * progress + (
                        barMargin + sortData[5][1] * (barWidth + barMargin)) * (1.0 - progress))
            elif i == sortData[5][1]:
                xPos = ((barMargin + i * (barWidth + barMargin)) * progress + (
                        barMargin + sortData[5][0] * (barWidth + barMargin)) * (1.0 - progress))
            else:
                xPos = barMargin + i * (barWidth + barMargin)

            pg.draw.rect(screen, black,
                         (int(xPos - barMargin), int(screenSize[1] - (barMaxHeight * floatList[i]) - barMargin),
                          int(barWidth + (2 * barMargin)),
                          int(barMaxHeight * floatList[i] + (2 * barMargin))))
            pg.draw.rect(screen, white,
                         (int(xPos), int(screenSize[1] - (barMaxHeight * floatList[i])),
                          int(barWidth),
                          int(barMaxHeight * floatList[i])))

        pg.display.update()

    pg.quit()


# if python says run, then we should run
if __name__ == "__main__":
    main()
