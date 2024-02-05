import csv
import random
import time

# Game class
class Game:
    # Constructor
    def __init__(self, game_id, name, user_rating, rating_count, developer, size):
        self.game_id = game_id
        self.name = name
        self.user_rating = user_rating
        self.rating_count = rating_count
        self.developer = developer
        self.size = size

# Game Linked List Node
class ListNode:
    # Constructor
    def __init__(self, game):
        self.game = game
        self.next = None
        self.prev = None

# Game Linked List
class gamesLinkedList:
    # Constructor
    def __init__(self):
        self.head = None
        self.tail = None

    # Append to list
    def append(self, game):
        new_node = ListNode(game)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    # Linear Search Method
    def linear_search(self, search_id):
        current = self.head
        while current:
            if current.game.game_id == search_id:
                return current.game
            current = current.next
        return None
    
    def binary_search(self, search_id):
        start = 0
        end = len(all_game_ids) - 1
        while start <= end:
            mid = (start + end) // 2
            if all_game_ids[mid] == search_id:
                return mid
            elif all_game_ids[mid] < search_id:
                start = mid + 1
            else:
                end = mid - 1
        return None
    
    # Helper function to swap two nodes
    def _swap_nodes(self, node1, node2):
        temp = node1.game
        node1.game = node2.game
        node2.game = temp

    # Insertion Sort
    def insertion_sort(self):
        if self.head is None:
            return

        current = self.head.next
        while current:
            key = current.game
            j = current.prev
            while j is not None and j.game.name > key.name:
                self._swap_nodes(j, j.next)
                j = j.prev
            current = current.next

    # Partition function for Quick Sort
    def _partition(self, low, high):
        pivot = high.game
        i = low.prev
        j = low
        while j != high:
            if j.game.name <= pivot.name:
                i = low if i is None else i.next
                self._swap_nodes(i, j)
            j = j.next
        i = low if i is None else i.next
        self._swap_nodes(i, high)
        return i

    # Quick Sort function
    def quick_sort(self):
        def partition(start, end):
            pivot = self._get_node(end).game
            pIndex = start
            for i in range(start, end):
                if self._get_node(i).game.name <= pivot.name:
                    self._swap_nodes(self._get_node(i), self._get_node(pIndex))
                    pIndex += 1
            self._swap_nodes(self._get_node(pIndex), self._get_node(end))
            return pIndex

        size = len(all_game_ids)
        stack = [(0, size - 1)]

        while stack:
            start, end = stack.pop()
            pIndex = partition(start, end)

            if pIndex - 1 > start:
                stack.append((start, pIndex - 1))
            if pIndex + 1 < end:
                stack.append((pIndex + 1, end))

    # Helper function to get a node at a specific index
    def _get_node(self, index):
        current = self.head
        for _ in range(index):
            current = current.next
        return current

# Read CSV and populate list
def read_csv_and_populate_list(file_name):
    games_list = gamesLinkedList()
    with open(file_name, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for row in csv_reader:
            game = Game(row[0], row[1], float(row[2]), int(row[3]), row[4], float(row[5]))
            games_list.append(game)
    return games_list

games_list = read_csv_and_populate_list('games.csv')


# Measure Linear Search Time
def measure_search_time(linked_list, search_key):
    start_time = time.perf_counter()
    result = linked_list.linear_search(search_key)
    end_time = time.perf_counter()
    return end_time - start_time, result

# Helper function to iterate through linked list
def iter(linked_list):
    current = linked_list.head
    while current:
        yield current
        current = current.next


all_game_ids = [node.game.game_id for node in iter(games_list)]
random_id = random.choice(all_game_ids)
search_time, found_game = measure_search_time(games_list, random_id)
found_game = games_list.linear_search(random_id)
if found_game is not None:
    print(f"Number of elements in list: {len(all_game_ids)}")
    print(f"*** Linear Search Test Before Sorting ***")
    print(f"Game ID: {found_game.game_id}")
    print(f"Name: {found_game.name}")
    print(f"Developer: {found_game.developer}")
    print(f"Size: {found_game.size} Bytes")
    print(f"Average User Rating: {found_game.user_rating}")
    print(f"User Rating Count: {found_game.rating_count}")
    print(f"Single Search Time: {search_time} seconds")
    print(f"Avg. Search Time: {search_time / len(all_game_ids)} seconds\n")
else:
    print('Game not found')

start_time = time.perf_counter()
games_list.insertion_sort()
end_time = time.perf_counter()
print(f"Insertion Sort Time: {end_time - start_time} seconds")

start_time = time.perf_counter()
games_list.quick_sort()
end_time = time.perf_counter()
print(f"Quick Sort Time: {end_time - start_time} seconds")


all_game_ids = [node.game.game_id for node in iter(games_list)]
random_id = random.choice(all_game_ids)
search_time, found_game = measure_search_time(games_list, random_id)
found_game = games_list.binary_search(random_id)
if found_game is not None:
    print(f"Number of elements in list: {len(all_game_ids)}")
    print(f"*** Binary Search Test After Sorting ***")
    print(f"Game ID: {found_game.game_id}")
    print(f"Name: {found_game.name}")
    print(f"Developer: {found_game.developer}")
    print(f"Size: {found_game.size} Bytes")
    print(f"Average User Rating: {found_game.user_rating}")
    print(f"User Rating Count: {found_game.rating_count}")
    print(f"Single Search Time: {search_time} seconds")
    print(f"Avg. Search Time: {search_time / len(all_game_ids)} seconds\n")
else:
    print('Game not found')