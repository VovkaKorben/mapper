import pygame, json, copy, random, box
from pygame.locals import *


def load_nodes():
    try:
        with open("nodes.json") as n:
            file_contents = n.read()
            result = json.loads(file_contents)
    except:
        result = []
    return result


def save_nodes(nodes):
    try:
        nc = nodes.copy()
        for n in nc:
            n.pop("selected", None)
            n.pop("used", None)
        nc = json.dumps(nc, indent=4)
        with open("nodes.json", "w") as n:
            n.write(nc)
        result = True
    except:
        result = False


def RectFromNode(node, size):
    return pygame.Rect(node["x"] - size, node["y"] - size, size * 2, size * 2)


def NodeAtMouse(nodes, mouse_pos):
    for n in nodes:
        if RectFromNode(n, NODE_SIZE).collidepoint(mouse_pos):
            return n
    return None


def NormalizeRect(rct):
    x1, y1, x2, y2 = rct
    if x1 > x2:
        x1, x2 = x2, x1
    if y1 > y2:
        y1, y2 = y2, y1
    return (x1, y1, x2 - x1, y2 - y1)


def init_nodes(nodes):
    for node in nodes:
        node["selected"] = False
        node["oldval"] = False
    return nodes


def AddNodes(nodes, cnt):
    MARGIN = 30
    for i in range(cnt):
        node = {
            "id": len(nodes),
            "x": random.randint(MARGIN, SCREEN_WIDTH - MARGIN),
            "y": random.randint(MARGIN, SCREEN_HEIGHT - MARGIN),
        }
        nodes.append(node)
    return nodes


mouse_down_pos, mouse_move_pos = (0, 0), (0, 0)
CLR_BG = (234, 212, 252)
CLR_BLACK = (0, 0, 0)
CLR_RED = (255, 0, 0)
CLR_BLUE = (0, 0, 255)
CLR_YELLOW = (200, 200, 0)
FONT_SIZE = 16
NODE_SIZE = 7
MODE_NONE = 0
MODE_DRAG = 1
MODE_NODE = 2
MODE_SELECTION = 3
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

mousemode = MODE_NONE


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("nodes test")
pygame.font.init()
my_font = pygame.font.SysFont("Courier New", FONT_SIZE)
node_font = pygame.font.SysFont("Arial Black", 12)

nodes = load_nodes()
nodes = init_nodes(nodes)
running = True

while running:
    shift = (pygame.key.get_mods() & pygame.KMOD_SHIFT) 
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_KP_PLUS:
                nodes = AddNodes(nodes, 1)
                nodes = init_nodes(nodes)  # reset node states
            elif event.key == pygame.K_KP_MINUS:
                nodes = nodes[:-1]
                nodes = init_nodes(nodes)  # reset node states

        elif event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEMOTION:
            mouse_move_pos = list(pygame.mouse.get_pos())
            if mousemode == MODE_NODE:
                delta = [mouse_move_pos[0] - mouse_down_pos[0], mouse_move_pos[1] - mouse_down_pos[1]]
                # print(f"delta: {delta}")

                for n in nodes:
                    if n["selected"]:
                        n["x"] += delta[0]
                        n["y"] += delta[1]
                mouse_down_pos = mouse_move_pos
            elif mousemode == MODE_SELECTION:
                rct = (
                    mouse_down_pos[0],
                    mouse_down_pos[1],
                    mouse_move_pos[0],
                    mouse_move_pos[1],
                )
                rct = pygame.Rect(NormalizeRect(rct))
                for n in nodes:
                    n["selected"] = n["oldval"] 
                    if rct.collidepoint(n["x"], n["y"]):
                        n["selected"] = not n["selected"]

        elif event.type == pygame.MOUSEBUTTONDOWN:

            mouse_down_pos = list(pygame.mouse.get_pos())
            current_node = NodeAtMouse(nodes, mouse_down_pos)

            if current_node == None:
                # empty space clicked
                if not shift:
                    for n in nodes:
                        n["selected"] = False
                for n in nodes:
                    n["oldval"] = n["selected"]

                mousemode = MODE_SELECTION
            else:
                # node clicked
                # if no SHIFT unselect all nodes
                if not shift:  # or (shift and current_node["selected"] == False):
                    for n in nodes:
                        n["selected"] = False
                current_node["selected"] = not current_node["selected"]
                mousemode = MODE_NODE

        elif event.type == pygame.MOUSEBUTTONUP:
            mousemode = MODE_NONE
    # bg
    screen.fill(CLR_BG)

    # draw nodes
    for n in nodes:
        rct = RectFromNode(n, NODE_SIZE)
        if n["selected"]:
            pygame.draw.rect(screen, CLR_BLACK, rct)
        else:
            pygame.draw.rect(screen, CLR_YELLOW, rct)
            pygame.draw.rect(screen, CLR_BLACK, rct, 2)
        # node ID
        text_surface = node_font.render(f"{n['id']}", True, CLR_BLACK)
        r = text_surface.get_rect()
        screen.blit(text_surface, (n["x"] + NODE_SIZE * 1.5, n["y"] - r[3] // 2))

    # draw hover node info
    line_pos = 5
    node = NodeAtMouse(nodes, mouse_move_pos)
    if node != None:
        text_surface = my_font.render(f"NodeID: {node['id']}", True, CLR_BLACK)
        ts = text_surface.get_rect()
        screen.blit(text_surface, (SCREEN_WIDTH - ts.w - 5, line_pos))
        line_pos += FONT_SIZE
    if shift:
        text_surface = my_font.render("SHIFT", True, CLR_BLACK)
        ts = text_surface.get_rect()
        screen.blit(text_surface, (SCREEN_WIDTH - ts.w - 5, line_pos))
        line_pos += FONT_SIZE

    # draw text info
    line_pos = 0
    if mousemode == MODE_NONE:
        text_surface = my_font.render(f"x:{mouse_move_pos[0]} y:{mouse_move_pos[1]}", True, CLR_BLACK)
        screen.blit(text_surface, (0, line_pos))
        line_pos += FONT_SIZE
    else:
        text_surface = my_font.render(f"x:{mouse_down_pos[0]} y:{mouse_down_pos[1]}", True, CLR_BLUE)
        screen.blit(text_surface, (0, line_pos))
        line_pos += FONT_SIZE
        text_surface = my_font.render(f"x:{mouse_move_pos[0]} y:{mouse_move_pos[1]}", True, CLR_BLACK)
        screen.blit(text_surface, (0, line_pos))
        line_pos += FONT_SIZE

    # draw selection if exists
    if mousemode == MODE_SELECTION:
        rct = (
            mouse_down_pos[0],
            mouse_down_pos[1],
            mouse_move_pos[0],
            mouse_move_pos[1],
        )
        rct = NormalizeRect(rct)
        pygame.draw.rect(screen, CLR_BLACK, rct, 1)

    pygame.display.flip()
    clock.tick(60)

save_nodes(nodes)
