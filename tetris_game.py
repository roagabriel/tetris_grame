import pygame
import random
from pygame.locals import *
#MUITO PROBLEMA FODA-SE

#REFERENCE IMAGES
PIECES = [('1.png', (1, 4)), ('L.png', (2, 3)), ('R.png', (2, 2)), ('S.png', (3, 2)), ('T_2.png', (3, 2))]
#SCREEN DIMENSIONS
def scale(x):
    return int(x*0.70)

SCREEN_WIDTH = scale(590)
SCREEN_HEIGHT = scale(960)
TILE_SIZE = scale(40)

LEFT_LINE = scale(16)
RIGHT_LINE = scale(400)
BOTTOM_LINE = scale(920)
TOP_LINE = scale((960 - (43*20)))

NEXT_X = scale(450)
NEXT_Y = scale(190)

drop_speed = TILE_SIZE

def bottom_limit(sprite):
    return sprite.rect[1] + sprite.rect[3]

def on_ground(piece):
    return bottom_limit(piece) >= BOTTOM_LINE

def get_random_piece(rescale = 0.5):
    piece_name, tiles = random.choice(PIECES)
    assert_path = f'assets/{piece_name}'
    print(f"Asset: {assert_path}")
    image = pygame.image.load(assert_path).convert_alpha()

    new_size = (tiles[0]*TILE_SIZE,tiles[1]*TILE_SIZE)
    scaled_image = pygame.transform.scale(image,new_size)

    return scaled_image

def fix_sprite_height(sprite):
    if on_ground(sprite):
        sprite.rect[1] = BOTTOM_LINE - sprite.rect[3]
        return sprite

    sprite.rect[1] = BOTTOM_LINE - ((BOTTOM_LINE - sprite.rect[1])//TILE_SIZE + 1) * TILE_SIZE
    return sprite

class Piece(pygame.sprite.Sprite):
    def __init__(self,next = False):
        pygame.sprite.Sprite.__init__(self)

        # USEF FOR THE NEXT PIECE
        if next:
            self.image = get_random_piece()
            self.rect = self.image.get_rect()
            self.rect[0], self.rect[1] = (NEXT_X,NEXT_Y)
        else:
            self.image = get_random_piece()
            self.rect = self.image.get_rect()
            self.rect[0] = LEFT_LINE
            self.rect[1] = TOP_LINE

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[1] += drop_speed

    def undo_update(self):
        self.rect[1] -= drop_speed

    def move_left(self):
        if self.rect[0] > LEFT_LINE:
            self.rect[0] -= TILE_SIZE

    def move_right(self):
        #IF WIDTH + BLOCK POSITION ARE WITHIN THE BORDER
        if self.rect[0] + self.rect[2] < RIGHT_LINE:
            self.rect[0] += TILE_SIZE
    def move_down(self):
        if self.rect[1] + self.rect[3] < BOTTOM_LINE:
            self.rect[1] += TILE_SIZE

    def rotate(self):
        self.image = pygame.transform.rotate(self.image,-90)
        self.mask = pygame.mask.from_surface(self.image)

    def reset(self):
        self.rect[0] = LEFT_LINE
        self.rect[1] = TOP_LINE

#MAIN()
pygame.init()
BACKGROUND = pygame.image.load('assets/background.jpg')
new_size = (SCREEN_WIDTH,SCREEN_HEIGHT)
BACKGROUND = pygame.transform.scale(BACKGROUND,new_size)
screen = pygame.display.set_mode(new_size)

current_piece = Piece()
current_group = pygame.sprite.GroupSingle()
current_group.add(current_piece)

next_piece = Piece(next = True)
next_group = pygame.sprite.GroupSingle()
next_group.add(next_piece)

ground_pieces = pygame.sprite.Group()

#CLOCK
clock = pygame.time.Clock()

while True:
    clock.tick(3)

    #EVENTS
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_q:
                pygame.quit()
                exit()
            if event.key == K_LEFT:
                current_group.sprite.move_left()
            if event.key == K_RIGHT:
                current_group.sprite.move_right()
            if event.key == K_DOWN:
               current_group.sprite.move_down()
            if event.key == K_UP:
                current_group.sprite.rotate()

    current_group.sprite.update()

    #CHECK IF MOVING CAUSEF ANY COLLISIONS OR COMPLETE ROWS AND FIX
    if (pygame.sprite.spritecollideany(current_group.sprite, ground_pieces, pygame.sprite.collide_mask) or on_ground(current_group.sprite)):
        #THE CURRENT SPRITE MIGHT HAVE "ENTERED" IN OTHER SPRITES
        #current_group.sprite = fix_sprite_height(current_group.sprite)
        if not on_ground(current_group.sprite):
            current_group.sprite.undo_update()

        ground_pieces.add(current_group.sprite)
        current_group.add(next_group.sprite)
        current_group.sprite.reset()

        next_group.add(Piece(next=True))

    #CLEAR THE SCREEN WITH BACKGROUND
    screen.blit(BACKGROUND,(0,0))

    #UPDATE THE PIECES SPRITE ON SCREEN
    current_group.draw(screen)
    next_group.draw(screen)

    ground_pieces.draw(screen)

    pygame.display.update()