from re import S
import pygame, random
from pygame.math import Vector2


pygame.font.init()

#Deffine fixed variable
CELL_SIZE = 20
CELL_NUMBER_WIDTH = 28
CELL_NUMBER_HEIGHT = 36
SCREEN = pygame.display.set_mode((CELL_SIZE * CELL_NUMBER_WIDTH, CELL_SIZE * CELL_NUMBER_HEIGHT,))
direction = 'STOP'
clock = pygame.time.Clock()
dt = clock.tick(60) / 1000
power_timer = 0
possible_directions = {'UP': Vector2(0,-1), 'DOWN': Vector2(0, 1), 'LEFT': Vector2(-1, 0), 'RIGHT': Vector2(1,0)}
door = [Vector2(13, 15), Vector2(14, 15)]

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
    def game_over(self):
        self.score.point = 0
        self.ghost.in_house = [False, True, True, True]
        self.walls.position.clear()
        self.coin.position.clear()
        self.powerups.position.clear()
        self.ghost.position.clear()
        self.level.positions()  
        self.state = 'STOPPED'

class Score:
    def __init__(self):
        self.position = Vector2(9, 1)
        self.point = 0
    def draw(self):
        font = pygame.font.Font('Graphics/arcade.ttf', 45)
        score_text = font.render(f'Score    {self.point}', True, 'red')
        SCREEN.blit(score_text, self.position * CELL_SIZE)

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

    def can_move(self, direction):
        if direction.length() == 0:
            return False
        next_tile = self.position + direction
        return next_tile not in game.walls.position

class Coins:
    def __init__(self):
        self.position = []
    def draw(self):
        for coin in self.position:
            pygame.draw.circle(SCREEN, (255, 215, 0), ((coin.x * CELL_SIZE) + CELL_SIZE // 2, (coin.y * CELL_SIZE) + CELL_SIZE // 2), CELL_SIZE // 6)

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
    def draw(self):
        for powerups in self.position:
            pygame.draw.circle(SCREEN, (255, 215, 0), ((powerups.x * CELL_SIZE) + CELL_SIZE // 2, (powerups.y * CELL_SIZE) + CELL_SIZE // 2), CELL_SIZE // 3)
        

class Ghost: #implement 4 different ghosts with different colors and behaviors
    def __init__(self):
        self.position = [] #0 = blinky, 1 = pinky, 2 = inky, 3 = clyde
        self.door_pos = Vector2(0, 0)
        self.in_house = [False, True, True, True]
        self.texture_blinky = pygame.image.load('Graphics/BLINKY.gif')
        self.texture_pinky = pygame.image.load('Graphics/PINKY.gif')
        self.texture_inky = pygame.image.load('Graphics/INKY.gif')
        self.texture_clyde = pygame.image.load('Graphics/CLYDE.gif')
        self.blinky_direction = Vector2(1,0)
        self.pinky_direction = Vector2(1,0)
    def draw(self):
        blinky_rect = pygame.Rect(self.position[0].x * CELL_SIZE, self.position[0].y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pinky_rect = pygame.Rect(self.position[1].x * CELL_SIZE, self.position[1].y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        inky_rect = pygame.Rect(self.position[2].x * CELL_SIZE, self.position[2].y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        clyde_rect = pygame.Rect(self.position[3].x * CELL_SIZE, self.position[3].y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        ghost_size = (CELL_SIZE, CELL_SIZE)
        blinky_scale = pygame.transform.scale(self.texture_blinky, ghost_size)
        pinky_scale = pygame.transform.scale(self.texture_pinky, ghost_size)
        inky_scale = pygame.transform.scale(self.texture_inky, ghost_size)
        clyde_scale = pygame.transform.scale(self.texture_clyde, ghost_size)
        SCREEN.blit(blinky_scale, blinky_rect)
        SCREEN.blit(pinky_scale, pinky_rect)
        SCREEN.blit(inky_scale, inky_rect)
        SCREEN.blit(clyde_scale, clyde_rect)
    def move_blinky(self):
        pos = self.position[0]

        if self.in_house[0]:
            pos = self.position[0]

            # 1) Move horizontally to align with door x
            if pos.x < self.door_pos.x:
                step = pos + Vector2(1, 0)
                if step not in game.walls.position:
                    self.position[0] = step
                    return
            elif pos.x > self.door_pos.x:
                step = pos + Vector2(-1, 0)
                if step not in game.walls.position:
                    self.position[0] = step
                    return

            # 2) Aligned: attempt to move up through the door
            step = pos + Vector2(0, -1)
            if step not in game.walls.position:
                self.position[0] = step
                # mark out once we've moved through the door tile or above it
                if step == self.door_pos or step.y < self.door_pos.y:
                    self.in_house[0] = False
                return

            # If blocked for some unexpected reason, do nothing this tick
            return
        if is_intersection(pos, game.walls.position):
            best_dir = self.blinky_direction
            best_dist = 99999
            for direction in possible_directions.values():
                if direction == -self.blinky_direction:
                    continue

                test_pos = pos + direction
                if test_pos not in game.walls.position and test_pos not in door:
                    dist = pytagore(
                        test_pos.x - game.pacman.position.x,
                        test_pos.y - game.pacman.position.y
                    )
                    if dist < best_dist:
                        best_dist = dist
                        best_dir = direction

            self.blinky_direction = best_dir

        next_pos = pos + self.blinky_direction
        if next_pos not in game.walls.position and next_pos not in door:
            self.position[0] = next_pos






    def move_pinky(self):
        pos = self.position[1]

        if self.in_house[1]:
            pos = self.position[1]

            # 1) Move horizontally to align with door x
            if pos.x < self.door_pos.x:
                step = pos + Vector2(1, 0)
                if step not in game.walls.position:
                    self.position[1] = step
                    return
            elif pos.x > self.door_pos.x:
                step = pos + Vector2(-1, 0)
                if step not in game.walls.position:
                    self.position[1] = step
                    return

            # 2) Aligned: attempt to move up through the door
            step = pos + Vector2(0, -1)
            if step not in game.walls.position:
                self.position[1] = step
                # mark out once we've moved through the door tile or above it
                if step.y < self.door_pos.y:
                    self.in_house[1] = False
                return

            # If blocked for some unexpected reason, do nothing this tick
            return
        
        if is_intersection(pos, game.walls.position):
            best_dir = self.pinky_direction
            best_dist = 99999
            for direction in possible_directions.values():
                if direction == -self.pinky_direction:
                    continue

                test_pos = pos + direction
                if test_pos not in game.walls.position and test_pos not in door:
                    dist = pytagore(
                        test_pos.x - (game.pacman.position.x + (game.pacman.next_direction.x * 4)),
                        test_pos.y - (game.pacman.position.y + (game.pacman.next_direction.y * 4))
                    )
                    if dist < best_dist:
                        best_dist = dist
                        best_dir = direction

            self.pinky_direction = best_dir

        next_pos = pos + self.pinky_direction
        if next_pos not in game.walls.position and next_pos not in door:
            self.position[1] = next_pos




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

            game.ghost.move_blinky()
            game.ghost.move_pinky()
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

    #Coin remove + score
    if game.pacman.position in game.coin.position:
        game.coin.position.remove(game.pacman.position)
        game.score.point += 1
    
    #powerup
    if game.pacman.position in game.powerups.position:
        game.powerups.position.remove(game.pacman.position)
        game.score.point += 10
        power_timer = 0
        game.powerups.power = True
    if power_timer >= 10:
        game.powerups.power = False

    #Pacman movement to opposite side of the grid
    if game.pacman.position == Vector2(CELL_NUMBER_WIDTH, game.pacman.position.y):
        game.pacman.position = Vector2(0, game.pacman.position.y)
    elif game.pacman.position == Vector2(- 1, game.pacman.position.y):
        game.pacman.position = Vector2(CELL_NUMBER_WIDTH - 1, game.pacman.position.y)

    #Ghost movement to opposite side of the grid
    for i in range(4):
        if game.ghost.position[i] == Vector2(CELL_NUMBER_WIDTH, game.ghost.position[i].y):
            game.ghost.position[i] = Vector2(0, game.ghost.position[i].y)
        elif game.ghost.position[i] == Vector2(- 1, game.ghost.position[i].y):
            game.ghost.position[i] = Vector2(CELL_NUMBER_WIDTH - 1, game.ghost.position[i].y) 

    if game.pacman.position in game.ghost.position:
        if game.powerups.power:
            ghost_index = game.ghost.position.index(game.pacman.position)
            game.ghost.position[ghost_index] = Vector2(13, 17)
            game.ghost.in_house[ghost_index] = True
            game.score.point += 50
        else:
            game.game_over()

    
    power_timer += dt
    #print(power_timer)
    clock.tick(60)
    pygame.display.update()

pygame.quit()

