from data_structures import Graph
from algorithms import bfs_traverse


def bfs_shortest_path(graph, start, end):   # Time Complexity: O(V + E), Space Complexity: O(V)
    """
    Wrapper function for BFS traversal to find shortest path.
    graph: adjacency list dictionary (from Graph.get_adjacency_list() or CITY_CONNECTIONS)
    Returns: list representing shortest path from start to end, or None if no path exists
    """
    return bfs_traverse(graph, start, end)


class Board:
    CITY_CONNECTIONS = {
        'Albufeira': ['Lisboa', 'Huelva'],
        'Lisboa': ['Porto', 'Coimbra', 'Evora', 'Albufeira'],
        'Porto': ['Lisboa', 'Coimbra', 'Vigo', 'Braga'],
        'Vigo': ['Porto', 'Santiago', 'Ourense', 'Braga'],
        'Santiago': ['Vigo', 'Ourense', 'Coruña'],
        'Coruña': ['Santiago', 'Gijon'],
        'Evora': ['Lisboa', 'Badajoz', 'Huelva'],
        'Coimbra': ['Lisboa', 'Porto', 'Caceres'],
        'Braga': ['Vigo', 'Porto', 'Salamanca'],
        'Ourense': ['Santiago', 'Vigo', 'Leon'],
        'Caceres': ['Coimbra', 'Salamanca', 'Toledo', 'Badajoz'],
        'Salamanca': ['Braga', 'Leon', 'Valladolid', 'Madrid', 'Caceres'],
        'Leon': ['Gijon', 'Salamanca', 'Ourense'],
        'Gijon': ['Leon', 'Coruña', 'Santander'],
        'Madrid': ['Toledo', 'Salamanca', 'Valladolid', 'Zaragoza', 'Cuenca', 'Ciudad Real'],
        'Valladolid': ['Salamanca', 'Santander', 'Burgos', 'Madrid'],
        'Santander': ['Valladolid', 'Gijon', 'Bilbao'],
        'Soria': ['Burgos', 'Zaragoza'],
        'Burgos': ['Valladolid', 'Vitoria Gasteiz', 'Soria'],
        'Vitoria Gasteiz': ['Burgos', 'Bilbao', 'Pamplona', 'Zaragoza'],
        'Bilbao': ['Santander', 'Vitoria Gasteiz', 'San Sebastian'],
        'Pamplona': ['Vitoria Gasteiz', 'San Sebastian', 'Huesca'],
        'San Sebastian': ['Bilbao', 'Pamplona'],
        'Huesca': ['Pamplona', 'Zaragoza', 'Andorra'],
        'Gibraltar': ['Cadiz', 'Malaga'],
        'Cadiz': ['Gibraltar', 'Sevilla'],
        'Huelva': ['Albufeira', 'Evora', 'Sevilla'],
        'Badajoz': ['Evora', 'Caceres', 'Ciudad Real', 'Cordoba'],
        'Malaga': ['Sevilla', 'Cordoba', 'Granada', 'Almeria', 'Gibraltar'],
        'Sevilla': ['Huelva', 'Cordoba', 'Malaga', 'Cadiz'],
        'Cordoba': ['Sevilla', 'Badajoz', 'Ciudad Real', 'Jaen', 'Malaga'],
        'Ciudad Real': ['Cordoba', 'Badajoz', 'Toledo', 'Madrid', 'Albacete'],
        'Toledo': ['Caceres', 'Madrid', 'Ciudad Real'],
        'Almeria': ['Malaga', 'Granada', 'Cartagena'],
        'Granada': ['Malaga', 'Jaen', 'Almeria'],
        'Jaen': ['Cordoba', 'Albacete', 'Granada'],
        'Cartagena': ['Almeria', 'Albacete', 'Alicante'],
        'Albacete': ['Jaen', 'Ciudad Real', 'Cuenca', 'Valencia', 'Cartagena'],
        'Cuenca': ['Albacete', 'Madrid', 'Teruel', 'Valencia'],
        'Teruel': ['Cuenca', 'Zaragoza', 'Tarragona'],
        'Zaragoza': ['Madrid', 'Soria', 'Vitoria Gasteiz', 'Huesca', 'Barcelona', 'Teruel'],
        'Alicante': ['Cartagena', 'Valencia'],
        'Valencia': ['Alicante', 'Albacete', 'Cuenca', 'Tarragona'],
        'Tarragona': ['Valencia', 'Teruel', 'Barcelona'],
        'Barcelona': ['Tarragona', 'Zaragoza', 'Girona'],
        'Girona': ['Barcelona', 'Andorra'],
        'Andorra': ['Girona', 'Huesca'],
        'Mallorca': [],
    }
    
    OUTBREAK_ONLY_CONNECTIONS = {
        'Mallorca': ['Valencia', 'Tarragona'],
        'Barcelona': ['Valencia'],
        'Valencia': ['Mallorca'],
    }
    
    CITY_COLORS = {
        'Albufeira': 'blue',
        'Lisboa': 'blue',
        'Porto': 'blue',
        'Vigo': 'blue',
        'Santiago': 'blue',
        'Coruña': 'blue',
        'Evora': 'blue',
        'Coimbra': 'blue',
        'Braga': 'blue',
        'Ourense': 'blue',
        'Caceres': 'blue',
        'Salamanca': 'blue',
        'Leon': 'red',
        'Gijon': 'red',
        'Madrid': 'red',
        'Valladolid': 'red',
        'Santander': 'red',
        'Soria': 'red',
        'Burgos': 'red',
        'Vitoria Gasteiz': 'red',
        'Bilbao': 'red',
        'Pamplona': 'red',
        'San Sebastian': 'red',
        'Huesca': 'red',
        'Gibraltar': 'black',
        'Cadiz': 'black',
        'Huelva': 'black',
        'Badajoz': 'black',
        'Malaga': 'black',
        'Sevilla': 'black',
        'Cordoba': 'black',
        'Ciudad Real': 'black',
        'Toledo': 'black',
        'Almeria': 'black',
        'Granada': 'black',
        'Jaen': 'black',
        'Cartagena': 'yellow',
        'Albacete': 'yellow',
        'Cuenca': 'yellow',
        'Teruel': 'yellow',
        'Zaragoza': 'yellow',
        'Alicante': 'yellow',
        'Valencia': 'yellow',
        'Tarragona': 'yellow',
        'Barcelona': 'yellow',
        'Girona': 'yellow',
        'Andorra': 'yellow',
        'Mallorca': 'yellow',
    }
    
    DISEASE_COLORS = ['yellow', 'blue', 'black', 'red']
    MAX_CUBES_PER_COLOR = 24
    
    def __init__(self):   # Time Complexity: O(V + E)
        self.cities = list(self.CITY_CONNECTIONS.keys())

        self.disease_cubes = {}
        for city in self.cities:
            self.disease_cubes[city] = {color: 0 for color in self.DISEASE_COLORS}
        
        self.hospitals = {}
        
        self.railroads = set()
        self.max_railroads = 20
        
        self._railroad_graph = Graph()
        self.update_railroad_graph()
        
        self.PORT_CITIES = {
            'Albufeira', 'Lisboa', 'Porto', 'Vigo', 'Coruña', 'Gijon', 'Santander',
            'San Sebastian', 'Barcelona', 'Tarragona', 'Valencia', 'Alicante',
            'Cartagena', 'Almeria', 'Malaga', 'Gibraltar', 'Cadiz', 'Huelva', 'Mallorca'
        }
    
    def get_neighbors(self, city):    # Time Complexity: O(1)
        return self.CITY_CONNECTIONS.get(city, [])
    
    def get_outbreak_neighbors(self, city):   # Time Complexity: O(degree)
        regular_neighbors = self.CITY_CONNECTIONS.get(city, [])
        outbreak_only     = self.OUTBREAK_ONLY_CONNECTIONS.get(city, [])
        return list(set(regular_neighbors + outbreak_only))
    
    def get_cubes_on_board(self, color): # Time Complexity: O(V)
        total = 0
        for city in self.cities:
            total += self.disease_cubes[city][color]
        return total
    
    def get_cube_supply_remaining(self, color): # Time Complexity: O(V)
        return max(0, self.MAX_CUBES_PER_COLOR - self.get_cubes_on_board(color))
    
    def add_cubes(self, city, color, count):   # Time Complexity: O(V)
        supply_remaining = self.get_cube_supply_remaining(color)
        if supply_remaining <= 0:
            return 0
        cubes_to_add = min(count, supply_remaining)
        self.disease_cubes[city][color] += cubes_to_add
        return cubes_to_add
    
    def remove_cubes(self, city, color, count): # Time Complexity: O(1)
        current = self.disease_cubes[city][color]
        removed = min(count, current)
        self.disease_cubes[city][color] -= removed
        return removed
    
    def get_cube_count(self, city, color): # Time Complexity: O(1)
        return self.disease_cubes[city].get(color, 0)
    
    def has_hospital(self, city): # Time Complexity: O(1) (D = 4, constant)
        return city in self.hospitals.values()
    
    def get_hospital_color(self, city): # Time Complexity: O(1) (D = 4, constant) 
        for color, hospital_city in self.hospitals.items():
            if hospital_city == city:
                return color
        return None
    
    def build_hospital(self, city, color): # Time Complexity: O(1)
        if color in self.hospitals:
            return False 
        self.hospitals[color] = city
        return True
    
    def has_railroad(self, city1, city2): # Time Complexity: O(degree) where degree = number of railroad neighbors
        return self._railroad_graph.has_edge(city1, city2)
    
    def build_railroad(self, city1, city2): # Time Complexity: O(V + E)
        if len(self.railroads) >= self.max_railroads:
            return False
        if self._railroad_graph.has_edge(city1, city2):
            return False
        pair = frozenset([city1, city2])
        self.railroads.add(pair)
        self.update_railroad_graph()
        return True
    
    def update_railroad_graph(self): # Time Complexity: O(V + E)
        self._railroad_graph = Graph()
        for city in self.cities:
            self._railroad_graph.add_vertex(city)
        for city in self.cities:
            for neighbor in self.get_neighbors(city):
                if frozenset([city, neighbor]) in self.railroads:
                    self._railroad_graph.add_edge(city, neighbor)
    
    def get_railroad_graph(self): # Time Complexity: O(V + E)
        return self._railroad_graph.get_adjacency_list()
    
    def get_railroads_remaining(self): # Time Complexity: O(1)
        return self.max_railroads - len(self.railroads)
    
    def is_port_city(self, city): # Time Complexity: O(1)
        return city in self.PORT_CITIES
    
    def get_city_color(self, city): # Time Complexity: O(1)
        return self.CITY_COLORS.get(city, None)