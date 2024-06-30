import pygame
import sys
import random

# Inisialiasi kelas Node
class Node:
    def __init__(self, position):
        self.position = position #posisi dari tiap node (x,y) tuple
        self.next = None

# inisialisasi kelas snake berisi method-method untuk manipulasi snake
class Snake:
    def __init__(self, position):
        self.head = Node(position)
        self.tail = self.head
        self.length = 1
    
    def addHead(self, position): #ini fungsi sama kayak addFront
        new_node = Node(position)
        new_node.next = self.head
        self.head = new_node
        self.length += 1
    
    def removeHead(self): #ini fungsi sama kayak removeFront
        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            self.head = self.head.next
        self.length -= 1
    
    def removeTail(self): #ini fungsi sama kayak removeBack
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
GRID_SIZE = 30 #ukuran per grid dalam layar
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

#masukin aset-aset gambar
judul = pygame.image.load('Assets/judul.png')
apple_image = pygame.image.load('Assets/buah/apple.png')
apple_image = pygame.transform.scale(apple_image, (GRID_SIZE, GRID_SIZE))
kulit_pisang = pygame.image.load('Assets/sampah/kulitPisang.png')
kulit_pisang = pygame.transform.scale(kulit_pisang, (GRID_SIZE, GRID_SIZE))
dirty = pygame.image.load('Assets/sampah/dirty.png')
dirty = pygame.transform.scale(dirty, (GRID_SIZE, GRID_SIZE))

#masukin suara
crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')
die_sound = pygame.mixer.Sound('Sound/mixkit-little-piano-game-over-1944.wav')

#Kelas utama untuk game
class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Proyek SD - Linkedlist Snake Game")
        self.clock = pygame.time.Clock() #buat ngatur fps pygame
        self.trash_positions = [] # inisialisasi posisi trash sebagai daftar kosong
        self.trash_timer = 0 # reset timer trash
        self.food_timer = 0
        self.reset()
        
    # kalau snake mati maka akan reset semuanya
    def reset(self):
        self.snake = Snake((GRID_WIDTH // 2, GRID_HEIGHT // 2))
        self.trash_positions = []
        self.trash_timer = 0
        self.food_timer = pygame.time.get_ticks()
        self.snake_direction = (1, 0) # 1,0 kanan -1,0 kiri 0,1 bawah 0,-1 atas
        self.food_position = self.getRandomFoodPos()
        self.score = 0
    
    def getRandomFoodPos(self):
        while True:
            position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)) #x,y
            if not self.isEatenBySnake(position): #cek apakah posisi random food nabrak ular atau ga
                return position
            self.food_timer = pygame.time.get_ticks() # Reset food timer

    def isEatenBySnake(self, position):
        current = self.snake.head
        while current: #selama current bukan None maka akan cek posisinya apakah sama dengan posisi yang diinput
            if current.position == position:
                return True
            current = current.next
        return False
    
    def isTrashEaten(self, position):
        return position in self.trash_positions #cek apakah position ada di list trash_positions

    # cek apakah posisi random trash bertabrakan dengan ular gak
    def getRandomTrashPos(self):
        while True:
            position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if not self.isEatenBySnake(position) and position != self.food_position:
                return position

    def update(self):
        # tuple of new head position, modulo buat ngecek apakah snake nabrak tembok atau ga
        # kalo nabrak tembok, bakal balik ke sisi seberang 
        # contoh: new_head_position (x) = 30 + 1 % 30 = 1, maka x sekarang di 1 (ujung kiri)
        new_head_position = (
            (self.snake.head.position[0] + self.snake_direction[0]) % GRID_WIDTH, #posisi baru x
            (self.snake.head.position[1] + self.snake_direction[1]) % GRID_HEIGHT #posisi baru y
        )
        
        if self.isEatenBySnake(new_head_position): # kondisi jika snake nabrak ke badan sendiri
            self.play_die_sound()
            self.reset()
        else:
            self.snake.addHead(new_head_position) #manipulasi movement snake
            
            if new_head_position == self.food_position: #jika snake makan food
                self.food_position = self.getRandomFoodPos() #spawn makanan baru
                self.play_crunch_sound()
                self.score += 1
                self.food_timer = pygame.time.get_ticks() # Reset food timer
                
            elif self.isTrashEaten(new_head_position):  #jika snake makan sampah
                self.snake.removeTail() #remove tail pertama untuk manipulasi gerakan
                self.snake.removeTail() #remove tail pertama untuk mengurangi segmen
                self.trash_positions.remove(new_head_position)
                self.play_crunch_sound()
                self.score -= 1
                if self.score == -1: #jika score -1 maka game over
                    self.play_die_sound()
                    self.reset()
                self.trash_timer = pygame.time.get_ticks() # Reset trash timer
            else:
                self.snake.removeTail() # Manipulasi movement snake

        if pygame.time.get_ticks() - self.food_timer > 5000: #5 detik ga diambil, reset food
            self.food_position = self.getRandomFoodPos()
            self.food_timer = pygame.time.get_ticks()

    def draw(self):
        self.screen.fill((108, 108, 108))
        
        # draw snake
        current = self.snake.head
        while current:
            pygame.draw.rect(
                self.screen,
                (0, 255, 0),
                pygame.Rect(current.position[0] * GRID_SIZE, current.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            )
            current = current.next
        
        # draw food image
        self.screen.blit(apple_image, (self.food_position[0] * GRID_SIZE, self.food_position[1] * GRID_SIZE))
        
        
        #draw trash 
        for position in self.trash_positions:
            self.screen.blit(dirty, (position[0] * GRID_SIZE, position[1] * GRID_SIZE))
        
        self.draw_score()
        pygame.display.flip() #update screen
    
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
    
    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.snake_direction != (0, 1): #kalo arahnya ke bawah, ga bisa ke atas
                    self.snake_direction = (0, -1)
                elif event.key == pygame.K_DOWN and self.snake_direction != (0, -1): #kalo arahnya ke atas, ga bisa ke bawah
                    self.snake_direction = (0, 1)
                elif event.key == pygame.K_LEFT and self.snake_direction != (1, 0): #kalo arahnya ke kanan, ga bisa ke kiri
                    self.snake_direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and self.snake_direction != (-1, 0): #kalo arahnya ke kiri, ga bisa ke kanan
                    self.snake_direction = (1, 0)

    def run(self):
        self.draw_start_screen()
        while True:
            self.handle_keys()
            self.update()
            self.draw()
            self.clock.tick(10) #artinya 10 fps
            if len(self.trash_positions) == 0:
                self.trash_positions.append(self.getRandomTrashPos()) # Spawn trash
                self.trash_timer = pygame.time.get_ticks() # Start timer
            elif len(self.trash_positions) > 0:
                if self.score > 10 and len(self.trash_positions) < 5: # jika skor lebih dari 10 dan jumlah trash kurang dari 5, trash baru akan spawn
                    self.trash_positions.append(self.getRandomTrashPos()) 
                    
                # jika trash tidak diambil dalam 3 detik, daftar trash direset menjadi kosong
                if pygame.time.get_ticks() - self.trash_timer > 3000: # 3 detik ga diambil, reset trash time
                    self.trash_positions = []  # inisialisasi posisi trash kosong

if __name__ == "__main__":
    SnakeGame().run()
