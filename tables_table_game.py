import pygame
import random

BLACK = (0, 0, 0)  # RGB
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
MY_FONT = "hy그래픽m"
CLEAR_LEVEL = 9

class TimesTableGame:
    def __init__(self):
        self.screen = None
        self.heart = 5
        self.screen_width = 1280
        self.screen_height = 720
        # 정보
        self.level = 1
        self.count = 0
        self.score = 0
        self.var_a = 0
        self.var_b = 0
        self.result = ""
        self.current_score = -1
        # Flag of game starting.
        self.start = False
        self.running = True
        self.display_time = None  # 숫자를 보여주는 시간
        self.start_ticks = None  # 시간 계산 (현재 시간 정보를 저장)
        self.setup_time()
        self.image = None
        self.check = False
        self.clear = False
        self.sound_fail = None
        self.sound_start = None
        self.sound_running = None
        self.sound_clear = None
        self.sound_pass = None

    def draw(self):
        self.image = pygame.image.load("image/heart_02.png").convert_alpha()
        for i in range(self.heart):
            self.screen.blit(self.image, (640 + (i * 60), 20))

    def init(self):
        screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("이은이 구구단 게임")
        return screen

    def setup_time(self):
        # 얼마동안 숫자를 보여줄지
        self.display_time = 10 - self.level

    def display_start_screen(self, start_button):
        """draw circle(surface, color, center, radius, tick)

        :return: void
        """
        my_font = pygame.font.SysFont(MY_FONT, 50, True, False)
        text_title = my_font.render("이은이 구구단 게임!", True, WHITE)
        self.screen.blit(text_title, [400, 200])
        text_start = my_font.render("시작!", True, WHITE)
        self.screen.blit(text_start, (self.screen_width / 2 - 60, self.screen_height - 140))
        pygame.draw.circle(self.screen, BLACK, start_button.center, 80, 5)

    def display_game_screen(self, key):
        self.display_score_screen()
        self.draw_random_number(key)

    def display_score_screen(self):
        my_font = pygame.font.SysFont(MY_FONT, 50, True, False)
        text_score = my_font.render(f"점수: {self.score}", True, WHITE)
        self.screen.blit(text_score, (950, 20))
        text_level = my_font.render(f"난이도: {self.level}단계", True, WHITE)
        self.screen.blit(text_level, (50, 20))

    def display_game_time_screen(self):
        self.display_score_screen()
        if self.current_score != self.score:
            self.current_score = self.score
            self.var_a = random.randint(2, 9)
            self.var_b = random.randint(2, 9)
            self.start_ticks = pygame.time.get_ticks()
        self.display_input_screen()
        pygame.display.update()

    def display_input_screen(self):
        elapsed_time = (pygame.time.get_ticks() - self.start_ticks) / 1000  # ms => sec
        my_font = pygame.font.SysFont(MY_FONT, 120, True, False)
        text_quiz = my_font.render(f"{self.var_a} X {self.var_b} = {self.result}", True, WHITE)
        self.screen.blit(text_quiz, (200, 300))
        my_font = pygame.font.SysFont(MY_FONT, 50, True, False)
        remain_time = self.display_time - int(elapsed_time)
        remain_time = max(remain_time, 0)
        text_time = my_font.render(f"{remain_time}", True, WHITE)
        self.screen.blit(text_time, (550, 20))
        self.draw()
        if elapsed_time > self.display_time + 1:
            self.timeout()

    def draw_random_number(self, key):
        if key == "return":
            if self.judge():
                self.next_step()
            else:
                self.fail_retry()
        elif key != "":
            self.set_result(key)
        self.display_input_screen()

    def next_step(self):
        self.count += 1
        self.score += self.level * 10
        self.result = ""
        self.sound_pass.play()
        if self.count == 10:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.count = 0
        self.setup_time()
        if self.level == CLEAR_LEVEL:
            self.clear = True

    def display_game_clear(self):
        self.clear = True
        self.sound_running.stop()
        self.sound_clear.play(-1)
        my_font = pygame.font.SysFont(MY_FONT, 50, True, False)
        text_title = my_font.render("축하합니다.", True, WHITE)
        text_title_02 = my_font.render("엄마에게 보여주고 칭찬스티커 받으세요!", True, WHITE)
        self.screen.blit(text_title, [20, 200])
        self.screen.blit(text_title_02, [20, 300])
        self.image = pygame.image.load("image/heart_02.png").convert_alpha()
        self.screen.blit(self.image, [330, 200])
        pygame.display.update()

    def fail_retry(self):
        self.result = ""
        self.heart -= 1
        print(f"HEART IS {self.heart}")
        self.start_ticks = pygame.time.get_ticks()
        self.sound_fail.play()
        if self.heart == 0:
            self.game_over()

    def timeout(self):
        self.result = ""
        self.heart -= 1
        print(f"HEART IS {self.heart}")
        self.current_score = -1
        pygame.time.delay(3000)
        self.start_ticks = pygame.time.get_ticks()
        if self.heart == 0:
            self.game_over()

    def judge(self):
        if self.result == "" and self.check is False:
            print(f"IT's NULL {self.heart}")
            return False
        else:
            print(f"JUDGE!!!")
            self.check = True
            return int(self.var_a) * int(self.var_b) == int(self.result)

    def set_result(self, key):
        numbers = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}
        if key in numbers:
            if len(self.result) > 1:
                pass
            else:
                self.result += key
        elif key == "backspace":
            self.result = self.result[:-1]

    def check_result(self):
        pass

    def game_over(self):
        self.level = 1
        self.count = 0
        self.score = 0
        self.var_a = 0
        self.var_b = 0
        self.heart = 5
        self.result = ""
        self.current_score = -1
        # Flag of game starting.
        self.start = False
        self.running = True
        self.sound_running.stop()
        self.screen.fill(BLACK)
        my_font = pygame.font.SysFont(MY_FONT, 70, True, False)
        text_title = my_font.render("GAME OVER!", True, WHITE)
        self.screen.blit(text_title, [400, 300])
        pygame.display.update()
        pygame.time.delay(3000)

    def check_buttons(self, pos, start_button):
        if start_button.collidepoint(pos):
            self.sound_start.play()
            self.start = True
            pygame.time.delay(1000)
            self.sound_running.play(-1)

    def main(self):
        pygame.init()
        self.screen = self.init()
        start_button = pygame.Rect(0, 0, 120, 120)
        start_button.center = (self.screen_width / 2, self.screen_height - 120)
        self.sound_fail = pygame.mixer.Sound("sound/fail.wav")
        self.sound_start = pygame.mixer.Sound("sound/start.wav")
        self.sound_running = pygame.mixer.Sound("sound/running.mp3")
        self.sound_clear = pygame.mixer.Sound("sound/clear.mp3")
        self.sound_pass = pygame.mixer.Sound("sound/pass.wav")
        while self.running:
            click_pos = None
            for event in pygame.event.get():
                key = ""
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    click_pos = pygame.mouse.get_pos()
                    print(click_pos)
                elif event.type == pygame.KEYDOWN:
                    self.check = False
                    key = pygame.key.name(event.key)
                    print(pygame.key.name(event.key))
                self.screen.fill(BLACK)
                if self.start:
                    if self.clear:
                        self.display_game_clear()
                    else:
                        self.display_game_screen(key)
                else:
                    self.display_start_screen(start_button)
                    # self.display_game_clear()

                if click_pos:
                    self.check_buttons(click_pos, start_button)
                pygame.display.update()
            self.screen.fill(BLACK)
            if self.start:
                if self.clear:
                    self.display_game_clear()
                else:
                    self.display_game_time_screen()


if __name__ == "__main__":
    my_game = TimesTableGame()
    my_game.main()
