from re import S
import pygame, random, sys
from pygame.math import Vector2


pygame.font.init()

#Deffine setup variables
CELL_SIZE = 20
CELL_NUMBER_WIDTH = 28
CELL_NUMBER_HEIGHT = 36
SCREEN = pygame.display.set_mode((CELL_SIZE * CELL_NUMBER_WIDTH, CELL_SIZE * CELL_NUMBER_HEIGHT,))
direction = 'STOP'
clock = pygame.time.Clock()
dt = clock.tick(60) / 1000
possible_directions = {'UP': Vector2(0,-1), 'DOWN': Vector2(0, 1), 'LEFT': Vector2(-1, 0), 'RIGHT': Vector2(1,0)}
door = []

#Creating a grid for dev purposes
def draw_grid():
    for x in range(0, CELL_NUMBER_WIDTH * CELL_SIZE, CELL_SIZE):
        for y in range(0, CELL_NUMBER_HEIGHT * CELL_SIZE, CELL_SIZE):
            grid_surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(grid_surface, (200, 200, 200, 60), (0, 0, CELL_SIZE, CELL_SIZE), 1)
            SCREEN.blit(grid_surface, (x, y))

#Place class to handle the position of objects on the grid
class Game:
    def __init__(self):
        self.state = 'RUNNING'
        self.level = Level()
        self.pacman = Pacman()
        self.coin = Coins()
        self.walls = Walls()
        self.powerups = PowerUps()
        self.ghost = Ghost()
        self.score = Score()
        
    def draw(self):
        self.walls.draw()
        #self.grid = draw_grid()
        self.pacman.draw()
        self.score.draw()
        self.powerups.draw()
        self.coin.draw()
        self.ghost.draw()
        
    def update(self):
        self.pacman.positioning()
        self.ghost.move_blinky()
        self.ghost.move_pinky()
        self.coin.collision()
        self.powerups.collision()
        self.ghost.transfer()
        self.pacman.collision()
        print(len(game.coin.position), len(game.powerups.position))
        if len(game.coin.position) < 1 and len(game.powerups.position) < 1:
            self.game_win()

    def reset(self):
        self.score.point = 0
        self.ghost.in_house = [False, True, True, True]
        self.ghost.unlock_timer = 0
        self.walls.position.clear()
        self.coin.position.clear()
        self.powerups.position.clear()
        self.ghost.position.clear()
        self.level.positions() 


    def game_over(self):
        self.reset() 
        self.state = 'STOPPED'
        while self.state == 'STOPPED':
            SCREEN.fill((0,0,0))
            font = pygame.font.Font('Graphics/arcade.ttf', 75)
            small_font = pygame.font.Font('Graphics/arcade.ttf', 35)
            game_over_text = font.render('GAME OVER', True, 'red')
            SCREEN.blit(game_over_text, (CELL_SIZE * 6, CELL_SIZE * 15))
            play_again = small_font.render('Press   SPACE  to   play   again', True, 'yellow')
            SCREEN.blit(play_again, (CELL_SIZE * 3, CELL_SIZE * 20))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.state = 'RUNNING'
    def game_win(self):
        self.reset()
        self.state = 'STOPPED'
        while self.state == 'STOPPED':
            SCREEN.fill((0,0,0))
            font = pygame.font.Font('Graphics/arcade.ttf', 75)
            small_font = pygame.font.Font('Graphics/arcade.ttf', 35)
            game_over_text = font.render('YOU  WIN', True, 'green')
            SCREEN.blit(game_over_text, (CELL_SIZE * 7, CELL_SIZE * 15))
            play_again = small_font.render('Press   SPACE  to   play   again', True, 'yellow')
            SCREEN.blit(play_again, (CELL_SIZE * 3, CELL_SIZE * 20))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.state = 'RUNNING'

class Pacman:
    def __init__(self):
        self.position = Vector2(0,0)
        self.texture = pygame.image.load('Graphics/pacman.png')
        self.direction = Vector2(0,0)
        self.next_direction = Vector2(0,0)
        self.speed = 1
    def draw(self):
        pacman_rect = pygame.Rect(self.position.x * CELL_SIZE, self.position.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pacman_size = (CELL_SIZE, CELL_SIZE)
        pacman_scale = pygame.transform.scale(self.texture, pacman_size)
        SCREEN.blit(pacman_scale, pacman_rect)
    def positioning(self): 
        # --- try to turn if possible ---
        if self.can_move(self.next_direction):
            self.direction = self.next_direction

        # --- move forward if possible ---
        if self.can_move(self.direction):
            self.position += self.direction
        
        if self.position == Vector2(CELL_NUMBER_WIDTH, self.position.y):
            self.position = Vector2(0, self.position.y)
        elif self.position == Vector2(- 1, self.position.y):
            self.position = Vector2(CELL_NUMBER_WIDTH - 1, self.position.y)

    def can_move(self, direction):
        if direction.length() == 0:
            return False
        next_tile = self.position + direction
        return next_tile not in game.walls.position

    def collision(self):
        if self.position in game.ghost.position:
            if game.powerups.power:
                ghost_index = game.ghost.position.index(self.position)
                game.ghost.position[ghost_index] = Vector2(13, 17)
                game.ghost.in_house[ghost_index] = True
                game.score.point += 50
            else:
                game.game_over()

class Score:
    def __init__(self):
        self.position = Vector2(9, 1)
        self.point = 0
    def draw(self):
        font = pygame.font.Font('Graphics/arcade.ttf', 45)
        score_text = font.render(f'Score    {self.point}', True, 'red')
        SCREEN.blit(score_text, self.position * CELL_SIZE)

class Coins:
    def __init__(self):
        self.position = []
    def draw(self):
        for coin in self.position:
            pygame.draw.circle(SCREEN, (255, 215, 0), ((coin.x * CELL_SIZE) + CELL_SIZE // 2, (coin.y * CELL_SIZE) + CELL_SIZE // 2), CELL_SIZE // 6)
    def collision(self):
        if game.pacman.position in self.position:
            self.position.remove(game.pacman.position)
            game.score.point += 1

class Walls:
    def __init__(self):
        self.position = []
    def draw(self):
        for wall in self.position:
            pygame.draw.rect(SCREEN, ('blue'), (int(wall.x) * CELL_SIZE, int(wall.y) * CELL_SIZE, CELL_SIZE - (CELL_SIZE / 4), CELL_SIZE - (CELL_SIZE / 4)))

class PowerUps:
    def __init__(self):
        self.position = []
        self.power = False
        self.timer = 0
    def draw(self):
        for powerups in self.position:
            pygame.draw.circle(SCREEN, (255, 215, 0), ((powerups.x * CELL_SIZE) + CELL_SIZE // 2, (powerups.y * CELL_SIZE) + CELL_SIZE // 2), CELL_SIZE // 3)
    def collision(self):
        if game.pacman.position in self.position:
            self.position.remove(game.pacman.position)
            game.score.point += 10
            self.timer = 0
            self.power = True
        if self.timer >= 5:
            self.power = False
        

class Ghost: #implement 4 different ghosts with different colors and behaviors
    def __init__(self):
        self.position = [] #0 = blinky, 1 = pinky, 2 = inky, 3 = clyde
        self.door_pos = Vector2(0, 0)
        self.in_house = [False, True, True, True]
        self.texture = {0: pygame.image.load('Graphics/BLINKY.gif'), 1: pygame.image.load('Graphics/PINKY.gif'),
                        2: pygame.image.load('Graphics/INKY.gif'), 3: pygame.image.load('Graphics/CLYDE.gif'),
                        4: pygame.image.load('Graphics/scared_ghost.png')}
        self.direction = {0: Vector2(1, 0), 1: Vector2(1, 0), 2: Vector2(1, 0), 3: Vector2(1, 0)}
        self.pinky_direction = Vector2(1,0)
        self.unlock_timer = 0
    def draw(self):
        if game.powerups.power == False:
            for ghost in range(4):
                rect = pygame.Rect(self.position[ghost].x * CELL_SIZE, self.position[ghost].y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                scale = pygame.transform.scale(self.texture[ghost], (CELL_SIZE, CELL_SIZE))
                SCREEN.blit(scale, rect)
        elif game.powerups.power:
            for ghost in range(4):
                rect = pygame.Rect(self.position[ghost].x * CELL_SIZE, self.position[ghost].y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                scale = pygame.transform.scale(self.texture[4], (CELL_SIZE, CELL_SIZE))
                SCREEN.blit(scale, rect)
    def transfer(self):
        for i in range(4):
            if self.position[i] == Vector2(CELL_NUMBER_WIDTH, self.position[i].y):
                self.position[i] = Vector2(0, self.position[i].y)
            elif self.position[i] == Vector2(- 1, self.position[i].y):
                self.position[i] = Vector2(CELL_NUMBER_WIDTH - 1, self.position[i].y)

    def move_blinky(self):
        pos = self.position[0]

        if self.in_house[0]:
            in_house(0)
            return
        if game.powerups.power == False:
            hunting(0,1)
        elif game.powerups.power:
            escaping(0,1)


    def move_pinky(self):
        if self.unlock_timer > 2:
            pos = self.position[1]

            if self.in_house[1]:
                in_house(1)
                return
            if game.powerups.power == False:
                hunting(1,4)
            elif game.powerups.power:
                escaping(1,4)

def hunting(gho,target):
        pos = game.ghost.position[gho]
        if is_intersection(pos, game.walls.position):
            best_dir = game.ghost.direction[gho]
            best_dist = 99999
            for direction in possible_directions.values():
                if direction == -game.ghost.direction[gho]:
                    continue

                test_pos = pos + direction
                if test_pos not in game.walls.position and test_pos not in door:
                    dist = pytagore(
                        test_pos.x - (game.pacman.position.x + (game.pacman.next_direction.x * target)),
                        test_pos.y - (game.pacman.position.y + (game.pacman.next_direction.y * target))
                    )
                    if dist < best_dist:
                        best_dist = dist
                        best_dir = direction

            game.ghost.direction[gho] = best_dir

        next_pos = pos + game.ghost.direction[gho]
        if next_pos not in game.walls.position and next_pos not in door:
            game.ghost.position[gho] = next_pos
def escaping(gho, target):
        pos = game.ghost.position[gho]
        if is_intersection(pos, game.walls.position):
            best_dir = game.ghost.direction[gho]
            best_dist = 0
            for direction in possible_directions.values():
                if direction == -game.ghost.direction[gho]:
                    continue

                test_pos = pos + direction
                if test_pos not in game.walls.position and test_pos not in door:
                    dist = pytagore(
                        test_pos.x - (game.pacman.position.x + (game.pacman.next_direction.x * target)),
                        test_pos.y - (game.pacman.position.y + (game.pacman.next_direction.y * target))
                    )
                    if dist > best_dist:
                        best_dist = dist
                        best_dir = direction

            game.ghost.direction[gho] = best_dir

        next_pos = pos + game.ghost.direction[gho]
        if next_pos not in game.walls.position and next_pos not in door:
            game.ghost.position[gho] = next_pos

def in_house(gho):
        pos = game.ghost.position[gho]

        # 1) Move horizontally to align with door x
        if pos.x < game.ghost.door_pos.x:
            step = pos + Vector2(1, 0)
            if step not in game.walls.position:
                game.ghost.position[gho] = step
                return
        elif pos.x > game.ghost.door_pos.x:
            step = pos + Vector2(-1, 0)
            if step not in game.walls.position:
                game.ghost.position[gho] = step
                return

        # 2) Aligned: attempt to move up through the door
        step = pos + Vector2(0, -1)
        if step not in game.walls.position:
            game.ghost.position[gho] = step
            # mark out once we've moved through the door tile or above it
            if step.y < game.ghost.door_pos.y:
                game.ghost.in_house[gho] = False
            return

        # If blocked for some unexpected reason, do nothing this tick
        return
def pytagore(a,b):
     c2 = a ** 2 + b ** 2
     return c2 ** 0.5
def is_intersection(pos, walls):
    dirs = [
        Vector2(1,0), Vector2(-1,0),
        Vector2(0,1), Vector2(0,-1)
    ]
    valid_dirs = [pos + d for d in dirs if pos + d not in walls]

    if len(valid_dirs) < 2:
        return False
    
    if len(valid_dirs) == 2:
        d1 = valid_dirs[0] - pos
        d2 = valid_dirs[1] - pos
        if d1 + d2 == Vector2(0,0):  # they are opposite
            return False

    return True



def load_level(number):
    file = f'lvl/level-{number}.txt'
    level = []
    with open(file, 'r') as level_file:
        for line in level_file:
            level.append(list(line.strip()))        
    return level

class Level:
    def __init__(self):
        self.lvl1 = load_level(1)

    def positions(self):
        for row_index, row in enumerate(self.lvl1):
            for col_index, cell in enumerate(row):
                if cell == '*':
                    game.ghost.door_pos = Vector2(col_index, row_index)
                    door.append(Vector2(col_index, row_index))
                elif cell == '0':
                    pass
                elif cell == '1':
                    game.walls.position.append(Vector2(col_index, row_index))
                elif cell == '2':
                    game.coin.position.append(Vector2(col_index, row_index))
                elif cell == '3':
                    game.powerups.position.append(Vector2(col_index, row_index))
                elif cell == 'B':
                    game.ghost.position.append(Vector2(col_index, row_index))
                elif cell == 'N':
                    game.ghost.position.append(Vector2(col_index, row_index))
                elif cell == 'I':
                    game.ghost.position.append(Vector2(col_index, row_index)) 
                elif cell == 'C':
                    game.ghost.position.append(Vector2(col_index, row_index))
                elif cell == 'P':
                    game.pacman.position = Vector2(col_index, row_index)
#Game loop
game = Game()
game.level.positions()
PACMAN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(PACMAN_UPDATE, 100)
run = True
while run:
    SCREEN.fill((0,0,0))
    
    game.draw()
    
    #Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == PACMAN_UPDATE:

            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                game.pacman.next_direction = Vector2(0, -1)
            elif keys[pygame.K_DOWN]:
                game.pacman.next_direction = Vector2(0, 1)
            elif keys[pygame.K_LEFT]:
                game.pacman.next_direction = Vector2(-1, 0)
            elif keys[pygame.K_RIGHT]:
                game.pacman.next_direction = Vector2(1, 0)

            game.update()

    game.powerups.timer += dt
    game.ghost.unlock_timer += dt
    #print(power_timer)
    clock.tick(60)
    pygame.display.update()

pygame.quit()

