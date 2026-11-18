import json
import sys
from pathlib import Path

import pygame

N = 6                      # board is N x N squares
CELL = 90                  # size of one square in pixels
MARGIN = 40                # space around the board
W = H = N * CELL + MARGIN * 2
TOP = 90                   # space above the board for the campaign header

# Each stick: [row, column, length, direction]. The first stick is the RED one.
LEVELS = [
    [[2,1,2,"h"],[1,1,2,"h"],[4,3,2,"v"],[2,4,2,"v"]],
    [[2,0,2,"h"],[5,3,3,"h"],[2,3,3,"v"],[4,0,2,"h"],[1,4,2,"v"],[2,2,2,"v"]],
    [[2,0,2,"h"],[3,0,3,"h"],[4,2,2,"v"],[4,0,2,"h"],[0,3,2,"v"],[5,3,3,"h"],[1,4,3,"v"],[1,5,3,"v"]],
    [[2,0,2,"h"],[1,4,3,"v"],[4,1,2,"v"],[4,2,2,"v"],[1,5,3,"v"],[0,2,3,"h"],[3,0,3,"h"],[5,3,2,"h"],[1,0,2,"h"]],
    [[2,1,2,"h"],[4,2,2,"v"],[0,0,3,"v"],[3,0,3,"h"],[0,5,3,"v"],[4,3,3,"h"],[5,0,2,"h"],[0,4,3,"v"],[1,1,2,"h"],[5,4,2,"h"]],
    [[2,1,2,"h"],[5,4,2,"h"],[4,2,2,"v"],[1,4,3,"v"],[1,5,2,"v"],[3,1,3,"h"],[1,2,2,"h"],[1,0,3,"v"],[0,3,3,"h"],[0,1,2,"v"],[4,3,2,"h"]],
    [[2,0,2,"h"],[3,0,2,"v"],[0,4,3,"v"],[3,5,2,"v"],[4,2,2,"h"],[0,1,3,"h"],[4,1,2,"v"],[2,2,2,"v"],[1,5,2,"v"],[1,3,2,"v"],[3,3,2,"h"]],
    [[2,0,2,"h"],[3,3,3,"v"],[4,0,3,"h"],[1,3,2,"h"],[4,5,2,"v"],[1,2,2,"v"],[0,4,2,"h"],[4,4,2,"v"],[0,0,2,"v"],[3,1,2,"h"],[1,5,2,"v"],[0,1,2,"h"]],
]
LEVELS.extend([
    [[2,0,2,"h"],[1,2,2,"v"],[5,2,2,"h"],[1,3,2,"v"],[0,1,2,"v"],[3,2,3,"h"],[1,5,3,"v"],[0,3,3,"h"],[3,1,3,"v"],[4,3,3,"h"],[4,0,2,"v"]],
    [[2,0,2,"h"],[1,2,2,"v"],[2,5,2,"v"],[3,1,2,"v"],[5,2,2,"h"],[4,5,2,"v"],[1,4,3,"v"],[1,0,2,"h"],[0,4,2,"h"]],
    [[2,0,2,"h"],[1,2,2,"v"],[3,0,2,"v"],[5,1,3,"h"],[4,2,3,"h"],[3,2,3,"h"],[0,4,2,"h"],[0,3,2,"v"],[2,4,2,"h"]],
    [[2,0,2,"h"],[1,3,2,"v"],[1,5,3,"v"],[3,3,3,"v"],[3,1,3,"v"],[1,4,3,"v"],[0,2,2,"v"],[4,4,2,"h"]],
    [[2,0,2,"h"],[1,3,2,"v"],[0,1,2,"h"],[3,5,2,"v"],[3,0,2,"v"],[1,1,2,"h"],[5,3,2,"h"],[1,4,3,"v"],[3,1,3,"v"],[3,2,2,"v"],[4,3,2,"h"]],
    [[2,0,2,"h"],[0,2,3,"v"],[4,3,2,"h"],[1,3,3,"h"],[3,1,3,"v"],[2,4,2,"v"],[0,0,2,"h"],[0,4,2,"h"],[4,5,2,"v"],[5,2,3,"h"]],
    [[2,0,2,"h"],[1,2,2,"v"],[2,3,3,"v"],[0,1,2,"h"],[1,5,3,"v"],[5,4,2,"h"],[4,1,2,"h"],[1,4,3,"v"],[4,4,2,"h"]],
    [[2,0,2,"h"],[2,3,3,"v"],[2,4,3,"v"],[5,4,2,"h"],[3,1,3,"v"],[1,5,3,"v"],[0,4,2,"h"],[0,0,2,"h"],[3,0,2,"v"]],
    [[2,0,2,"h"],[2,3,2,"v"],[1,2,2,"h"],[0,0,2,"v"],[2,4,2,"v"],[4,3,3,"h"],[2,5,2,"v"],[2,2,3,"v"],[3,1,3,"v"],[0,3,3,"h"],[5,2,3,"h"]],
    [[2,0,2,"h"],[2,2,2,"v"],[2,4,2,"h"],[4,4,2,"h"],[3,3,2,"h"],[1,3,3,"h"],[0,0,2,"v"]],
    [[2,0,2,"h"],[1,2,2,"v"],[2,3,3,"v"],[0,4,2,"v"],[3,0,3,"h"],[2,4,2,"h"],[3,5,3,"v"],[5,0,3,"h"]],
    [[2,0,2,"h"],[1,3,2,"v"],[2,2,2,"v"],[1,4,2,"v"],[3,5,3,"v"],[3,4,2,"v"],[5,0,3,"h"],[1,5,2,"v"]],
])
EXTRA_LEVEL_ORDER = [0, 2, 9, 11, 5, 1, 7, 8, 10, 4, 3, 6]
LEVELS[8:] = [LEVELS[8 + index] for index in EXTRA_LEVEL_ORDER]
PARS = [2, 2, 5, 5, 9, 5, 5, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 5, 7, 7]
CHAPTERS = ["Courtyard", "Pillar Hall", "Royal Archive", "Sunken Sanctum"]
PROGRESS_FILE = Path.home() / ".slide_out_progress.json"


def load_progress():
    try:
        progress = json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return set()
    except (OSError, json.JSONDecodeError) as error:
        print(f"Could not read saved progress: {error}", file=sys.stderr)
        return set()
    if not isinstance(progress, list):
        return set()
    return {i for i in progress if isinstance(i, int) and not isinstance(i, bool) and 0 <= i < len(LEVELS)}


def save_progress(solved):
    try:
        PROGRESS_FILE.write_text(json.dumps(sorted(solved)), encoding="utf-8")
    except OSError as error:
        print(f"Could not save progress: {error}", file=sys.stderr)

pygame.init()
screen = pygame.display.set_mode((W, H + TOP))
pygame.display.set_caption("Slide Out")
font = pygame.font.SysFont("arial", 22, bold=True)
big = pygame.font.SysFont("georgia", 44, bold=True)
clock = pygame.time.Clock()


class Stick:
    def __init__(self, r, c, length, direction):
        self.r, self.c, self.len, self.dir = r, c, length, direction

    def cells(self):
        """All squares this stick covers."""
        if self.dir == "h":
            return [(self.r, self.c + i) for i in range(self.len)]
        return [(self.r + i, self.c) for i in range(self.len)]

    def rect(self, offset=0):
        """Pixel rectangle on the screen. offset is the drag distance in pixels."""
        x = MARGIN + self.c * CELL
        y = TOP + MARGIN + self.r * CELL
        w = self.len * CELL if self.dir == "h" else CELL
        h = self.len * CELL if self.dir == "v" else CELL
        if self.dir == "h":
            x += offset
        else:
            y += offset
        return pygame.Rect(x + 4, y + 4, w - 8, h - 8)


class Game:
    def __init__(self):
        self.level = 0
        self.solved = load_progress()
        self.screen = "home"
        self.buttons = []
        self.load()

    def load(self):
        self.sticks = [Stick(*p) for p in LEVELS[self.level]]
        self.moves = 0
        self.won = False
        self.drag = None        # (stick, mouse start, back squares, forward squares)
        self.offset = 0

    def unlocked_count(self):
        count = 1
        while count < len(LEVELS) and count - 1 in self.solved:
            count += 1
        return count

    def begin_level(self, level):
        if not 0 <= level < self.unlocked_count():
            return
        self.level = level
        self.load()
        self.screen = "game"

    def next_level(self):
        if self.level + 1 < len(LEVELS):
            self.begin_level(self.level + 1)
        else:
            self.screen = "levels"

    def occupied(self, skip=None):
        taken = set()
        for s in self.sticks:
            if s is not skip:
                taken.update(s.cells())
        return taken

    def free_space(self, s):
        """How many empty squares are behind and in front of stick s."""
        taken = self.occupied(skip=s)
        back = fwd = 0
        while True:
            r, c = (s.r, s.c - back - 1) if s.dir == "h" else (s.r - back - 1, s.c)
            if r < 0 or c < 0 or (r, c) in taken:
                break
            back += 1
        while True:
            r, c = (s.r, s.c + s.len + fwd) if s.dir == "h" else (s.r + s.len + fwd, s.c)
            if r >= N or c >= N or (r, c) in taken:
                break
            fwd += 1
        return back, fwd

    def press(self, pos):
        if self.won:
            return
        for s in self.sticks:
            if s.rect().collidepoint(pos):
                back, fwd = self.free_space(s)
                self.drag = (s, pos, back, fwd)
                self.offset = 0

    def motion(self, pos):
        if self.drag:
            s, start, back, fwd = self.drag
            d = (pos[0] - start[0]) if s.dir == "h" else (pos[1] - start[1])
            self.offset = max(-back * CELL, min(fwd * CELL, d))

    def release(self):
        if not self.drag:
            return
        s, _, _, _ = self.drag
        step = round(self.offset / CELL)
        if step:
            if s.dir == "h":
                s.c += step
            else:
                s.r += step
            self.moves += 1
            red = self.sticks[0]
            if red.c + red.len == N:      # red stick touched the door
                self.won = True
                self.solved.add(self.level)
                save_progress(self.solved)
        self.drag = None
        self.offset = 0

    def button(self, rect, label, action, payload=None, disabled=False, primary=False):
        fill = (115, 80, 36) if primary else (48, 59, 51)
        edge = (241, 210, 140) if primary else (159, 134, 87)
        text_color = (255, 243, 212) if not disabled else (133, 132, 119)
        if disabled:
            fill, edge = (38, 44, 40), (66, 72, 66)
        pygame.draw.rect(screen, (24, 28, 25), rect.move(0, 3), border_radius=8)
        pygame.draw.rect(screen, fill, rect, border_radius=8)
        pygame.draw.rect(screen, edge, rect, width=1, border_radius=8)
        label_font = pygame.font.SysFont("arial", 16 if primary else 13, bold=True)
        text = label_font.render(label, True, text_color)
        screen.blit(text, text.get_rect(center=rect.center))
        self.buttons.append((rect, action, payload, disabled))

    def menu_click(self, pos):
        for rect, action, payload, disabled in reversed(self.buttons):
            if disabled or not rect.collidepoint(pos):
                continue
            if action == "start":
                self.screen = "levels"
            elif action == "home":
                self.screen = "home"
            elif action == "level":
                self.begin_level(payload)
            elif action == "next":
                self.next_level()
            elif action == "levels":
                self.screen = "levels"
            return True
        return False

    def draw_home(self):
        screen.fill((27, 33, 30))
        pygame.draw.circle(screen, (35, 44, 38), (W // 2, 235), 125)
        pygame.draw.circle(screen, (190, 149, 75), (W // 2, 235), 100, 2)
        pygame.draw.circle(screen, (190, 149, 75), (W // 2, 235), 91, 1)
        gold, light = (228, 184, 94), (239, 209, 146)
        cx, cy = W // 2, 235
        pygame.draw.line(screen, gold, (cx - 58, cy + 40), (cx + 58, cy + 40), 3)
        pygame.draw.line(screen, gold, (cx - 48, cy + 31), (cx + 48, cy + 31), 2)
        pygame.draw.arc(screen, light, pygame.Rect(cx - 36, cy - 36, 72, 72), 3.14159, 6.28318, 3)
        pygame.draw.line(screen, light, (cx - 36, cy), (cx + 36, cy), 3)
        for dx in (-24, 0, 24):
            pygame.draw.line(screen, light, (cx + dx, cy + 2), (cx + dx, cy + 31), 3)
        pygame.draw.line(screen, gold, (cx - 52, cy + 48), (cx + 52, cy + 48), 2)
        pygame.draw.circle(screen, (173, 69, 51), (cx, cy - 19), 5)
        pygame.draw.circle(screen, light, (cx, cy - 19), 5, 1)
        title_font = pygame.font.SysFont("georgia", 56, bold=True)
        title = title_font.render("SLIDE OUT", True, (233, 199, 127))
        screen.blit(title, title.get_rect(center=(W // 2, 390)))
        kicker = pygame.font.SysFont("arial", 14, bold=True)
        line = kicker.render("AN ANCIENT PUZZLE ADVENTURE", True, (189, 165, 111))
        screen.blit(line, line.get_rect(center=(W // 2, 435)))
        subtitle = font.render("A path through the temple awaits.", True, (183, 173, 153))
        screen.blit(subtitle, subtitle.get_rect(center=(W // 2, 478)))
        self.button(pygame.Rect(W // 2 - 135, 525, 270, 52), "BEGIN YOUR JOURNEY   →", "start", primary=True)
        foot_font = pygame.font.SysFont("arial", 12)
        foot = foot_font.render("20 HANDCRAFTED TRIALS     ·     4 ANCIENT CHAMBERS", True, (169, 158, 137))
        screen.blit(foot, foot.get_rect(center=(W // 2, 602)))
        if self.solved:
            progress = foot_font.render(f"{len(self.solved)} OF {len(LEVELS)} TRIALS CLEARED", True, (215, 193, 142))
            screen.blit(progress, progress.get_rect(center=(W // 2, 627)))

    def draw_levels(self):
        screen.fill((27, 33, 30))
        self.button(pygame.Rect(22, 22, 100, 36), "←  HOME", "home")
        title_font = pygame.font.SysFont("georgia", 34, bold=True)
        title = title_font.render("Choose a chamber", True, (233, 199, 127))
        screen.blit(title, title.get_rect(center=(W // 2, 68)))
        subtitle_font = pygame.font.SysFont("arial", 14)
        subtitle = subtitle_font.render("Complete each trial to unlock the next.", True, (183, 173, 153))
        screen.blit(subtitle, subtitle.get_rect(center=(W // 2, 100)))

        progress_label = subtitle_font.render(
            f"TEMPLE PROGRESS     {len(self.solved)} / {len(LEVELS)} TRIALS CLEARED",
            True, (215, 193, 142))
        screen.blit(progress_label, (34, 138))
        bar = pygame.Rect(34, 160, W - 68, 7)
        pygame.draw.rect(screen, (19, 24, 21), bar, border_radius=4)
        fill = bar.copy()
        fill.width = round(bar.width * len(self.solved) / len(LEVELS))
        pygame.draw.rect(screen, (228, 184, 94), fill, border_radius=4)

        gap, left = 9, 24
        card_width = (W - left * 2 - gap * 3) // 4
        for chapter_index, chapter_name in enumerate(CHAPTERS):
            x = left + chapter_index * (card_width + gap)
            card = pygame.Rect(x, 185, card_width, 400)
            pygame.draw.rect(screen, (37, 45, 39), card, border_radius=9)
            pygame.draw.rect(screen, (96, 78, 51), card, width=1, border_radius=9)
            kicker = pygame.font.SysFont("arial", 10, bold=True)
            label = kicker.render(f"CHAMBER {chapter_index + 1:02}", True, (189, 165, 111))
            screen.blit(label, (x + 10, 198))
            chapter_font = pygame.font.SysFont("georgia", 15, bold=True)
            title = chapter_font.render(chapter_name, True, (240, 229, 207))
            screen.blit(title, (x + 10, 216))
            first_level = chapter_index * 5
            chapter_solved = sum(first_level + offset in self.solved for offset in range(5))
            count_font = pygame.font.SysFont("arial", 10)
            count_label = count_font.render(f"{chapter_solved}/5", True, (183, 173, 153))
            screen.blit(count_label, count_label.get_rect(topright=(x + card_width - 10, 201)))
            for offset in range(5):
                level = first_level + offset
                available = level < self.unlocked_count()
                complete = level in self.solved
                level_rect = pygame.Rect(x + 9, 243 + offset * 63, card_width - 18, 53)
                if complete:
                    fill, edge, number_color = (91, 69, 37), (228, 184, 94), (241, 210, 140)
                    state = "CLEARED"
                elif available:
                    fill, edge, number_color = (47, 76, 67), (77, 139, 119), (240, 229, 207)
                    state = "READY"
                else:
                    fill, edge, number_color = (35, 40, 37), (57, 63, 58), (135, 138, 128)
                    state = "LOCKED"
                pygame.draw.rect(screen, fill, level_rect, border_radius=7)
                pygame.draw.rect(screen, edge, level_rect, width=1, border_radius=7)
                level_font = pygame.font.SysFont("georgia", 20, bold=True)
                number = level_font.render(f"{level + 1:02}", True, number_color)
                screen.blit(number, (level_rect.x + 12, level_rect.y + 13))
                state_font = pygame.font.SysFont("arial", 9, bold=True)
                status = state_font.render(state, True, number_color)
                screen.blit(status, status.get_rect(midright=(level_rect.right - 10, level_rect.centery)))
                self.buttons.append((level_rect, "level", level, not available))

        hint_font = pygame.font.SysFont("arial", 12)
        hint = hint_font.render("The next chamber opens when you clear the current trial.", True, (169, 158, 137))
        screen.blit(hint, hint.get_rect(center=(W // 2, 624)))

    def draw(self):
        self.buttons = []
        if self.screen == "home":
            self.draw_home()
        elif self.screen == "levels":
            self.draw_levels()
        else:
            self.draw_game()

    def draw_game(self):
        screen.fill((27, 33, 30))
        pygame.draw.rect(screen, (37, 48, 41), (0, 0, W, 132))
        self.button(pygame.Rect(16, 39, 105, 30), "←  CHAMBERS", "levels")
        title_font = pygame.font.SysFont("georgia", 29, bold=True)
        title = title_font.render("SLIDE OUT", True, (233, 199, 127))
        screen.blit(title, title.get_rect(center=(W // 2, 25)))
        chapter_name = CHAPTERS[self.level // 5].upper()
        chapter_font = pygame.font.SysFont("arial", 13, bold=True)
        chapter = chapter_font.render(f"CHAPTER {self.level // 5 + 1}  ·  {chapter_name}", True, (215, 193, 142))
        screen.blit(chapter, chapter.get_rect(center=(W // 2, 53)))
        progress = pygame.Rect(130, 66, W - 260, 5)
        pygame.draw.rect(screen, (22, 29, 25), progress, border_radius=4)
        fill = progress.copy()
        fill.width = round(progress.width * (self.level + 1) / len(LEVELS))
        pygame.draw.rect(screen, (228, 184, 94), fill, border_radius=4)
        status = font.render(
            f"LEVEL  {self.level + 1} / {len(LEVELS)}     MOVES  {self.moves}     BEST  {PARS[self.level]}",
            True, (240, 229, 207))
        screen.blit(status, status.get_rect(center=(W // 2, 96)))
        board = pygame.Rect(MARGIN - 8, TOP + MARGIN - 8, N * CELL + 16, N * CELL + 16)
        pygame.draw.rect(screen, (69, 49, 32), board.inflate(4, 5), border_radius=16)
        pygame.draw.rect(screen, (133, 100, 64), board, border_radius=14)
        pygame.draw.rect(screen, (190, 155, 103), board, width=2, border_radius=14)
        for r in range(N):
            for c in range(N):
                sq = pygame.Rect(MARGIN + c * CELL + 3, TOP + MARGIN + r * CELL + 3, CELL - 6, CELL - 6)
                shade = 8 if (r + c) % 2 else 0
                stone = (185 - shade, 148 - shade, 96 - shade)
                pygame.draw.rect(screen, (85, 62, 39), sq, border_radius=5)
                face = sq.inflate(-3, -3)
                pygame.draw.rect(screen, stone, face, border_radius=4)
                pygame.draw.line(screen, (215, 181, 126), (face.left + 5, face.top + 2),
                                 (face.right - 5, face.top + 2), 1)
                pygame.draw.line(screen, (128, 96, 59), (face.left + 4, face.bottom - 2),
                                 (face.right - 4, face.bottom - 2), 1)
                pygame.draw.line(screen, (174, 137, 87), (face.left + 8, face.top + 12),
                                 (face.right - 8, face.top + 12), 1)
        door = pygame.Rect(MARGIN + N * CELL + 8, TOP + MARGIN + 2 * CELL + 6, 12, CELL - 12)
        pygame.draw.rect(screen, (255, 220, 137), door.inflate(4, 4), border_radius=5)
        pygame.draw.rect(screen, (203, 148, 57), door, border_radius=4)
        pygame.draw.line(screen, (255, 231, 173), (door.left + 3, door.top + 5),
                         (door.left + 3, door.bottom - 5), 2)
        for i, s in enumerate(self.sticks):
            off = self.offset if (self.drag and self.drag[0] is s) else 0
            rect = s.rect(off)
            shadow = rect.move(2, 6)
            pygame.draw.rect(screen, (42, 29, 21), shadow, border_radius=9)
            color = (173, 69, 51) if i == 0 else (40, 108, 116)
            edge = (112, 43, 33) if i == 0 else (23, 67, 73)
            pygame.draw.rect(screen, edge, rect, border_radius=9)
            face = rect.inflate(-3, -3)
            pygame.draw.rect(screen, color, face, border_radius=7)
            hi = (222, 129, 88) if i == 0 else (93, 159, 158)
            pygame.draw.line(screen, hi, (face.left + 7, face.top + 3),
                             (face.right - 7, face.top + 3), 2)
            inset = face.inflate(-12, -12)
            pygame.draw.rect(screen, (210, 145, 94) if i == 0 else (106, 162, 155),
                             inset, width=1, border_radius=5)
            points = ((face.left + 10, face.centery), (face.right - 10, face.centery)) if s.dir == "h" \
                else ((face.centerx, face.top + 10), (face.centerx, face.bottom - 10))
            for point in points:
                pygame.draw.circle(screen, (91, 61, 38), point, 4)
                pygame.draw.circle(screen, (231, 195, 119), point, 2)
        if self.won:
            shade = pygame.Surface((W, H + TOP), pygame.SRCALPHA)
            shade.fill((0, 0, 0, 150))
            screen.blit(shade, (0, 0))
            center_y = (H + TOP) // 2
            last_level = self.level == len(LEVELS) - 1
            title = "Temple conquered!" if last_level else "Chamber complete!"
            t = big.render(title, True, (241, 210, 140))
            screen.blit(t, t.get_rect(center=(W // 2, center_y - 25)))
            result = font.render(f"{self.moves} moves  ·  Best {PARS[self.level]}", True, (255, 255, 255))
            screen.blit(result, result.get_rect(center=(W // 2, center_y + 25)))
            if last_level:
                self.button(pygame.Rect(W // 2 - 135, center_y + 68, 270, 44),
                            "RETURN TO CHAMBERS", "levels", primary=True)
            else:
                self.button(pygame.Rect(W // 2 - 190, center_y + 68, 220, 44),
                            "NEXT CHAMBER  →", "next", primary=True)
                self.button(pygame.Rect(W // 2 + 38, center_y + 68, 152, 44),
                            "LEVEL MAP", "levels")


game = Game()
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        elif e.type == pygame.MOUSEBUTTONDOWN:
            previous_screen = game.screen
            button_clicked = game.menu_click(e.pos)
            if previous_screen == game.screen == "game" and not button_clicked and not game.won:
                game.press(e.pos)
        elif e.type == pygame.MOUSEMOTION:
            if game.screen == "game" and not game.won:
                game.motion(e.pos)
        elif e.type == pygame.MOUSEBUTTONUP:
            if game.screen == "game" and not game.won:
                game.release()
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE and game.screen == "game":
                game.screen = "levels"
            elif e.key in (pygame.K_RETURN, pygame.K_SPACE) and game.screen == "home":
                game.screen = "levels"
            elif e.key == pygame.K_r and game.screen == "game" and not game.won:
                game.load()                                   # restart level
            elif e.key == pygame.K_SPACE and game.screen == "game" and game.won:
                game.next_level()
    game.draw()
    pygame.display.flip()
    clock.tick(60)
