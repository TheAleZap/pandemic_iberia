import random
import time
import sys
import select
import os
import pygame
from game_state import GameState
from board import bfs_shortest_path
from pygame_visualizer import PygameMapVisualizer
from cpu_player import choose_starting_city_for_cpu, choose_cpu_action


# bug fix: ensures it runs on windows and all platforms
def get_user_input(prompt=""):  # Time Complexity: O(m)
    if prompt:
        print(prompt, end="", flush=True)

    if os.name == "nt":
        # Windows: use simple input() since select.select() doesn't work with stdin on Windows
        try:
            try:
                pygame.event.pump()
            except (pygame.error, AttributeError):
                pass
            line = input()
            try:
                pygame.event.pump()
            except (pygame.error, AttributeError):
                pass
        except (EOFError, OSError, KeyboardInterrupt):
            return ""
        return line.strip()

    # Unix-like systems: try select.select() for non-blocking input
    try:
        stdin = sys.stdin
        while True:
            try:
                pygame.event.pump()
            except (pygame.error, AttributeError):
                pass
            try:
                readable, _, _ = select.select([stdin], [], [], 0.05)
                if readable:
                    line = stdin.readline()
                    if not line:
                        return ""
                    return line.strip()
            except (OSError, ValueError):
                # select.select() may fail on some systems or file types
                # Fall back to blocking input
                try:
                    line = input()
                    return line.strip()
                except (EOFError, OSError, KeyboardInterrupt):
                    return ""
    except (EOFError, OSError, KeyboardInterrupt):
        return ""

def cpu_type_print(text, delay=0.02):  # Time Complexity: O(n)
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()

def print_intro():  # Time Complexity: O(1)
    intro = """It is the mid-19th century, and as members of the Second Royal Philanthropic Expedition, the two of you have been sent across the Iberian Peninsula to research four deadly diseases spreading rapidly through the region:
- Cholera (Blue)
- Typhus (Red)
- Malaria (Black)
- Yellow Fever (Yellow)
In this cooperative game, both players win together or lose together. You'll need planning, teamwork, strategic thinking, and good communication to succeed.

CONTENTS: 
This game is composed by the following elements:
- 1 board: The Iberian Peninsula map with all cities marked with a specific colour (blue, red, black or yellow)
- 48 Infection Cards: each corresponding to one city on the board. These add disease cubes of the city's colour onto the board. 
- 53 Player Cards: 
    * 48 City Cards: each corresponding to one city on the board. These are used by Players to research the 4 diseases and win.
    * 5 Epidemic Cards: these are not very fun... you'll get to see why down below. 
- 96 Disease Cubes (24 of each disease colour): these represent how much 'disease' there is in a city. 
- 4 Hospitals (1 of each disease colour)
- 2 Player Pawns
- 20 Railroad Tokens: these are strategically placed by players onto the board to connect cities and be able to move around faster. 

HOW YOU WIN: 
- Research all four diseases.

HOW YOU LOSE: 
Your team loses immediately if ANY of the following occur:
- 8 outbreaks happen 
- A disease cube cannot be placed onto a city because the supply for that colour is empty (i.e. 0/24 cubes of that colour left)
- The Player Deck runs out when you must draw 2 cards

SETTING UP THE GAME: 
Once you type "Play", the game will automatically:
1. Shuffle the Infection Deck
2. Draw 9 cards from the top and infect them:
   - 3 cities receive 3 cubes
   - 3 cities receive 2 cubes
   - 3 cities receive 1 cube
   All cubes match the disease color of the city 
3. Discard the 9 cards into the Infection Discard Pile
4. Shuffle the Player Deck (exluding the 'Epidemic' Cards)
5. Deal 4 starting Player Cards to each player
6. Prompt each of the players to choose their starting location - each player has to type the name of one of the cities from his starting Player cards to place his pawn there 
After all players choose, Player 1 begins the game.

HOW A TURN WORKS:
Each turn has three steps, always in the same order:
1. Do 4 Actions: Choose any combination of actions below. Actions may be repeated per round.
2. Draw 2 Player Cards: If any Epidemic cards appear, the game resolves them automatically.
3. Infect Cities: Two Infection Cards are drawn, and those cities receive 1 disease cube each, matching their colour.
Then the next player begins their turn.

STEP 1 - ACTIONS YOU CAN TAKE:
1. Move to <City name>: 
  - You can move: 
    * By carriage: to a city directly connected to yours by a brown line
    * By train: move along a continuous chain of railroad tokens 
    * By ship: move between any two port cities.
2. Build railroad to <City name>:
   - Place a railroad token on a brown line connected to your current city.
3. Build Hospital:
   - Discard the Player Card matching your current city to build a hospital of that color in that city.
4. Treat <colour> disease: 
   - Remove one disease cube of the specified color from your current city.
   - Note: Even after a disease is researched, you still remove only one cube at a time.
5. Give card to <Player> OR Take card from <Player>:
   - You and the other player must be in the same city, and the card exchanged must match that city.
   - Note: The receiving player must not exceed the hand limit of 7 cards.
6. Research Disease: 
   - At a hospital of that color, discard 5 Player Cards of that color to research the disease.
   - Note: Researching a disease does not remove cubes already on the board.

STEP 2 - DRAWING PLAYER CARDS: 
- After your 4 actions, the game will automatically draw 2 Player Cards for you one by one.
- If you reach 8 cards, the game will pause and ask you to discard down to 7 (the hand limit).
- In the case that an Epidemic Card is drawn, the Epidemic Card is discarded to the Player Discard Pile (i.e. is not added to the Player's hand) and the game resolves the Epidemic immediately:
    1. The BOTTOM card from the Infection Deck is drawn, and 3 disease cubes of the city's colour are placed onto that city.
    2. That Infection Card is discared to the Infection Discard Pile.
    3. The Infection Discard Pile is reshuffled and placed ON TOP of the Infection Deck.
    * Note: Why is this bad? Because all cities that already have disease cubes on them will now be the first to be drawn again, therefore there is a risk of an 'Outbreak' occuring. 
    * Note 2: If the BOTTOM card from the Infection Deck that was drawn was a city that already had disease cubes on it, adding 3 cubes to it will cause an 'Outbreak'.
    * Note 3: If two Epidemic cards appear together, the process is repeated twice.

STEP 3 - INFECTING CITIES:
- After drawing Player Cards, the game will automatically draw 2 Infection Cards for you.
- Each city drawn receives 1 cube of its disease color.
- If a city already has 3 cubes and has to be added a fourth one, an Outbreak occurs.

OUTBREAKS:
Whenever a city outbreaks (i.e. has 3 cubes and has to be added a fourth one):
- The Outbreak Tracker increases by 1 (Remember: you lose if it reaches 8).
- All cities directly connected to the 'outbreaking' city receive 1 cube of that color.
- Directly connected cities that already have 3 cubes trigger chain outbreaks - A city can outbreak only once during the same chain reaction.
- Note: Mallorca, while in an isolated island that doesn't have direct connections (i.e. brown lines) to any other city, does outbreak to Valencia and Tarragona (and viceversa). 

VIEWING GAME INFORMATION: 
At any moment, you can type:
- see Player inventories: to check what Player Cards you and the other players have. 
- see Player discard pile
- see Infection discard pile: after an 'Epidemic', you might want to check which cities with 3 cubes have already been drawn, and are therefore not at an immediate threat of an 'Outbreak'. 
- rules: to get this message again.

Work together, plan strategically, manage outbreaks early, and share cards wisely. Good Luck!
The fate of Iberia is now in your hands — may your expedition succeed!
"""
    print("\n" + "="*60)
    print("WELCOME TO PANDEMIC IBERIA!")
    print("="*60)
    print(intro)

class PandemicTextGame:  
    def __init__(self):  # Time Complexity: O(V) where V = number of cities
        self.game_state = GameState()
        self.visualizer = None
        self.cpu_players = set()
        self._city_name_lookup = {city.lower(): city for city in self.game_state.board.cities}
    
    def update_visualizer(self): # Time Complexity: O(W × H + V) via underlying pygame redraw
        if self.visualizer:
            self.visualizer.mark_dirty()
            # Pump events to keep window responsive
            try:
                pygame.event.pump()
                # Do a quick update if possible (non-blocking)
                self.visualizer.update()
            except (pygame.error, AttributeError, Exception):
                pass
    
    def find_city_name(self, city_input): # Time Complexity: O(1)
        if not city_input:
            return None
        city_lower = city_input.lower().strip()
        return self._city_name_lookup.get(city_lower)
    
    def format_city_name(self, city): # Time Complexity: O(1)
        if city in self.game_state.board.cities:
            color = self.game_state.board.get_city_color(city)
            return f"{city} ({color})"
        return city
    
    def _format_location(self, location): # Time Complexity: O(1)
        return self.format_city_name(location) if location else "None"
    
    def _format_hand(self, player): # Time Complexity: O(H log H) where H = hand size
        return [self.format_city_name(card) for card in sorted(player.hand)]
    
    def _infect_cities_in_setup(self, count, cube_count): # Time Complexity: O(count × V)
        cities = []
        for _ in range(count):
            if self.game_state.infection_deck.is_empty():
                break
            city = self.game_state.infection_deck.dequeue()
            if city is None:
                break
            cities.append(city)
            color = self.game_state.board.get_city_color(city)
            if color is None:
                # Skip cities without valid colors (should not happen, but safety check)
                continue
            self.game_state.board.add_cubes(city, color, cube_count)
            self.game_state.infection_discard.push(city)
        return cities
    
    def _display_epidemic_info(self, epidemic_info, card_num, card): # Time Complexity: O(S) where S = number of epidemic steps (bounded by 3 cubes)
        if epidemic_info:
            print(f"\n   Card {card_num}: EPIDEMIC!")
            self.game_state.player_discard.push(card)
            
            if not epidemic_info['city']:
                print("   Infection deck is empty, no city infected")
                return True
            
            city = epidemic_info['city']
            color = epidemic_info['color']
            city_formatted = self.format_city_name(city)
            steps = epidemic_info.get('epidemic_steps', [])
            
            print("   Resolving epidemic...")
            print(f"    - Drawing bottom card from Infection deck: {city_formatted}")
            
            for i, step in enumerate(steps):
                if step['type'] == 'before_add':
                    current_cubes = step['current_cubes']
                    print(f"    - {city_formatted} currently has: {current_cubes} {color} cube{'s' if current_cubes != 1 else ''}")
                    if i + 1 < len(steps) and steps[i + 1]['type'] == 'outbreak_triggered':
                        print(f"    - Adding 1 {color} cube to {city_formatted}.")
                
                elif step['type'] == 'outbreak_triggered':
                    print(f"   OUTBREAK in {city_formatted}!")
                    print("   Resolving outbreak...")
                
                elif step['type'] == 'outbreak_resolved':
                    outbreaks_in_chain = step['outbreaks_in_chain']
                    print(f"    - Outbreak tracker: {self.game_state.outbreak_count}/8")
                    print(f"    - Spreading 1 {color} cube to each neighbouring city")
                    if outbreaks_in_chain > 1:
                        print(f"    - Chain outbreak: {outbreaks_in_chain} outbreaks occurred")
                    print("   Resolving epidemic (continued)...")
                
                elif step['type'] == 'cube_added':
                    print(f"    - Adding 1 {color} cube to {city_formatted}.")
                
                elif step['type'] == 'cube_skipped':
                    print(f"    - Skipping cube addition (outbreak already occurred during this epidemic).")
                
                elif step['type'] == 'supply_exhausted':
                    print(f"    - Cannot add cube - {color} disease supply is empty! Game Over!")
                    return True
            
            print("    - Reshuffling Infection Discard Pile and placing it on top of the Infection Deck")
            return True
        return False
    
    def _handle_hand_limit_human(self, player): # Time Complexity: O(1) worst case (H ≤ 8, bounded by hand limit check after each card)
        while player.get_hand_size() > player.max_hand_size:
            print(f"\nPlayer {player.id + 1}, you have exceeded the hand limit of 7 cards.")
            formatted_hand = self._format_hand(player)
            print(f"   Your cards: {', '.join(formatted_hand)}")
            while True:
                discard_input = get_user_input(f"   Please discard a card: ").strip()
                discard = self.find_city_name(discard_input)
                if discard is not None and discard in player.hand:
                    player.remove_card(discard)
                    self.game_state.player_discard.push(discard)
                    discard_formatted = self.format_city_name(discard)
                    print(f"   ✓ Discarded {discard_formatted}")
                    break
                else:
                    print(f"   ✗ Invalid card. Choose from: {', '.join(formatted_hand)}")
    
    def _handle_hand_limit_cpu(self, player): # Time Complexity: O(1) worst case (H ≤ 8, bounded by hand limit check after each card)
        while player.get_hand_size() > player.max_hand_size:
            color_counts = {}
            for card in player.hand:
                color = self.game_state.board.get_city_color(card)
                if color is not None:
                    color_counts[color] = color_counts.get(color, 0) + 1
            
            if not color_counts:
                # Fallback: discard first card if no valid colors found
                discard = next(iter(player.hand), None)
                if discard is None:
                    break
            else:
                min_count = min(color_counts.values())
                min_colors = [color for color, count in color_counts.items() if count == min_count]
                min_color = random.choice(min_colors)
                discard = None
                for card in player.hand:
                    if self.game_state.board.get_city_color(card) == min_color:
                        discard = card
                        break
                if discard is None:
                    # Fallback if no card matches
                    discard = next(iter(player.hand), None)
                    if discard is None:
                        break
            
            player.remove_card(discard)
            self.game_state.player_discard.push(discard)
            discard_formatted = self.format_city_name(discard)
            print(f"   CPU discarded {discard_formatted} to keep hand at 7 cards or less.")
    
    def _draw_player_cards(self, player, is_cpu=False): # Time Complexity: O(1) worst case (H ≤ 8, bounded by hand limit check after each card)
        cards_drawn = 0
        for i in range(2):
            if self.game_state.supply_exhausted:
                return
            card, epidemic_info = self.game_state.draw_player_card()
            if card is None:
                print("Player deck is empty! Game Over!")
                return
            
            cards_drawn += 1
            
            if not self._display_epidemic_info(epidemic_info, cards_drawn, card):
                print(f"   Card {cards_drawn}: {self.format_city_name(card)}")
                player.add_card(card)
            else:
                if self.check_loss():
                    return
            
            if self.game_state.supply_exhausted or self.check_loss():
                return
            
            if is_cpu:
                self._handle_hand_limit_cpu(player)
            else:
                self._handle_hand_limit_human(player)
    
    def _display_discard_pile(self, discard_stack, pile_name, format_epidemic=False): # Time Complexity: O(C)
        print("\n" + "-"*60)
        discard_count = len(discard_stack)
        print(f"Cards in {pile_name}: {discard_count}")
        print("-"*60)
        discard_list = []
        temp_stack = []
        while not discard_stack.is_empty():
            card = discard_stack.pop()
            discard_list.append(card)
            temp_stack.append(card)
        
        for card in reversed(temp_stack):
            discard_stack.push(card)
        
        if discard_list:
            for card in discard_list:
                if format_epidemic and card == 'EPIDEMIC':
                    card_formatted = card
                else:
                    card_formatted = self.format_city_name(card)
                print(f"  - {card_formatted}")
        else:
            print("  (empty)")
        print("-"*60)
    
    def setup_game(self): # Time Complexity: O(P + C) where P = number of players, C = number of cards
        if self.game_state.game_started:
            print("✗ Game has already started. Cannot setup again.")
            return
        
        print("\n" + "="*60)
        print("GAME SETUP:")
        print("="*60)
        
        print("Infecting 9 cities...")
        
        cities_3 = self._infect_cities_in_setup(3, 3)
        formatted_cities_3 = [self.format_city_name(city) for city in cities_3]
        print(f"   - 3 Infection cards to place 3 cubes: {', '.join(formatted_cities_3)}")
        
        cities_2 = self._infect_cities_in_setup(3, 2)
        formatted_cities_2 = [self.format_city_name(city) for city in cities_2]
        print(f"   - 3 Infection cards to place 2 cubes: {', '.join(formatted_cities_2)}")
        
        cities_1 = self._infect_cities_in_setup(3, 1)
        formatted_cities_1 = [self.format_city_name(city) for city in cities_1]
        print(f"   - 3 Infection cards to place 1 cube: {', '.join(formatted_cities_1)}")
        
        self.update_visualizer()
        

        print("\nDealing starting hands...")
    
        for player in self.game_state.players:
            for _ in range(4):
                card = self.game_state.player_deck.dequeue()
                player.add_card(card)
            formatted_cards = self._format_hand(player)
            print(f"   - Player {player.id + 1} received 4 cards: {', '.join(formatted_cards)}")
        
        epidemic_cards = ['EPIDEMIC'] * 5
        all_remaining = []
        while not self.game_state.player_deck.is_empty():
            all_remaining.append(self.game_state.player_deck.dequeue())
        all_remaining.extend(epidemic_cards)
        random.shuffle(all_remaining)
        for card in all_remaining:
            self.game_state.player_deck.enqueue(card)
        



        print("\nChoose starting cities...")
        for player in self.game_state.players:
            formatted_cards = self._format_hand(player)
            if player.id in self.cpu_players:
                city = choose_starting_city_for_cpu(self.game_state, player)
                player.location = city
                city_formatted = self.format_city_name(city)
                print(f"\n   ✓ CPU Player {player.id + 1} automatically starts in {city_formatted}")
                self.update_visualizer()
            else:
                print(f"\n   - Player {player.id + 1}, choose your starting city from your cards: {', '.join(formatted_cards)}")
                while True:
                    city_input = get_user_input(f"   Player {player.id + 1}, type the name of your desired starting city: ").strip()
                    city = self.find_city_name(city_input)
                    if city is not None and city in player.hand:
                        player.location = city
                        print(f"   ✓ Player {player.id + 1} starts in {self.format_city_name(city)}")
                        self.update_visualizer()
                        break
                    else:
                        print(f"   ✗ Invalid city. You must choose from your cards: {', '.join(formatted_cards)}")
        
        self.game_state.game_started = True
        print("\nSETUP COMPLETE! Game begins now.")
    


    def run(self): # Time Complexity: O(1) per iteration
        print_intro()
        
        while True:
            command = get_user_input("\nType 'Play' to begin: ").strip()
            if command.lower() == "play":
                break
            elif command.lower() == "rules":
                print_intro()
            else:
                print("Please type 'Play' to begin the game, or 'rules' to see the rules again.")
        
        print("\n" + "="*60)
        print("CPU PLAYER SETUP (2-player game):")
        print("="*60)
        print("Hello Player 1! You can choose whether Player 2 is human or CPU-controlled.")
        player2 = self.game_state.players[1]
        while True:
            response = get_user_input(
                f"Should Player 2 be CPU-controlled? (yes/no, default = yes): "
            ).strip().lower()
            if response in ("yes", "y", ""):
                self.cpu_players.add(player2.id)
                print("   -> Player 2 will be controlled by the CPU.")
                break
            elif response in ("no", "n"):
                print("   -> Player 2 will be controlled by a human.")
                break
            else:
                print("   Please answer 'yes' or 'no'.")
        




        try:
            self.visualizer = PygameMapVisualizer(self.game_state)
            # Force immediate first render
            self.visualizer.mark_dirty()
            self.visualizer.update()
            # Pump events to ensure window is responsive
            pygame.event.pump()
        except Exception as e:
            print(f"Error: Could not initialize pygame visualizer: {e}")
            import traceback
            traceback.print_exc()
            self.visualizer = None
        
        self.setup_game()
        
        # Force update after setup
        if self.visualizer:
            self.visualizer.mark_dirty()
            self.visualizer.update()
            pygame.event.pump()
        
        last_update = 0
        update_interval = 0.05  # More frequent updates
        
        while True:
            # Always pump pygame events to keep window responsive
            if self.visualizer:
                try:
                    pygame.event.pump()
                except:
                    pass
            
            current_time = time.time()
            if (current_time - last_update) > update_interval:
                if self.visualizer:
                    try:
                        self.visualizer.update()
                        last_update = current_time
                    except Exception:
                        if hasattr(self.visualizer, 'running') and not self.visualizer.running:
                            print("\nGame window closed. Exiting...")
                            return
                        # Silently continue on pygame errors
                        pass
            
            if self.check_win():
                print("\n" + "="*60)
                print("YOU WON! All four diseases have been researched!")
                print("="*60)
                break
            
            if self.check_loss():
                print("\n" + "="*60)
                print("DEFEAT! Game Over!")
                print("="*60)
                break
            

            player = self.game_state.get_current_player()
            if player.id in self.cpu_players:
                self.play_cpu_turn(player)
            else:
                self.play_turn(player)
            self.game_state.next_turn()
            
            # Force update after each turn
            if self.visualizer:
                self.visualizer.mark_dirty()
        
        if self.visualizer:
            self.visualizer.running = False
            print("\nGame ended. Closing visualization...")
            time.sleep(1)
    
    def play_turn(self, player): # Time Complexity: O(A × M) where A = number of actions, M = max action complexity
        if self.check_loss() or self.check_win():
            return
        
        print("\n" + "="*60)
        print(f"Player {player.id + 1}'s Turn")
        print("="*60)
        location_formatted = self._format_location(player.location)
        print(f"Location: {location_formatted}")
        formatted_hand = self._format_hand(player)
        print(f"Hand ({len(player.hand)} cards): {', '.join(formatted_hand)}")
        print(f"Actions remaining: {player.actions_remaining}/4")
        


        print("\nAvailable actions:")
        print("  • Move to <City name>")
        print("  • Build Railroad to <City>")
        print("  • Build Hospital")
        print("  • Treat <color> Disease")
        print("  • Give card to <Player>")
        print("  • Take card from <Player>")
        print("  • Research Disease")
        print("  • see Player inventories")
        print("  • see Player discard pile")
        print("  • see Infection discard pile")
        print("  • rules")
        
        for action_num in range(1, 5):
            if player.actions_remaining <= 0:
                break
            if self.check_loss() or self.check_win():
                return
            
            while True:
                command = get_user_input(f"\nAction {action_num}/4: ").strip()
                
                if command.lower() == "see player inventories":
                    self.show_player_inventories()
                    continue
                elif command.lower() == "see player discard pile":
                    self.show_player_discard()
                    continue
                elif command.lower() == "see infection discard pile":
                    self.show_infection_discard()
                    continue
                elif command.lower() == "rules":
                    print_intro()
                    continue
                
                if self.execute_action(player, command):
                    if self.check_loss() or self.check_win():
                        return
                    break
                else:
                    print("Invalid action. Please try again.")
        
        if self.check_loss() or self.check_win():
            return
        


        print("\n" + "-"*60)
        print("Drawing 2 Player Cards...")
        print("-"*60)
        
        self._draw_player_cards(player, is_cpu=False)
        if self.check_loss() or self.check_win():
            return
        self.infect_cities_phase()
    
    def infect_cities_phase(self): # Time Complexity: O(1) average, O(k × degree) worst case where k = outbreak chain length
        print("\n" + "-"*60)
        print("Infecting Cities...")
        print("-"*60)
        
        for i in range(2):
            if self.game_state.supply_exhausted:
                return
            if self.game_state.infection_deck.is_empty():
                if not self.game_state.infection_discard.is_empty():
                    print("Infection deck is empty! Reshuffling Infection Discard Pile...")
                    self.game_state.reshuffle_infection_discard()
                else:
                    print("Infection deck is empty!")
                    break
            


            city = self.game_state.infection_deck.dequeue()
            if city is None:
                break
            color = self.game_state.board.get_city_color(city)
            if color is None:
                print(f"   Warning: City {city} has no valid color. Skipping infection.")
                self.game_state.infection_discard.push(city)
                continue
            current_cubes = self.game_state.board.get_cube_count(city, color)
            city_formatted = self.format_city_name(city)
            
            print(f"   Infection card {i+1}: {city_formatted}")
            
            if color is None:
                print(f"   Warning: {city_formatted} has no valid color. Skipping infection.")
                self.game_state.infection_discard.push(city)
                continue
            
            if current_cubes >= 3:
                print(f"   {city_formatted} already has 3 {color} cubes! Outbreak occurs!")
                old_outbreak_count = self.game_state.outbreak_count
                supply_exhausted = self.game_state.handle_outbreak(city, color)
                if supply_exhausted:
                    self.game_state.supply_exhausted = True
                    print(f"   Cannot add cube - {color} disease supply is empty! Game Over!")
                    return
                if self.check_loss():
                    return
                new_outbreak_count = self.game_state.outbreak_count
                outbreaks_this_chain = new_outbreak_count - old_outbreak_count
                if outbreaks_this_chain > 0:
                    if outbreaks_this_chain == 1:
                        print(f"   Outbreak! Outbreak tracker: {new_outbreak_count}/8")
                    else:
                        print(f"   Chain outbreak! {outbreaks_this_chain} outbreaks occurred. Outbreak tracker: {new_outbreak_count}/8")
                    if new_outbreak_count >= self.game_state.max_outbreaks:
                        print("   Outbreak tracker reached 8! Game Over!")
            else:
                cubes_added = self.game_state.board.add_cubes(city, color, 1)
                if cubes_added == 0:
                    self.game_state.supply_exhausted = True
                    print(f"   Cannot add cube - {color} disease supply is empty! Game Over!")
                    return
                print(f"   ✓ Added 1 {color} cube to {city_formatted}")
            
            self.game_state.infection_discard.push(city)
        
        self.update_visualizer()

    def play_cpu_turn(self, player): # Time Complexity: O(A × M) where A = number of actions, M = max action complexity
        if self.check_loss() or self.check_win():
            return
        
        print("\n" + "="*60)
        cpu_type_print(f"CPU Player {player.id + 1}'s Turn")
        print("="*60)
        location_formatted = self._format_location(player.location)
        formatted_hand = self._format_hand(player)
        cpu_type_print(f"Location: {location_formatted}")
        cpu_type_print(f"Hand ({len(player.hand)} cards): {', '.join(formatted_hand)}")
        cpu_type_print(f"Actions remaining: {player.actions_remaining}/4")
        
        for action_num in range(1, 5):
            if player.actions_remaining <= 0:
                break
            if self.check_loss() or self.check_win():
                return
            
            print(f"\n   Playing CPU action {action_num}/4", end="", flush=True)
            for _ in range(3):
                time.sleep(0.4)
                print(".", end="", flush=True)
            print()
            


            decision = choose_cpu_action(self.game_state, player)
            action_type = decision[0]
            if action_type == "treat":
                color = decision[1]
                cpu_type_print(f"   CPU Action {action_num}/4: Treat {color} disease.")
                self.action_treat_disease(player, color)
            elif action_type == "move":
                destination = decision[1]
                dest_formatted = self.format_city_name(destination)
                cpu_type_print(f"   CPU Action {action_num}/4: Move to {dest_formatted}.")
                self.action_move(player, destination)
            elif action_type == "build_hospital":
                cpu_type_print(f"   CPU Action {action_num}/4: Build Hospital.")
                self.action_build_hospital(player)
            elif action_type == "research":
                color = decision[1]
                cpu_type_print(f"   CPU Action {action_num}/4: Research {color} disease.")
                self.action_research_disease(player)
                if self.check_loss() or self.check_win():
                    return
            else:
                break
            
            if self.check_loss() or self.check_win():
                return
        
        if self.check_loss() or self.check_win():
            return
        
        print("\n" + "-"*60)
        print("Drawing 2 Player Cards for CPU player...")
        print("-"*60)
        
        self._draw_player_cards(player, is_cpu=True)
        if self.check_loss() or self.check_win():
            return
        self.infect_cities_phase()
    


    def execute_action(self, player, command): # Time Complexity: O(1) for parsing, depends on action called (O(1) to O(V+E))
        if self.check_loss() or self.check_win():
            return False
        
        if not command or not command.strip():
            return False
        
        command_lower = command.lower()
        
        if command_lower.startswith("move to "):
            city_input = command[8:].strip()
            city = self.find_city_name(city_input)
            if city is None:
                print(f"✗ Invalid city name: {city_input}")
                return False
            return self.action_move(player, city)
        


        elif command_lower.startswith("build railroad to "):
            city_input = command[18:].strip()
            city = self.find_city_name(city_input)
            if city is None:
                print(f"✗ Invalid city name: {city_input}")
                return False
            return self.action_build_railroad(player, city)
        
        elif command_lower == "build hospital":
            return self.action_build_hospital(player)
        
        elif command_lower.startswith("treat "):
            parts = command[6:].strip().split()
            if len(parts) >= 2 and parts[1].lower() == "disease":
                color = parts[0].lower()
                return self.action_treat_disease(player, color)
        
        elif command_lower.startswith("give card to player "):
            try:
                other_player_num = int(command[20:].strip()) - 1
                if 0 <= other_player_num < len(self.game_state.players):
                    return self.action_share_knowledge(player, other_player_num, give=True)
            except (ValueError, IndexError, TypeError):
                pass
        elif command_lower.startswith("take card from player "):
            try:
                other_player_num = int(command[22:].strip()) - 1
                if 0 <= other_player_num < len(self.game_state.players):
                    return self.action_share_knowledge(player, other_player_num, give=False)
            except (ValueError, IndexError, TypeError):
                pass
        

        elif command_lower == "research disease":
            return self.action_research_disease(player)
        
        return False
    
    def action_move(self, player, destination): # Time Complexity: O(1) average, O(V + E) worst case
        if destination not in self.game_state.board.cities:
            print(f"✗ Invalid city name: {destination}")
            return False
        
        current = player.location
        if current is None:
            print("✗ Player has no location set")
            return False
        
        if destination == current:
            print(f"✗ You are already in {self._format_location(current)}")
            return False
        
        movement_type = None
        
        if destination in self.game_state.board.get_neighbors(current):
            movement_type = "carriage"
        elif self.can_move_by_train(current, destination):
            movement_type = "train"
        elif (self.game_state.board.is_port_city(current) and 
              self.game_state.board.is_port_city(destination)):
            movement_type = "ship"
        
        dest_formatted = self.format_city_name(destination)
        
        if movement_type:
            player.location = destination
            player.actions_remaining -= 1
            print(f"✓ Moved to {dest_formatted} by {movement_type}")
            self.update_visualizer()
            return True
        
        print(f"✗ Cannot move to {dest_formatted}. Not connected by carriage, train, or ship.")
        return False
    
    def can_move_by_train(self, start, end): # Time Complexity: O(V + E)
        railroad_graph = self.game_state.board.get_railroad_graph()
        path = bfs_shortest_path(railroad_graph, start, end)
        return path is not None
    
    def action_build_railroad(self, player, destination): # Time Complexity: O(1)
        if destination not in self.game_state.board.cities:
            print(f"✗ Invalid city name: {destination}")
            return False
        
        current = player.location
        if current is None:
            print("✗ Player has no location set")
            return False
        
        if destination == current:
            print(f"✗ Cannot build railroad to your current city ({self._format_location(current)})")
            return False
        
        if destination not in self.game_state.board.get_neighbors(current):
            print(f"✗ {self.format_city_name(destination)} is not directly connected to {self._format_location(current)}")
            return False
        
        if self.game_state.board.has_railroad(current, destination):
            current_formatted = self.format_city_name(current)
            dest_formatted = self.format_city_name(destination)
            print(f"✗ Railroad already exists between {current_formatted} and {dest_formatted}")
            return False
        
        if self.game_state.board.get_railroads_remaining() <= 0:
            print(f"✗ No railroads remaining (20/20 used)")
            return False
        
        if self.game_state.board.build_railroad(current, destination):
            current_formatted = self.format_city_name(current)
            dest_formatted = self.format_city_name(destination)
            player.actions_remaining -= 1
            print(f"✓ Built railroad between {current_formatted} and {dest_formatted}")
            print(f"  Railroads remaining: {self.game_state.board.get_railroads_remaining()}/20")
            self.update_visualizer()
            return True
        
        return False
    
    def action_build_hospital(self, player): # Time Complexity: O(1)
        current = player.location
        if current is None:
            print("✗ Player has no location set")
            return False
        color = self.game_state.board.get_city_color(current)
        if color is None:
            print(f"✗ City {current} has no valid color")
            return False
        
        if current not in player.hand:
            print(f"✗ You don't have the {self.format_city_name(current)} card in your hand")
            return False
        
        if color in self.game_state.board.hospitals:
            existing_city = self.game_state.board.hospitals[color]
            print(f"✗ A {color} hospital already exists in {self.format_city_name(existing_city)}")
            return False
        
        if self.game_state.board.build_hospital(current, color):
            player.remove_card(current)
            self.game_state.player_discard.push(current)
            player.actions_remaining -= 1
            print(f"✓ Built {color} hospital in {self.format_city_name(current)}")
            self.update_visualizer()
            return True
        
        return False
    
    def action_treat_disease(self, player, color): # Time Complexity: O(1)
        if color not in ['red', 'blue', 'black', 'yellow']:
            print(f"✗ Invalid color: {color}")
            return False
        
        current = player.location
        if current is None:
            print("✗ Player has no location set")
            return False
        cube_count = self.game_state.board.get_cube_count(current, color)
        
        if cube_count == 0:
            print(f"✗ No {color} cubes in {self.format_city_name(current)}")
            return False
        
        self.game_state.board.remove_cubes(current, color, 1)
        player.actions_remaining -= 1
        print(f"✓ Removed 1 {color} cube from {self.format_city_name(current)}")
        
        self.update_visualizer()
        return True
    
    def action_share_knowledge(self, player, other_player_num, give=True): # Time Complexity: O(1) worst case (H ≤ 8, as it's bounded by hand limit)
        other_player = self.game_state.players[other_player_num]
        
        if player.id == other_player.id:
            print("✗ You cannot give or take a card from yourself")
            return False
        
        current = player.location
        if current is None:
            print("✗ Player has no location set")
            return False
        if other_player.location is None:
            print(f"✗ Player {other_player_num + 1} has no location set")
            return False
        
        if current != other_player.location:
            print(f"✗ You and Player {other_player_num + 1} must be in the same city")
            return False
        
        current_formatted = self.format_city_name(current)
        
        if current not in player.hand and give:
            print(f"✗ You don't have the {current_formatted} card")
            return False
        if current not in other_player.hand and not give:
            print(f"✗ Player {other_player_num + 1} doesn't have the {current_formatted} card")
            return False
        
        if give and other_player.get_hand_size() >= other_player.max_hand_size:
            print(f"✗ Player {other_player_num + 1} already has {other_player.max_hand_size} cards (hand limit). Cannot receive more cards.")
            return False
        
        is_other_player_cpu = other_player.id in self.cpu_players
        
        if not is_other_player_cpu or give:
            action_desc = f"Player {player.id + 1} {'give' if give else 'take'} {current_formatted} card to/from Player {other_player_num + 1}"
            response = get_user_input(f"Player {other_player_num + 1}, do you agree for {action_desc}? (yes/no): ").strip().lower()
            
            if response != "yes":
                print("✗ Action cancelled")
                return False
        
        if give:
            player.remove_card(current)
            other_player.add_card(current)
            print(f"✓ Player {player.id + 1} gave {current_formatted} to Player {other_player_num + 1}")
        else:
            other_player.remove_card(current)
            player.add_card(current)
            print(f"✓ Player {player.id + 1} took {current_formatted} from Player {other_player_num + 1}")
        
        player.actions_remaining -= 1
        
        for p in [player, other_player]:
            if p.id in self.cpu_players:
                self._handle_hand_limit_cpu(p)
            else:
                self._handle_hand_limit_human(p)
        
        return True
    
    def action_research_disease(self, player): # Time Complexity: O(1) worst case (H ≤ 7, bounded by hand limit)
        current = player.location
        if current is None:
            print("✗ Player has no location set")
            return False
        hospital_color = self.game_state.board.get_hospital_color(current)
        
        if hospital_color is None:
            print("✗ You must be in a city with a hospital")
            return False
        
        color_cards = [card for card in player.hand if 
                      self.game_state.board.get_city_color(card) == hospital_color]
        
        if len(color_cards) < 5:
            print(f"✗ You need 5 {hospital_color} cards. You have {len(color_cards)}")
            return False
        
        if hospital_color in self.game_state.cured_diseases:
            print(f"✗ {hospital_color} disease is already researched")
            return False
        
        cards_to_discard = color_cards[:5]
        for card in cards_to_discard:
            player.remove_card(card)
            self.game_state.player_discard.push(card)
        
        self.game_state.cured_diseases.add(hospital_color)
        player.actions_remaining -= 1
        print(f"✓ Researched {hospital_color} disease!")
        
        self.update_visualizer()
        
        if self.check_win():
            return True
        
        return True
    
    def show_player_inventories(self): # Time Complexity: O(P) worst case (H ≤ 7, bounded by hand limit)
        print("\n" + "-"*60)
        print("Player Inventories:")
        print("-"*60)
        for player in self.game_state.players:
            print(f"Player {player.id + 1}:")
            if player.hand:
                formatted_hand = self._format_hand(player)
                for formatted_card in formatted_hand:
                    print(f"  - {formatted_card}")
            else:
                print("  (no cards)")
        print("-"*60)
    
    def show_player_discard(self): # Time Complexity: O(C) where C = number of cards in discard pile
        self._display_discard_pile(self.game_state.player_discard, "Player Discard Pile", format_epidemic=True)
    
    def show_infection_discard(self): # Time Complexity: O(C) where C = number of cards in discard pile
        self._display_discard_pile(self.game_state.infection_discard, "Infection Discard Pile", format_epidemic=False)
    

    def check_win(self): # Time Complexity: O(1)
        return len(self.game_state.cured_diseases) == len(self.game_state.board.DISEASE_COLORS)
    

    def check_loss(self): # Time Complexity: O(1)
        if self.game_state.outbreak_count >= self.game_state.max_outbreaks:
            return True
        if self.game_state.player_deck_exhausted:
            return True
        if self.game_state.supply_exhausted:
            return True
        return False