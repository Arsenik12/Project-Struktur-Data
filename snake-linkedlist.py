import pygame
import sys
import random

# Inisialisasi kelas Node
class Node:
    def __init__(self, position):
        self.position = position
        self.next = None

# Inisialisasi kelas Snake
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

# Inisialisasi pygame
pygame.init()

# Mengatur ukuran window
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 500
GRID_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Memasukkan aset-aset gambar
judul = pygame.image.load('Assets/judul.png')

# asset buah
apple = pygame.image.load('Assets/buah/apple.png')
apple = pygame.transform.scale(apple, (GRID_SIZE, GRID_SIZE))
banana = pygame.image.load('Assets/buah/banana.png')
banana = pygame.transform.scale(banana, (GRID_SIZE, GRID_SIZE))
watermelon = pygame.image.load('Assets/buah/watermelon.png')
watermelon = pygame.transform.scale(watermelon, (GRID_SIZE, GRID_SIZE))

# asset sampah
dirty = pygame.image.load('Assets/sampah/dirty.png')
dirty = pygame.transform.scale(dirty, (GRID_SIZE, GRID_SIZE))
kulitPisang = pygame.image.load('Assets/sampah/kulitPisang.png')
kulitPisang = pygame.transform.scale(kulitPisang, (GRID_SIZE, GRID_SIZE))
appleSisa = pygame.image.load('Assets/sampah/appleSisa.png')
appleSisa = pygame.transform.scale(appleSisa, (GRID_SIZE, GRID_SIZE))
trash = pygame.image.load('Assets/sampah/trash.png')
trash = pygame.transform.scale(trash, (GRID_SIZE, GRID_SIZE))

# asset obstacle
stone1 = pygame.image.load('Assets/obstacle/stone1.png')
stone1 = pygame.transform.scale(stone1, (GRID_SIZE, GRID_SIZE))
stone2 = pygame.image.load('Assets/obstacle/stone2.png')
stone2 = pygame.transform.scale(stone2, (GRID_SIZE, GRID_SIZE))
stone3 = pygame.image.load('Assets/obstacle/stone3.png')
stone3 = pygame.transform.scale(stone3, (GRID_SIZE, GRID_SIZE))
stone4 = pygame.image.load('Assets/obstacle/stone4.png')
stone4 = pygame.transform.scale(stone4, (GRID_SIZE, GRID_SIZE))
stone5 = pygame.image.load('Assets/obstacle/stone5.png')
stone5 = pygame.transform.scale(stone5, (GRID_SIZE, GRID_SIZE))
stone6 = pygame.image.load('Assets/obstacle/stone6.png')
stone6 = pygame.transform.scale(stone6, (GRID_SIZE, GRID_SIZE))
stone7 = pygame.image.load('Assets/obstacle/stone7.png')
stone7 = pygame.transform.scale(stone7, (GRID_SIZE, GRID_SIZE))
stone8 = pygame.image.load('Assets/obstacle/stone8.png')
stone8 = pygame.transform.scale(stone8, (GRID_SIZE, GRID_SIZE))
stone9 = pygame.image.load('Assets/obstacle/stone9.png')
stone9 = pygame.transform.scale(stone9, (GRID_SIZE, GRID_SIZE))

# Menambahkan daftar gambar sampah
sampah_images = [dirty, kulitPisang, appleSisa, trash]

# Menambahkan daftar gambar buah
buah_images = [apple, banana, watermelon]

# Menambahkan daftar gambar obstacle
obstacle_images = [stone1, stone2, stone3, stone4, stone5, stone6, stone7, stone8, stone9]

# Memasukkan suara
crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')
die_sound = pygame.mixer.Sound('Sound/mixkit-little-piano-game-over-1944.wav')

# Kelas utama untuk game
class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Proyek SD - Linkedlist Snake Game")
        self.clock = pygame.time.Clock()
        self.sampah_positions = []  # Inisialisasi posisi sampah sebagai daftar kosong
        self.sampah_images = []     # Inisialisasi daftar gambar sampah yang sesuai dengan posisi sampah
        self.buah_positions = [] # Inisialisasi posisi buah sebagai daftar kosong
        self.buah_images = []  # Inisialisasi daftar gambar buah yang sesuai dengan posisi buah
        self.obstacle_positions = []  # Inisialisasi posisi obstacle sebagai daftar kosong
        self.obstacle_images = []  # Inisialisasi daftar gambar obstacle yang sesuai dengan posisi obstacle
        self.sampah_timer = 0       # Reset timer sampah
        self.buah_timer = 0
        self.obstacle_timer = 0
        self.reset()
        
    # Kalau snake mati maka akan reset semuanya
    def reset(self):
        self.snake = Snake((GRID_WIDTH // 2, GRID_HEIGHT // 2))
        self.sampah_positions = []
        self.sampah_images = []
        self.sampah_timer = 0
        self.buah_positions = []
        self.buah_images = []
        self.buah_timer = 0
        self.obstacle_positions = []
        self.obstacle_images = []
        self.obstacle_timer = 0
        self.snake_direction = (1, 0)
        self.food_position = self.getRandomFoodPos()
        self.food_image = random.choice(buah_images)
        self.score = 0
    
    def getRandomFoodPos(self):
        while True:
            position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if not self.isEatenBySnake(position) and position not in self.sampah_positions and position not in self.obstacle_positions:
                return position

    def isEatenBySnake(self, position):
        current = self.snake.head
        while current:
            if current.position == position:
                return True
            current = current.next
        return False
    
    def isTrashEaten(self, position):
        return position in self.sampah_positions
    
    def isObstacle(self, position):
        return position in self.obstacle_positions

    # Cek apakah posisi random trash bertabrakan dengan ular atau makanan
    def getRandomTrashPos(self):
        while True:
            position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if not self.isEatenBySnake(position) and position != self.food_position and position not in self.obstacle_positions:
                return position

    # Cek apakah posisi random obstacle bertabrakan dengan ular atau makanan
    def getRandomObstaclePos(self):
        while True:
            position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if not self.isEatenBySnake(position) and position != self.food_position and position not in self.sampah_positions:
                return position

    def update(self):
        new_head_position = (
            (self.snake.head.position[0] + self.snake_direction[0]) % GRID_WIDTH,
            (self.snake.head.position[1] + self.snake_direction[1]) % GRID_HEIGHT
        )
        
        if self.isEatenBySnake(new_head_position) or self.isObstacle(new_head_position):
            self.play_die_sound()
            self.show_game_over_screen()
            self.reset()
        else:
            self.snake.addHead(new_head_position)
            
            if new_head_position == self.food_position:
                self.food_position = self.getRandomFoodPos()
                self.food_image = random.choice(buah_images)
                self.play_crunch_sound()
                self.score += 1
                self.buah_timer = pygame.time.get_ticks()  # Reset food timer
                
            elif self.isTrashEaten(new_head_position):
                self.snake.removeTail()
                self.snake.removeTail()
                index = self.sampah_positions.index(new_head_position)
                del self.sampah_positions[index]
                del self.sampah_images[index]
                self.play_crunch_sound()
                self.score -= 1
                if self.score == -1:
                    self.play_die_sound()
                    self.show_game_over_screen()
                    self.reset()
                self.sampah_timer = pygame.time.get_ticks()  # Reset sampah timer
            else:
                self.snake.removeTail()

        if pygame.time.get_ticks() - self.buah_timer > 5000:  # 5 detik ga diambil, reset food
            self.food_position = self.getRandomFoodPos()
            self.food_image = random.choice(buah_images)
            self.buah_timer = pygame.time.get_ticks()

    def draw(self):
        self.screen.fill((108, 108, 108))
        
        # Draw snake
        current = self.snake.head
        while current:
            pygame.draw.rect(
                self.screen,
                (0, 255, 0),
                pygame.Rect(current.position[0] * GRID_SIZE, current.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            )
            current = current.next
        
        # Draw food image
        self.screen.blit(self.food_image, (self.food_position[0] * GRID_SIZE, self.food_position[1] * GRID_SIZE))
        
        # Draw trash images
        for position, image in zip(self.sampah_positions, self.sampah_images):
            self.screen.blit(image, (position[0] * GRID_SIZE, position[1] * GRID_SIZE))

        # Draw obstacle images
        for position, image in zip(self.obstacle_positions, self.obstacle_images):
            self.screen.blit(image, (position[0] * GRID_SIZE, position[1] * GRID_SIZE))
        
        self.draw_score()
        pygame.display.flip()  # Update screen
    
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
            self.screen.blit(scaled_judul, (SCREEN_WIDTH//2-150, 20))
            score_text = font.render(f"Press any key to start", True, font_color)
            name1 = font.render(f"Crisnanda", True, font_color)
            name2 = font.render(f"Victor", True, font_color)
            name3 = font.render(f"Billy", True, font_color)

            text_rect = score_text.get_rect()
            name1_rect = name1.get_rect()
            name2_rect = name2.get_rect()
            name3_rect = name3.get_rect()
            # Posisi teks di tengah
            name1_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT//2-40)
            name2_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT//2-15)
            name3_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT//2+10)
            text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT//2+100)
        
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
    
    def show_game_over_screen(self):
        running = True
        while running:
            self.screen.fill((108, 108, 108))
            font_color = (0, 0, 0)
            font = pygame.font.Font(None, 36)
            scaled_judul = pygame.transform.scale(judul, (290, 200))
            self.screen.blit(scaled_judul, (SCREEN_WIDTH//2-150, 20))
            game_over_text = font.render(f"Game Over", True, font_color)
            score_text = font.render(f"Score: {self.score}", True, font_color)
            restart_text = font.render(f"Press any key to restart", True, font_color)
            
            game_over_rect = game_over_text.get_rect()
            score_rect = score_text.get_rect()
            restart_rect = restart_text.get_rect()
            
            game_over_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)
            score_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 )
            restart_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)
            
            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(score_text, score_rect)
            self.screen.blit(restart_text, restart_rect)
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
            if len(self.sampah_positions) == 0:
                self.sampah_positions.append(self.getRandomTrashPos())  # Spawn sampah
                self.sampah_images.append(random.choice(sampah_images))  # Randomly select a sampah image
                self.sampah_timer = pygame.time.get_ticks()  # Start timer
            elif len(self.sampah_positions) > 0:
                if self.score > 10 and len(self.sampah_positions) < 5:
                    self.sampah_positions.append(self.getRandomTrashPos())
                    self.sampah_images.append(random.choice(sampah_images))  # Randomly select a sampah image
                    
                if pygame.time.get_ticks() - self.sampah_timer > 3000:  # 3 detik ga diambil, reset sampah time
                    self.sampah_positions = []  # Inisialisasi posisi sampah kosong
                    self.sampah_images = []  # Inisialisasi daftar gambar sampah kosong

            if pygame.time.get_ticks() - self.obstacle_timer > 7000:  # 7 detik untuk spawn obstacle baru
                self.obstacle_positions = []
                self.obstacle_images = []
                for _ in range(5):  # Spawn 5 obstacles
                    self.obstacle_positions.append(self.getRandomObstaclePos())
                    self.obstacle_images.append(random.choice(obstacle_images))
                self.obstacle_timer = pygame.time.get_ticks()

if __name__ == "__main__":
    SnakeGame().run()
