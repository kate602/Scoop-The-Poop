import random
import pygame as pg

# --CONSTANTS--
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

WIDTH = 1200
HEIGHT = 600
GROUND = 410
SCREEN_SIZE = (WIDTH, HEIGHT)

DOG = pg.image.load("./Images/dog.webp")
DOG = pg.transform.scale(
    DOG, (DOG.get_width() // 12, DOG.get_height() // 12))  

PEOPLE = pg.image.load("./Images/people.png")
PEOPLE = pg.transform.scale(
    PEOPLE, (PEOPLE.get_width() // 2, PEOPLE.get_height() // 2)) 
PEPOPLE = pg.transform.flip(PEOPLE, True, False)

POOP = pg.image.load("./Images/poop.png")
POOP = pg.transform.scale(
    POOP, (POOP.get_width() // 12, POOP.get_height() // 12))
  
BACKGROUND = pg.image.load("./Images/bg.jpg")
BACKGROUND = pg.transform.scale(BACKGROUND, (1200, 600))

BASKET = pg.image.load("./Images/basket.png")
BASKET = pg.transform.scale(
    BASKET, (BASKET.get_width() // 2, BASKET.get_height() // 2))

ENEMY = pg.image.load("./Images/cat.png")
ENEMY = pg.transform.scale(
    ENEMY, (ENEMY.get_width() // 6, ENEMY.get_height() // 6))

class Background(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # creates the background
        self.image = BACKGROUND
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # creating the image, starting position, velocity
        self.image = DOG
        self.rect = self.image.get_rect()
        self.rect.x = 600
        self.rect.y = 450
        self.vel_x = 0
        self.vel_y = 0

    # gravity always exists as well as the ability to move around
    def update(self):
        self.grav()

        # Moves left and right and up and down
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
    
    # flips the player and moves it left
    def go_left(self):
        self.vel_x = -7
        self.image = pg.transform.flip(DOG, True, False)

    # moves the player right
    def go_right(self):
        self.vel_x = 7
        self.image = DOG

    # moves the player up when jumping
    def jump(self):
        self.vel_y = -10
    
    # moves the player down due to gravity
    def grav(self):
        if self.vel_y == 0:
            self.vel_y = 1
        else:
            self.vel_y += .25
        
        # stop player when lands on ground
        if self.rect.y >= GROUND and self.vel_y >= 0:
            self.vel_y = 0
            self.rect.y = GROUND

    # stops movement
    def stop(self):
        self.vel_x = 0
        self.vel_y = 0
 
class Poop(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # creates the image
        self.image = POOP
        self.rect = self.image.get_rect()

        # spawns in random location in air
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = 0
        self.vel_y = 5
        
    def update(self):
        self.rect.y += self.vel_y

class Basket(pg.sprite.Sprite):
    def __init__(self, player: Player):
        super().__init__()

        # creates the image
        self.image = BASKET
        self.rect = self.image.get_rect()
        self.rect.y = 365

        self.player = player
    
    # the basket will always follow the location of the player
    def update(self):
        self.rect.x = self.player.rect.x
        self.rect.y = self.player.rect.y - 40

class Enemy(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # creates the image and starting position and velocity
        self.image = ENEMY
        self.rect = self.image.get_rect()

        self.rect.x = -200
        self.rect.y = GROUND + 20

        self.vel_x = 0

    def update(self):
        self.rect.x += self.vel_x

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
    last_poop = 0
    last_enemy = 0

    # --SPRITE GROUPS--
    all_sprites = pg.sprite.Group()
    player_sprites = pg.sprite.Group()
    poop_sprites = pg.sprite.Group()
    enemy_sprites = pg.sprite.Group()

    background = Background()
    all_sprites.add(background)

    # CREATING PLAYER SPRITE
    player = Player()
    basket = Basket(player)
    player_sprites.add(player)
    all_sprites.add(basket)
    all_sprites.add(player)

    # CREATING ENEMY SPRITE
    enemy = Enemy()
    all_sprites.add(enemy)
    enemy_sprites.add(enemy)

    # CREATING POOP SPRITE
    poop = Poop()
    all_sprites.add(poop)
    poop_sprites.add(poop)

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
                    if player.rect.y == GROUND:
                        player.jump()

            # Stop player if arrow key is released
            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT and (player.vel_y != 0 or player.vel_x != 0):
                    player.stop()
                if event.key == pg.K_RIGHT and (player.vel_y != 0 or player.vel_x != 0):
                    player.stop()

        # if poop is dropped on the ground, it stays there
        for sprite in poop_sprites:
            if sprite.rect.y == GROUND + 40:
                sprite.vel_y = 0

        # add a new poop if _ millseconds elapses
        if pg.time.get_ticks() - last_poop > 2000:
            # set last_poop to current tick
            last_poop = pg.time.get_ticks()

            # adds poop
            poop1 = Poop()
            poop_sprites.add(poop1)
            all_sprites.add(poop1)

        # after _ amount of time, move the enemy
        if pg.time.get_ticks() - last_enemy > 2000:
            # set last_enemy to current tick
            last_enemy = pg.time.get_ticks()

            # if enemy is on left side
            if enemy.rect.x < -100:
                enemy.vel_x = random.choice((10, 15, 20))
                enemy.image = ENEMY
                if enemy.rect.x > 1215:
                    enemy.vel_x = 0

            # if enemy is on right side
            if enemy.rect.x > 1215:
                enemy.vel_x = random.choice((-10, -15, -20))
                enemy.image = pg.transform.flip(ENEMY, True, False)
                if enemy.rect.x < -15:
                    enemy.vel_x = 0
            

        # --- Update the world state
        all_sprites.update()

        # increase score once dog collects poop
        poop_collected = pg.sprite.spritecollide(player, poop_sprites, False)

        for poop in poop_collected:
            if poop.vel_y != 0:
                score += 1
                poop.kill()

        # --- Draw items
        screen.fill(BLACK)

        all_sprites.draw(screen)

        score_image = font.render(f"Poop points: {score}", True, WHITE)
        screen.blit(score_image, (5, 5))

        # Update the screen with anything new
        pg.display.flip()

        # --- Tick the Clock
        clock.tick(60)  # 60 fps

        # stop game if caught by enemy
        gameend = pg.sprite.spritecollide(player, enemy_sprites, False)
        # if len(gameend) > 0:
        #     player.kill()
        #     enemy.kill()
        #     basket.kill()
        
        # stop game if too much poop is on the ground
        if len(poop_sprites) > 2:
            player.kill()
            enemy.kill()
            basket.kill()
            gameover = font.render("TOO MUCH POOP IS ON THE GROUND", True, WHITE)
            screen.blit(gameover, (450, 300))


def main():
    start()


if __name__ == "__main__":
    main()
