#Memory Game by Beckx
#



import pygame, sys, random, os
from pygame.locals import *


WIN_WIDTH = 1024
WIN_HEIGHT = 768
BOX_SIZE = 150
GAP_SIZE = 20

COL = 4



def main():
    global FPSCLOCK, DISPLAYSURF, ICONS
    pygame.init()

    DISPLAYSURF = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT), SRCALPHA, 32)

    bg_image_path = os.path.join("motives", "bg_page.jpg")
    bg_image = pygame.image.load(bg_image_path)
    bg_image = pygame.transform.smoothscale(bg_image, (WIN_WIDTH, WIN_HEIGHT)).convert()
    DISPLAYSURF.blit(bg_image,(0,0))

    #IMAGES = loadIconImgs()

    #stores x and y coordinates of mouse event
    mousex = 0
    mousey = 0

    new_game_image_path = os.path.join("motives", "new_button.png")
    new_game = pygame.image.load(new_game_image_path)
    new_game = pygame.transform.smoothscale(new_game,(250,75)).convert_alpha()
    new_rect = new_game.get_rect()
    new_rect.move_ip(WIN_WIDTH - 260,WIN_HEIGHT - 150)

    ICONS=create_icons()

    first_revealed = None
    mouse_clicked = False
    draw_board()
    DISPLAYSURF.blit(new_game, new_rect)

    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEMOTION:
                mousey, mousex = event.pos

            elif event.type == MOUSEBUTTONDOWN:

                if first_revealed is None:
                    first_revealed = get_icon(mousex, mousey) # returns None if no icon at point
                    if first_revealed is not None:
                        DISPLAYSURF.blit(bg_image, first_revealed.pos,first_revealed.pos)
                        first_revealed.display_image = first_revealed.image

                        DISPLAYSURF.blit(first_revealed.display_image,first_revealed.pos)
                        first_revealed.clickable = False

                if new_rect.collidepoint(mousey,mousex):
                    # new game button clicked ;  create new Game
                    ICONS = create_icons()
                    DISPLAYSURF.blit(bg_image,(0,0))
                    draw_board()
                    DISPLAYSURF.blit(new_game, new_rect)
                mouse_clicked = True

            else: mouse_clicked = False



        for icon in ICONS:
            if mouse_clicked and first_revealed is None and icon.pos != first_revealed.pos:

                if icon.pos.collidepoint(mousey, mousex):
                    #show icon image
                    DISPLAYSURF.blit(bg_image, icon.pos,icon.pos)
                    icon.display_image = icon.image
                    DISPLAYSURF.blit(icon.display_image,icon.pos)
                    pygame.display.update()


                    if first_revealed.name == icon.name: #got a pair
                        icon.clickable = False
                        first_revealed = None
                    else :
                        #show icon image a little while
                        pygame.time.delay(200)
                        # reset turn
                        icon.display_image = icon.cover
                        first_revealed.display_image = first_revealed.cover
                        icon.clickable = True
                        first_revealed.clickable = True
                        DISPLAYSURF.blit(bg_image, icon.pos,icon.pos)
                        DISPLAYSURF.blit(icon.display_image,icon.pos)

                        DISPLAYSURF.blit(bg_image, first_revealed.pos, first_revealed.pos)
                        DISPLAYSURF.blit(first_revealed.display_image, first_revealed.pos)

                        first_revealed = None

        # change mouse cursor if above clickable item
        if any((icon.pos.collidepoint(mousey,mousex) and icon.clickable) for icon in ICONS) or new_rect.collidepoint(mousey,mousex) :
            pygame.mouse.set_cursor(*pygame.cursors.diamond)
        else:
            pygame.mouse.set_cursor(*pygame.cursors.broken_x)

        pygame.display.update()



def get_icon(mousex, mousey):
    for icon in ICONS:
        if icon.pos.collidepoint(mousey,mousex):
            return icon

def draw_board():
    board_height = WIN_HEIGHT - 100
    board_width = WIN_WIDTH - 100

    board = pygame.Surface((board_width,board_height), SRCALPHA , 32)
    board_rect = board.get_rect(center=((DISPLAYSURF.get_rect().center)))
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





def create_icons():

    icons = []
    for name in ("flower", "bottle"):
        for num in range (1, 4):

            image_path = os.path.join("motives", "{}_{}.png".format(name, num))

            img = pygame.image.load(image_path).convert_alpha()
            image = pygame.transform.smoothscale(img, (BOX_SIZE,BOX_SIZE))
            icon_name = "{}_{}".format(name, num)
            for x in range(2):
                icons.append(Icon(icon_name, image))
    return icons



class Icon:
    def __init__(self,name,image):
        self.name = name
        self.image = image
        self.cover = pygame.transform.smoothscale(pygame.image.load('motives/cover.png'),(BOX_SIZE,BOX_SIZE)).convert_alpha()
        self.pos = self.image.get_rect()
        self.clickable = True

        self.display_image=self.cover


if __name__=='__main__':
    main()
