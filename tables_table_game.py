import pygame
import random
import json
from dataclasses import dataclass

BLACK = (0, 0, 0)  # RGB
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

MY_FONT = "hy그래픽m"
CLEAR_LEVEL = 9
COUNT_OF_LEVELUP = 10
TIME_LIMIT = 10


def get_options():
    global MY_FONT, CLEAR_LEVEL, COUNT_OF_LEVELUP, TIME_LIMIT
    with open("option.json", "r", encoding="utf-8") as st_json:
        my_option = json.load(st_json)
    MY_FONT = my_option["MY_FONT"]
    CLEAR_LEVEL = my_option["CLEAR_LEVEL"]
    COUNT_OF_LEVELUP = my_option["COUNT_OF_LEVELUP"]
    TIME_LIMIT = my_option["TIME_LIMIT"]


class MySound:
    def __init__(self):
        self.fail = pygame.mixer.Sound("sound/fail.wav")
        self.start = pygame.mixer.Sound("sound/start.wav")
        self.running = pygame.mixer.Sound("sound/running.mp3")
        self.game_clear = pygame.mixer.Sound("sound/clear.mp3")
        self.collect = pygame.mixer.Sound("sound/pass.wav")


GAME_STATUS = {"START_STATUS": 0, "ENDING_STATUS": 1, "READY_STATUS": 2, "FAIL_STATUS": 3}


class TimesTableGame:
    def __init__(self):
        self.screen = None
        # 정보
        self.heart = 5
        self.level = 1
        self.count = 0
        self.score = 0
        self.var_a = 0
        self.var_b = 0
        self.result = ""
        self.is_new_problem = True
        # Flag of game starting.
        self.game_status = GAME_STATUS["READY_STATUS"]
        self.is_game_running = True
        self.display_time = None  # 숫자를 보여주는 시간
        self.start_ticks = None  # 시간 계산 (현재 시간 정보를 저장)
        self.image = None
        self.done_display_key_number = False
        self.is_game_clear = False
        self.sound_effect = None
        self.start_button = None
        self.click_pos = None
        self.key = ""

    def reset_status(self):
        """게임을 새로 시작하기전에 상태값을 초기화.

        :return:
        """
        self.heart = 5
        self.level = 1
        self.count = 0
        self.score = 0
        self.var_a = 0
        self.var_b = 0
        self.result = ""
        self.is_new_problem = True
        self.game_status = False
        self.is_game_running = True

    def init_screen(self):
        """pygame screen을 초기화.

        :return:
        """
        pygame.display.set_caption("이은이 구구단 게임")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.start_button = pygame.Rect(0, 0, 120, 120)
        self.start_button.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 120)

    def set_time_limit(self):
        """레벨별에 맞춰 시간제한을 설정함.

        :return:
        """
        # 얼마동안 숫자를 보여줄지
        self.display_time = TIME_LIMIT - self.level

    def display_opening_screen(self):
        """게임 opening 화면 출력

        :return: void
        """
        my_font = pygame.font.SysFont(MY_FONT, 50, True, False)
        text_title = my_font.render("이은이 구구단 게임!", True, WHITE)
        self.screen.blit(text_title, (400, 200))

        text_start = my_font.render("시작!", True, WHITE)
        self.screen.blit(text_start, (SCREEN_WIDTH / 2 - 60, SCREEN_HEIGHT - 140))

        pygame.draw.circle(self.screen, BLACK, self.start_button.center, 80, 5)

    def display_game_screen(self):
        """게임 진행 중인 화면을 출력함.

        :return:
        """
        self.set_key_value()
        self.draw_score()
        self.draw_heart()
        if self.is_new_problem:
            self.shuffle_numbers()
        self.draw_main_game_display()

    def shuffle_numbers(self):
        """새로운 문제를 내기 위해 1~9의 랜덤값을 var_a 와 var_b에 저장한다.
        그리고 제한시간을 체크하기 위한 시작 시간을 저장한다.

        :return:
        """
        self.is_new_problem = False
        self.var_a = random.randint(2, 9)
        self.var_b = random.randint(2, 9)
        self.start_ticks = pygame.time.get_ticks()

    def draw_score(self):
        """게임 스코어와 난이도를 화면에 출력한다.

        :return:
        """
        my_font = pygame.font.SysFont(MY_FONT, 50, True, False)
        text_score = my_font.render(f"점수: {self.score}", True, WHITE)
        self.screen.blit(text_score, (950, 20))

        text_level = my_font.render(f"난이도: {self.level}단계", True, WHITE)
        self.screen.blit(text_level, (50, 20))

    def draw_main_game_display(self):
        """구구단 문제와 key 입력값 그리고 시간제한을 화면에 출력한다.

        :return:
        """
        # 구구단 문제
        elapsed_time = (pygame.time.get_ticks() - self.start_ticks) / 1000  # ms => sec
        my_font = pygame.font.SysFont(MY_FONT, 120, True, False)
        text_quiz = my_font.render(f"{self.var_a} X {self.var_b} = {self.result}", True, WHITE)
        self.screen.blit(text_quiz, (200, 300))
        # 시간제한 출력
        my_font = pygame.font.SysFont(MY_FONT, 50, True, False)
        remain_time = max(self.display_time - int(elapsed_time), 0)
        text_time = my_font.render(f"{remain_time}", True, WHITE)
        self.screen.blit(text_time, (550, 20))
        # 시간제한을 넘기면 timeout 처리
        if elapsed_time > self.display_time + 1:
            self.is_new_problem = True
            self.fail_retry()

    def draw_heart(self):
        """Heart 화면에 출력
        
        :return: 
        """
        # Heart 그림 출력
        heard_image = pygame.image.load("image/heart_02.png").convert_alpha()
        for i in range(self.heart):
            self.screen.blit(heard_image, (640 + (i * 60), 20))

    def next_problem(self):
        """문제 맞았을 경우 처리
        
        :return: 
        """
        self.count += 1
        self.score += self.level * 10
        self.result = ""
        self.is_new_problem = True
        self.sound_effect.collect.play()
        if self.count == COUNT_OF_LEVELUP:
            self.level_up()

    def level_up(self):
        """레벨업 처리
        
        :return: 
        """
        self.level += 1
        self.count = 0
        self.set_time_limit()
        self.is_new_problem = True
        if self.level == CLEAR_LEVEL:
            self.game_status = GAME_STATUS["ENDING_STATUS"]

    def display_ending_screen(self):
        """게임 클리어 화면 출력.

        :return:
        """
        self.sound_effect.running.stop()
        self.sound_effect.game_clear.play(-1)
        my_font = pygame.font.SysFont(MY_FONT, 50, True, False)
        text_title = my_font.render("축하합니다.", True, WHITE)
        text_title_02 = my_font.render("엄마에게 보여주고 칭찬스티커 받으세요!", True, WHITE)
        self.screen.blit(text_title, [20, 200])
        self.screen.blit(text_title_02, [20, 300])
        self.image = pygame.image.load("image/heart_02.png").convert_alpha()
        self.screen.blit(self.image, [330, 200])

    def fail_retry(self):
        """문제를 틀렸을 때 Heart가 줄어들고 시간제한이 리셋됨.

        :return:
        """
        self.result = ""
        self.heart -= 1
        self.start_ticks = pygame.time.get_ticks()
        self.sound_effect.fail.play()
        if self.heart == 0:
            self.game_status = GAME_STATUS["FAIL_STATUS"]

    def judge_answer(self):
        """문제 결과를 판단한다.
        
        :return:
        """
        result = int(self.var_a) * int(self.var_b) == int(self.result) if self.result != "" else 0
        if result:
            self.next_problem()
        else:
            self.fail_retry()

    def set_key_value(self):
        """key 입력값을 숫자면 result에 저장하고 backspace일 경우 값 하나를 지운다.
        그리고 마지막에 동작 처리를 했다고 done_display_key_number 을 true 바꿔준다.
        바꾸지 않으면 key가 여러번 입력 처리되버린다.

        :return:
        """
        numbers = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}
        if self.key != "" and not self.done_display_key_number:
            if self.key in numbers and len(self.result) < 2:
                self.result += self.key
            elif self.key == "return":
                self.judge_answer()
            elif self.key == "backspace":
                self.result = self.result[:-1]
            self.done_display_key_number = True

    def display_game_over_screen(self):
        self.game_status = GAME_STATUS["FAIL_STATUS"]
        self.is_game_running = True
        self.sound_effect.running.stop()
        self.screen.fill(BLACK)
        my_font = pygame.font.SysFont(MY_FONT, 70, True, False)
        text_title = my_font.render("GAME OVER!", True, WHITE)
        self.screen.blit(text_title, [400, 300])
        text_score = my_font.render(f"레벨: {self.level}  점수: {self.score}", True, WHITE)
        self.screen.blit(text_score, [350, 400])
        pygame.display.update()
        pygame.time.delay(3000)
        self.reset_status()
        self.game_status = GAME_STATUS["READY_STATUS"]

    def check_clicked_start_btn(self, click_pos):
        if self.start_button.collidepoint(click_pos):
            self.sound_effect.start.play()
            self.game_status = GAME_STATUS["START_STATUS"]
            self.set_time_limit()
            pygame.time.delay(1000)
            self.sound_effect.running.play(-1)

    def get_event_status(self, event):
        """event를 전달받아 game status에 따라 data를 업데이트 한다.

        :param event: pygame.event.get() 으로 받은 event 중 하나를 전달 받음.
        :return:
        """
        if event.type == pygame.QUIT:
            self.is_game_running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            click_pos = pygame.mouse.get_pos()
            if self.game_status == GAME_STATUS["READY_STATUS"]:
                self.check_clicked_start_btn(click_pos)
        elif event.type == pygame.KEYDOWN:
            if self.game_status == GAME_STATUS["START_STATUS"]:
                self.done_display_key_number = False
                self.key = pygame.key.name(event.key)

    def display_screen(self):
        """game status에 따라 화면출력 함수를 호출
        검은화면을 채우고 data와 game status에 맞는 화면을 출력하고
        pygame.display.update() 로 화면 update 한다.

        :return:
        """
        self.screen.fill(BLACK)
        if self.game_status == GAME_STATUS["READY_STATUS"]:
            self.display_opening_screen()
        elif self.game_status == GAME_STATUS["START_STATUS"]:
            self.display_game_screen()
        elif self.game_status == GAME_STATUS["ENDING_STATUS"]:
            self.display_ending_screen()
        elif self.game_status == GAME_STATUS["FAIL_STATUS"]:
            self.display_game_over_screen()
        pygame.display.update()

    def run_game(self):
        """game loop 시작점, Event handling

        :return:
        """
        while self.is_game_running:
            self.key = ""
            for event in pygame.event.get():
                self.get_event_status(event)
            self.display_screen()

    def main(self):
        """game 시작점. main함수
        
        :return: 
        """
        pygame.init()
        self.init_screen()
        self.sound_effect = MySound()
        self.run_game()


if __name__ == "__main__":
    get_options()
    my_game = TimesTableGame()
    my_game.main()
