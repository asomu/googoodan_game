import pygame

# Global
# color
BLACK = (0, 0, 0)  # RGB
WHITE = (255, 255, 255)

screen_width = 1280
screen_height = 720

# 정보
level = 1
score = 0


def init():
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("이은이 구구단 게임")
    return screen


def display_start_screen(screen, start_button):
    """draw circle(surface, color, center, radius, tick)

    :return: void
    """
    my_font = pygame.font.SysFont("hy그래픽m", 50, True, False)
    text_title = my_font.render("장이은 구구단 게임!", True, WHITE)
    screen.blit(text_title, [400, 200])
    text_start = my_font.render("시작!", True, WHITE)
    screen.blit(text_start, (screen_width / 2 - 60, screen_height - 140))
    pygame.draw.circle(screen, BLACK, start_button.center, 80, 5)


def start_game(screen):
    my_font = pygame.font.SysFont("hy그래픽m", 50, True, False)
    text_score = my_font.render(f"점수: {score}", True, WHITE)
    screen.blit(text_score, (800, 20))
    text_level = my_font.render(f"난이도: {level}단계", True, WHITE)
    screen.blit(text_level, (50, 20))


def main():
    pygame.init()
    screen = init()
    start_button = pygame.Rect(0, 0, 120, 120)
    start_button.center = (screen_width / 2, screen_height - 120)
    # display_stastart_gamert_screen(screen, start_button)
    start_game(screen)
    pygame.display.update()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(BLACK)


if __name__ == "__main__":
    main()
