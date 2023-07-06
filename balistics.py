import pygame
import sys
from math import sin, cos, pi
import matplotlib.pyplot as plt

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

# Definir um evento personalizado
CUSTOM_EVENT = pygame.USEREVENT + 1

# Criar um evento que será disparado a cada 0.5 segundos
pygame.time.set_timer(CUSTOM_EVENT, 500)

# Matriz de velocidades horizontal, vertical e módulo
tempo = list()
velocidades_x = list()
velocidades_y = list()
velocidades = list()

# Set the clock object to track time
clock = pygame.time.Clock()

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)
SKY = (135, 206, 235)  # Azul céu
GRASS = (34, 139, 34)  # Verde grama
SUN = (255, 255, 0)  # Amarelo sol

# Altura máxima
alt_max = 0.0

# Lista para armazenar os pontos da trajetória
trajetoria = [(int(posicao_x), int(posicao_y))]

# Tempo inicial do programa
start_time = pygame.time.get_ticks()

# Loop principal
while True:
    # Atualização do movimento
    dt = pygame.time.Clock().tick(60) / 1000.0  # Delta time
    posicao_x += velocidade_x * dt
    velocidade_y -= gravidade * dt
    posicao_y -= velocidade_y * dt

    altura = height - posicao_y

    if(altura > alt_max):
        alt_max = altura

    # Adiciona a posição atual na lista de trajetória
    trajetoria.append((int(posicao_x), int(posicao_y)))

    # Verificar se o projétil atingiu o solo
    if posicao_y >= height:
        break

    # Preencha o fundo da janela com a cor do céu
    window.fill(SKY)

    # Desenhe o sol
    pygame.draw.circle(window, SUN, (300, 125), 50)

    # Desenhe a grama
    pygame.draw.rect(window, GRASS, (0, height - 50, width, 50))

    # Atualizar o tempo decorrido
    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time - start_time) / 1000

    # Criar os objetos de texto para exibir a posição e a velocidade
    position_text = font.render(
        f'Posição: ({posicao_x:.2f}, {height - posicao_y:.2f}) m',
        True, BLACK
    )
    velocity_text = font.render(
        f'Velocidade: ({velocidade_x:.2f}, {velocidade_y:.2f}) m/s',
        True, BLACK
    )
    time_text = font.render(
        f'Tempo: {elapsed_time:.1f} s',
        True, BLACK
    )
    posicao_x_text = font.render(
        f'Distância horizontal: {posicao_x:.2f} m',
        True, BLACK
    )
    alt_max_text = font.render(
        f'Altura máxima: {alt_max:.2f} m',
        True, BLACK
    )

    # Exibir os textos na janela
    window.blit(position_text, (10, 10))
    window.blit(velocity_text, (10, 40))
    window.blit(time_text, (10, 70))
    window.blit(posicao_x_text, (10, 100))
    window.blit(alt_max_text, (10, 130))

    # Desenho da trajetória
    pygame.draw.lines(window, PURPLE, False, trajetoria, 5)

    # Desenho do projétil
    pygame.draw.circle(window, BLACK, (int(posicao_x), int(posicao_y)), 10)

    # Atualizar a lista
    for event in pygame.event.get():
        if event.type == CUSTOM_EVENT:
            tempo.append(elapsed_time)
            velocidades_x.append(velocidade_x)
            velocidades_y.append(velocidade_y)
            velocidades.append((velocidade_x**2 + velocidade_y**2)**0.5)

    # Atualização da tela
    pygame.display.flip()

#print(f'Posição: ({posicao_x:.2f}, {height - posicao_y:.2f})')
#print(f'Velocidade: ({velocidade_x:.2f}, {velocidade_y:.2f})')

# Plotar a curva com diferentes pontos
plt.plot(tempo, velocidades, marker='o', linestyle='-')
plt.plot(tempo, velocidades_x, marker='o', linestyle='-')
plt.plot(tempo, velocidades_y, marker='o', linestyle='-')

# Personalizar o gráfico
plt.legend(['Módulo', 'Horizontal', 'Vertical'])
plt.title('Velocidades')
plt.xlabel('Tempo (s)')
plt.ylabel('Velocidade (m/s)')

# Exibir o gráfico
plt.show()

sys.exit()
