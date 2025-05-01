import random
from setting import *

class Terrain:
    def __init__(self, mlx, mly):
        """
        Initializes the Terrain object with map dimensions.
        """
        self.mlx = mlx
        self.mly = mly
        self.map = [[0 for _ in range(mlx)] for _ in range(mly)]
        self.biomes = [0 for _ in range(mlx)] #added biomes
        self.generate_terrain()

    def generate_terrain(self):
        """
        Generates the terrain with biomes, beaches, and varied trees.
        """
        # 1. Create initial heightmap
        height_map = [self.mly // 2 + random.randint(-2, 2) for _ in range(self.mlx)]

        # 2. Smooth heightmap
        for _ in range(3):
            for i in range(1, self.mlx - 1):
                height_map[i] = (height_map[i - 1] + height_map[i] + height_map[i + 1]) // 3

        # 3. Generate biomes - simplified biome generation
        biome_width = 90 #each biome will be 90 blocks
        for x in range(self.mlx):
            self.biomes[x] = int(x // biome_width) % 5

        # 4. Introduce variation and averaging huge bumbs
        for i in range(1, self.mlx - 1):
            if self.biomes[i] == 4:
               height_map[i] = max(min(height_map[i - 1] + random.randint(-2, 2), self.mly - 2), 1)
            dif_from_last = height_map[i - 1] - height_map[i]
            if abs(dif_from_last) > 2:
                height_map[i] += dif_from_last - (abs(dif_from_last) // dif_from_last)

        # 5. Generate main terrain based on heightmap and biomes
        for x in range(self.mlx):
            height = height_map[x]
            biome = self.biomes[x] #get biome type.

            # Create the surface layer, adjusted for biomes
            if biome == 1: # Desert
                self.map[height][x] = 11 #sand
            elif biome == 2: # Plains
                self.map[height][x] = 3  # Grass
            elif biome == 3: # Mountains
                if height >= self.mly - 8:
                    self.map[height][x] = 3 #stone
                else:
                    self.map[height][x] = 3
            else:
                self.map[height][x] = 3

            # Create the dirt layer
            for y in range(height + 1, min(height + 4, self.mly)):
                if self.biomes[x] == 1:
                    self.map[y][x] = 11
                else:
                    self.map[y][x] = 2  # Dirt

            # Create the deeper layers.  Ore generation can be adjusted per biome if desired.
            for y in range(min(height + 4, self.mly), self.mly - 1):
                ore_chance = random.random()
                if ore_chance < 0.005:
                    self.map[y][x] = 16  # Diamond
                elif ore_chance < 0.01:
                    self.map[y][x] = 15  # Gold
                elif ore_chance < 0.03:
                    self.map[y][x] = 13  # Iron
                elif ore_chance < 0.06:
                    self.map[y][x] = 14  # Coal
                else:
                    self.map[y][x] = 7  # Stone
            self.map[self.mly - 1][x] = 1 #Bedrock

        # 6. Generate beaches
        self.generate_beaches(height_map)
        # 7. Generate trees
        self.generate_trees(height_map)

    def generate_beaches(self, height_map):
        """
        Generates beaches, now biome-aware (deserts don't have beaches).
        """
        beach_level = self.mly - 3
        for x in range(self.mlx):
            biome = self.biomes[x]
            if biome != 1: #no beaches in desert
                if height_map[x] >= self.mly - 4:
                    for y in range(max(1, beach_level), self.mly - 1):
                        self.map[y][x] = 12  # Sand
                    if x > 0 and height_map[x - 1] < self.mly - 1:
                        self.map[beach_level][x - 1] = 12
                    if x < self.mlx - 1 and height_map[x + 1] < self.mly - 1:
                        self.map[beach_level][x + 1] = 12

    def generate_trees(self, height_map):
        """
        Generates trees with variation, now biome-aware.  Reduced tree density.
        """
        for x in range(2, self.mlx - 2):
            ground_y = height_map[x]
            biome = self.biomes[x]

            # Conditions for tree placement, now biome-specific
            if (0 <= ground_y < self.mly and
                self.map[ground_y][x] == 3 and #only on grass
                all(0 <= ground_y - i - 1 < self.mly and self.map[ground_y - i - 1][x] == 0 for i in range(3)) and
                random.random() < 0.05 and biome != 1):  # Reduced chance, no trees in desert

                tree_height = random.randint(3, 7)
                leaf_radius = random.randint(2, 3)

                # Generate the tree trunk
                for y in range(tree_height):
                    if 0 <= ground_y - y - 1 < self.mly:
                        self.map[ground_y - y - 1][x] = 8  # Trunk

                # Generate the tree leaves
                leaf_height = ground_y - tree_height - 3
                for dx in range(-leaf_radius, leaf_radius + 1):
                    for dy in range(-leaf_radius, leaf_radius + 1):
                        if (abs(dx) + abs(dy) <= leaf_radius + 1 and
                            0 <= leaf_height + dy < self.mly and
                            0 <= x + dx < self.mlx):
                            if self.map[leaf_height + dy][x + dx] != 8:
                                self.map[leaf_height + dy][x + dx] = 9 if random.random() < 0.98 else 10

class Level:
    def __init__(self):
        """
        Initializes the Level object.
        """
        self.px, self.py = 0, 0

    def init(self, mlx, mly) -> list[list[int]]:
        """
        Initializes the level with generated terrain and spawn position.
        """
        t = Terrain(mlx, mly)
        self.px, self.py = self.find_spawn_position(t.map)
        return t.map

    def find_spawn_position(self, level: list[list[int]]) -> tuple[int, int] | None:
        """
        Finds a suitable spawn position (grass with air above).
        """
        mlx = len(level[0])
        mly = len(level)
        possible_areas = []

        for x in range(mlx):
            for y in range(1, mly):
                if level[y][x] == 3 and level[y - 1][x] == 0:
                    possible_areas.append((x * TILE_SIZE, (y - 1) * TILE_SIZE))

        if possible_areas:
            return random.choice(possible_areas)
        else:
            return None
