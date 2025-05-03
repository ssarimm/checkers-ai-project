import os
import sys
import pygame
from game.game import Game
from ai.q_learning import QLearningAgent
from ai.minimax import MinimaxAgent
from config import *
import numpy as np


# Fonts
pygame.font.init()
TITLE_FONT  = pygame.font.SysFont("Verdana", 72, bold=True)
OPT_FONT    = pygame.font.SysFont("Verdana", 28)
CREDIT_FONT = pygame.font.SysFont("Verdana", 20, italic=True)


def draw_vertical_gradient(surface, top_color, bottom_color):
    h = surface.get_height()
    w = surface.get_width()
    for y in range(h):
        t = y / h
        r = int(top_color[0] * (1 - t) + bottom_color[0] * t)
        g = int(top_color[1] * (1 - t) + bottom_color[1] * t)
        b = int(top_color[2] * (1 - t) + bottom_color[2] * t)
        pygame.draw.line(surface, (r, g, b), (0, y), (w, y))


def draw_text_center(surface, text, font, color, center, shadow=False):
    if shadow:
        lbl = font.render(text, True, (0, 0, 0))
        rect = lbl.get_rect(center=(center[0] + 2, center[1] + 2))
        surface.blit(lbl, rect)
    lbl = font.render(text, True, color)
    rect = lbl.get_rect(center=center)
    surface.blit(lbl, rect)


def show_menu(screen):
    """Returns 0=HvH, 1=HvMinimax, 2=HvQ-Learning"""
    WIDTH, HEIGHT = screen.get_size()
    options = ["Human vs Human", "Human vs Minimax", "Human vs Q-Learning"]
    total_h = len(options) * BTN_H + (len(options) - 1) * GAP
    # shift button block up by 20px (or adjust as needed)
    start_y = HEIGHT // 2 - total_h // 2 + 20

    buttons = []
    for i, text in enumerate(options):
        x = (WIDTH - BTN_W) // 2
        y = start_y + i * (BTN_H + GAP)
        buttons.append((pygame.Rect(x, y, BTN_W, BTN_H), text))

    clock = pygame.time.Clock()
    selected = None
    while selected is None:
        clock.tick(FPS)
        mx, my = pygame.mouse.get_pos()

        # background
        draw_vertical_gradient(screen, TOP_COLOR, BOTTOM_COLOR)
        # title
        draw_text_center(screen, "Checkers AI", TITLE_FONT, WHITE, (WIDTH // 2, 80), shadow=True)

        # draw buttons
        for rect, text in buttons:
            hover = rect.collidepoint(mx, my)
            bg = BTN_HOVER if hover else BTN_COLOR
            pygame.draw.rect(screen, bg, rect, border_radius=BTN_RADIUS)
            pygame.draw.rect(screen, WHITE, rect, 2, border_radius=BTN_RADIUS)
            draw_text_center(screen, text, OPT_FONT, WHITE, rect.center)

        # credits
        draw_text_center(screen,
                         "BY: Sarim Shah, Moiz Ul Haq, Muhammad Rouhan",
                         CREDIT_FONT, YELLOW,
                         (WIDTH // 2, HEIGHT - 40))

        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                for idx, (rect, _) in enumerate(buttons):
                    if rect.collidepoint(e.pos):
                        selected = idx
                        break
    return selected


def show_winner(screen, winner):
    WIDTH, HEIGHT = screen.get_size()
    font = pygame.font.SysFont(None, 72)
    if winner == RED:
        text = "Red Wins!"
    elif winner == WHITE:
        text = "White Wins!"
    else:
        text = "Draw!"
    label = font.render(text, True, YELLOW)
    rect = label.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
    prompt = pygame.font.SysFont(None, 36).render("Click to return to menu", True, YELLOW)
    prect = prompt.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
    while True:
        screen.fill(BLACK)
        screen.blit(label, rect)
        screen.blit(prompt, prect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type in (pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                return


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Checkers AI")

    # ← Add these three lines to the top of main()
    TRAIN_MODE    = False   # Set True to train the Q‑agent when you pick option 3
    EPISODES      = 200     # How many episodes to run during training
    SAVE_INTERVAL = 50      # Save the model every N episodes

    while True:
        mode = show_menu(screen)
        #mode=2 for training purpose
        game = Game(screen)
        clock = pygame.time.Clock()

        ai_agent = None
        if mode == 1:
            ai_agent = MinimaxAgent(depth=DEPTH_LIMIT, color=WHITE)

        elif mode == 2:
            ai_agent = QLearningAgent(state_shape=STATE_SHAPE, action_size=ACTION_SIZE)
            ai_agent.color = WHITE

            # ← Load only if you're in PLAY mode
            if os.path.isfile(MODEL_PATH) and not TRAIN_MODE:
                ai_agent.load(MODEL_PATH)

            # ← If TRAIN_MODE, run the training loop, then go back to menu
            if TRAIN_MODE:
                print("\nStarting Q-Learning training...")
                best_reward = -np.inf
                for ep in range(1, EPISODES + 1):
                    game.reset()
                    r = ai_agent.train_episode(game)

                    if ep % SAVE_INTERVAL == 0:
                        ai_agent.save(MODEL_PATH)
                        print(f"Episode {ep}: reward = {r:.2f}")
                        if r > best_reward:
                            best_reward = r
                            ai_agent.save(f"data/best_model_{ep}.weights.h5")

                    # optional slow render to watch training
                    if ep % 100 == 0:
                        game.draw()
                        pygame.display.flip()
                        clock.tick(1)

                ai_agent.save(MODEL_PATH)
                print("Training completed!")
                ai_agent.plot_training()
                

                # back to menu
                continue

        # ─────────────────────────────────────────────
        # Now the same play loop you already have:
        running = True
        while running:
            clock.tick(FPS)
            running = game.handle_events(ai_agent if mode != 0 else None)
            game.update()
            game.draw()
            pygame.display.flip()
            if game.get_winner() is not None:
                running = False

        show_winner(screen, game.get_winner())

if __name__ == "__main__":
    main()
