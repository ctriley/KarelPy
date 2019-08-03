from beeper import Beeper
from dot import Dot
from karel import Karel
from ikarel import KarelInterface
from wall import Wall
import config
import pygame


class World:
    def __init__(self, template):
        self.template = template
        self.dimension = (0, 0)
        # Values from parsing template
        self.beeper = {}
        self.karel = {}
        self.beeper_bag = None
        self.wall = {}
        self.speed = 1.00
        # Sprites
        self.real_karel = None
        self.dot_sprites = pygame.sprite.Group()
        self.beeper_sprites = pygame.sprite.Group()
        self.wall_sprites = pygame.sprite.Group()
        self.karel_sprites = pygame.sprite.Group()
        # World attributes
        self.width = self.dimension[0]
        self.height = self.dimension[1]
        self.screen = None


    def parse_template(self):
        with open(self.template, "r") as template:
            raw_commands = template.readlines()
        parsed_commands = []
        for command in raw_commands:
            bad_characters = [":", "\n", "(", ")", ","]
            command = "".join(char for char in command if char not in bad_characters)
            parsed_commands.append(command.split(" "))
        for command in parsed_commands:
            if command[0] == "Dimension":
                x = int(command[1]) * config.DIMENSION_UNIT
                y = int(command[2]) * config.DIMENSION_UNIT
                self.dimension = (x, y)
            elif command[0] == "Beeper":
                x = int(command[1]) * config.DIMENSION_UNIT
                y = int(command[2]) * config.DIMENSION_UNIT
                quantity = int(command[3])
                self.beeper[(x, y)] = self.beeper.get((x, y), 0) + quantity
            elif command[0] == "BeeperBag":
                quantity = command[1]
                if quantity == "INFINITE":
                    self.beeper_bag = float("inf")
                else:
                    self.beeper_bag = int(quantity)
            elif command[0] == "Wall":
                x = int(command[1]) * config.DIMENSION_UNIT
                y = int(command[2]) * config.DIMENSION_UNIT
                direction = config.DIRECTION_MAP[command[3]]
                self.wall[(x, y)] = self.wall.get((x, y), []) + [direction]
            elif command[0] == "Karel":
                x = int(command[1]) * config.DIMENSION_UNIT
                y = int(command[2]) * config.DIMENSION_UNIT
                direction = config.DIRECTION_MAP[command[3]]
                self.karel[(x, y)] = direction
            elif command[0] == "Speed":
                self.speed = float(command[1])

    def create_dot_sprites(self):
        x_axis = self.dimension[0] // config.DIMENSION_UNIT + 1
        y_axis = self.dimension[1] // config.DIMENSION_UNIT + 1
        for horizontal in range(x_axis):
            for vertical in range(y_axis):
                x = horizontal * config.DIMENSION_UNIT - config.DIMENSION_UNIT / 2
                y = self.dimension[1] - (vertical * config.DIMENSION_UNIT - config.DIMENSION_UNIT / 2)
                center = x, y
                self.dot_sprites.add(Dot(center))

    def create_beeper_sprites(self):
        for location, quantity in self.beeper.items():
            for beeper in range(quantity):
                x = location[0] - config.DIMENSION_UNIT/2
                y = self.dimension[1] - (location[1] - config.DIMENSION_UNIT/2)
                center = x, y
                self.beeper_sprites.add(Beeper(center))

    def create_wall_sprites(self):
        for location, directions in self.wall.items():
            for direction in directions:
                if direction == config.DIRECTION_MAP["North"]:
                    x = location[0] - config.DIMENSION_UNIT / 2
                    y = self.dimension[1] - location[1]
                    orientation = "h"
                elif direction == config.DIRECTION_MAP["South"]:
                    x = location[0] - config.DIMENSION_UNIT / 2
                    y = self.dimension[1] - (location[1] - config.DIMENSION_UNIT)
                    orientation = "h"
                elif direction == config.DIRECTION_MAP["East"]:
                    x = location[0]
                    y = self.dimension[1] - (location[1] - config.DIMENSION_UNIT / 2)
                    orientation = "v"
                elif direction == config.DIRECTION_MAP["West"]:
                    x = location[0] - config.DIMENSION_UNIT
                    y = self.dimension[1] - (location[1] - config.DIMENSION_UNIT / 2)
                    orientation = "v"
                center = x, y
                self.wall_sprites.add(Wall(center, orientation))

    def create_karel_sprites(self):
        for location, direction in self.karel.items():
            x = location[0] - config.DIMENSION_UNIT/2
            y = self.dimension[1] - (location[1] - config.DIMENSION_UNIT/2)
            center = x, y
            self.karel_sprites.add(Karel(center, direction))

    def build(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Karel Learns Python")
        self.screen = pygame.display.set_mode((self.width, self.height), flags=pygame.RESIZABLE)
        self.create_dot_sprites()
        self.create_wall_sprites()
        self.create_karel_sprites()
        self.create_beeper_sprites()
        self.real_karel = KarelInterface(self.karel_sprites, self.beeper_sprites, self.wall_sprites,
                                         self.dot_sprites, self.screen, self.speed)

    def display(self):
        self.dot_sprites.update()
        self.beeper_sprites.update()
        self.wall_sprites.update()
        self.karel_sprites.update()
        self.screen.fill(config.WHITE)
        self.dot_sprites.draw(self.screen)
        self.beeper_sprites.draw(self.screen)
        self.wall_sprites.draw(self.screen)
        self.karel_sprites.draw(self.screen)
        pygame.display.flip()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

    # def close(self):
    #     pygame.display.set_mode()
    #     running = True
    #     while running:
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 running = False


world = World("world/unitednations.w")
world.parse_template()
world.build()
real_karel = world.real_karel
display = world.display









