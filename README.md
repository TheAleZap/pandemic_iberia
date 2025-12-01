# Pandemic Iberia - Game Implementation

## Introduction

**Authors**: Tatiana Quinn, Alejandro Zapata, Ali Ahmad Lufti, Gabriel Queiroz Santiago  
**Assignment**: Boardgame Final Project  
**Class**: Algorithms and Data Structures  
**Institution**: IE University  
**Term**: Winter 2025

## Overview
This is a simplified version of Pandemic Iberia, a cooperative board game where players work together to research 4 diseases across the Iberian Peninsula. In our case, we have adapted it so that there is 1 player and 1 CPU player or 2 players, the user is prompted to select if he wished to make Player 2 a CPU player.

## Important! - How To Run the Game:

### 1. Prerequisites:
```bash
pip install -r requirements.txt
```

### 2. Run the game:
```bash
python main.py
```

## Data Structures Used

### 1. **Graph (Adjacency List)**
- **Purpose**: Represent the board with cities as nodes and connections as edges; enable graph algorithms.
- **Complexity**: O(V + E) space, O(1) neighbor lookup average case

### 2. **Queue**
- **Purpose**: Manage player deck and infection deck (FIFO order of cards)
- **Complexity**: O(1) enqueue/dequeue, O(n) space where n = number of cards in the queue

### 3. **Stack**
- **Purpose**: Discard piles (LIFO behaviour for reshuffling on epidemics)
- **Complexity**: O(1) push/pop, O(n) space where n = number of cards in the stack

## Algorithms Used

### 1. **Breadth-First Search (BFS) for Movement**
- **Purpose**: Find shortest path between cities for movement by train.
- **Complexity**: O(V + E) time, O(V) space

### 2. **Breadth-First Search (BFS) for Outbreaks**
- **Purpose**: Propagate disease outbreaks through directly connected cities (chain reactions).
- **Complexity**: O(k × degree) time, O(k) space where k = number of cities in outbreak chain, degree = average number of neighbors

### 3. **Greedy Algorithm for CPU Player**
- **Purpose**: Choose simple, locally best actions for the CPU player without look-ahead.
- **Complexity**: O((H + V) × (V + E)) per decision where H = hand size, V = cities, E = edges