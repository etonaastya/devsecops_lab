import pygame
pygame.init()

screen_width = 800
screen_height = 600
window_size = (screen_width, screen_height)



bg_color = (255, 255, 255)
# Для заливки используйте ширину 0, иначе нарисуется только рамка
pygame.draw.rect(screen, bg_color, [0, 0, screen_width, screen_height], 0)

font = pygame.font.SysFont(None, 75)
text = font.render("Hello appsec world*", True, (0, 255, 0))
text_rect = text.get_rect()
text_rect.center = (400, 300)
screen.blit(text, text_rect)

# Выносим обновление экрана в цикл для корректной отрисовки
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()

pygame.quit()