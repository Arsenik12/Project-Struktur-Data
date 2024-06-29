import pygame
import sys
import random
from pygame.math import Vector2

class Node:
    def __init__(self, position):
        self.position = position
        self.next = None

class SNAKE:
    def __init__(self):
        head = Node(Vector2(5, 10))
        body = Node(Vector2(4, 10))
        tail = Node(Vector2(3, 10))
        
        head.next = body
        body.next = tail
        
        self.head = head
        self.body = body
        self.tail = tail
        self.direction = Vector2(1, 0)
        self.new_block = False

        self.head_up = pygame.image.load(
            'Assets/ular/head_up.png').convert_alpha()
        self.head_down = pygame.image.load(
            'Assets/ular/head_down.png').convert_alpha()
        self.head_right = pygame.image.load(
            'Assets/ular/head_right.png').convert_alpha()
        self.head_left = pygame.image.load(
            'Assets/ular/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load(
            'Assets/ular/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load(
            'Assets/ular/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load(
            'Assets/ular/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load(
            'Assets/ular/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load(
            'Assets/ular/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load(
            'Assets/ular/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load(
            'Assets/ular/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load(
            'Assets/ular/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load(
            'Assets/ular/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load(
            'Assets/ular/body_bl.png').convert_alpha()
        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')
        self.gameOver_sound = pygame.mixer.Sound(
            'Sound/mixkit-little-piano-game-over-1944.wav')
        self.walk_sound = pygame.mixer.Sound(
            'Sound/SMEFMQE-snake-movement.wav')

    def draw_snake(self):
        current_node = self.head
        while current_node is not None:
            x_pos = int(current_node.x * cell_size)
            y_pos = int(current_node.y * cell_size)
            node_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            
            if current_node == self.head:
                screen.blit(self.head, node_rect)
            elif current_node == self.tail:
                screen.blit(self.tail, node_rect)
            else:
                screen.blit(self.body, node_rect)
            
            current_node = current_node.next
    
    def update_head_graphics(self):
        head_relation = self.body.position - self.head.position
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.tail.position - self.body.position
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down

    def move_snake(self):
        new_head_pos = self.head.position + self.direction
        new_head = Node(new_head_pos)
        
        new_head.next = self.head
        self.head = new_head
        
        if not self.new_block:
            current = self.head
            while current.next and current.next.next:
                current = current.next
            current.next = None
            self.tail = current
        else:
            self.new_block = False

    def add_block(self):
        self.new_block = True

    def remove_block(self):
        if self.head is None or self.head.next is None:
            main_game.game_over()
        
        current = self.head 
        while current.next.next:
            current = current.next
        current.next = None
        
        if self.head.next is None:
            main_game.game_over()

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def play_gameOver_sound(self):
        self.gameOver_sound.play()

    def play_walk_sound(self):
        self.walk_sound.play()

    def reset(self):
        
        head = Node(Vector2(5, 10))
        middle = Node(Vector2(4, 10))
        tail = Node(Vector2(3, 10))
    
        head.next = middle
        middle.next = tail
    
        self.head = head
        self.tail = tail
        self.direction = Vector2(0, 0)
        self.new_block = False  # Ensure this flag is reset as well


class FRUIT:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(
            int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class TRASH:
    def __init__(self):
        self.randomize()

    def draw_trash(self):
        trash_rect = pygame.Rect(
            int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(trash, trash_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.trash = TRASH()
        self.active_object = 'fruit'  # Memulai permainan dengan apple
        self.object_timer = pygame.time.get_ticks()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()
        self.check_object_timeout()

    def draw_elements(self):
        self.draw_grass()
        if self.active_object == 'fruit':
            self.fruit.draw_fruit()
        else:
            self.trash.draw_trash()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):

        if self.active_object == 'fruit' and self.fruit.pos == self.snake.head.value:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()
            self.switch_object()
    

        if self.active_object == 'trash' and self.trash.pos == self.snake.head.value:
            self.snake.remove_block()
            self.switch_object()
    
  
        current = self.snake.head.next
        while current:
            if current.value == self.fruit.pos:
                self.fruit.randomize()
            if current.value == self.trash.pos:
                self.trash.randomize()
            current = current.next

    def check_fail(self):
        # Boundary check
        if not 0 <= self.snake.head.value.x < cell_number or not 0 <= self.snake.head.value.y < cell_number:
            self.game_over()
            self.snake.play_gameOver_sound()
    
        # Body collision check
        current = self.snake.head.next
        while current:
            if current.value == self.snake.head.value:
                self.game_over()
                break
            current = current.next

    def game_over(self):
        self.snake.reset()

    def draw_grass(self):
        grass_color = (167, 209, 61)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(
                            col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(
                            col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        count = 0
        current_node = self.snake.body
        while current_node is not None:
            count += 1
            current_node = current_node.next

        score_text = str(count - 3)  # Assuming the initial length is 3
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple_rect = apple.get_rect(
            midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top,
                              apple_rect.width + score_rect.width + 6, apple_rect.height)

        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)

    def switch_object(self):
        if self.active_object == 'fruit':
            self.active_object = 'trash'
        else:
            self.active_object = 'fruit'
        self.object_timer = pygame.time.get_ticks()

    def check_object_timeout(self):
        # 5000 ms = 5 detik (waktu untuk mengganti objectnya)
        if pygame.time.get_ticks() - self.object_timer > 5000:
            self.switch_object()


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
cell_size = 28
cell_number = 24
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
apple = pygame.image.load('Assets/buah/apple.png').convert_alpha()
trash = pygame.image.load('Assets/sampah/appleSisa.png').convert_alpha()
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)

    screen.fill((175, 215, 70))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)
