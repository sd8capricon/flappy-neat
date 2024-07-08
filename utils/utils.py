import pickle


def draw_text(text, font, text_col, x, y, screen):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def loadFile(path):
    with open(path, "rb") as f:
        file = pickle.load(f)
    return file
