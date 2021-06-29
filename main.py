import pygame
import operator
import random

class Game():       # 난수 생성 클래스
    def random_calc(self, difficulty):
        ops = {'+': operator.add,
                '-': operator.sub,
                '*': operator.mul,
        }
        num1 = random.randint(0, difficulty)
        num2 = random.randint(1, difficulty)
        num3 = random.randint(1, 10)
        op = random.choice(list(ops.keys()))
        if op == '*':       # '*' 일때 숫자가 너무 크면 계산하기 힘드므로 num2는 1에서 10까지로 제한함
            num2 = num3
        nums = [num1, op, num2]
        return nums

    def question(self, nums):
        return f"{nums[0]} {nums[1]} {nums[2]}"     # return 앞에있는 f는 문자열 포맷팅 str을 리턴

    def getAnswer(self, nums):
        if nums[1] == '+':
            answer = nums[0] + nums[2]
        elif nums[1] == '-':
            answer = nums[0] - nums[2]
        elif nums[1] == '*':
            answer = nums[0] * nums[2]
        return answer

class TextInputBox(pygame.sprite.Sprite):   # 문제와 정답 생성 클래스
    def __init__(self, x, y, w, font):
        super().__init__()
        self.color_WHITE = (255, 255, 255)
        self.color_BLACK = (0, 0, 0)
        self.backcolor = None
        self.pos = (x, y) 
        self.width = w
        self.font = font
        self.active = True
        self.text = ""
        self.render_text()

    def render_text(self):
        # render() method를 통해 Text를 Surface 객체에 그려줌
        t_surf = self.font.render(self.text, True, self.color_BLACK, self.backcolor)
        self.image = pygame.Surface((max(self.width, t_surf.get_width()+10), t_surf.get_height()+10), pygame.SRCALPHA)
        self.image.blit(t_surf, (5, 5)) # 입력받은 글자를 그림
        pygame.draw.rect(self.image, self.color_WHITE, self.image.get_rect().inflate(-2, -2), 2)    # 정답 박스를 그림
        # self.image의 좌표와 크기를 저장
        self.rect = self.image.get_rect(topleft = self.pos)

    def reset(self):    # text 초기화
        self.text = ""
        self.active = True
        self.render_text()

    def update(self, event_list):
        for event in event_list:
            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_RETURN:    # 엔터를 누를 시 active에 False 대입
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:   # Backspace를 누를 시 하나 지움
                    self.text = self.text[:-1]
                else:   # text에 unicode 기반 문자를 추가함
                    self.text += event.unicode
                self.render_text()
    
    def request(self):  # 문제를 다시 생성
        global questions
        global answer
        global nums
        global quest
        global answer
        nums = g.random_calc(difficulty)
        quest = g.question(nums)
        answer = str(g.getAnswer(nums))
        questions = [quest]
        answer = [answer]

g = Game()
score = 0   # 점수
difficulty = 10 # 난이도
nums = g.random_calc(difficulty)    # 문제의 난수들
quest = g.question(nums)    # 문제
answer = str(g.getAnswer(nums))     # 문제의 답
questions = [quest]
answer = [answer]
current_question = 0 # 문제 번호(questions의 리스트 방식을 없앤다면 없어도 되는 기능)
lives = 3   # 목숨

pygame.init()   # pygame 초기화
window = pygame.display.set_mode((720, 720))    # 720, 720 사이즈
clock = pygame.time.Clock()     # fps
font100 = pygame.font.SysFont(None, 100)    # 글자 font100
font50 = pygame.font.SysFont(None, 50)      # 글자 font50

background_W = 720
background_H = 720
background = pygame.image.load('image/background01.jpg')
background = pygame.transform.scale(background, (background_W, background_H))

char_W = 60     # 캐릭터 가로 길이
char_H = 60     # 캐릭터 세로 길이
char_pos_x = 60     # 캐릭터 x좌표값 위치
char_pos_y = 495    # 캐릭터 y좌푝값 위치
char = pygame.image.load('image/pikachu.png')     # 이미지 불러오기
char = pygame.transform.scale(char, (char_W, char_H))   # 이미지 사이즈를 새로 맞춤

boss = pygame.image.load('image/dugtrio.png')     # 보스 이미지를 불러옴
boss_W = 180
boss_H = 180
boss = pygame.transform.scale(boss, (boss_W, boss_H))
boss_pos_x = 500
boss_pos_y = 420
boss_display = True     # True면 보스 생성
angle = 10      # 각도 값
def rotated_boss(boss, angle):      # 보스가 죽을 시 회전하는 함수
    global boss_pos_x
    global boss_pos_y
    boss_pos_x += 4             # 보스의 x위치 +4
    boss_pos_y -= 2             # 보스의 y위치 -2
    rotate = pygame.transform.rotate(boss, angle)   # 보스를 angle 만큼 회전
    window.blit(rotate, (boss_pos_x, boss_pos_y))   # 회전한 보스를 그림
Hp_pos_x = 200  # boss hp는 200
    

char_attack = pygame.image.load('image/attack.png')
char_attack = pygame.transform.scale(char_attack, (62, 42))
attack_active = False
attack_speed = 15   # 공격이 나가는 속도
attack_pos_x = 120  # 공격이 처음 생성되는 좌표 값
attack_pos_y = 500


text_input_box = TextInputBox(20, 250, 460, font100)
group_text = pygame.sprite.Group(text_input_box)

pygame.display.set_caption('Math Game')     # 제목

game_over_display = False   # game over 화면
##############################################
# main loop
##############################################
run = True  # 게임 동작 여부
while run:
    clock.tick(60) # fps는 60 (1초에 60번)
    event_list = pygame.event.get()     # 마우스 클릭을 했더나 키보드를 누른다거나 하는 것들
    for event in event_list:
        if event.type == pygame.QUIT:   # 위쪽 상단에 x 버튼 나가면 종료
            run = False
    ##########################################
    # Game Playing
    ##########################################
    if lives > 0: # 목숨이 0 이상이면
        group_text.update(event_list)       # TextInputBox의 update 함수 글자 입력과 지우는 기능과 텍스트가 너무 길시 박스를 늘리는 기능
        window.blit(background, (0, 0))     # 배경화면을 창에 띄움
        window.blit(char, (char_pos_x, char_pos_y))     # 캐릭터를 띄움
        score_surf = font50.render("score: " + str(score), True, (255, 255, 255))   # score 텍스트 쓰기
        window.blit(score_surf, (20, 20))       # 텍스트 띄우기
        lives_surf = font50.render("lives: " + str(lives), True, (255, 255, 255))   # lives text
        window.blit(lives_surf, (550, 20))
        question_surf = font100.render(questions[current_question], True, (255, 255, 255))  # question text
        window.blit(question_surf, (20, 150))
        group_text.draw(window)     # 답을 적을 공간을 그림
        if boss_display == True:
            window.blit(boss, (boss_pos_x, boss_pos_y))     # boss 이미지를 창에 띄움
        else:                           # 보스가 죽으면
            rotated_boss(boss, angle)   # 보스를 매 FPS마다 10도씩 회전시킴
            angle += 10
            if boss_pos_x >= 720:       # 화면 밖으로 벗어나면 
                boss_pos_x = 500        # 보스를 다시 생성시킴
                boss_pos_y = 420
                boss_display = True
                
        pygame.draw.rect(window, (255, 0, 0), [500, 400, Hp_pos_x, 20])     # Hp 바 그리기
        if attack_active == True:   # 문제를 맞췄다면
            window.blit(char_attack, (attack_pos_x, attack_pos_y))  # 공격 이미지를 그림
            attack_pos_x += attack_speed    # 공격의 x 좌표에 스피드 값만큼을 추가함
            if attack_pos_x >= 500:     # boss 이미지의 x 좌표에 도달했다면
                attack_active = False   # 공격 이미지를 삭제하고
                attack_pos_x = 120      # 공격 x좌표값을 초기화함
        if not text_input_box.active:   # 엔터를 눌렀을 때
            if text_input_box.text == answer[current_question]: # 답이 정답과 같다면
                attack_active = True    # 공격 이미지 활성화
                if int(text_input_box.text) >= 100: # 답이 100 이상이고
                    if score <= 1:      # score가 1보다 작거나 같을 때는
                        Hp_pos_x -= abs(int(text_input_box.text))   # 답만큼 hp바가 깎이고
                    else:   # score가 1보다 크면
                        Hp_pos_x -= abs(int(text_input_box.text) / (score / 2)) # score의 절반만큼 답을 나눈 값으로 hp바를 깎음
                else:   # 답이 100보다 작을 시
                    Hp_pos_x -= abs(int(text_input_box.text))   
                if Hp_pos_x <= 0:   # hp바가 다 깎였을 시 
                    boss_display = False    # 보스 이미지를 지움
                    Hp_pos_x = 200  # hp바 초기화
                    score += 1      # score + 1
                difficulty += 2     ## 정답을 맞출때마다 num2의 상한이 2씩 올라감 Game 클래스의 random_calc 매개변수 참고
                text_input_box.request()    # 문제다시 생성
            else:   # 답이 정답과 다르다면
                lives -= 1  # lives를 1깎음
                text_input_box.request()    # 문제 다시 생성
            text_input_box.reset()  # 정답란 초기화
    #########################################
    # Game Over
    #########################################
    elif lives == 0:
        window.fill(0)  # 화면 초기화(BLACK)
        game_over_display = True
        if game_over_display == True:
            game_over_surf = font100.render("Game Over", True, (255, 255, 255)) 
            window.blit(game_over_surf, game_over_surf.get_rect(centerx = 360, centery = 200))  # Game Over text를 띄움
            restart_surf = font50.render("Restart : Backspace", True, (255, 255, 255))
            window.blit(restart_surf, restart_surf.get_rect(centerx = 360, centery = 360))      # Restart text를 띄움
            if event in event_list:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE: # Backspace를 눌렀을 시 초기화
                        game_over_display = False       
                        lives += 3
                        score = 0
                        difficulty = 10
                        Hp_pos_x = 200
                        text_input_box.request()

    pygame.display.flip()   # 화면을 계속 업데이트 함

pygame.quit()   # Main Loop를 벗어나면 종료

### 코드 출처 :  https://www.debugcn.com/ko/article/107413267.html
#               https://github.com/GreggRoll/Halloween-Math/blob/master/game.py
#               https://snowdeer.github.io/python/2018/09/22/stars-in-space/
### 이미지 출처 : 
# (background) : https://www.freepik.com/free-vector/arcade-game-world-pixel-scene_4815143.htm#query=arcade-game-world-pixel-scene&position=8
# character : https://www.spriters-resource.com/custom_edited/supersmashbroscustoms/sheet/17154/
# boss : https://www.spriters-resource.com/game_boy_advance/pokemonfireredleafgreen/sheet/3713/ 
# attack : https://www.spriters-resource.com/custom_edited/supersmashbroscustoms/sheet/17154/