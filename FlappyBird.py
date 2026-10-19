import pygame
import os
import random

#CRIAR CLASSE PARAMETERS EM ARQUIVO SEPARADO
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 400

PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
FLOOR_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
BACKGROUND_IMG = pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'bg.png')), (400, 600))
BIRD_IMGS = [
    pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'bird1.png')), (63, 45)),
    pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'bird2.png')), (63, 45)),
    pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'bird3.png')), (63, 45))  
]

pygame.font.init()
POINTS_FONT = pygame.font.SysFont('arial', 50)

class Bird:

    IMGS = BIRD_IMGS

    #Animações da Rotação
    MAX_ROTATION = 25
    ROTATION_VELOCITY = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):        

        self.x = x
        self.y = y
        self.angle = 0
        self.velocity = 0
        self.height = self.y
        self.time = 0
        self.img_cont = 0
        self.current_img = self.IMGS[0]

    def jump(self):

        self.velocity = -10.5
        self.time = 0
        self.height = self.y

    def move(self):

        # Cálculo deslocamento
        self.time += 1
        displacement = 1.5 * (self.time**2) + self.velocity * self.time

        # Restrição deslocamento
        if displacement > 16:
            displacement = 16
        elif displacement < 0: # Testar sem essa condição
            displacement -= 2
        
        self.y += displacement

        # Ângulo do pássaro
        if displacement < 0 or self.y < (self.height + 50):
            if self.angle < self.MAX_ROTATION:
                self.angle = self.MAX_ROTATION
        else:
            if self.angle > -90:
                self.angle -= self.ROTATION_VELOCITY

    def draw(self, screen):

        # Definir qual imagem do pássro utilizar
        self.img_cont += 1

        if self.img_cont < self.ANIMATION_TIME:
            self.current_img = self.IMGS[0]
        elif self.img_cont < self.ANIMATION_TIME*2:
            self.current_img = self.IMGS[1]
        elif self.img_cont < self.ANIMATION_TIME*3:
            self.current_img = self.IMGS[2]
        elif self.img_cont < self.ANIMATION_TIME*4:
            self.current_img = self.IMGS[1]
        elif self.img_cont >= self.ANIMATION_TIME*4 + 1:
            self.current_img = self.IMGS[0]
            self.img_cont = 0

        # Se o pássaro estiver caindo, não irá bater as asas
        if self.angle <= -80:
            self.current_img = self.IMGS[1]
            self.img_cont = self.ANIMATION_TIME*2

        # Desenhar a imagem
        rotated_img = pygame.transform.rotate(self.current_img, self.angle)
        center_img = self.current_img.get_rect(topleft=(self.x, self.y)).center
        rectangle = rotated_img.get_rect(center=center_img)
        screen.blit(rotated_img, rectangle.topleft)

    def get_mask(self):

        return pygame.mask.from_surface(self.current_img)

class Pipe:

    DISTANCE = 200
    VELOCITY = 5

    def __init__(self, x):

        self.x = x
        self.height = 0
        self.pos_top = 0
        self.pos_bottom = 0
        self.TOP_PIPE = pygame.transform.flip(PIPE_IMG, False, True)
        self.BOTTOM_PIPE = PIPE_IMG
        self.passed = False
        self.define_height()

    def define_height(self):

        self.height = random.randrange(50, 350)
        self.pos_top = self.height - self.TOP_PIPE.get_height()
        self.pos_bottom = self.height + self.DISTANCE

    def move(self):

        self.x -= self.VELOCITY

    def draw(self, screen):

        screen.blit(self.TOP_PIPE, (self.x, self.pos_top))
        screen.blit(self.BOTTOM_PIPE, (self.x, self.pos_bottom))

    def colision(self, bird):
        
        bird_mask = bird.get_mask()

        top_mask = pygame.mask.from_surface(self.TOP_PIPE)
        bottom_mask = pygame.mask.from_surface(self.BOTTOM_PIPE)

        top_distance = (self.x - bird.x, self.pos_top - round(bird.y))
        bottom_distance = (self.x - bird.x, self.pos_bottom - round(bird.y))

        top_point = bird_mask.overlap(top_mask, top_distance)
        bottom_point = bird_mask.overlap(bottom_mask, bottom_distance)

        if top_point or bottom_point:
            return True
        else:
            return False

class Floor:

    VELOCITY = 5
    WIDTH = FLOOR_IMG.get_width()
    IMAGE = FLOOR_IMG

    def __init__(self, y):

        self.y = y
        self.x0 = 0
        self.x1 = self.WIDTH

    def move(self):

        self.x0 -= self.VELOCITY
        self.x1 -= self.VELOCITY

        if self.x0 + self.WIDTH < 0:
            self.x0 = self.x1 + self.WIDTH
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x0 + self.WIDTH
    
    def draw(self, screen):

        screen.blit(self.IMAGE, (self.x0, self.y))
        screen.blit(self.IMAGE, (self.x1, self.y))

def draw_screen(screen, birds, pipes, floor, points):

    screen.blit(BACKGROUND_IMG, (0, 0))
    
    for bird in birds:
        bird.draw(screen)

    for pipe in pipes:
        pipe.draw(screen)

    text = POINTS_FONT.render(f'Pontuação: {points}', 1, (255, 255, 255))

    screen.blit(text, (WINDOW_WIDTH - 10 - text.get_width(), 10))

    floor.draw(screen)

    pygame.display.update()

def main():

    birds = [Bird(50, 250)]
    floor = Floor(530)
    pipes = [Pipe(500)]
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    points = 0

    clock = pygame.time.Clock()

    running = True

    while running:

        clock.tick(30)

        # Interação com o usuário
        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                running = False
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:

                    for bird in birds:

                        bird.jump()

        # Mover objetos
        for bird in birds:

            bird.move()
        
        floor.move()

        add_pipe = False
        remove_pipe = []

        for pipe in pipes:

            for i, bird in enumerate(birds):

                if pipe.colision(bird):
                    
                    birds.pop(i)

                if not pipe.passed and bird.x > pipe.x:

                    pipe.passed = True
                    add_pipe = True
                
            pipe.move()

            if pipe.x + pipe.TOP_PIPE.get_width() < 0:

                remove_pipe.append(pipe)

        if add_pipe:

            points += 1
            pipes.append(Pipe(600))

        for pipe in remove_pipe:

            pipes.remove(pipe)
        
        for i, bird in enumerate(birds):

            if (bird.y + bird.current_img.get_height()) > floor.y or bird.y < 0:

                birds.pop(i)

        draw_screen(screen, birds, pipes, floor, points)

if __name__ == '__main__':

    main()