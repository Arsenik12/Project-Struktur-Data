import pygame
import sys
import random

# Inisialiasi kelas Node
class Node:
    def __init__(self, position):
        self.position = position
        self.next = None

# inisialisasi kelas snake berisi method-method untuk manipulasi snake
class Snake:
    def __init__(self, position):
        self.head = Node(position)
        self.tail = self.head
        self.length = 1
    
    def addHead(self, position):
        new_node = Node(position)
        new_node.next = self.head
        self.head = new_node
        self.length += 1
    
    def removeHead(self):
        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            self.head = self.head.next
        self.length -= 1
    
    def removeTail(self):
        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            current = self.head
            while current.next != self.tail:
                current = current.next
            current.next = None
            self.tail = current
        self.length -= 1

# inisialiasi pygame
pygame.init()

# ngatur ukuran window
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 500
GRID_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

#masukin aset-aset gambar
judul = pygame.image.load('Assets/judul.png')
apple_image = pygame.image.load('Assets/buah/apple.png')
apple_image = pygame.transform.scale(apple_image, (GRID_SIZE, GRID_SIZE))
banana_image = pygame.image.load('Assets/buah/banana.png')
banana_image = pygame.transform.scale(banana_image, (GRID_SIZE, GRID_SIZE))
kulit_pisang = pygame.image.load('Assets/sampah/kulitPisang.png')
kulit_pisang = pygame.transform.scale(kulit_pisang, (GRID_SIZE, GRID_SIZE))
dirty = pygame.image.load('Assets/sampah/dirty.png')
dirty = pygame.transform.scale(dirty, (GRID_SIZE, GRID_SIZE))
sampah = pygame.image.load('Assets/sampah/trash.png')
sampah = pygame.transform.scale(sampah, (GRID_SIZE, GRID_SIZE))
applesisa = pygame.image.load('Assets/sampah/appleSisa.png')
applesisa = pygame.transform.scale(applesisa, (GRID_SIZE, GRID_SIZE))
batu = pygame.image.load('Assets/obstacle/batu.png')
batu = pygame.transform.scale(batu, (GRID_SIZE, GRID_SIZE))

#masukin suara
crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')
die_sound = pygame.mixer.Sound('Sound/mixkit-little-piano-game-over-1944.wav')

#Kelas utama untuk game
class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Proyek SD - Linkedlist Snake Game")
        self.clock = pygame.time.Clock()
        self.trash_positions = []
        self.trash_timer = 0
        self.food_timer = 0
        self.buah_images = [apple_image, banana_image]
        self.buah_items = []
        self.trash_images = [kulit_pisang, dirty, sampah, applesisa]
        self.trash_items = []
        self.reset()
        
    def reset(self):
        self.snake = Snake((GRID_WIDTH // 2, GRID_HEIGHT // 2))
        self.trash_positions = []
        self.trash_items = []
        self.trash_timer = 0
        self.food_timer = pygame.time.get_ticks()
        self.snake_direction = (1, 0)
        self.food_position, self.current_food_image = self.getRandomFood()
        self.score = 0
    
    def getRandomFood(self):
        while True:
            position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if not self.isEatenBySnake(position):
                image = random.choice(self.buah_images)
                return position, image

    def isEatenBySnake(self, position):
        current = self.snake.head
        while current:
            if current.position == position:
                return True
            current = current.next
        return False
    
    def isTrashEaten(self, position):
        return position in self.trash_positions

    def getRandomTrashPos(self):
        while True:
            position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if not self.isEatenBySnake(position) and position != self.food_position:
                return position

    def update(self):
        new_head_position = (
            (self.snake.head.position[0] + self.snake_direction[0]) % GRID_WIDTH,
            (self.snake.head.position[1] + self.snake_direction[1]) % GRID_HEIGHT
        )
        
        if self.isEatenBySnake(new_head_position):
            self.play_die_sound()
            self.reset()
        else:
            self.snake.addHead(new_head_position)
            
            if new_head_position == self.food_position:
                self.food_position, self.current_food_image = self.getRandomFood()
                self.play_crunch_sound()
                self.score += 1
                self.food_timer = pygame.time.get_ticks()
                
            elif self.isTrashEaten(new_head_position):
                self.snake.removeTail()
                self.snake.removeTail()
                trash_index = self.trash_positions.index(new_head_position)
                del self.trash_positions[trash_index]
                del self.trash_items[trash_index]
                self.play_crunch_sound()
                self.score -= 1
                if self.score == -1:
                    self.play_die_sound()
                    self.reset()
                self.trash_timer = pygame.time.get_ticks()
            else:
                self.snake.removeTail()

        if pygame.time.get_ticks() - self.food_timer > 5000:
            self.food_position, self.current_food_image = self.getRandomFood()
            self.food_timer = pygame.time.get_ticks()

    def draw(self):
        self.screen.fill((108, 108, 108))
        
        current = self.snake.head
        while current:
            pygame.draw.rect(
                self.screen,
                (0, 255, 0),
                pygame.Rect(current.position[0] * GRID_SIZE, current.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            )
            current = current.next
        
        self.screen.blit(self.current_food_image, (self.food_position[0] * GRID_SIZE, self.food_position[1] * GRID_SIZE))
        
        for index, position in enumerate(self.trash_positions):
            self.screen.blit(self.trash_items[index], (position[0] * GRID_SIZE, position[1] * GRID_SIZE))
        
        self.draw_score()
        pygame.display.flip()
    
    def play_crunch_sound(self):
        pygame.mixer.Sound.play(crunch_sound)
    
    def play_die_sound(self):
        pygame.mixer.Sound.play(die_sound)
    
    def draw_score(self):
        font_color = (0, 0, 0)
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, font_color)
        text_rect = score_text.get_rect()
        text_rect.topleft = (10, 10)
        self.screen.blit(score_text, text_rect)
    
    def draw_start_screen(self):
        running = True
        while running:
            self.screen.fill((108, 108, 108))
            font_color = (0, 0, 0)
            font = pygame.font.Font(None, 36)
            scaled_judul = pygame.transform.scale(judul, (290, 200))
            self.screen.blit(scaled_judul, (SCREEN_WIDTH // 2 - 150, 20))
            score_text = font.render("Press any key to start", True, font_color)
            name1 = font.render("Crisnanda", True, font_color)
            name2 = font.render("Victor", True, font_color)
            name3 = font.render("Billy", True, font_color)

            text_rect = score_text.get_rect()
            name1_rect = name1.get_rect()
            name2_rect = name2.get_rect()
            name3_rect = name3.get_rect()
            name1_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)
            name2_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 15)
            name3_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10)
            text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
          
            self.screen.blit(score_text, text_rect)
            self.screen.blit(name1, name1_rect)
            self.screen.blit(name2, name2_rect)
            self.screen.blit(name3, name3_rect)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    running = False
    
    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.snake_direction != (0, 1):
                    self.snake_direction = (0, -1)
                elif event.key == pygame.K_DOWN and self.snake_direction != (0, -1):
                    self.snake_direction = (0, 1)
                elif event.key == pygame.K_LEFT and self.snake_direction != (1, 0):
                    self.snake_direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and self.snake_direction != (-1, 0):
                    self.snake_direction = (1, 0)

    def run(self):
        self.draw_start_screen()
        while True:
            self.handle_keys()
            self.update()
            self.draw()
            self.clock.tick(10)
            if len(self.trash_positions) == 0:
                self.spawn_trash()
            elif len(self.trash_positions) > 0:
                if self.score > 10 and len(self.trash_positions) < 5:
                    self.spawn_trash()
                    
                if pygame.time.get_ticks() - self.trash_timer > 3000:
                    self.trash_positions = []
                    self.trash_items = []

    def spawn_trash(self):
        new_trash_position = self.getRandomTrashPos()
        new_trash_image = random.choice(self.trash_images)
        self.trash_positions.append(new_trash_position)
        self.trash_items.append(new_trash_image)
        self.trash_timer = pygame.time.get_ticks()

if __name__ == "__main__":
    SnakeGame().run()
