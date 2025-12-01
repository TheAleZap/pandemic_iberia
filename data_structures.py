class Node:
    def __init__(self, value, next=None):  # Time Complexity: O(1)
        self.value = value
        self.next  = next

class Stack:
    def __init__(self):  # Time Complexity: O(1)
        self.top  = None
        self.size = 0
    
    def push(self, value):   # Time Complexity: O(1)
        node = Node(value, self.top)
        self.top = node
        self.size += 1
    
    def pop(self):   # Time Complexity: O(1)
        if self.is_empty():
            return None
        value = self.top.value
        self.top  = self.top.next
        self.size -= 1
        return value
    
    def is_empty(self):   # Time Complexity: O(1)
        return self.top is None
    
    def __len__(self):    # Time Complexity: O(1)
        return self.size

class Queue:
    def __init__(self):  # Time Complexity: O(1)
        self.head = None
        self.tail = None
        self.size = 0
    
    def enqueue(self, value):   # Time Complexity: O(1)
        node = Node(value)
        if self.is_empty():
            self.head = node
        else:
            self.tail.next = node
        self.tail = node
        self.size += 1
    
    def dequeue(self):   # Time Complexity: O(1)
        if self.is_empty():
            return None
        value = self.head.value
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self.size -= 1
        return value
    
    def is_empty(self):   # Time Complexity: O(1)
        return self.head is None
    
    def __len__(self):    # Time Complexity: O(1)
        return self.size

class Graph:
    def __init__(self):  # Time Complexity: O(1)
        self.adjacency_list = {}
    
    def add_vertex(self, vertex):   # Time Complexity: O(1)
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = []
    
    def add_edge(self, vertex1, vertex2):   # Time Complexity: O(degree)
        if vertex1 not in self.adjacency_list:
            self.adjacency_list[vertex1] = []
        if vertex2 not in self.adjacency_list:
            self.adjacency_list[vertex2] = []
        
        if vertex2 not in self.adjacency_list[vertex1]:
            self.adjacency_list[vertex1].append(vertex2)
        if vertex1 not in self.adjacency_list[vertex2]:
            self.adjacency_list[vertex2].append(vertex1)
    
    def get_neighbors(self, vertex):   # Time Complexity: O(1)
        return self.adjacency_list.get(vertex, [])
    
    def has_edge(self, vertex1, vertex2):   # Time Complexity: O(degree)
        if vertex1 not in self.adjacency_list:
            return False
        return vertex2 in self.adjacency_list[vertex1]
    
    def get_vertices(self):   # Time Complexity: O(V)
        return list(self.adjacency_list.keys())
    
    def get_adjacency_list(self):   # Time Complexity: O(V + E)
        return self.adjacency_list.copy()