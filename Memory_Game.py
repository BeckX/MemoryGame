#Memory Game by Beckx
#



import pygame, sys, random, copy
from pygame.locals import *


WIN_WIDTH = 1024
WIN_HEIGHT = 768
BOX_SIZE = 150
GAP_SIZE = 20

COL = 4
ROWS = 3


def main():
    global FPSCLOCK, DISPLAYSURF, ICONS, IMAGES
    pygame.init()

    DISPLAYSURF = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT), SRCALPHA, 32)

    bg_image = pygame.image.load('motives/bg_page.jpg')
    bg_image = pygame.transform.smoothscale(bg_image, (WIN_WIDTH, WIN_HEIGHT))
    DISPLAYSURF.blit(bg_image,(0,0))

    IMAGES = loadIconImgs()

    #stores x and y coordinates of mouse event
    mousex = 0
    mousey = 0

    new_game = pygame.image.load('motives/new_button.png')
    new_game = pygame.transform.smoothscale(new_game,(250,75))
    new_rect = new_game.get_rect()
    new_rect.move_ip(WIN_WIDTH - 260,WIN_HEIGHT - 150)

    ICONS=createIcons()

    firstRevealed = None
    mouseClicked = False
    drawBoard()
    DISPLAYSURF.blit(new_game, new_rect)

    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEMOTION:
                mousey, mousex = event.pos

            elif event.type == MOUSEBUTTONDOWN:

                if firstRevealed == None:
                    firstRevealed = getIcon(mousex,mousey) # returns None if no icon at point
                    if firstRevealed != None:
                        DISPLAYSURF.blit(bg_image, firstRevealed.pos,firstRevealed.pos)
                        firstRevealed.displayImage = firstRevealed.image

                        DISPLAYSURF.blit(firstRevealed.displayImage,firstRevealed.pos)
                        firstRevealed.clickable = False

                if new_rect.collidepoint(mousey,mousex):
                    # new game button clicked ;  create new Game
                    ICONS = createIcons()
                    DISPLAYSURF.blit(bg_image,(0,0))
                    drawBoard()
                    DISPLAYSURF.blit(new_game, new_rect)
                mouseClicked = True

            else: mouseClicked = False



        for icon in ICONS:
            if mouseClicked and firstRevealed != None and icon.pos != firstRevealed.pos:

                if icon.pos.collidepoint(mousey, mousex):
                    #show icon image
                    DISPLAYSURF.blit(bg_image, icon.pos,icon.pos)
                    icon.displayImage = icon.image
                    DISPLAYSURF.blit(icon.displayImage,icon.pos)
                    pygame.display.update()


                    if firstRevealed.name == icon.name: #got a pair
                        icon.clickable = False
                        firstRevealed = None
                    else :
                        #show icon image a little while
                        pygame.time.delay(200)
                        # reset turn
                        icon.displayImage = icon.cover
                        firstRevealed.displayImage = firstRevealed.cover
                        icon.clickable = True
                        firstRevealed.clickable = True
                        DISPLAYSURF.blit(bg_image, icon.pos,icon.pos)
                        DISPLAYSURF.blit(icon.displayImage,icon.pos)

                        DISPLAYSURF.blit(bg_image, firstRevealed.pos, firstRevealed.pos)
                        DISPLAYSURF.blit(firstRevealed.displayImage, firstRevealed.pos)

                        firstRevealed = None

        # change mouse cursor if above clickable item
        if any((icon.pos.collidepoint(mousey,mousex) and icon.clickable) for icon in ICONS) or new_rect.collidepoint(mousey,mousex) :
            pygame.mouse.set_cursor(*pygame.cursors.diamond)
        else:
            pygame.mouse.set_cursor(*pygame.cursors.broken_x)

        pygame.display.update()



def getIcon(mousex, mousey):
    for icon in ICONS:
        if icon.pos.collidepoint(mousey,mousex):
            return icon

def drawBoard():
    board_height = WIN_HEIGHT - 100
    board_width = WIN_WIDTH - 100

    board = pygame.Surface((board_width,board_height), SRCALPHA , 32)
    board_rect = board.get_rect(center=((get_screen_center(DISPLAYSURF))))
    #board.fill((255,255,255))



    box_x = board_rect.x + GAP_SIZE
    box_y = board_rect.y + GAP_SIZE
    distance = BOX_SIZE + GAP_SIZE
    icons=ICONS
    col_count=0

    random.shuffle(icons)
    DISPLAYSURF.blit(board,board_rect)
    for icon in icons:

        if col_count == COL:
            # begin new row
            box_x = board_rect.x + GAP_SIZE
            box_y += distance
            col_count=0

        icon.pos.move_ip(box_x,box_y)
        icon.clickable = True
        icon.displayImage = icon.cover
        box_x += BOX_SIZE + GAP_SIZE

        DISPLAYSURF.blit(icon.displayImage,icon.pos)

        col_count+=1




def get_screen_center(surface):
    centerx = (surface.get_width()) // 2
    centery = (surface.get_height()) // 2
    return (centerx, centery)


def get_screen_centerx(surface):
    centerx = (surface.get_width()) // 2
    return centerx


def get_screen_centery(surface):
    centery = (surface.get_height()) // 2
    return centery


def createIcons():
    images = IMAGES
    icons = []
    flower_1 = Icon('flower_1',images[0])
    icons.append(flower_1)
    flower_2 = Icon('flower_2', images[1])
    icons.append(flower_2)
    flower_3 = Icon('flower_3', images[2])
    icons.append(flower_3)
    bottle_1 = Icon('bottle_1', images[3])
    icons.append(bottle_1)
    bottle_2 = Icon('bottle_2', images[4])
    icons.append(bottle_2)
    bottle_3 = Icon('bottle_3', images[5])
    icons.append(bottle_3)

    flower_1_1 = Icon('flower_1',images[0])
    icons.append(flower_1_1)
    flower_2_2 = Icon('flower_2', images[1])
    icons.append(flower_2_2)
    flower_3_3 = Icon('flower_3', images[2])
    icons.append(flower_3_3)
    bottle_1_1 = Icon('bottle_1', images[3])
    icons.append(bottle_1_1)
    bottle_2_2 = Icon('bottle_2', images[4])
    icons.append(bottle_2_2)
    bottle_3_3 = Icon('bottle_3', images[5])
    icons.append(bottle_3_3)

    return icons


def loadIconImgs():
    images=[]
    images.append(pygame.image.load('motives/flower_1.png'))
    images.append(pygame.image.load('motives/flower_2.png'))
    images.append(pygame.image.load('motives/flower_3.png'))
    images.append(pygame.image.load('motives/bottle_1.png'))
    images.append(pygame.image.load('motives/bottle_2.png'))
    images.append(pygame.image.load('motives/bottle_3.png'))
    images=[pygame.transform.smoothscale(i, (BOX_SIZE,BOX_SIZE))for i in images]
    return images

class Icon:
    def __init__(self,name,image):
        self.name = name
        self.image = image
        self.cover = pygame.transform.smoothscale(pygame.image.load('motives/cover.png'),(BOX_SIZE,BOX_SIZE))
        self.pos = self.image.get_rect()
        self.clickable = True

        self.displayImage=self.cover


if __name__=='__main__':
    main()
