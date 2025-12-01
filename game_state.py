import random
from data_structures import Queue, Stack
from board import Board


class Player:
    def __init__(self, player_id, starting_city):  # Time Complexity: O(1)
        self.id = player_id
        self.location = starting_city
        self.hand = set()
        self.actions_remaining = 4
        self.max_hand_size = 7
        self.cpu_first_action_done = False
        self.cpu_committed_plan = None
    
    def add_card(self, card):  # Time Complexity: O(1)
        self.hand.add(card)
    
    def remove_card(self, card):  # Time Complexity: O(1)
        if card in self.hand:
            self.hand.remove(card)
            return True
        return False
    
    def has_card(self, card):  # Time Complexity: O(1)
        return card in self.hand
    
    def get_hand_size(self):  # Time Complexity: O(1)
        return len(self.hand)


class GameState:
    def __init__(self):  # Time Complexity: O(V + C)
        """
        This class is holding everything that defines the current game:
        board, decks, players, counters, and win/lose flags.
        """
        self.board = Board()

        self.players = []
        for i in range(2):
            self.players.append(Player(i, None))
        
        self.player_deck    = Queue()
        self.infection_deck = Queue()
        
        self.player_discard    = Stack()
        self.infection_discard = Stack()
        
        self.initialize_decks()
        self.cured_diseases = set()
        
        self.outbreak_count  = 0
        self.max_outbreaks   = 8
        self.infection_rate  = 2
        self.epidemic_count  = 0
        self.max_epidemics   = 4
        
        self.current_player_idx = 0
        self.game_started       = False
        self.supply_exhausted   = False
        self.player_deck_exhausted = False
    
    def initialize_decks(self):  # Time Complexity: O(C)
        """Create, shuffle and deal the starting player + infection decks."""
        city_cards = list(self.board.cities)
        random.shuffle(city_cards)
        
        for card in city_cards:
            self.player_deck.enqueue(card)
        
        infection_cards = city_cards.copy()
        random.shuffle(infection_cards)
        
        for card in infection_cards:
            self.infection_deck.enqueue(card)
    
    def get_current_player(self): # Time Complexity: O(1)
        return self.players[self.current_player_idx]
    
    def next_turn(self): # Time Complexity: O(1)
        self.current_player_idx = (self.current_player_idx + 1) % len(self.players)
        player = self.get_current_player()
        player.actions_remaining = 4
    
    def draw_player_card(self): # Time Complexity: O(1) average, O(C + k * degree) worst case
        if self.player_deck.is_empty():
            self.player_deck_exhausted = True
            return None, None
        
        card = self.player_deck.dequeue()
        
        if card == 'EPIDEMIC':
            epidemic_info = self.handle_epidemic()
            return 'EPIDEMIC', epidemic_info
        
        return card, None
    
    def handle_epidemic(self): # Time Complexity: O(C + k * degree) where k = outbreak chain length
        self.epidemic_count += 1
        
        if self.infection_deck.is_empty():
            if not self.infection_discard.is_empty():
                self.reshuffle_infection_discard()
            else:
                return {'city': None, 'color': None, 'cubes_added': 0, 'outbreak_occurred': False, 'supply_exhausted': False, 'epidemic_steps': []}
        
        temp_stack = Stack()
        while not self.infection_deck.is_empty():
            temp_stack.push(self.infection_deck.dequeue())
        bottom_city = temp_stack.pop()
        
        while not temp_stack.is_empty():
            self.infection_deck.enqueue(temp_stack.pop())
        
        color = self.board.get_city_color(bottom_city)
        old_outbreak_count = self.outbreak_count
        
        supply_exhausted = False
        outbreak_occurred = False
        cubes_to_add = 3
        cubes_added_total = 0
        epidemic_steps = []
        outbreak_occurred_during_epidemic = False
        
        for cube_num in range(cubes_to_add):
            current_cubes = self.board.get_cube_count(bottom_city, color)
            epidemic_steps.append({
                'type': 'before_add',
                'current_cubes': current_cubes
            })
            
            if outbreak_occurred_during_epidemic:
                epidemic_steps.append({
                    'type': 'cube_skipped',
                    'reason': 'outbreak_already_occurred'
                })
                continue
            
            if current_cubes >= 3:
                outbreak_occurred = True
                outbreak_occurred_during_epidemic = True
                outbreak_count_before = self.outbreak_count
                epidemic_steps.append({
                    'type': 'outbreak_triggered',
                    'outbreak_count_before': outbreak_count_before
                })
                supply_exhausted = self.handle_outbreak(bottom_city, color) or supply_exhausted
                epidemic_steps.append({
                    'type': 'outbreak_resolved',
                    'outbreak_count_after': self.outbreak_count,
                    'outbreaks_in_chain': self.outbreak_count - outbreak_count_before
                })
            else:
                cubes_added = self.board.add_cubes(bottom_city, color, 1)
                if cubes_added == 0:
                    supply_exhausted = True
                    epidemic_steps.append({
                        'type': 'supply_exhausted'
                    })
                    break
                else:
                    cubes_added_total += cubes_added
                    epidemic_steps.append({
                        'type': 'cube_added',
                        'cubes_after': self.board.get_cube_count(bottom_city, color)
                    })
        
        if supply_exhausted:
            self.supply_exhausted = True
        
        self.infection_discard.push(bottom_city)
        self.reshuffle_infection_discard(place_on_top=True)
        
        return {
            'city': bottom_city,
            'color': color,
            'cubes_added': cubes_added_total,
            'outbreak_occurred': outbreak_occurred,
            'outbreak_count': self.outbreak_count - old_outbreak_count if outbreak_occurred else 0,
            'supply_exhausted': supply_exhausted,
            'epidemic_steps': epidemic_steps
        }
    
    def reshuffle_infection_discard(self, place_on_top=False): # Time Complexity: O(C)
        discard_list = []
        while not self.infection_discard.is_empty():
            discard_list.append(self.infection_discard.pop())
        random.shuffle(discard_list)
        
        if place_on_top and not self.infection_deck.is_empty():
            current_deck = []
            while not self.infection_deck.is_empty():
                current_deck.append(self.infection_deck.dequeue())
            
            for card in discard_list:
                self.infection_deck.enqueue(card)
            
            for card in current_deck:
                self.infection_deck.enqueue(card)
        else:
            for card in discard_list:
                self.infection_deck.enqueue(card)
    
    def handle_outbreak(self, city, color): # Time Complexity: O(k * degree)
        if self.outbreak_count >= self.max_outbreaks:
            return None
        visited_this_outbreak = set([city])
    
        queue = Queue()
        queue.enqueue(city)
        outbreaks_in_chain = 1
        supply_exhausted = False
        
        while not queue.is_empty():
            if self.outbreak_count + outbreaks_in_chain >= self.max_outbreaks:
                outbreaks_in_chain = self.max_outbreaks - self.outbreak_count
                break
            
            current = queue.dequeue()
            neighbors = self.board.get_outbreak_neighbors(current)
            
            for neighbor in neighbors:
                if neighbor in visited_this_outbreak:
                    continue
                visited_this_outbreak.add(neighbor)
                current_cubes = self.board.get_cube_count(neighbor, color)
                if current_cubes >= 3:
                    outbreaks_in_chain += 1
                    if self.outbreak_count + outbreaks_in_chain >= self.max_outbreaks:
                        outbreaks_in_chain = self.max_outbreaks - self.outbreak_count
                        break
                    queue.enqueue(neighbor)
                else:
                    cubes_added = self.board.add_cubes(neighbor, color, 1)
                    if cubes_added == 0:
                        supply_exhausted = True
                        continue
            
            if self.outbreak_count + outbreaks_in_chain >= self.max_outbreaks:
                break

        self.outbreak_count += outbreaks_in_chain
        return supply_exhausted
    
    def infect_cities(self): # Time Complexity: O(infection_rate × (V + k * degree)) worst case where k = outbreak chain length
        for _ in range(self.infection_rate):
            if self.infection_deck.is_empty():
                if not self.infection_discard.is_empty():
                    self.reshuffle_infection_discard()
                else:
                    continue
            
            city = self.infection_deck.dequeue()
            color = self.board.get_city_color(city)
            
            current_cubes = self.board.get_cube_count(city, color)
            
            if current_cubes < 3:
                self.board.add_cubes(city, color, 1)
            else:
                self.handle_outbreak(city, color)
            
            self.infection_discard.push(city)
    
    def check_win(self): # Time Complexity: O(1)
        return len(self.cured_diseases) == len(self.board.DISEASE_COLORS)
    
    def check_loss(self): # Time Complexity: O(1)
        if self.outbreak_count >= self.max_outbreaks:
            return True
        if self.player_deck_exhausted:
            return True
        if self.supply_exhausted:
            return True
        return False