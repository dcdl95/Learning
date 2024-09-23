import pygame
import json
import random
import time

# 初始化Pygame
pygame.init()

# 屏幕设置
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("贪吃蛇游戏")

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 字体设置
font_large = pygame.font.Font(None, 50)
font_small = pygame.font.Font(None, 30)

# 游戏参数
snake_block_size = 10
snake_speed = 15

# 菜单相关
menu_items = {
    "Start": (300, 200),
    "High Scores": (300, 300),
    "Exit": (300, 400)
}

def draw_text(surface, text, color, size, position):
    """绘制文本到指定位置"""
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect(center=position)
    surface.blit(text_surface, rect)

def draw_snake(block_size, snake_list):
    """绘制蛇的身体"""
    for block in snake_list:
        pygame.draw.rect(screen, BLACK, [block[0], block[1], block_size, block_size])

def show_high_scores(scores):
    """显示历史最高分"""
    screen.fill(WHITE)
    draw_text(screen, "High Scores", RED, 50, (screen_width/2, screen_height/4))
    y = screen_height / 3
    for score in scores:
        draw_text(screen, str(score), BLUE, 30, (screen_width/2, y))
        y += 40
    pygame.display.flip()

def load_high_scores():
    """加载历史最高分"""
    try:
        with open("scores.txt", "r") as file:
            return [int(line.strip()) for line in file.readlines()]
    except FileNotFoundError:
        return []

def save_high_score(score):
    """保存新的高分"""
    high_scores = load_high_scores()
    if score > min(high_scores):
        high_scores[-1] = score
        high_scores.sort(reverse=True)
        with open("scores.txt", "w") as file:
            for s in high_scores[:5]:  # 仅保存前五名
                file.write(f"{s}\n")

def main_menu():
    """主菜单界面"""
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for action, pos in menu_items.items():
                    if pos[0]-50 <= x <= pos[0]+50 and pos[1]-50 <= y <= pos[1]+50:
                        if action == "Start":
                            game_loop()
                        elif action == "High Scores":
                            scores = load_high_scores()
                            show_high_scores(scores)
                        elif action == "Exit":
                            pygame.quit()
                            return
        screen.fill(WHITE)
        for action, pos in menu_items.items():
            draw_text(screen, action, GREEN if action != "Exit" else RED, 50, pos)
        pygame.display.flip()

def game_loop():
    """游戏主循环"""
    # 初始化游戏状态
    game_over = False
    game_close = False
    snake_x, snake_y = screen_width//2, screen_height//2
    snake_list = [[snake_x, snake_y]]
    length_of_snake = 1
    direction = 'RIGHT'
    score = 0
    
    food_x, food_y = round(random.randrange(0, screen_width - snake_block_size)/10.0)*10.0, round(random.randrange(0, screen_height - snake_block_size)/10.0)*10.0
    
    clock = pygame.time.Clock()
    
    while not game_over:
        while game_close:
            screen.fill(WHITE)
            draw_text(screen, f"Game Over!\nScore: {length_of_snake-1}\nPress C to play again or Q to quit.", RED, 30, (screen_width/2, screen_height/2))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction != 'RIGHT':
                    direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    direction = 'RIGHT'
                elif event.key == pygame.K_UP and direction != 'DOWN':
                    direction = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    direction = 'DOWN'
                    
        # 移动蛇
        if direction == 'LEFT':
            snake_x -= snake_block_size
        elif direction == 'RIGHT':
            snake_x += snake_block_size
        elif direction == 'UP':
            snake_y -= snake_block_size
        elif direction == 'DOWN':
            snake_y += snake_block_size
        
        # 检查碰撞
        snake_head = [snake_x, snake_y]
        if snake_head in snake_list[:-1] or \
           snake_x < 0 or snake_x >= screen_width or \
           snake_y < 0 or snake_y >= screen_height:
            game_close = True
        else:
            snake_list.append(snake_head)
            if len(snake_list) > length_of_snake:
                del snake_list[0]
            
            # 吃食物
            if snake_x == food_x and snake_y == food_y:
                food_x, food_y = round(random.randrange(0, screen_width - snake_block_size)/10.0)*10.0, round(random.randrange(0, screen_height - snake_block_size)/10.0)*10.0
                length_of_snake += 1
                score += 1
                
        # 绘制画面
        screen.fill(WHITE)
        draw_snake(snake_block_size, snake_list)
        pygame.draw.rect(screen, RED, [food_x, food_y, snake_block_size, snake_block_size])
        draw_text(screen, f"Score: {score}", GREEN, 30, (10, 10))
        pygame.display.update()
        
        clock.tick(snake_speed)
    save_high_score(score)
    pygame.quit()
    quit()

if __name__ == "__main__":
    main_menu()