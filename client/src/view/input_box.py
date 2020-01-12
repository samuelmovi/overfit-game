import pygame


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.SMALLFONT = pygame.font.Font('freesansbold.ttf', 22)
        self.rect = pygame.Rect(x, y, w, h)
        grey = (100, 100, 100)
        self.color = grey
        self.text = text
        self.txt_surface = self.SMALLFONT.render(self.text, True, self.color)
        self.active = False
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    if len(self.text) > 0:
                        self.text = self.text[:-1]
                        print("[#] Removing last character from input box: {}".format(self.text))
                        self.txt_surface = self.SMALLFONT.render(self.text, True, (0, 0, 0))
                else:
                    self.text += event.unicode
                    print("[#] adding character to input box: {}".format(self.text))
                # Re-render the text.
                self.txt_surface = self.SMALLFONT.render(self.text, True, self.color)
    
    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width
    
    def draw(self, screen):
        # blackout box
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 0)
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
    
    def get_text(self):
        return self.text
