import pygame
from random import randint

class Pixels():
    def __init__(self, type, x, y, last_updated_tick, effects):
        self.type = type
        self.x = x
        self.y = y
        self.last_updated_tick = last_updated_tick
        self.effects = effects
    
    def behaviour(self, grid, cur_tick):
        if self.last_updated_tick == cur_tick or "dead" in self.effects:
            return

        to_displace = 0

        match self.type:
            case 1: # sand, falls, and can go down slopes
                if self.y == 4:
                    self.effects[0] = "dead"
                    return

                new_y = self.y
                new_x = self.x

                move_dir = randint(0, 1)
                if grid[self.y + 1][self.x] in [0, 4]:
                    new_y = self.y + 1

                    to_displace = grid[self.y + 1][self.x]
                
                elif move_dir == 0 and grid[self.y + 1][self.x - 1] == 0 and self.y < 4:
                    new_y = self.y + 1
                    new_x = self.x - 1

                elif move_dir == 1 and grid[self.y + 1][self.x + 1] == 0 and self.y < 4:
                    new_y = self.y + 1
                    new_x = self.x + 1
            
            case 2: # metal, doesn't move
                new_y = self.y
                new_x = self.x

            case 3: # stone, can only move down
                if self.y == 4:
                    self.effects[0] = "dead"
                    return

                new_y = self.y
                new_x = self.x
                
                if grid[self.y + 1][self.x] in [0, 4]:
                    new_y = self.y + 1

                    to_displace = grid[self.y + 1][self.x]
            
            case 4: # water, moves down, and if can't, moves left or right
                new_y = self.y
                new_x = self.x

                move_dir = randint(0, 2) # if 2, don't move
                if self.y != 4 and grid[self.y + 1][self.x] == 0:
                    new_y = self.y + 1
                
                elif move_dir == 0 and self.x != 0 and grid[self.y][self.x - 1] == 0:
                    new_x = self.x - 1

                elif move_dir == 1 and self.x != COLUMNS - 1 and grid[self.y][self.x + 1] == 0:
                    new_x = self.x + 1
            
            case 5: # steam, moves up, and if can't, moves left or right
                new_y = self.y
                new_x = self.x

                move_dir = randint(0, 2) # if 2, don't move
                if self.y != 0 and grid[self.y - 1][self.x] == 0:
                    new_y = self.y - 1
                
                elif self.y != 0 and move_dir == 0 and grid[self.y - 1][self.x - 1] == 0:
                    new_y = self.y - 1
                    new_x = self.x - 1

                elif self.y != 0 and move_dir == 1 and grid[self.y - 1][self.x + 1] == 0:
                    new_y = self.y - 1
                    new_x = self.x + 1

                elif move_dir == 0 and self.x != 0 and grid[self.y][self.x - 1] == 0:
                    new_x = self.x - 1

                elif move_dir == 1 and self.x != COLUMNS - 1 and grid[self.y][self.x + 1] == 0:
                    new_x = self.x + 1

        grid[self.y][self.x] = to_displace
        grid[new_y][new_x] = self.type
        self.y, self.x = new_y, new_x

        self.last_updated_tick = cur_tick

def drawGrid(grid, mouse_grid_pos):
    screen.fill("black")

    changed_win_width = WIDTH - (HEIGHT)

    every_second_pixel = True

    for i in range(COLUMNS):
        for j in range(ROWS):
            every_second_pixel = not every_second_pixel
            match grid[j][i]:
                case 0: pixel = pygame.draw.rect(screen, "white", (i + changed_win_width // 2, j, WIDTH, (HEIGHT - 100)))
                case 1: pixel = pygame.draw.rect(screen, "yellow", (i + changed_win_width // 2, j, WIDTH, (HEIGHT - 100)))
                case 2: pixel = pygame.draw.rect(screen, "#424242", (i + changed_win_width // 2, j, WIDTH, (HEIGHT - 100)))
                case 3: pixel = pygame.draw.rect(screen, "gray", (i + changed_win_width // 2, j, WIDTH, (HEIGHT - 100)))
                case 4: pixel = pygame.draw.rect(screen, "blue", (i + changed_win_width // 2, j, WIDTH, (HEIGHT - 100)))
                case 5: pixel = pygame.draw.rect(screen, "#BDBDBD", (i + changed_win_width // 2, j, WIDTH, (HEIGHT - 100)))
                case _:
                    if every_second_pixel:
                        placeholder_texture = "purple"
                    else:
                        placeholder_texture = "black"
                    pygame.draw.rect(screen, placeholder_texture,  (i + changed_win_width // 2, j, WIDTH, (HEIGHT - 100)))
                    break
            if mouse_grid_pos == [i, j]:
                shape_surf = pygame.Surface(pygame.Rect(pixel).size, pygame.SRCALPHA)
                pygame.draw.rect(shape_surf, (255, 255, 255, 50), shape_surf.get_rect())
                screen.blit(shape_surf, pixel)
    
    pygame.draw.rect(screen, "white", (0, HEIGHT - 100, WIDTH, 100)) # To get rid of overhanging pixels

def createGrid():
    grid = []

    for i in range(ROWS):
        row = []
        for j in range(COLUMNS):
            row.append(0)
        grid.append(row)
    
    return grid

ROWS, COLUMNS = 5, 5
WIDTH, HEIGHT = COLUMNS * 100, ROWS * 100 + 100

pygame.init()
pygame.display.set_caption("Powder Simulation")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
started = True
dt = 0

running = True
mouse_grid_pos = [0, 0]
grid = createGrid()

cur_tick = 1
pixel_types = ("air", "sand", "metal", "stone", "water", "steam")
total_pixels = 25
all_pixels = {}

action_type = "sand 2 0"

while running:
    for event in pygame.event.get():
        print('event')
        if event.type == pygame.QUIT:
            started = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and mouse_grid_pos[1] > 0:
                mouse_grid_pos[1] -= 1
            elif event.key == pygame.K_a and mouse_grid_pos[0] > 0:
                mouse_grid_pos[0] -= 1
            elif event.key == pygame.K_s and mouse_grid_pos[1] < ROWS - 1:
                mouse_grid_pos[1] += 1
            elif event.key == pygame.K_d and mouse_grid_pos[0] < COLUMNS - 1:
                mouse_grid_pos[0] += 1
        
    if action_type != None:
        if total_pixels == 0:
            print("Cannot place any more pixels")
            break

        possible_pixel = []

        for char in action_type:
            possible_pixel.append(char)
            if ''.join(possible_pixel) in pixel_types:
                break

        pixel_type = pixel_types.index(''.join(possible_pixel))

        pixel_x, pixel_y = int(action_type[-3]), int(action_type[-1])
        grid[pixel_y][pixel_x] = pixel_type

        all_pixels.update({25 - total_pixels: Pixels(pixel_type, pixel_x, pixel_y, cur_tick, [None])})
        total_pixels -= 1

    drawGrid(grid, mouse_grid_pos)

    pygame.display.flip()
    clock.tick(1)

    i = 0
    for _ in all_pixels:
        all_pixels[i].behaviour(grid, cur_tick - 1)
        i += 1
    cur_tick += 1

    action_type = None
    i = 0
    for item in grid:
        print(grid[i])
        i += 1
    print(f"Tick: {cur_tick}")
    print(f"{25 - total_pixels} pixel/s on screen")

pygame.quit()