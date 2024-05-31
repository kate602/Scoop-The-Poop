import random
import pygame as pg

# --CONSTANTS--
# COLOURS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
EMERALD = (21, 219, 147)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

WIDTH = 1200
HEIGHT = 900
SCREEN_SIZE = (WIDTH, HEIGHT)

DOG = pg.image.load("./Images/dog.webp")
DOG = pg.transform.scale(
    DOG, (DOG.get_width() // 20, DOG.get_height() // 20))  

PEOPLE = pg.image.load("./Images/people.png")
PEOPLE = pg.transform.scale(
    PEOPLE, (PEOPLE.get_width() // 7, PEOPLE.get_height() // 7))  

POOP = pg.image.load("./Images/poop.png")
POOP = pg.transform.scale(
    POOP, (POOP.get_width() // 12, POOP.get_height() // 12))
  
BACKGROUND = pg.image.load("./Images/dirtbg.jpg")
BACKGROUND = pg.transform.scale(BACKGROUND, (1200, 900))

class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = DOG
        self.rect = self.image.get_rect()
        # Initialize velocity
        self.vel_x = 0
        self.vel_y = 0

    def update(self):
        # Moves left and right
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

    def go_left(self):
        self.vel_x = -5
        self.image = pg.transform.flip(DOG, True, False)

    def go_right(self):
        self.vel_x = 5
        self.image = DOG

    def go_up(self):
        self.vel_y = -5
        self.image = DOG

    def go_down(self):
        self.vel_y = 5
        self.image = DOG



    # Stop function
    def stop(self):
        self.vel_x = 0
        self.vel_y = 0
 

class Poop(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = POOP
        self.rect = self.image.get_rect()

        # spawns in random location
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(0, HEIGHT - self.rect.height)

class Enemy(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = PEOPLE
        self.rect = self.image.get_rect()

        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = HEIGHT - 200

        self.vel_x = -6
    

    def update(self):
        self.rect.x += self.vel_x

        if self.rect.left < 0:
            self.rect.left = 0
            self.vel_x = -self.vel_x
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.vel_x = -self.vel_x
    

class Wall(pg.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
 
        self.image = pg.image.load("./Images/bush.webp")
        self.image = pg.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()


def start():
    """Environment Setup and Game Loop"""

    pg.init()
    pg.display.set_caption("Collect the Poop!")

    # --Game State Variables--
    screen = pg.display.set_mode(SCREEN_SIZE)
    done = False
    clock = pg.time.Clock()
    score = 0
    font = pg.font.SysFont("Futura", 24)

    # sprite groups
    all_sprites = pg.sprite.Group()
    player_sprites = pg.sprite.Group()
    poop_sprites = pg.sprite.Group()
    enemy_sprites = pg.sprite.Group()
    wall_sprites = pg.sprite.Group()

    # create player sprite object
    player = Player()
    all_sprites.add(player)
    player_sprites.add(player)

    # create enemy sprite objects
    for _ in range(1):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemy_sprites.add(enemy)

    # create poop
    for _ in range(10):
        poop = Poop()

        all_sprites.add(poop)
        poop_sprites.add(poop)


    # create walls
    #(width, height, x, y)
    walls = [[200, 80, 0, 500],
             [200, 80, 180, 500],
             [200, 80, 360, 500],
             [200, 80, 540, 500],
             [200, 80, 900, 500],
                 ]
    
    for wall in walls:
        block = Wall(wall[0], wall[1])
        block.rect.x = wall[2]
        block.rect.y = wall[3]

        all_sprites.add(block)

    # --Main Loop--
    while not done:
        # --- Event Listener
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True

            # moves player using arrow key functions
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RIGHT:
                    player.go_right()
                if event.key == pg.K_LEFT:
                    player.go_left()
                if event.key == pg.K_UP:
                    player.go_up()
                if event.key == pg.K_DOWN:
                    player.go_down()

            # Stop player if arrow key is released
            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT and player.vel_y != 0 or player.vel_x != 0:
                    player.stop()
                if event.key == pg.K_RIGHT and player.vel_y != 0 or player.vel_x != 0:
                    player.stop()
                if event.key == pg.K_UP and player.vel_y != 0 or player.vel_x != 0:
                    player.stop()
                if event.key == pg.K_DOWN and player.vel_y != 0 or player.vel_x != 0:
                    player.stop()

        # keep player on screen
        if player.rect.right > WIDTH:
            player.rect.right = WIDTH
        if player.rect.left < 0:
            player.rect.left = 0
        if player.rect.top > HEIGHT-50:
            player.rect.top = HEIGHT-50
        if player.rect.bottom < 50:
            player.rect.bottom = 50

        # --- Update the world state
        all_sprites.update()

        # --- Draw items
        screen.fill(BLACK)

        all_sprites.draw(screen)

        score_image = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_image, (5, 5))

        # Update the screen with anything new
        pg.display.flip()

        # --- Tick the Clock
        clock.tick(60)  # 60 fps


        # increase score once dog collects poop
        poop_collected = pg.sprite.spritecollide(player, poop_sprites, True)

        for poop in poop_collected:
              score += 1
              poop.kill()

        # stop game if caught by people
        gameend = pg.sprite.spritecollide(player, enemy_sprites, False)
        if len(gameend) > 0:
            player.kill()


def main():
    start()


if __name__ == "__main__":
    main()
