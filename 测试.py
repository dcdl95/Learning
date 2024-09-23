import pygame
import time
import random
import json

# 初始化pygame库
pygame.init()

# 设置窗口大小
dis_width = 800
dis_height = 600
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')  # 设置窗口标题

# 定义颜色
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)

# 定义蛇的速度
snake_speed = 15
snake_block = 10

# 设置时钟，用于控制帧率
clock = pygame.time.Clock()

# 定义字体样式
font_style = pygame.font.SysFont(None, 50)

# 绘制蛇的身体
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])  # 绘制蛇的身体

# 显示消息
def message(msg, color):
    mesg = font_style.render(msg, True, color)  # 渲染文本
    dis.blit(mesg, [dis_width / 6, dis_height / 3])  # 在屏幕上显示文本

# 显示得分
def display_score(score):
    value = font_style.render("Score: " + str(score), True, green)  # 渲染得分文本
    dis.blit(value, [0, 0])  # 在屏幕上显示得分

# 保存历史分数
def save_high_scores(scores):
    with open('high_scores.json', 'w') as f:
        json.dump(scores, f)

# 加载历史分数
def load_high_scores():
    try:
        with open('high_scores.json', 'r') as f:
            scores = json.load(f)
    except FileNotFoundError:
        scores = []
    return scores

# 游戏主循环
def gameLoop():
    game_over = False  # 游戏是否结束
    game_close = False  # 游戏是否关闭

    # 初始化蛇的起始位置
    x1 = dis_width / 2
    y1 = dis_height / 2

    # 初始化蛇的方向变化量
    x1_change = 0
    y1_change = 0

    snake_List = []  # 蛇的身体列表
    Length_of_snake = 1  # 蛇的长度

    # 随机生成食物的位置
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    # 加载历史分数
    high_scores = load_high_scores()

    # 游戏主循环
    while not game_over:
        # 游戏结束处理
        while game_close == True:
            dis.fill(white)  # 清空屏幕
            message("You Lost! Press Q-Quit or C-Play Again", red)  # 显示游戏结束消息
            display_score(Length_of_snake - 1)  # 显示得分
            pygame.display.update()  # 更新屏幕

            # 处理键盘事件
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:  # 按Q键退出游戏
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:  # 按C键重新开始游戏
                        gameLoop()

        # 处理键盘事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 点击关闭按钮退出游戏
                game_over = True
            if event.type == pygame.KEYDOWN:  # 处理键盘按键
                if event.key == pygame.K_LEFT:  # 左箭头键
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:  # 右箭头键
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:  # 上箭头键
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:  # 下箭头键
                    y1_change = snake_block
                    x1_change = 0

        # 检测蛇是否撞墙或撞到自己
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change  # 更新蛇的横坐标
        y1 += y1_change  # 更新蛇的纵坐标

        # 清空屏幕
        dis.fill(white)
        # 绘制食物
        pygame.draw.rect(dis, red, [foodx, foody, snake_block, snake_block])

        # 更新蛇的身体列表
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # 检测蛇是否撞到自己
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        # 绘制蛇的身体
        our_snake(snake_block, snake_List)
        # 显示得分
        display_score(Length_of_snake - 1)

        # 更新屏幕
        pygame.display.update()

        # 检测蛇是否吃到食物
        if x1 == foodx and y1 == foody:
            # 重新生成食物位置
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            # 增加蛇的长度
            Length_of_snake += 1

            # 保存当前分数到历史分数
            score = Length_of_snake - 1
            high_scores.append(score)
            save_high_scores(high_scores)

        # 控制帧率
        clock.tick(snake_speed)

    # 退出游戏
    pygame.quit()
    quit()

# 启动游戏
gameLoop()