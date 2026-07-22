from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import time

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

# In a real application, this would be a database (e.g., SQLite, PostgreSQL)
# For this example, we'll use a simple in-memory dictionary.
# This data will reset every time the Flask app restarts.
users_db = {}
game_history_db = [] # Stores all game results
game_attempts_db = {} # Tracks attempts per user per game-topic: {username: {game_type: {topic: count}}}
perfect_wins_db = {} # Tracks perfect wins per user: {username: count}

@app.route('/')
def home():
    return "Learnova Backend is running!"

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'success': False, 'message': 'Username and password are required.'}), 400

    if username in users_db:
        return jsonify({'success': False, 'message': 'Username already exists.'}), 409

    users_db[username] = {'password': password}
    game_attempts_db[username] = {} # Initialize attempts for new user
    perfect_wins_db[username] = 0 # Initialize perfect wins for new user
    print(f"Registered new user: {username}")
    return jsonify({'success': True, 'message': 'Registration successful!'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'success': False, 'message': 'Username and password are required.'}), 400

    user = users_db.get(username)
    if user and user['password'] == password:
        print(f"User logged in: {username}")
        return jsonify({'success': True, 'message': 'Login successful!'}), 200
    else:
        return jsonify({'success': False, 'message': 'Invalid username or password.'}), 401

@app.route('/generate_game_content', methods=['POST'])
def generate_game_content():
    data = request.get_json()
    game_type = data.get('game_type')
    topic = data.get('topic') # Can be None for games like Spin and Solve or Boss Fight

    if not game_type:
        return jsonify({'success': False, 'message': 'Game type is required.'}), 400

    print(f"Generating content for Game: {game_type}, Topic: {topic}")

    game_content = {}
    success = True
    message = "Content generated successfully."

    # Mock content generation based on game type and topic
    # All content is now hardcoded directly in this file.
    if game_type == "Mystery Match":
        if topic == "Linked Lists":
            game_content = [
                {"riddle": "I am a sequence of nodes, where each node points to the next. What am I?", "answer": "Linked List"},
                {"riddle": "I am the first node in a linked list. What am I called?", "answer": "Head"},
                {"riddle": "I am a node that points to nothing, signifying the end of a linked list. What am I?", "answer": "Null"}
            ]
        elif topic == "Stacks":
            game_content = [
                {"riddle": "I follow the Last-In, First-Out principle. What am I?", "answer": "Stack"},
                {"riddle": "I am the operation to add an element to a stack. What am I?", "answer": "Push"},
                {"riddle": "I am the operation to remove an element from a stack. What am I?", "answer": "Pop"}
            ]
        elif topic == "Queues":
            game_content = [
                {"riddle": "I follow the First-In, First-Out principle. What am I?", "answer": "Queue"},
                {"riddle": "I am the operation to add an element to a queue. What am I?", "answer": "Enqueue"},
                {"riddle": "I am the operation to remove an element from a queue. What am I?", "answer": "Dequeue"}
            ]
        elif topic == "Trees":
            game_content = [
                {"riddle": "I am a non-linear data structure with a root and child nodes. What am I?", "answer": "Tree"},
                {"riddle": "I am the topmost node in a tree. What am I called?", "answer": "Root"},
                {"riddle": "I am a node with no children. What am I?", "answer": "Leaf"}
            ]
        elif topic == "Heaps":
            game_content = [
                {"riddle": "I am a complete binary tree where parent nodes are compared to their children. What am I?", "answer": "Heap"},
                {"riddle": "In a max-heap, I am the largest element. Where am I located?", "answer": "Root"},
                {"riddle": "I am the process of restoring the heap property after an insertion or deletion. What am I?", "answer": "Heapify"}
            ]
        else:
            success = False
            message = "Topic not found for Mystery Match."

    elif game_type == "Rapid Recall Arena":
        if topic == "Linked Lists":
            game_content = [
                {"question": "Which type of linked list allows traversal in both directions?", "options": {"A": "Singly", "B": "Doubly", "C": "Circular", "D": "Linear"}, "correct_answer": "B"},
                {"question": "What is the time complexity to insert a node at the beginning of a singly linked list?", "options": {"A": "O(1)", "B": "O(n)", "C": "O(log n)", "D": "O(n log n)"}, "correct_answer": "A"},
                {"question": "What does a 'null' pointer in a linked list signify?", "options": {"A": "An error", "B": "The end of the list", "C": "A circular reference", "D": "An empty node"}, "correct_answer": "B"},
                {"question": "Which operation is typically O(n) in a singly linked list?", "options": {"A": "Insertion at head", "B": "Deletion at tail", "C": "Accessing head", "D": "Updating a node's value"}, "correct_answer": "B"},
                {"question": "In a circular linked list, how do you detect the end?", "options": {"A": "When next is null", "B": "When next points to head", "C": "When size is zero", "D": "When current is head"}, "correct_answer": "B"}
            ]
        elif topic == "Stacks":
            game_content = [
                {"question": "Which operation adds an element to the top of a stack?", "options": {"A": "Pop", "B": "Peek", "C": "Push", "D": "Enqueue"}, "correct_answer": "C"},
                {"question": "What is the time complexity for push and pop operations in a stack (array-based)?", "options": {"A": "O(n)", "B": "O(log n)", "C": "O(1)", "D": "O(n log n)"}, "correct_answer": "C"},
                {"question": "What principle does a stack follow?", "options": {"A": "FIFO", "B": "LIFO", "C": "FILO", "D": "LILO"}, "correct_answer": "B"},
                {"question": "If a stack is empty, what does the 'pop' operation result in?", "options": {"A": "Returns 0", "B": "Returns null", "C": "Underflow error", "D": "No operation"}, "correct_answer": "C"},
                {"question": "Which data structure is often used to implement function call stacks?", "options": {"A": "Queue", "B": "Linked List", "C": "Stack", "D": "Tree"}, "correct_answer": "C"}
            ]
        elif topic == "Queues":
            game_content = [
                {"question": "Which operation removes an element from the front of a queue?", "options": {"A": "Enqueue", "B": "Dequeue", "C": "Peek", "D": "Push"}, "correct_answer": "B"},
                {"question": "What is the time complexity for enqueue and dequeue operations in a queue (linked list-based)?", "options": {"A": "O(n)", "B": "O(log n)", "C": "O(1)", "D": "O(n log n)"}, "correct_answer": "C"},
                {"question": "What principle does a queue follow?", "options": {"A": "LIFO", "B": "FILO", "C": "FIFO", "D": "LILO"}, "correct_answer": "C"},
                {"question": "If a queue is full, what does the 'enqueue' operation result in?", "options": {"A": "Returns 0", "B": "Returns null", "C": "Overflow error", "D": "No operation"}, "correct_answer": "C"},
                {"question": "Which data structure is best for managing tasks in a printer spooler?", "options": {"A": "Stack", "B": "Tree", "C": "Queue", "D": "Hash Table"}, "correct_answer": "C"}
            ]
        elif topic == "Trees":
            game_content = [
                {"question": "In a Binary Search Tree, all nodes in the left subtree of a node are ____ its value.", "options": {"A": "greater than", "B": "less than", "C": "equal to", "D": "unrelated to"}, "correct_answer": "B"},
                {"question": "What is the maximum number of children a binary tree node can have?", "options": {"A": "1", "B": "2", "C": "3", "D": "Any number"}, "correct_answer": "B"},
                {"question": "Which traversal visits the root node last?", "options": {"A": "Inorder", "B": "Preorder", "C": "Postorder", "D": "Level-order"}, "correct_answer": "C"},
                {"question": "A tree where each node has at most 'm' children is called a(n) ____ tree.", "options": {"A": "Binary", "B": "Complete", "C": "M-ary", "D": "Full"}, "correct_answer": "C"},
                {"question": "What is the height of a tree with only one node (the root)?", "options": {"A": "0", "B": "1", "C": "Undefined", "D": "Infinite"}, "correct_answer": "A"}
            ]
        elif topic == "Heaps":
            game_content = [
                {"question": "Which property defines a min-heap?", "options": {"A": "Parent is smaller than children", "B": "Parent is larger than children", "C": "Nodes are sorted", "D": "It's a balanced tree"}, "correct_answer": "A"},
                {"question": "What is the time complexity to insert an element into a heap?", "options": {"A": "O(1)", "B": "O(log n)", "C": "O(n)", "D": "O(n log n)"}, "correct_answer": "B"},
                {"question": "Heaps are typically implemented using which data structure?", "options": {"A": "Linked List", "B": "Array", "C": "Stack", "D": "Queue"}, "correct_answer": "B"},
                {"question": "Which algorithm commonly uses a min-priority queue (often implemented with a min-heap)?", "options": {"A": "Bubble Sort", "B": "Quick Sort", "C": "Dijkstra's Shortest Path", "D": "Merge Sort"}, "correct_answer": "C"},
                {"question": "What is the process of rearranging a heap to maintain its properties after an operation?", "options": {"A": "Sorting", "B": "Balancing", "C": "Heapify", "D": "Traversing"}, "correct_answer": "C"}
            ]
        else:
            success = False
            message = "Topic not found for Rapid Recall Arena."

    elif game_type == "Concept Rocket Launch":
        if topic == "Linked Lists":
            game_content = [
                {"correct_order": ["Define Node structure", "Create Head pointer", "Insert first node", "Traverse list", "Delete a node"]},
                {"correct_order": ["Initialize head to null", "Allocate memory for new node", "Set new node's data", "Point new node's next to current head", "Update head to new node"]},
                {"correct_order": ["Find node to delete", "Update previous node's next pointer", "Free memory of deleted node", "Handle edge case: head deletion", "Ensure no dangling pointers"]}
            ]
        elif topic == "Stacks":
            game_content = [
                {"correct_order": ["Initialize empty array/list", "Push element A", "Push element B", "Pop element B", "Pop element A"]},
                {"correct_order": ["Check if stack is full (overflow)", "Add element to top", "Increment top pointer", "Return success"]},
                {"correct_order": ["Check if stack is empty (underflow)", "Retrieve element from top", "Decrement top pointer", "Return element"]}
            ]
        elif topic == "Queues":
            game_content = [
                {"correct_order": ["Initialize empty array/list", "Enqueue element A", "Enqueue element B", "Dequeue element A", "Dequeue element B"]},
                {"correct_order": ["Check if queue is full (overflow)", "Add element to rear", "Increment rear pointer", "Return success"]},
                {"correct_order": ["Check if queue is empty (underflow)", "Retrieve element from front", "Increment front pointer", "Return element"]}
            ]
        elif topic == "Trees":
            game_content = [
                {"correct_order": ["Define Node (data, left, right)", "Create root node", "Insert left child", "Insert right child", "Perform Inorder Traversal"]},
                {"correct_order": ["Start at root", "Visit current node", "Recursively traverse left subtree", "Recursively traverse right subtree", "Preorder Traversal"]},
                {"correct_order": ["Start at root", "Recursively traverse left subtree", "Recursively traverse right subtree", "Visit current node", "Postorder Traversal"]}
            ]
        elif topic == "Heaps":
            game_content = [
                {"correct_order": ["Represent as array", "Insert new element at end", "Heapify up (bubble up)", "Extract max/min element", "Heapify down (sink down)"]},
                {"correct_order": ["Add new element to end of array", "Compare with parent", "Swap if heap property violated", "Repeat until root or property satisfied"]},
                {"correct_order": ["Remove root (max/min element)", "Move last element to root", "Compare with children", "Swap with largest/smallest child", "Repeat until heap property restored"]}
            ]
        else:
            success = False
            message = "Topic not found for Concept Rocket Launch."

    elif game_type == "Fix the Code":
        if topic == "Linked Lists":
            game_content = [
                {"description": "Fix the code to correctly insert a new node at the beginning of a singly linked list.",
                 "code_snippet": "class Node:\n    def __init__(self, data):\n        self.data = data\n        self.next = None\n\nclass LinkedList:\n    def __init__(self):\n        self.head = None\n\n    def insert_at_beginning(self, data):\n        new_node = Node(data)\n        new_node.next = self.head\n        MISSING_LINE\n",
                 "missing_line": "self.head = new_node"},
                {"description": "Complete the function to traverse and print all elements of a linked list.",
                 "code_snippet": "class Node:\n    def __init__(self, data):\n        self.data = data\n        self.next = None\n\nclass LinkedList:\n    # ... (assume insert_at_beginning exists)\n\n    def print_list(self):\n        current = self.head\n        while current:\n            print(current.data, end=' -> ')\n            MISSING_LINE\n        print('None')\n",
                 "missing_line": "current = current.next"},
                {"description": "Fix the code to correctly delete the head node of a singly linked list.",
                 "code_snippet": "class Node:\n    def __init__(self, data):\n        self.data = data\n        self.next = None\n\nclass LinkedList:\n    # ... (assume other methods exist)\n\n    def delete_head(self):\n        if self.head is None:\n            return\n        MISSING_LINE\n",
                 "missing_line": "self.head = self.head.next"}
            ]
        elif topic == "Stacks":
            game_content = [
                {"description": "Fix the `push` operation for a list-based stack.",
                 "code_snippet": "class Stack:\n    def __init__(self):\n        self.items = []\n\n    def push(self, item):\n        MISSING_LINE\n\n    def peek(self): return self.items[-1] if not self.is_empty() else None\n    def is_empty(self): return len(self.items) == 0\n",
                 "missing_line": "self.items.append(item)"},
                {"description": "Fix the `pop` operation for a list-based stack.",
                 "code_snippet": "class Stack:\n    def __init__(self):\n        self.items = []\n\n    def pop(self):\n        if self.is_empty():\n            return None # Or raise an error\n        MISSING_LINE\n\n    def is_empty(self): return len(self.items) == 0\n",
                 "missing_line": "return self.items.pop()"},
                {"description": "Complete the `size` method for a stack.",
                 "code_snippet": "class Stack:\n    def __init__(self):\n        self.items = []\n\n    def size(self):\n        MISSING_LINE\n\n    # ... (other methods)\n",
                 "missing_line": "return len(self.items)"}
            ]
        elif topic == "Queues":
            game_content = [
                {"description": "Fix the `enqueue` operation for a list-based queue.",
                 "code_snippet": "class Queue:\n    def __init__(self):\n        self.items = []\n\n    def enqueue(self, item):\n        MISSING_LINE\n\n    def is_empty(self): return len(self.items) == 0\n",
                 "missing_line": "self.items.append(item)"},
                {"description": "Fix the `dequeue` operation for a list-based queue.",
                 "code_snippet": "class Queue:\n    def __init__(self):\n        self.items = []\n\n    def dequeue(self):\n        if self.is_empty():\n            return None # Or raise an error\n        MISSING_LINE\n\n    def is_empty(self): return len(self.items) == 0\n",
                 "missing_line": "return self.items.pop(0)"},
                {"description": "Complete the `front` method to peek at the front element without removing it.",
                 "code_snippet": "class Queue:\n    def __init__(self):\n        self.items = []\n\n    def front(self):\n        if self.is_empty():\n            return None\n        MISSING_LINE\n\n    # ... (other methods)\n",
                 "missing_line": "return self.items[0]"}
            ]
        elif topic == "Trees":
            game_content = [
                {"description": "Complete the `insert` method for a simple Binary Search Tree.",
                 "code_snippet": "class Node:\n    def __init__(self, key):\n        self.key = key\n        self.left = None\n        self.right = None\n\ndef insert(node, key):\n    if node is None:\n        MISSING_LINE\n    if key < node.key:\n        node.left = insert(node.left, key)\n    else:\n        node.right = insert(node.right, key)\n    return node\n",
                 "missing_line": "return Node(key)"},
                {"description": "Fix the `inorder_traversal` function for a Binary Tree.",
                 "code_snippet": "class Node:\n    def __init__(self, key):\n        self.key = key\n        self.left = None\n        self.right = None\n\ndef inorder_traversal(node):\n    if node:\n        inorder_traversal(node.left)\n        MISSING_LINE\n        inorder_traversal(node.right)\n",
                 "missing_line": "print(node.key, end=' ')"},
                {"description": "Complete the `find_min` function in a BST.",
                 "code_snippet": "class Node:\n    def __init__(self, key):\n        self.key = key\n        self.left = None\n        self.right = None\n\ndef find_min(node):\n    current = node\n    while current.left is not None:\n        MISSING_LINE\n    return current.key\n",
                 "missing_line": "current = current.left"}
            ]
        elif topic == "Heaps":
            game_content = [
                {"description": "Fix the `heapify_down` function for a max-heap (simplified).",
                 "code_snippet": "def heapify_down(arr, n, i):\n    largest = i\n    left = 2 * i + 1\n    right = 2 * i + 2\n\n    if left < n and arr[left] > arr[largest]:\n        largest = left\n\n    if right < n and arr[right] > arr[largest]:\n        largest = right\n\n    if largest != i:\n        arr[i], arr[largest] = arr[largest], arr[i] # Swap\n        MISSING_LINE\n",
                 "missing_line": "heapify_down(arr, n, largest)"},
                {"description": "Complete the `build_max_heap` function.",
                 "code_snippet": "def build_max_heap(arr):\n    n = len(arr)\n    # Start from the last non-leaf node and heapify down each one\n    for i in range(n // 2 - 1, -1, -1):\n        MISSING_LINE\n\n",
                 "missing_line": "heapify_down(arr, n, i)"},
                {"description": "Fix the `insert` operation for a max-heap (simplified).",
                 "code_snippet": "def insert_heap(arr, item):\n    arr.append(item)\n    i = len(arr) - 1\n    parent = (i - 1) // 2\n    while i > 0 and arr[parent] < arr[i]:\n        arr[i], arr[parent] = arr[parent], arr[i]\n        i = parent\n        MISSING_LINE\n",
                 "missing_line": "parent = (i - 1) // 2"}
            ]
        else:
            success = False
            message = "Topic not found for Fix the Code."

    elif game_type == "Block Identifier":
        if topic == "Linked Lists":
            game_content = [
                {"description": "Identify the missing step in creating a new node for a Linked List.",
                 "correct_sequence": [
                     {"concept": "Define Node Class", "is_missing_block": False},
                     {"concept": "Create Node Instance", "is_missing_block": True},
                     {"concept": "Set Node's Next to None", "is_missing_block": False}
                 ]},
                {"description": "Identify the missing step when inserting at the head of a Linked List.",
                 "correct_sequence": [
                     {"concept": "Create New Node", "is_missing_block": False},
                     {"concept": "Point New Node's Next to Head", "is_missing_block": False},
                     {"concept": "Update Head to New Node", "is_missing_block": True}
                 ]},
                {"description": "Identify the missing step when traversing a Linked List.",
                 "correct_sequence": [
                     {"concept": "Start at Head", "is_missing_block": False},
                     {"concept": "Process Current Node", "is_missing_block": False},
                     {"concept": "Move to Next Node", "is_missing_block": True},
                     {"concept": "Repeat until Null", "is_missing_block": False}
                 ]}
            ]
        elif topic == "Stacks":
            game_content = [
                {"description": "Identify the missing step in a Push operation on a Stack.",
                 "correct_sequence": [
                     {"concept": "Check for Overflow", "is_missing_block": False},
                     {"concept": "Add Element to Top", "is_missing_block": True},
                     {"concept": "Increment Top Pointer", "is_missing_block": False}
                 ]},
                {"description": "Identify the missing step in a Pop operation on a Stack.",
                 "correct_sequence": [
                     {"concept": "Check for Underflow", "is_missing_block": False},
                     {"concept": "Retrieve Element from Top", "is_missing_block": True},
                     {"concept": "Decrement Top Pointer", "is_missing_block": False}
                 ]},
                {"description": "Identify the missing step in checking if a Stack is empty.",
                 "correct_sequence": [
                     {"concept": "Access Stack Size", "is_missing_block": False},
                     {"concept": "Compare Size to Zero", "is_missing_block": True},
                     {"concept": "Return True/False", "is_missing_block": False}
                 ]}
            ]
        elif topic == "Queues":
            game_content = [
                {"description": "Identify the missing step in an Enqueue operation on a Queue.",
                 "correct_sequence": [
                     {"concept": "Check for Overflow", "is_missing_block": False},
                     {"concept": "Add Element to Rear", "is_missing_block": True},
                     {"concept": "Increment Rear Pointer", "is_missing_block": False}
                 ]},
                {"description": "Identify the missing step in a Dequeue operation on a Queue.",
                 "correct_sequence": [
                     {"concept": "Check for Underflow", "is_missing_block": False},
                     {"concept": "Retrieve Element from Front", "is_missing_block": True},
                     {"concept": "Increment Front Pointer", "is_missing_block": False}
                 ]},
                {"description": "Identify the missing step in checking if a Queue is empty.",
                 "correct_sequence": [
                     {"concept": "Access Queue Size", "is_missing_block": False},
                     {"concept": "Compare Size to Zero", "is_missing_block": True},
                     {"concept": "Return True/False", "is_missing_block": False}
                 ]}
            ]
        elif topic == "Trees":
            game_content = [
                {"description": "Identify the missing step in inserting a node into a Binary Search Tree.",
                 "correct_sequence": [
                     {"concept": "Start at Root", "is_missing_block": False},
                     {"concept": "Compare New Value with Node", "is_missing_block": False},
                     {"concept": "Move Left/Right", "is_missing_block": True},
                     {"concept": "Insert at Null Position", "is_missing_block": False}
                 ]},
                {"description": "Identify the missing step in an Inorder Traversal of a Binary Tree.",
                 "correct_sequence": [
                     {"concept": "Traverse Left Subtree", "is_missing_block": False},
                     {"concept": "Visit Current Node", "is_missing_block": True},
                     {"concept": "Traverse Right Subtree", "is_missing_block": False}
                 ]},
                {"description": "Identify the missing step in finding the minimum element in a BST.",
                 "correct_sequence": [
                     {"concept": "Start at Root", "is_missing_block": False},
                     {"concept": "Move to Left Child", "is_missing_block": True},
                     {"concept": "Repeat until Left is Null", "is_missing_block": False},
                     {"concept": "Return Current Node's Value", "is_missing_block": False}
                 ]}
            ]
        elif topic == "Heaps":
            game_content = [
                {"description": "Identify the missing step in inserting into a Max-Heap.",
                 "correct_sequence": [
                     {"concept": "Add element to end", "is_missing_block": False},
                     {"concept": "Bubble Up (Heapify Up)", "is_missing_block": True},
                     {"concept": "Maintain Heap Property", "is_missing_block": False}
                 ]},
                {"description": "Identify the missing step in extracting the max element from a Max-Heap.",
                 "correct_sequence": [
                     {"concept": "Swap Root with Last Element", "is_missing_block": False},
                     {"concept": "Remove Last Element", "is_missing_block": False},
                     {"concept": "Sink Down (Heapify Down)", "is_missing_block": True},
                     {"concept": "Return Original Root", "is_missing_block": False}
                 ]},
                {"description": "Identify the missing step in building a Max-Heap from an array.",
                 "correct_sequence": [
                     {"concept": "Start from Last Non-Leaf Node", "is_missing_block": False},
                     {"concept": "Perform Heapify Down", "is_missing_block": True},
                     {"concept": "Iterate Up to Root", "is_missing_block": False}
                 ]}
            ]
        else:
            success = False
            message = "Topic not found for Block Identifier."

    elif game_type == "Spin and Solve":
        
            # Hardcoded content for Spin and Solve based on topic
            if topic == "Linked Lists":
                game_content = {
                    "mcqs": [
                        {"question": "Which type of linked list allows traversal in both directions?", "options": {"A": "Singly", "B": "Doubly", "C": "Circular", "D": "Linear"}, "correct_answer": "B"},
                        {"question": "What is the time complexity to insert a node at the beginning of a singly linked list?", "options": {"A": "O(1)", "B": "O(n)", "C": "O(log n)", "D": "O(n log n)"}, "correct_answer": "A"},
                        {"question": "What does a 'null' pointer in a linked list signify?", "options": {"A": "An error", "B": "The end of the list", "D": "An empty node"}, "correct_answer": "B"}
                    ],
                    "riddles": [
                        {"riddle": "I am a sequence of nodes, where each node points to the next. What am I?", "answer": "Linked List"},
                        {"riddle": "I am the first node in a linked list. What am I called?", "answer": "Head"}
                    ]
                }
            elif topic == "Stacks":
                game_content = {
                    "mcqs": [
                        {"question": "Which operation adds an element to the top of a stack?", "options": {"A": "Pop", "B": "Peek", "C": "Push", "D": "Enqueue"}, "correct_answer": "C"},
                        {"question": "What is the time complexity for push and pop operations in a stack (array-based)?", "options": {"A": "O(n)", "B": "O(log n)", "C": "O(1)", "D": "O(n log n)"}, "correct_answer": "C"},
                        {"question": "What principle does a stack follow?", "options": {"A": "FIFO", "B": "LIFO", "C": "FILO", "D": "LILO"}, "correct_answer": "B"}
                    ],
                    "riddles": [
                        {"riddle": "I follow the Last-In, First-Out principle. What am I?", "answer": "Stack"},
                        {"riddle": "I am the operation to add an element to a stack. What am I?", "answer": "Push"}
                    ]
                }
            elif topic == "Queues":
                game_content = {
                    "mcqs": [
                        {"question": "Which operation removes an element from the front of a queue?", "options": {"A": "Enqueue", "B": "Dequeue", "C": "Peek", "D": "Push"}, "correct_answer": "B"},
                        {"question": "What is the time complexity for enqueue and dequeue operations in a queue (linked list-based)?", "options": {"A": "O(n)", "B": "O(log n)", "C": "O(1)", "D": "O(n log n)"}, "correct_answer": "C"},
                        {"question": "What principle does a queue follow?", "options": {"A": "LIFO", "B": "FILO", "C": "FIFO", "D": "LILO"}, "correct_answer": "C"}
                    ],
                    "riddles": [
                        {"riddle": "I follow the First-In, First-Out principle. What am I?", "answer": "Queue"},
                        {"riddle": "I am the operation to add an element to a queue. What am I?", "answer": "Enqueue"}
                    ]
                }
            elif topic == "Trees":
                game_content = {
                    "mcqs": [
                        {"question": "In a Binary Search Tree, all nodes in the left subtree of a node are ____ its value.", "options": {"A": "greater than", "B": "less than", "C": "equal to", "D": "unrelated to"}, "correct_answer": "B"},
                        {"question": "What is the maximum number of children a binary tree node can have?", "options": {"A": "1", "B": "2", "C": "3", "D": "Any number"}, "correct_answer": "B"},
                        {"question": "Which traversal visits the root node last?", "options": {"A": "Inorder", "B": "Preorder", "C": "Postorder", "D": "Level-order"}, "correct_answer": "C"}
                    ],
                    "riddles": [
                        {"riddle": "I am a non-linear data structure with a root and child nodes. What am I?", "answer": "Tree"},
                        {"riddle": "I am the topmost node in a tree. What am I called?", "answer": "Root"}
                    ]
                }
            elif topic == "Heaps":
                game_content = {
                    "mcqs": [
                        {"question": "Which property defines a min-heap?", "options": {"A": "Parent is smaller than children", "B": "Parent is larger than children", "C": "Nodes are sorted", "D": "It's a balanced tree"}, "correct_answer": "A"},
                        {"question": "What is the time complexity to insert an element into a heap?", "options": {"A": "O(1)", "B": "O(log n)", "C": "O(n)", "D": "O(n log n)"}, "correct_answer": "B"},
                        {"question": "Heaps are typically implemented using which data structure?", "options": {"A": "Linked List", "B": "Array", "C": "Stack", "D": "Queue"}, "correct_answer": "B"}
                    ],
                    "riddles": [
                        {"riddle": "I am a complete binary tree where parent nodes are compared to their children. What am I?", "answer": "Heap"},
                        {"riddle": "In a max-heap, I am the largest element. Where am I located?", "answer": "Root"}
                    ]
                }
            

    elif game_type == "Boss Fight":
        # Boss Fight questions are a mix of all 5 core topics
        all_mcqs = []
        all_riddles = []

        # Aggregate questions from all topics
        for t in ["Linked Lists", "Stacks", "Queues", "Trees", "Heaps"]:
            mcqs_for_topic = []
            riddles_for_topic = []

            if t == "Linked Lists":
                mcqs_for_topic = [
                    {"type": "mcq", "question": "Which type of linked list allows traversal in both directions?", "options": {"A": "Singly", "B": "Doubly", "C": "Circular", "D": "Linear"}, "correct_answer": "B"},
                    {"type": "mcq", "question": "What is the time complexity to insert a node at the beginning of a singly linked list?", "options": {"A": "O(1)", "B": "O(n)", "C": "O(log n)", "D": "O(n log n)"}, "correct_answer": "A"}
                ]
                riddles_for_topic = [
                    {"type": "riddle", "riddle": "I am a sequence of nodes, where each node points to the next. What am I?", "answer": "Linked List"},
                    {"type": "riddle", "riddle": "I am the first node in a linked list. What am I called?", "answer": "Head"}
                ]
            elif t == "Stacks":
                mcqs_for_topic = [
                    {"type": "mcq", "question": "Which operation adds an element to the top of a stack?", "options": {"A": "Pop", "B": "Peek", "C": "Push", "D": "Enqueue"}, "correct_answer": "C"},
                    {"type": "mcq", "question": "What is the time complexity for push and pop operations in a stack (array-based)?", "options": {"A": "O(n)", "B": "O(log n)", "C": "O(1)", "D": "O(n log n)"}, "correct_answer": "C"}
                ]
                riddles_for_topic = [
                    {"type": "riddle", "riddle": "I follow the Last-In, First-Out principle. What am I?", "answer": "Stack"},
                    {"type": "riddle", "riddle": "I am the operation to add an element to a stack. What am I?", "answer": "Push"}
                ]
            elif t == "Queues":
                mcqs_for_topic = [
                    {"type": "mcq", "question": "Which operation removes an element from the front of a queue?", "options": {"A": "Enqueue", "B": "Dequeue", "C": "Peek", "D": "Push"}, "correct_answer": "B"},
                    {"type": "mcq", "question": "What is the time complexity for enqueue and dequeue operations in a queue (linked list-based)?", "options": {"A": "O(n)", "B": "O(log n)", "C": "O(1)", "D": "O(n log n)"}, "correct_answer": "C"}
                ]
                riddles_for_topic = [
                    {"type": "riddle", "riddle": "I follow the First-In, First-Out principle. What am I?", "answer": "Queue"},
                    {"type": "riddle", "riddle": "I am the operation to add an element to a queue. What am I?", "answer": "Enqueue"}
                ]
            elif t == "Trees":
                mcqs_for_topic = [
                    {"type": "mcq", "question": "In a Binary Search Tree, all nodes in the left subtree of a node are ____ its value.", "options": {"A": "greater than", "B": "less than", "C": "equal to", "D": "unrelated to"}, "correct_answer": "B"},
                    {"type": "mcq", "question": "What is the maximum number of children a binary tree node can have?", "options": {"A": "1", "B": "2", "C": "3", "D": "Any number"}, "correct_answer": "B"}
                ]
                riddles_for_topic = [
                    {"type": "riddle", "riddle": "I am a non-linear data structure with a root and child nodes. What am I?", "answer": "Tree"},
                    {"type": "riddle", "riddle": "I am the topmost node in a tree. What am I called?", "answer": "Root"}
                ]
            elif t == "Heaps":
                mcqs_for_topic = [
                    {"type": "mcq", "question": "Which property defines a min-heap?", "options": {"A": "Parent is smaller than children", "B": "Parent is larger than children", "C": "Nodes are sorted", "D": "It's a balanced tree"}, "correct_answer": "A"},
                    {"type": "mcq", "question": "What is the time complexity to insert an element into a heap?", "options": {"A": "O(1)", "B": "O(log n)", "C": "O(n)", "D": "O(n log n)"}, "correct_answer": "B"}
                ]
                riddles_for_topic = [
                    {"type": "riddle", "riddle": "I am a complete binary tree where parent nodes are compared to their children. What am I?", "answer": "Heap"},
                    {"type": "riddle", "riddle": "In a max-heap, I am the largest element. Where am I located?", "answer": "Root"}
                ]
            
            all_mcqs.extend(mcqs_for_topic)
            all_riddles.extend(riddles_for_topic)

        # Combine and shuffle to get 10 questions for Boss Fight
        # Prioritize MCQs if available, then riddles to reach 10
        boss_fight_questions = []
        boss_fight_questions.extend(all_mcqs)
        boss_fight_questions.extend(all_riddles)

        # Shuffle and take the first 10
        import random
        random.shuffle(boss_fight_questions)
        game_content = boss_fight_questions[:10]

        if not game_content:
            success = False
            message = "Could not generate enough content for Boss Fight."

    else:
        success = False
        message = "Unknown game type or game under development."

    return jsonify({'success': success, 'message': message, 'content': game_content})

@app.route('/record_game_result', methods=['POST'])
def record_game_result():
    data = request.get_json()
    username = data.get('username')
    game_type = data.get('game_type')
    total_questions = data.get('total_questions')
    correct_answers = data.get('correct_answers')
    topic = data.get('topic', 'N/A') # Default to N/A if topic not provided

    if not all([username, game_type, total_questions is not None, correct_answers is not None]):
        return jsonify({'success': False, 'message': 'Missing data for game result.'}), 400

    game_history_db.append({
        'username': username,
        'game_type': game_type,
        'topic': topic,
        'total_questions': total_questions,
        'correct_answers': correct_answers,
        'timestamp': int(time.time())
    })

    # Update game attempts
    if username not in game_attempts_db:
        game_attempts_db[username] = {}
    if game_type not in game_attempts_db[username]:
        game_attempts_db[username][game_type] = {}
    
    # Use a combined key for game_type and topic for attempts
    game_attempts_db[username][game_type][topic] = game_attempts_db[username][game_type].get(topic, 0) + 1
    print(f"Recorded attempt for {username} on {game_type} ({topic}): {game_attempts_db[username][game_type][topic]} attempts")


    # Update perfect wins for rewards and Boss Fight unlock
    if correct_answers == total_questions and total_questions > 0: # Ensure it's a perfect score
        perfect_wins_db[username] = perfect_wins_db.get(username, 0) + 1
        print(f"User {username} achieved a perfect win! Total perfect wins: {perfect_wins_db[username]}")
    else:
        print(f"User {username} did not achieve a perfect win.")


    return jsonify({'success': True, 'message': 'Game result recorded successfully!'}), 200

@app.route('/get_user_history', methods=['GET'])
def get_user_history():
    username = request.args.get('username')
    if not username:
        return jsonify({'success': False, 'message': 'Username is required.'}), 400

    user_history = [record for record in game_history_db if record['username'] == username]
    # Sort by timestamp in descending order (most recent first)
    user_history.sort(key=lambda x: x['timestamp'], reverse=True)
    return jsonify({'success': True, 'history': user_history}), 200

@app.route('/check_boss_fight_status', methods=['POST'])
def check_boss_fight_status():
    data = request.get_json()
    username = data.get('username')

    if not username:
        return jsonify({'success': False, 'message': 'Username is required.'}), 400

    # Boss Fight unlocks after 2 perfect games
    required_perfect_wins = 2
    user_perfect_wins = perfect_wins_db.get(username, 0)
    is_unlocked = user_perfect_wins >= required_perfect_wins
    
    print(f"Boss Fight status for {username}: Unlocked={is_unlocked}, Perfect Wins={user_perfect_wins}")
    return jsonify({'success': True, 'is_unlocked': is_unlocked}), 200

@app.route('/get_game_attempts', methods=['POST'])
def get_game_attempts():
    data = request.get_json()
    username = data.get('username')
    game_type = data.get('game_type')
    topic = data.get('topic', 'N/A')

    if not all([username, game_type]):
        return jsonify({'success': False, 'message': 'Username and game type are required.'}), 400

    attempts = game_attempts_db.get(username, {}).get(game_type, {}).get(topic, 0)
    print(f"Attempts for {username}, {game_type}, {topic}: {attempts}")
    return jsonify({'success': True, 'attempts': attempts}), 200

@app.route('/get_user_perfect_wins', methods=['GET'])
def get_user_perfect_wins():
    username = request.args.get('username')
    if not username:
        return jsonify({'success': False, 'message': 'Username is required.'}), 400

    perfect_wins = perfect_wins_db.get(username, 0)
    print(f"Perfect wins for {username}: {perfect_wins}")
    return jsonify({'success': True, 'perfect_wins': perfect_wins}), 200


if __name__ == '__main__':
    app.run(debug=True)
