import pygame
import sys
from math import sin, cos, pi

# Largura e altura da janela
width = 1024
height = 640

def H(v, o):
    return (v*sin(o*pi/180))**2 / 19.6

def R(v, o):
    return v**2/9.8 * sin(2*o*pi/180)

def menu():
    while(True):
        # Requere a velocidade inicial ao usuário
        velocidade = float(input('Velocidade inicial: '))
        if velocidade < 0:
            print('A velocidade inicial deve ser maior que zero!')
            continue

        # Requere o ângulo ao usuário
        angulo = float(input('Angulo com a horizontal: '))
        if angulo < 0 or angulo > 90:
            print('O angulo deve possuir valor entre 0° e 90°!')
            continue

        # Verifica se os valores excedem os limites da tela
        if R(velocidade, angulo) > width:
            print(f'O alcance horizontal deve ser menor que {width} m!')
            continue
        elif H(velocidade, angulo) > height:
            print(f'O alcance vertical deve ser menor que {height} m!')
            continue
        else:
            return velocidade * cos(angulo * pi / 180), \
                   velocidade * sin(angulo * pi / 180)

# Velocidade e aceleração do experimento
velocidade_x, velocidade_y = menu()
#velocidade_x = 50.00
#velocidade_y = 50.00
gravidade = 9.8

# Inicialização do Pygame
pygame.init()

# Configurações da janela
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Experimento de Física - Balística")

# Definir a fonte e tamanho do texto
font = pygame.font.Font(None, 24)

# Posição inicial do experimento
posicao_x = 0
posicao_y = height

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)
SKY = (135, 206, 235)  # Azul céu
GRASS = (34, 139, 34)  # Verde grama
SUN = (255, 255, 0)  # Amarelo sol

# Lista para armazenar os pontos da trajetória
trajetoria = [(int(posicao_x), int(posicao_y))]

# Loop principal
while True:
    # Atualização do movimento
    dt = pygame.time.Clock().tick(60) / 1000.0  # Delta time
    posicao_x += velocidade_x * dt
    velocidade_y -= gravidade * dt
    posicao_y -= velocidade_y * dt

    # Adiciona a posição atual na lista de trajetória
    trajetoria.append((int(posicao_x), int(posicao_y)))

    # Verificar se o projétil atingiu o solo
    if posicao_y >= height:
        pygame.quit()
        print(f'Posição: ({posicao_x:.2f}, {height - posicao_y:.2f})')
        print(f'Velocidade: ({velocidade_x:.2f}, {velocidade_y:.2f})')
        sys.exit()

    # Preencha o fundo da janela com a cor do céu
    window.fill(SKY)

    # Desenhe o sol
    pygame.draw.circle(window, SUN, (100, 125), 50)

    # Desenhe a grama
    pygame.draw.rect(window, GRASS, (0, height - 50, width, 50))

    # Criar os objetos de texto para exibir a posição e a velocidade
    position_text = font.render(
        f'Posição: ({posicao_x:.2f}, {height - posicao_y:.2f}) m',
        True, BLACK
    )
    velocity_text = font.render(
        f'Velocidade: ({velocidade_x:.2f}, {velocidade_y:.2f}) m/s',
        True, BLACK
    )

    # Exibir os textos na janela
    window.blit(position_text, (10, 10))
    window.blit(velocity_text, (10, 40))

    # Desenho da trajetória
    pygame.draw.lines(window, PURPLE, False, trajetoria, 5)

    # Desenho do projétil
    pygame.draw.circle(window, BLACK, (int(posicao_x), int(posicao_y)), 10)

    # Atualização da tela
    pygame.display.flip()
