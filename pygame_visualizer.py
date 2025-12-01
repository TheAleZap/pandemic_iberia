import pygame
import sys
import os


class PygameMapVisualizer:
    CITY_COORDINATES = {
        'Albufeira': (193, 1205),
        'Lisboa': (105, 942),
        'Porto': (203, 591),
        'Vigo': (191, 388),
        'Santiago': (247, 278),
        'Coruña': (237, 190),
        'Evora': (271, 998),
        'Coimbra': (300, 737),
        'Braga': (337, 507),
        'Ourense': (380, 371),
        'Caceres': (463, 844),
        'Salamanca': (568, 608),
        'Leon': (565, 353),
        'Gijon': (551, 190),
        'Madrid': (786, 699),
        'Valladolid': (664, 509),
        'Santander': (774, 207),
        'Soria': (905, 518),
        'Burgos': (781, 397),
        'Vitoria Gasteiz': (922, 371),
        'Bilbao': (884, 241),
        'Pamplona': (1044, 319),
        'San Sebastian': (1015, 200),
        'Huesca': (1187, 407),
        'Gibraltar': (570, 1377),
        'Cadiz': (478, 1345),
        'Huelva': (380, 1195),
        'Badajoz': (388, 935),
        'Malaga': (687, 1299),
        'Sevilla': (507, 1178),
        'Cordoba': (657, 1095),
        'Ciudad Real': (757, 918),
        'Toledo': (660, 796),
        'Almeria': (951, 1263),
        'Granada': (815, 1168),
        'Jaen': (798, 1061),
        'Cartagena': (1122, 1146),
        'Albacete': (1010, 922),
        'Cuenca': (964, 760),
        'Teruel': (1100, 706),
        'Zaragoza': (1129, 499),
        'Alicante': (1188, 1025),
        'Valencia': (1195, 859),
        'Tarragona': (1323, 606),
        'Barcelona': (1481, 535),
        'Girona': (1557, 438),
        'Andorra': (1401, 351),
        'Mallorca': (1588, 813),
    }

    RAILROAD_POSITIONS = {
        ('Albacete', 'Cartagena'): {'x': 1063, 'y': 1029, 'angle': -116.6},
        ('Albacete', 'Ciudad Real'): {'x': 876, 'y': 918, 'angle': 0.9},
        ('Albacete', 'Cuenca'): {'x': 988, 'y': 839, 'angle': -105.9},
        ('Albacete', 'Jaen'): {'x': 900, 'y': 990, 'angle': -33.3},
        ('Albacete', 'Valencia'): {'x': 1095, 'y': 891, 'angle': -18.8},
        ('Albufeira', 'Huelva'): {'x': 281, 'y': 1188, 'angle': -3.1},
        ('Albufeira', 'Lisboa'): {'x': 156, 'y': 1063, 'angle': -108.5},
        ('Alicante', 'Cartagena'): {'x': 1146, 'y': 1078, 'angle': -61.4},
        ('Alicante', 'Valencia'): {'x': 1190, 'y': 942, 'angle': -87.6},
        ('Almeria', 'Cartagena'): {'x': 1020, 'y': 1180, 'angle': -34.4},
        ('Almeria', 'Granada'): {'x': 881, 'y': 1214, 'angle': -145.1},
        ('Almeria', 'Malaga'): {'x': 820, 'y': 1273, 'angle': -7.8},
        ('Andorra', 'Girona'): {'x': 1474, 'y': 400, 'angle': -150.9},
        ('Andorra', 'Huesca'): {'x': 1290, 'y': 373, 'angle': -14.7},
        ('Badajoz', 'Caceres'): {'x': 428, 'y': 886, 'angle': 129.5},
        ('Badajoz', 'Ciudad Real'): {'x': 579, 'y': 920, 'angle': -2.6},
        ('Badajoz', 'Cordoba'): {'x': 524, 'y': 1008, 'angle': 30.7},
        ('Badajoz', 'Evora'): {'x': 327, 'y': 964, 'angle': -28.3},
        ('Barcelona', 'Girona'): {'x': 1509, 'y': 478, 'angle': -51.9},
        ('Barcelona', 'Tarragona'): {'x': 1387, 'y': 560, 'angle': -24.2},
        ('Barcelona', 'Zaragoza'): {'x': 1289, 'y': 511, 'angle': 5.8},
        ('Bilbao', 'San Sebastian'): {'x': 946, 'y': 219, 'angle': -17.4},
        ('Bilbao', 'Santander'): {'x': 828, 'y': 222, 'angle': 17.2},
        ('Bilbao', 'Vitoria Gasteiz'): {'x': 903, 'y': 305, 'angle': -106.3},
        ('Braga', 'Porto'): {'x': 273, 'y': 545, 'angle': -32.1},
        ('Braga', 'Salamanca'): {'x': 443, 'y': 550, 'angle': 23.6},
        ('Braga', 'Vigo'): {'x': 266, 'y': 448, 'angle': 39.2},
        ('Burgos', 'Soria'): {'x': 839, 'y': 458, 'angle': -135.7},
        ('Burgos', 'Valladolid'): {'x': 725, 'y': 451, 'angle': -43.7},
        ('Burgos', 'Vitoria Gasteiz'): {'x': 850, 'y': 382, 'angle': -10.4},
        ('Caceres', 'Coimbra'): {'x': 375, 'y': 788, 'angle': 33.3},
        ('Caceres', 'Salamanca'): {'x': 528, 'y': 723, 'angle': -66.0},
        ('Caceres', 'Toledo'): {'x': 562, 'y': 816, 'angle': -13.7},
        ('Cadiz', 'Gibraltar'): {'x': 528, 'y': 1357, 'angle': -160.8},
        ('Cadiz', 'Sevilla'): {'x': 494, 'y': 1261, 'angle': -80.1},
        ('Ciudad Real', 'Cordoba'): {'x': 704, 'y': 998, 'angle': -60.5},
        ('Ciudad Real', 'Madrid'): {'x': 806, 'y': 808, 'angle': 97.5},
        ('Ciudad Real', 'Toledo'): {'x': 706, 'y': 854, 'angle': -128.5},
        ('Coimbra', 'Lisboa'): {'x': 207, 'y': 832, 'angle': -46.4},
        ('Coimbra', 'Porto'): {'x': 253, 'y': 664, 'angle': 56.4},
        ('Cordoba', 'Jaen'): {'x': 726, 'y': 1071, 'angle': -13.6},
        ('Cordoba', 'Malaga'): {'x': 672, 'y': 1192, 'angle': -98.4},
        ('Cordoba', 'Sevilla'): {'x': 580, 'y': 1134, 'angle': -29.0},
        ('Coruña', 'Gijon'): {'x': 400, 'y': 186, 'angle': 0.0},
        ('Coruña', 'Santiago'): {'x': 242, 'y': 230, 'angle': -96.5},
        ('Cuenca', 'Madrid'): {'x': 881, 'y': 725, 'angle': 18.9},
        ('Cuenca', 'Teruel'): {'x': 1034, 'y': 730, 'angle': -21.7},
        ('Cuenca', 'Valencia'): {'x': 1075, 'y': 803, 'angle': 23.2},
        ('Evora', 'Huelva'): {'x': 326, 'y': 1093, 'angle': 61.0},
        ('Evora', 'Lisboa'): {'x': 188, 'y': 968, 'angle': 18.6},
        ('Gibraltar', 'Malaga'): {'x': 613, 'y': 1316, 'angle': -33.7},
        ('Gijon', 'Leon'): {'x': 558, 'y': 273, 'angle': -94.9},
        ('Gijon', 'Santander'): {'x': 655, 'y': 227, 'angle': 4.4},
        ('Granada', 'Jaen'): {'x': 806, 'y': 1112, 'angle': -99.0},
        ('Granada', 'Malaga'): {'x': 750, 'y': 1229, 'angle': -45.7},
        ('Huelva', 'Sevilla'): {'x': 439, 'y': 1185, 'angle': -7.6},
        ('Huesca', 'Pamplona'): {'x': 1112, 'y': 358, 'angle': 31.6},
        ('Huesca', 'Zaragoza'): {'x': 1158, 'y': 451, 'angle': 122.2},
        ('Leon', 'Ourense'): {'x': 467, 'y': 361, 'angle': -5.6},
        ('Leon', 'Salamanca'): {'x': 565, 'y': 475, 'angle': -90.7},
        ('Lisboa', 'Porto'): {'x': 180, 'y': 752, 'angle': -74.4},
        ('Madrid', 'Salamanca'): {'x': 674, 'y': 648, 'angle': 22.7},
        ('Madrid', 'Toledo'): {'x': 726, 'y': 745, 'angle': 142.4},
        ('Madrid', 'Valladolid'): {'x': 726, 'y': 599, 'angle': -122.7},
        ('Madrid', 'Zaragoza'): {'x': 944, 'y': 602, 'angle': -30.2},
        ('Malaga', 'Sevilla'): {'x': 596, 'y': 1246, 'angle': -146.1},
        ('Ourense', 'Santiago'): {'x': 312, 'y': 319, 'angle': 35.0},
        ('Ourense', 'Vigo'): {'x': 285, 'y': 387, 'angle': -5.1},
        ('Pamplona', 'San Sebastian'): {'x': 1030, 'y': 254, 'angle': -103.7},
        ('Pamplona', 'Vitoria Gasteiz'): {'x': 979, 'y': 344, 'angle': -23.1},
        ('Porto', 'Vigo'): {'x': 197, 'y': 490, 'angle': -93.4},
        ('Salamanca', 'Valladolid'): {'x': 614, 'y': 557, 'angle': -45.9},
        ('Santander', 'Valladolid'): {'x': 725, 'y': 341, 'angle': -70.0},
        ('Santiago', 'Vigo'): {'x': 220, 'y': 332, 'angle': -63.0},
        ('Soria', 'Zaragoza'): {'x': 1017, 'y': 506, 'angle': -4.8},
        ('Tarragona', 'Teruel'): {'x': 1202, 'y': 657, 'angle': -24.2},
        ('Tarragona', 'Valencia'): {'x': 1243, 'y': 733, 'angle': -63.2},
        ('Teruel', 'Zaragoza'): {'x': 1114, 'y': 599, 'angle': -82.0},
        ('Vitoria Gasteiz', 'Zaragoza'): {'x': 1019, 'y': 429, 'angle': 31.7},
    }
    
    IMAGE_FOLDER = "map_images"
    MAP_IMAGE_FILE = "iberia_map.png"
    RAILROAD_IMAGE_FILE = "railroad.png"
    HOSPITAL_IMAGES = {
        'blue': "hospital_blue.png",
        'red': "hospital_red.png",
        'black': "hospital_black.png",
        'yellow': "hospital_yellow.png",
    }
    CUBE_IMAGES = {
        'blue': {
            1: "cube_blue_1.png",
            2: "cube_blue_2.png",
            3: "cube_blue_3.png",
        },
        'red': {
            1: "cube_red_1.png",
            2: "cube_red_2.png",
            3: "cube_red_3.png",
        },
        'black': {
            1: "cube_black_1.png",
            2: "cube_black_2.png",
            3: "cube_black_3.png",
        },
        'yellow': {
            1: "cube_yellow_1.png",
            2: "cube_yellow_2.png",
            3: "cube_yellow_3.png",
        },
    }
    PLAYER_IMAGES = {
        0: "pawn_player1.png",
        1: "pawn_player2.png",
        2: "pawn_player3.png",
    }
    
    ELEMENT_SPACING = 13
    PAWN_OFFSET_Y = -12
    HOSPITAL_OFFSET_Y = -3
    CUBE_LEFT_EXTRA_OFFSET = -4
    SINGLE_CUBE_CENTER_OFFSET_X = 3
    SINGLE_CUBE_CENTER_OFFSET_Y = -3
    TWO_CUBE_CENTER_OFFSET_X = 2
    TWO_CUBE_CENTER_OFFSET_Y = -2

    RAILROAD_SCALE = 0.032
    PAWN_SCALE = 0.035
    CUBE_1_SCALE = 0.017
    CUBE_2_SCALE = 0.021
    CUBE_3_SCALE = 0.025
    HOSPITAL_SCALE = 0.026
    
    TEXT_COLOR = (0, 0, 0)
    FONT_SIZE = 12
    
    def __init__(self, game_state):  # Time Complexity: O(V) where V = number of cities
        """
        Sets up the pygame window, loads all the assets, and prepares
        cached surfaces so drawing stays reasonably fast while the
        text game is running in parallel.
        """
        self.game_state = game_state
        
        pygame.init()
        map_path = os.path.join(self.IMAGE_FOLDER, self.MAP_IMAGE_FILE)
        
        try:
            original_map_image = pygame.image.load(map_path)
            original_width, original_height = original_map_image.get_size()
        except FileNotFoundError:
            print(f"ERROR: Map image '{map_path}' not found!")
            sys.exit(1)
        
        screen_info = pygame.display.Info()
        max_screen_width = screen_info.current_w - 300
        max_screen_height = screen_info.current_h - 300
        
        scale_x = max_screen_width / original_width
        scale_y = max_screen_height / original_height
        self.map_scale = min(scale_x, scale_y, 1.0)
        
        self.WINDOW_WIDTH = int(original_width * self.map_scale)
        self.WINDOW_HEIGHT = int(original_height * self.map_scale)
        
        self.map_image = pygame.transform.scale(original_map_image, (self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Pandemic Iberia")
        
        self.CITY_COORDINATES = {}
        for city, (orig_x, orig_y) in PygameMapVisualizer.CITY_COORDINATES.items():
            scaled_x = int(orig_x * self.map_scale)
            scaled_y = int(orig_y * self.map_scale)
            self.CITY_COORDINATES[city] = (scaled_x, scaled_y)
        
        self.hospital_images = {}
        for color, filename in self.HOSPITAL_IMAGES.items():
            image_path = os.path.join(self.IMAGE_FOLDER, filename)
            try:
                img = pygame.image.load(image_path)
                if self.HOSPITAL_SCALE != 1.0:
                    original_size = img.get_size()
                    new_size = (int(original_size[0] * self.HOSPITAL_SCALE), int(original_size[1] * self.HOSPITAL_SCALE))
                    img = pygame.transform.scale(img, new_size)
                self.hospital_images[color] = img
            except FileNotFoundError:
                print(f"ERROR: Hospital image '{image_path}' not found!")
                print(f"Please save your hospital image as '{filename}' in the '{self.IMAGE_FOLDER}' folder")
                sys.exit(1)
        
        self.cube_images = {}
        scale_map = {1: self.CUBE_1_SCALE, 2: self.CUBE_2_SCALE, 3: self.CUBE_3_SCALE}
        for color, cube_dict in self.CUBE_IMAGES.items():
            self.cube_images[color] = {}
            for count, filename in cube_dict.items():
                image_path = os.path.join(self.IMAGE_FOLDER, filename)
                try:
                    img = pygame.image.load(image_path)
                    scale = scale_map.get(count, 1.0)
                    if scale != 1.0:
                        original_size = img.get_size()
                        new_size = (int(original_size[0] * scale), int(original_size[1] * scale))
                        img = pygame.transform.scale(img, new_size)
                    self.cube_images[color][count] = img
                except FileNotFoundError:
                    print(f"ERROR: Cube image '{image_path}' not found!")
                    print(f"Please save your cube image as '{filename}' in the '{self.IMAGE_FOLDER}' folder")
                    sys.exit(1)
        
        self.player_images = {}
        for player_id, filename in self.PLAYER_IMAGES.items():
            image_path = os.path.join(self.IMAGE_FOLDER, filename)
            try:
                img = pygame.image.load(image_path)
                if self.PAWN_SCALE != 1.0:
                    original_size = img.get_size()
                    new_size = (int(original_size[0] * self.PAWN_SCALE), int(original_size[1] * self.PAWN_SCALE))
                    img = pygame.transform.scale(img, new_size)
                self.player_images[player_id] = img
            except FileNotFoundError:
                print(f"ERROR: Player image '{image_path}' not found!")
                print(f"Please save your player image as '{filename}' in the '{self.IMAGE_FOLDER}' folder")
                sys.exit(1)
        
        railroad_path = os.path.join(self.IMAGE_FOLDER, self.RAILROAD_IMAGE_FILE)
        try:
            railroad_img = pygame.image.load(railroad_path)
            if self.RAILROAD_SCALE != 1.0:
                original_size = railroad_img.get_size()
                new_width = max(1, int(original_size[0] * self.RAILROAD_SCALE))
                new_height = max(1, int(original_size[1] * self.RAILROAD_SCALE))
                new_size = (new_width, new_height)
                railroad_img = pygame.transform.scale(railroad_img, new_size)
            self.railroad_image = railroad_img
        except FileNotFoundError:
            print(f"ERROR: Railroad image '{railroad_path}' not found!")
            print(f"Please save your railroad image as '{self.RAILROAD_IMAGE_FILE}' in the '{self.IMAGE_FOLDER}' folder")
            sys.exit(1)
        
        self.font = pygame.font.Font(None, self.FONT_SIZE)
        self.font_bold = pygame.font.Font(None, self.FONT_SIZE + 4)
        self.font_ui = pygame.font.Font(None, 24)
        self.font_status = pygame.font.Font(None, 14)
        self.font_status_bold = pygame.font.Font(None, 15)
        
        self.running = True
        
        self.dirty = True
        self.railroad_cache = {}
        self.frame_count = 0
        
        self.background_surface = None
        self.background_dirty = True
        self.last_railroad_count = 0
        
        self.status_board_surface = None
        self.status_board_rect = None
        self.status_board_dirty = True
        self.last_game_state_hash = None

        self.last_city_states = None
    
    def draw_map_background(self): # Time Complexity: O(1)
        self.screen.blit(self.map_image, (0, 0))
    
    def build_background_surface(self): # Time Complexity: O(W × H + E) where W = window width, H = window height, E = number of edges
        self.background_surface = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        
        self.background_surface.blit(self.map_image, (0, 0))
        
        board = self.game_state.board
        for city, neighbors in board.CITY_CONNECTIONS.items():
            for neighbor in neighbors:
                if not board.has_railroad(city, neighbor):
                    continue
                
                pair = tuple(sorted([city, neighbor]))
                if pair in self.RAILROAD_POSITIONS:
                    data = self.RAILROAD_POSITIONS[pair]
                    x = int(data['x'] * self.map_scale)
                    y = int(data['y'] * self.map_scale)
                    angle = data['angle']
                    
                    cache_key = angle
                    if cache_key not in self.railroad_cache:
                        rotated_railroad = pygame.transform.rotate(self.railroad_image, -angle)
                        self.railroad_cache[cache_key] = rotated_railroad
                    else:
                        rotated_railroad = self.railroad_cache[cache_key]
                    
                    rect = rotated_railroad.get_rect(center=(x, y))
                    self.background_surface.blit(rotated_railroad, rect)
        
        self.background_dirty = False
        if hasattr(self.game_state, 'board'):
            self.last_railroad_count = len(self.game_state.board.railroads)
    
    def check_background_needs_rebuild(self): # Time Complexity: O(1) average, O(R) worst case where R = number of railroads
        if self.background_surface is None or self.background_dirty:
            return True
        
        if hasattr(self.game_state, 'board'):
            current_railroad_count = len(self.game_state.board.railroads)
            if current_railroad_count != self.last_railroad_count:
                return True
        
        return False
    
    def build_status_board_surface(self): # Time Complexity: O(V) where V = number of cities
        padding = 7
        line_height = 15
        
        lines = []
        lines.append(("Game Status", ""))
        lines.append((""))
        
        lines.append(("Researched Diseases (Y/N):", ""))
        color_names = {'red': 'Red', 'blue': 'Blue', 'black': 'Black', 'yellow': 'Yellow'}
        for color in ['red', 'blue', 'black', 'yellow']:
            status = "Y" if color in self.game_state.cured_diseases else "N"
            lines.append((f"- {color_names[color]}:", status))
        lines.append((""))
        
        lines.append(("Epidemics:", f"{self.game_state.epidemic_count}/{self.game_state.max_epidemics}"))
        lines.append(("Outbreaks:", f"{self.game_state.outbreak_count}/{self.game_state.max_outbreaks}"))
        lines.append((""))
        
        deck_size = len(self.game_state.player_deck)
        total_cities = len(self.game_state.board.cities)
        total_epidemics = self.game_state.max_epidemics
        total_deck_size = total_cities + total_epidemics
        lines.append(("Player Deck cards remaining:", f"{deck_size}/{total_deck_size}"))
        
        lines.append(("Cubes remaining:", ""))
        max_cubes_per_color = 24
        for color in ['red', 'blue', 'black', 'yellow']:
            if not self.game_state.game_started:
                cubes_remaining = max_cubes_per_color
            else:
                cubes_on_board = sum(
                    self.game_state.board.disease_cubes[city].get(color, 0)
                    for city in self.game_state.board.cities
                )
                cubes_remaining = max(0, max_cubes_per_color - cubes_on_board)
            lines.append((f"- {color_names[color]}:", f"{cubes_remaining}/{max_cubes_per_color}"))
        
        railroads_remaining = self.game_state.board.get_railroads_remaining()
        max_railroads = self.game_state.board.max_railroads
        lines.append(("Railroads remaining:", f"{railroads_remaining}/{max_railroads}"))
        
        max_label_width = 0
        max_value_width = 0
        for line in lines:
            if isinstance(line, tuple):
                label, value = line
                label_width = self.font_status.size(label)[0]
                value_width = self.font_status.size(value)[0]
                max_label_width = max(max_label_width, label_width)
                max_value_width = max(max_value_width, value_width)
        
        box_width = max_label_width + max_value_width + 18
        box_height = len(lines) * line_height + padding * 2 + 4
        
        box_x = self.WINDOW_WIDTH - box_width 
        box_y = self.WINDOW_HEIGHT - box_height
        
        self.status_board_surface = pygame.Surface((box_width, box_height))
        self.status_board_surface.set_alpha(230)
        self.status_board_surface.fill((255, 255, 255))
        
        pygame.draw.rect(self.status_board_surface, (0, 0, 0), (0, 0, box_width, box_height), 2)
        
        y_offset = padding + 3
        for line in lines:
            if isinstance(line, tuple):
                label, value = line
                if label == "Game Status" and value == "":
                    title_text = self.font_status_bold.render(label, True, (0, 0, 0))
                    title_x = (box_width - title_text.get_width()) // 2
                    self.status_board_surface.blit(title_text, (title_x, y_offset))
                else:
                    label_text = self.font_status.render(label, True, (0, 0, 0))
                    value_text = self.font_status.render(value, True, (0, 0, 0))
                    self.status_board_surface.blit(label_text, (padding, y_offset))
                    self.status_board_surface.blit(value_text, (box_width - padding - value_text.get_width(), y_offset))
            y_offset += line_height
        
        self.status_board_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        self.status_board_dirty = False
    
    def check_status_board_needs_rebuild(self): # Time Complexity: O(V) where V = number of cities
        if self.status_board_surface is None or self.status_board_dirty:
            return True
        
        try:
            state_hash = (
                tuple(sorted(self.game_state.cured_diseases)),
                self.game_state.epidemic_count,
                self.game_state.outbreak_count,
                len(self.game_state.player_deck),
                self.game_state.board.get_railroads_remaining(),
                sum(
                    self.game_state.board.disease_cubes[city].get(color, 0)
                    for city in self.game_state.board.cities
                    for color in ['red', 'blue', 'black', 'yellow']
                )
            )
            
            if state_hash != self.last_game_state_hash:
                self.last_game_state_hash = state_hash
                return True
        except:
            return True
        
        return False
    
    def check_city_states_changed(self): # Time Complexity: O(V) where V = number of cities
        if self.last_city_states is None:
            self.last_city_states = {}
            for city in self.game_state.board.cities:
                self.last_city_states[city] = (
                    tuple(sorted(self.game_state.board.disease_cubes[city].items())),
                    self.game_state.board.has_hospital(city),
                    tuple(i for i, p in enumerate(self.game_state.players) if p.location == city)
                )
            return True
        
        for city in self.game_state.board.cities:
            current_state = (
                tuple(sorted(self.game_state.board.disease_cubes[city].items())),
                self.game_state.board.has_hospital(city),
                tuple(i for i, p in enumerate(self.game_state.players) if p.location == city)
            )
            
            if city not in self.last_city_states or self.last_city_states[city] != current_state:
                self.last_city_states[city] = current_state
                return True
        
        if set(self.last_city_states.keys()) != set(self.game_state.board.cities):
            self.last_city_states = {}
            return True
        
        return False
    
    def draw_connections(self): # Time Complexity: O(E) where E = number of edges
        board = self.game_state.board
        
        for city, neighbors in board.CITY_CONNECTIONS.items():
            for neighbor in neighbors:
                if not board.has_railroad(city, neighbor):
                    continue
                
                pair = tuple(sorted([city, neighbor]))
                if pair in self.RAILROAD_POSITIONS:
                    data = self.RAILROAD_POSITIONS[pair]
                    
                    x = int(data['x'] * self.map_scale)
                    y = int(data['y'] * self.map_scale)
                    angle = data['angle']
                    
                    cache_key = angle
                    if cache_key not in self.railroad_cache:
                        rotated_railroad = pygame.transform.rotate(self.railroad_image, -angle)
                        self.railroad_cache[cache_key] = rotated_railroad
                    else:
                        rotated_railroad = self.railroad_cache[cache_key]
                    
                    rect = rotated_railroad.get_rect(center=(x, y))
                    
                    self.screen.blit(rotated_railroad, rect)
    
    def collect_city_elements(self, city): # Time Complexity: O(1)
        elements = []
        board = self.game_state.board
        city_color = board.get_city_color(city)
        cubes = board.disease_cubes[city]
        
        if board.has_hospital(city):
            color = board.get_hospital_color(city)
            if color and color in self.hospital_images:
                elements.append({
                    'type': 'hospital',
                    'image': self.hospital_images[color],
                    'priority': 0,
                    'color': color
                })
        
        matching_cube_count = cubes.get(city_color, 0)
        if matching_cube_count > 0:
            cube_count = min(matching_cube_count, 3)
            if city_color in self.cube_images and cube_count in self.cube_images[city_color]:
                elements.append({
                    'type': 'cube',
                    'image': self.cube_images[city_color][cube_count],
                    'priority': 1,
                    'color': city_color,
                    'count': matching_cube_count
                })
        
        for color_name, count in cubes.items():
            if color_name != city_color and count > 0:
                cube_count = min(count, 3)
                if color_name in self.cube_images and cube_count in self.cube_images[color_name]:
                    elements.append({
                        'type': 'cube',
                        'image': self.cube_images[color_name][cube_count],
                        'priority': 2,
                        'color': color_name,
                        'count': count
                    })

        for i, player in enumerate(self.game_state.players):
            if player.location and player.location == city:
                if i in self.player_images:
                    elements.append({
                        'type': 'pawn',
                        'image': self.player_images[i],
                        'priority': 3,
                        'player_id': i
                    })
        
        elements.sort(key=lambda x: x['priority'])
        return elements
    
    def get_element_positions(self, num_elements, spacing): # Time Complexity: O(1)
        positions = []
        
        if num_elements == 0:
            return positions
        
        positions.append((0, 0))
        if num_elements == 1:
            return positions
        
        positions.append((-spacing, spacing))
        if num_elements == 2:
            return positions
        
        positions.append((spacing, spacing))
        if num_elements == 3:
            return positions

        positions.append((0, -spacing))
        if num_elements >= 5:
            positions.append((-spacing, -spacing))
        if num_elements >= 6:
            positions.append((spacing, -spacing))
        if num_elements >= 7:
            positions.append((-spacing * 2, 0))
        if num_elements >= 8:
            positions.append((spacing * 2, 0))
        
        return positions[:num_elements]
    
    def draw_element(self, element, x, y, position_index=0): # Time Complexity: O(1)
        if element['type'] == 'hospital':
            y = y + self.HOSPITAL_OFFSET_Y
        
        if element['type'] == 'pawn':
            y = y + self.PAWN_OFFSET_Y
        
        if element['type'] == 'cube' and position_index == 1:
            if element.get('count', 0) == 3:
                x = x + self.CUBE_LEFT_EXTRA_OFFSET
        
        if element['type'] == 'cube' and element.get('count', 0) == 1:
            if position_index == 1:
                x = x + self.SINGLE_CUBE_CENTER_OFFSET_X
                y = y + self.SINGLE_CUBE_CENTER_OFFSET_Y
            elif position_index == 2:
                x = x - self.SINGLE_CUBE_CENTER_OFFSET_X
                y = y + self.SINGLE_CUBE_CENTER_OFFSET_Y
        
        if element['type'] == 'cube' and element.get('count', 0) == 2:
            if position_index == 1:
                x = x + self.TWO_CUBE_CENTER_OFFSET_X
                y = y + self.TWO_CUBE_CENTER_OFFSET_Y
        
        image = element['image']
        if image is None:
            element_type = element.get('type', 'unknown')
            print(f"ERROR: Image for {element_type} element is missing!")
            if element_type == 'hospital':
                print(f"ERROR: Hospital image is missing!")
            elif element_type == 'cube':
                print(f"ERROR: Cube image for {element.get('color', 'unknown')} color is missing!")
            elif element_type == 'pawn':
                print(f"ERROR: Player image for player {element.get('player_id', 'unknown')} is missing!")
            sys.exit(1)
        
        img_width, img_height = image.get_size()
        draw_x = x - (img_width // 2)
        draw_y = y - (img_height // 2)
        self.screen.blit(image, (draw_x, draw_y))
    
    def draw_all_cities(self): # Time Complexity: O(V) where V = number of cities
        for city, (city_x, city_y) in self.CITY_COORDINATES.items():
            elements = self.collect_city_elements(city)
            
            if elements:
                positions = self.get_element_positions(len(elements), self.ELEMENT_SPACING)
                top_positions = [3, 4, 5]
                top_pawns = []
                other_elements = []
                
                for position_index, (element, pos) in enumerate(zip(elements, positions)):
                    if element['type'] == 'pawn' and position_index in top_positions:
                        top_pawns.append((position_index, element, pos))
                    else:
                        other_elements.append((position_index, element, pos))
                
                for position_index, element, (offset_x, offset_y) in top_pawns:
                    element_x = city_x + offset_x
                    element_y = city_y + offset_y
                    self.draw_element(element, element_x, element_y, position_index)
                
                for position_index, element, (offset_x, offset_y) in other_elements:
                    element_x = city_x + offset_x
                    element_y = city_y + offset_y
                    self.draw_element(element, element_x, element_y, position_index)
    
    def get_city_at_position(self, x, y): # Time Complexity: O(V) where V = number of cities
        for city, (city_x, city_y) in self.CITY_COORDINATES.items():
            distance = ((x - city_x) ** 2 + (y - city_y) ** 2) ** 0.5
            if distance <= 15:
                return city
        return None
    
    def draw_status_board(self): # Time Complexity: O(1)
        if self.status_board_surface is not None and self.status_board_rect is not None:
            self.screen.blit(self.status_board_surface, self.status_board_rect)
    
    def update(self): # Time Complexity: O(V) average, O(W × H + V) worst case where W = window width, H = window height, V = number of cities
        self.frame_count += 1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
        
        needs_full_redraw = self.dirty
        
        if not needs_full_redraw and self.frame_count % 5 == 0:
            if self.check_city_states_changed():
                needs_full_redraw = True
        
        if self.check_background_needs_rebuild():
            self.build_background_surface()
            needs_full_redraw = True
        
        if self.check_status_board_needs_rebuild():
            self.build_status_board_surface()
            needs_full_redraw = True
        
        if needs_full_redraw:
            if self.background_surface is not None:
                self.screen.blit(self.background_surface, (0, 0))
            else:
                self.draw_map_background()
                self.draw_connections()
            
            self.draw_all_cities()
            
            self.draw_status_board()
            
            pygame.display.flip()
            self.dirty = False
    
    def run_display(self): # Time Complexity: O(1) per iteration
        clock = pygame.time.Clock()
        self.running = True
        
        try:
            self.dirty = True
            self.background_dirty = True
            self.status_board_dirty = True
            self.update()
        except Exception as e:
            print(f"Warning: Error in pygame display: {e}")
            self.running = False
            return
        
        while self.running:
            try:
                self.update()
                clock.tick(20)
            except Exception as e:
                print(f"Warning: Error in pygame loop: {e}")
                break
    
    def mark_dirty(self): # Time Complexity: O(1)
        self.dirty = True
        self.status_board_dirty = True
        self.last_city_states = None
        self.last_game_state_hash = None
    
    def force_update(self): # Time Complexity: O(W × H + V) where W = window width, H = window height, V = number of cities
        self.mark_dirty()
        self.update()
        pygame.event.pump()
    
    def close(self): # Time Complexity: O(1)
        self.running = False
        pygame.quit()