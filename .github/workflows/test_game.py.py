import pygame
import sys  # 需要这个来完全退出

# 初始化
pygame.init()

# ==================== 1. 设置棋盘参数 ====================
BOARD_SIZE = 15       # 15x15标准棋盘
GRID_SIZE = 30        # 每个格子30像素
MARGIN = 30           # 边距30像素
WINDOW_SIZE = 2 * MARGIN + GRID_SIZE * (BOARD_SIZE - 1)  # 计算窗口大小

# ==================== 2. 创建窗口 ====================
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("五子棋 - 红色菊花 vs 黄色菊花")

# ==================== 3. 颜色定义 ====================
BOARD_COLOR = (220, 179, 92)  # 棋盘木色
LINE_COLOR = (0, 0, 0)        # 网格线黑色
RED = (255, 100, 100)         # 红色菊花
YELLOW = (255, 255, 150)      # 黄色菊花
CENTER_COLOR = (255, 180, 0)  # 花蕊橙色

# ==================== 4. 游戏数据 ====================
# 棋盘状态：0=空，1=红色菊花，2=黄色菊花
board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
current_player = 1  # 1=红色先手，2=黄色
game_over = False
winner = 0

# ==================== 5. 绘制棋盘 ====================
def draw_board():
    """绘制棋盘网格和定位点"""
    # 填充棋盘背景
    screen.fill(BOARD_COLOR)
    
    # 绘制网格线
    for i in range(BOARD_SIZE):
        # 横线
        start_pos = (MARGIN, MARGIN + i * GRID_SIZE)
        end_pos = (WINDOW_SIZE - MARGIN, MARGIN + i * GRID_SIZE)
        pygame.draw.line(screen, LINE_COLOR, start_pos, end_pos, 2)
        
        # 竖线
        start_pos = (MARGIN + i * GRID_SIZE, MARGIN)
        end_pos = (MARGIN + i * GRID_SIZE, WINDOW_SIZE - MARGIN)
        pygame.draw.line(screen, LINE_COLOR, start_pos, end_pos, 2)
    
    # 绘制五个定位点（天元和星）
    points = [(3, 3), (3, 11), (7, 7), (11, 3), (11, 11)]
    for x, y in points:
        center = (MARGIN + x * GRID_SIZE, MARGIN + y * GRID_SIZE)
        pygame.draw.circle(screen, LINE_COLOR, center, 6)

# ==================== 6. 绘制菊花棋子 ====================
def draw_flower_piece(row, col, player):
    """在指定位置绘制菊花棋子"""
    center_x = MARGIN + col * GRID_SIZE
    center_y = MARGIN + row * GRID_SIZE
    radius = GRID_SIZE // 2 - 3  # 棋子半径
    
    # 选择颜色
    if player == 1:  # 红色菊花
        petal_color = RED
        center_color = CENTER_COLOR
    else:  # 黄色菊花
        petal_color = YELLOW
        center_color = CENTER_COLOR
    
    # 绘制8个花瓣（菊花形状）
    for angle in range(0, 360, 45):
        # 计算花瓣位置
        rad = angle * 3.14159 / 180
        petal_x = center_x + 0.7 * radius * pygame.math.Vector2(1, 0).rotate(angle).x
        petal_y = center_y + 0.7 * radius * pygame.math.Vector2(1, 0).rotate(angle).y
        
        # 绘制椭圆形花瓣
        pygame.draw.ellipse(screen, petal_color,
                           (petal_x - radius//3, petal_y - radius//4,
                            radius//1.5, radius//2))
    
    # 绘制花蕊
    pygame.draw.circle(screen, center_color, (center_x, center_y), radius//3)
    
    # 绘制花蕊细节（小点）
    for i in range(8):
        angle = i * 45
        dot_x = center_x + radius//5 * pygame.math.Vector2(1, 0).rotate(angle).x
        dot_y = center_y + radius//5 * pygame.math.Vector2(1, 0).rotate(angle).y
        pygame.draw.circle(screen, (200, 100, 0), (int(dot_x), int(dot_y)), radius//10)

# ==================== 7. 绘制所有棋子 ====================
def draw_all_pieces():
    """绘制棋盘上所有棋子"""
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] != 0:  # 如果有棋子
                draw_flower_piece(row, col, board[row][col])

# ==================== 8. 胜负判定 ====================
def check_win(row, col, player):
    """检查是否五子连珠"""
    # 四个方向：水平、垂直、对角线、反对角线
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    for dx, dy in directions:
        count = 1  # 当前位置已经有1个
        
        # 向正方向检查
        for step in range(1, 5):
            r, c = row + step * dx, col + step * dy
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == player:
                count += 1
            else:
                break
        
        # 向反方向检查
        for step in range(1, 5):
            r, c = row - step * dx, col - step * dy
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == player:
                count += 1
            else:
                break
        
        # 如果某个方向有5个或以上
        if count >= 5:
            return True
    
    return False

# ==================== 9. 显示状态信息 ====================
def draw_status():
    """显示当前游戏状态"""
    font = pygame.font.SysFont(None, 28)
    
    if game_over:
        if winner == 1:
            text = "🎯 红色菊花获胜！点击重新开始"
        else:
            text = "🎯 黄色菊花获胜！点击重新开始"
    else:
        if current_player == 1:
            text = "🌺 当前：红色菊花下棋"
        else:
            text = "🌼 当前：黄色菊花下棋"
    
    # 渲染文字
    text_surface = font.render(text, True, (50, 50, 50))
    
    # 绘制半透明背景
    text_bg = pygame.Surface((text_surface.get_width() + 20, text_surface.get_height() + 10))
    text_bg.set_alpha(180)
    text_bg.fill((255, 255, 255))
    
    # 显示文字
    screen.blit(text_bg, (WINDOW_SIZE//2 - text_surface.get_width()//2 - 10, 5))
    screen.blit(text_surface, (WINDOW_SIZE//2 - text_surface.get_width()//2, 10))

# ==================== 10. 重置游戏 ====================
def reset_game():
    """重新开始游戏"""
    global board, current_player, game_over, winner
    board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    current_player = 1  # 红色先手
    game_over = False
    winner = 0

# ==================== 11. 主游戏循环 ====================
running = True
while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 鼠标左键点击
            mouse_x, mouse_y = event.pos
            
            if game_over:
                # 游戏结束，点击重新开始
                reset_game()
            else:
                # 计算点击的棋盘位置
                col = round((mouse_x - MARGIN) / GRID_SIZE)
                row = round((mouse_y - MARGIN) / GRID_SIZE)
                
                # 检查是否在棋盘内且位置为空
                if (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and 
                    board[row][col] == 0):
                    
                    # 放置棋子
                    board[row][col] = current_player
                    
                    # 检查是否获胜
                    if check_win(row, col, current_player):
                        game_over = True
                        winner = current_player
                    else:
                        # 切换玩家
                        current_player = 3 - current_player  # 1变2，2变1
    
    # ==================== 绘制所有内容 ====================
    draw_board()          # 1. 绘制棋盘
    draw_all_pieces()     # 2. 绘制所有棋子
    draw_status()         # 3. 显示状态
    
    # 更新显示
    pygame.display.flip()

# ==================== 12. 退出游戏 ====================
pygame.quit()
sys.exit()