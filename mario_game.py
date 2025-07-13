import pygame
import sys
import math

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
DARK_GREEN = (0, 128, 0)
SKY_BLUE = (135, 206, 235)

# Physics
GRAVITY = 0.8
JUMP_SPEED = -18
MARIO_SPEED = 5

class Mario:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.facing_right = True
        self.lives = 3
        self.score = 0
        self.power_up = 0  # 0: small, 1: big, 2: fire
        
    def update(self, platforms):
        keys = pygame.key.get_pressed()
        
        # Horizontal movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -MARIO_SPEED
            self.facing_right = False
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = MARIO_SPEED
            self.facing_right = True
        else:
            self.vel_x = 0
            
        # Jumping
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.vel_y = JUMP_SPEED
            self.on_ground = False
            
        # Apply gravity
        self.vel_y += GRAVITY
        
        # Update position
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Keep Mario on screen horizontally
        if self.x < 0:
            self.x = 0
        elif self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width
            
        # Check platform collisions
        self.on_ground = False
        mario_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        for platform in platforms:
            if mario_rect.colliderect(platform.rect):
                # Landing on top of platform
                if self.vel_y > 0 and self.y < platform.rect.top:
                    self.y = platform.rect.top - self.height
                    self.vel_y = 0
                    self.on_ground = True
                # Hitting platform from below
                elif self.vel_y < 0 and self.y > platform.rect.bottom:
                    self.y = platform.rect.bottom
                    self.vel_y = 0
                # Hitting platform from side
                elif self.vel_x > 0:
                    self.x = platform.rect.left - self.width
                elif self.vel_x < 0:
                    self.x = platform.rect.right
                    
        # Ground collision
        if self.y >= SCREEN_HEIGHT - self.height - 100:  # Ground level
            self.y = SCREEN_HEIGHT - self.height - 100
            self.vel_y = 0
            self.on_ground = True
            
        # Death condition
        if self.y > SCREEN_HEIGHT:
            self.lives -= 1
            self.x = 100
            self.y = SCREEN_HEIGHT - self.height - 100
            self.vel_y = 0
            
    def draw(self, screen):
        # Draw Mario as a simple colored rectangle with details
        mario_color = RED if self.power_up == 2 else (BLUE if self.power_up == 1 else RED)
        height = self.height if self.power_up == 0 else self.height + 16
        
        # Body
        pygame.draw.rect(screen, mario_color, (self.x, self.y, self.width, height))
        
        # Hat
        pygame.draw.rect(screen, RED, (self.x + 4, self.y - 8, self.width - 8, 8))
        
        # Overalls
        pygame.draw.rect(screen, BLUE, (self.x + 8, self.y + 12, self.width - 16, height - 12))
        
        # Face
        pygame.draw.circle(screen, (255, 220, 177), (int(self.x + self.width/2), int(self.y + 8)), 6)
        
        # Mustache
        pygame.draw.rect(screen, BLACK, (self.x + 12, self.y + 8, 8, 3))

class Platform:
    def __init__(self, x, y, width, height, color=BROWN):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)

class Goomba:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 24
        self.height = 24
        self.vel_x = -1
        self.alive = True
        
    def update(self, platforms):
        if not self.alive:
            return
            
        self.x += self.vel_x
        
        # Check platform collisions
        goomba_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        on_platform = False
        
        for platform in platforms:
            if goomba_rect.colliderect(platform.rect):
                if self.y < platform.rect.top:
                    self.y = platform.rect.top - self.height
                    on_platform = True
                elif self.vel_x > 0:
                    self.x = platform.rect.left - self.width
                    self.vel_x = -self.vel_x
                elif self.vel_x < 0:
                    self.x = platform.rect.right
                    self.vel_x = -self.vel_x
                    
        # Ground collision
        if self.y >= SCREEN_HEIGHT - self.height - 100:
            self.y = SCREEN_HEIGHT - self.height - 100
            on_platform = True
            
        # Turn around at screen edges
        if self.x <= 0 or self.x >= SCREEN_WIDTH - self.width:
            self.vel_x = -self.vel_x
            
    def draw(self, screen):
        if not self.alive:
            return
        # Draw Goomba as brown mushroom-like enemy
        pygame.draw.ellipse(screen, BROWN, (self.x, self.y + 8, self.width, self.height - 8))
        pygame.draw.ellipse(screen, (101, 67, 33), (self.x + 2, self.y, self.width - 4, 16))
        # Eyes
        pygame.draw.circle(screen, BLACK, (int(self.x + 6), int(self.y + 6)), 2)
        pygame.draw.circle(screen, BLACK, (int(self.x + 18), int(self.y + 6)), 2)

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 16
        self.height = 16
        self.collected = False
        self.rotation = 0
        
    def update(self):
        if not self.collected:
            self.rotation += 5
            
    def draw(self, screen):
        if not self.collected:
            # Draw spinning coin
            offset = math.sin(math.radians(self.rotation)) * 4
            pygame.draw.ellipse(screen, YELLOW, (self.x + offset, self.y, self.width - abs(offset*2), self.height))
            pygame.draw.ellipse(screen, ORANGE, (self.x + offset + 2, self.y + 2, self.width - abs(offset*2) - 4, self.height - 4))

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Super Mario Game")
        self.clock = pygame.time.Clock()
        
        # Initialize game objects
        self.mario = Mario(100, SCREEN_HEIGHT - 132)
        
        # Create platforms
        self.platforms = [
            Platform(300, SCREEN_HEIGHT - 200, 150, 20),
            Platform(500, SCREEN_HEIGHT - 300, 100, 20),
            Platform(750, SCREEN_HEIGHT - 250, 120, 20),
            Platform(950, SCREEN_HEIGHT - 400, 100, 20),
            Platform(1100, SCREEN_HEIGHT - 180, 80, 20),
            Platform(200, SCREEN_HEIGHT - 350, 80, 20),
            Platform(600, SCREEN_HEIGHT - 450, 100, 20),
        ]
        
        # Create enemies
        self.goombas = [
            Goomba(400, SCREEN_HEIGHT - 124),
            Goomba(800, SCREEN_HEIGHT - 124),
            Goomba(1000, SCREEN_HEIGHT - 124),
        ]
        
        # Create coins
        self.coins = [
            Coin(320, SCREEN_HEIGHT - 240),
            Coin(520, SCREEN_HEIGHT - 340),
            Coin(770, SCREEN_HEIGHT - 290),
            Coin(970, SCREEN_HEIGHT - 440),
            Coin(220, SCREEN_HEIGHT - 390),
        ]
        
        # Game state
        self.running = True
        self.game_over = False
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and self.game_over:
                    self.restart_game()
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
                    
    def update(self):
        if self.game_over:
            return
            
        # Update Mario
        self.mario.update(self.platforms)
        
        # Update enemies
        for goomba in self.goombas:
            goomba.update(self.platforms)
            
        # Update coins
        for coin in self.coins:
            coin.update()
            
        # Check collisions
        self.check_collisions()
        
        # Check game over conditions
        if self.mario.lives <= 0:
            self.game_over = True
            
    def check_collisions(self):
        mario_rect = pygame.Rect(self.mario.x, self.mario.y, self.mario.width, self.mario.height)
        
        # Mario vs Goombas
        for goomba in self.goombas:
            if goomba.alive:
                goomba_rect = pygame.Rect(goomba.x, goomba.y, goomba.width, goomba.height)
                if mario_rect.colliderect(goomba_rect):
                    # Mario jumping on Goomba
                    if self.mario.vel_y > 0 and self.mario.y < goomba.y:
                        goomba.alive = False
                        self.mario.vel_y = JUMP_SPEED // 2  # Small bounce
                        self.mario.score += 100
                    else:
                        # Mario hit by Goomba
                        if self.mario.power_up > 0:
                            self.mario.power_up -= 1
                        else:
                            self.mario.lives -= 1
                            self.mario.x = 100
                            self.mario.y = SCREEN_HEIGHT - self.mario.height - 100
                            
        # Mario vs Coins
        for coin in self.coins:
            if not coin.collected:
                coin_rect = pygame.Rect(coin.x, coin.y, coin.width, coin.height)
                if mario_rect.colliderect(coin_rect):
                    coin.collected = True
                    self.mario.score += 200
                    
    def draw(self):
        # Sky background
        self.screen.fill(SKY_BLUE)
        
        # Draw clouds
        for i in range(3):
            x = 200 + i * 400
            y = 100 + i * 50
            pygame.draw.circle(self.screen, WHITE, (x, y), 30)
            pygame.draw.circle(self.screen, WHITE, (x + 25, y), 35)
            pygame.draw.circle(self.screen, WHITE, (x + 50, y), 30)
            pygame.draw.circle(self.screen, WHITE, (x - 25, y), 25)
            
        # Draw ground
        pygame.draw.rect(self.screen, DARK_GREEN, (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))
        
        # Draw platforms
        for platform in self.platforms:
            platform.draw(self.screen)
            
        # Draw coins
        for coin in self.coins:
            coin.draw(self.screen)
            
        # Draw enemies
        for goomba in self.goombas:
            goomba.draw(self.screen)
            
        # Draw Mario
        self.mario.draw(self.screen)
        
        # Draw UI
        self.draw_ui()
        
        if self.game_over:
            self.draw_game_over()
            
        pygame.display.flip()
        
    def draw_ui(self):
        font = pygame.font.Font(None, 36)
        
        # Score
        score_text = font.render(f"Score: {self.mario.score}", True, BLACK)
        self.screen.blit(score_text, (10, 10))
        
        # Lives
        lives_text = font.render(f"Lives: {self.mario.lives}", True, BLACK)
        self.screen.blit(lives_text, (10, 50))
        
        # Power-up indicator
        power_names = ["Small", "Big", "Fire"]
        power_text = font.render(f"Power: {power_names[self.mario.power_up]}", True, BLACK)
        self.screen.blit(power_text, (10, 90))
        
    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        font = pygame.font.Font(None, 72)
        game_over_text = font.render("GAME OVER", True, WHITE)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        self.screen.blit(game_over_text, text_rect)
        
        font = pygame.font.Font(None, 36)
        restart_text = font.render("Press R to Restart or ESC to Quit", True, WHITE)
        text_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20))
        self.screen.blit(restart_text, text_rect)
        
        final_score_text = font.render(f"Final Score: {self.mario.score}", True, YELLOW)
        text_rect = final_score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 70))
        self.screen.blit(final_score_text, text_rect)
        
    def restart_game(self):
        self.mario = Mario(100, SCREEN_HEIGHT - 132)
        self.goombas = [
            Goomba(400, SCREEN_HEIGHT - 124),
            Goomba(800, SCREEN_HEIGHT - 124),
            Goomba(1000, SCREEN_HEIGHT - 124),
        ]
        self.coins = [
            Coin(320, SCREEN_HEIGHT - 240),
            Coin(520, SCREEN_HEIGHT - 340),
            Coin(770, SCREEN_HEIGHT - 290),
            Coin(970, SCREEN_HEIGHT - 440),
            Coin(220, SCREEN_HEIGHT - 390),
        ]
        self.game_over = False
        
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()