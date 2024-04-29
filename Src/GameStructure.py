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
    
    def to_array(self):
        array = []
        current = self.head
        while current:
            array.append(current.game)
            current = current.next
        return array

    def quick_sort(self):
        games_array = self.to_array()  # Convert linked list to array
        self._quick_sort_iterative(games_array)
        self._array_to_linked_list(games_array)  # Convert array back to linked list

    def _quick_sort_iterative(self, arr):
        stack = [(0, len(arr) - 1)]

        while stack:
            start, end = stack.pop()
            pIndex = self._partition_array(arr, start, end)

            if pIndex - 1 > start:
                stack.append((start, pIndex - 1))
            if pIndex + 1 < end:
                stack.append((pIndex + 1, end))

    def _partition_array(self, arr, start, end):
        pivot = arr[end]
        pIndex = start
        for i in range(start, end):
            if arr[i].name <= pivot.name:
                arr[i], arr[pIndex] = arr[pIndex], arr[i]
                pIndex += 1
        arr[pIndex], arr[end] = arr[end], arr[pIndex]
        return pIndex

    def _array_to_linked_list(self, arr):
        self.head = None
        self.tail = None
        for game in arr:
            self.append(game)
    
    
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


    # Helper function to get a node at a specific index
    def _get_node(self, index):
        current = self.head
        for _ in range(index):
            current = current.next
        return current
    
    def print_first_five(self):
        current = self.head
        count = 0
        while current and count < 5:
            game = current.game
            print(f"{game.game_id}, {game.name}, {game.user_rating}, {game.rating_count}, {game.developer}, {game.size}")
            current = current.next
            count += 1

    def get_game_by_index(self, index):
        current = self.head
        for _ in range(index):
            if current is None:
                return None
            current = current.next
        return current.game if current else None

    

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
def measure_search_time(linked_list, search_key, binary_search=False):
    start_time = time.perf_counter()
    if binary_search:
        index = linked_list.binary_search(search_key)
    else:
        result = linked_list.linear_search(search_key)
        index = None
    end_time = time.perf_counter()
    return end_time - start_time, index


# Helper function to iterate through linked list
def iter(linked_list):
    current = linked_list.head
    while current:
        yield current
        current = current.next

def total_time_linear_searches(linked_list, search_keys):
    total_time = 0
    for key in search_keys:
        start = time.perf_counter()
        linked_list.linear_search(key)
        end = time.perf_counter()
        total_time += (end - start)
    return total_time

def total_time_sort_and_binary_searches(linked_list, search_keys):
    # Sort the list once
    start = time.perf_counter()
    linked_list.quick_sort()
    end = time.perf_counter()
    sort_time = end - start

    # Perform binary searches
    binary_search_time = 0
    for key in search_keys:
        start = time.perf_counter()
        linked_list.binary_search(key)
        end = time.perf_counter()
        binary_search_time += (end - start)

    return sort_time + binary_search_time


all_game_ids = [node.game.game_id for node in iter(games_list)]
random_id = random.choice(all_game_ids)
search_time, found_game = measure_search_time(games_list, random_id)
found_game = games_list.linear_search(random_id)

def find_breakpoint_m(linked_list, max_m=100):
    m = 1
    while m <= max_m:
        search_keys = [random.choice(all_game_ids) for _ in range(m)]
        linear_time = total_time_linear_searches(linked_list, search_keys)
        sort_and_binary_time = total_time_sort_and_binary_searches(linked_list, search_keys)

        print(f"Checking for m={m}: Linear Time = {linear_time}, Sort+Binary Time = {sort_and_binary_time}")  # For debugging

        if linear_time > sort_and_binary_time:
            return m
        m += 1

    return -1  # Indicates no breakpoint found within the specified range


breakpoint_m = find_breakpoint_m(games_list)

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

#start_time = time.perf_counter()
#games_list.insertion_sort()
#end_time = time.perf_counter()
#print(f"Insertion Sort Time: {end_time - start_time} seconds")

#start_time = time.perf_counter()
#games_list.quick_sort()
#end_time = time.perf_counter()
#print(f"Quick Sort Time: {end_time - start_time} seconds")



# Print first five elements before sorting
print(f"Number of elements in LinkedList: {len(all_game_ids)}")
print("*** Linear Search Test ***\nBefore sorting:")
games_list.print_first_five()

# Perform three linear searches
for i in range(1, 4):
    random_id = random.choice(all_game_ids)
    search_time, found_game = measure_search_time(games_list, random_id)
    found_game = games_list.linear_search(random_id)
    if found_game:
        print(f"Search number {i}:")
        print(f"Searching for {found_game.name}...")
        print(f"Single search time: {search_time} seconds.")
        print(f"Average search time: {search_time / len(all_game_ids)} seconds.\n")

# Sort the list
start_time = time.perf_counter()
games_list.quick_sort()
end_time = time.perf_counter()
quick_sort_time = end_time - start_time
print(f"Time for quick sort: {quick_sort_time} seconds")
start_time = time.perf_counter()
games_list.insertion_sort()
end_time = time.perf_counter()
insertion_sort_time = end_time - start_time
print(f"Time for quick sort: {insertion_sort_time} seconds")


# Print first five elements after sorting
print("After sorting:")
games_list.print_first_five()



print("*** Binary Search Test ***")
# Perform three binary searches
print("*** Binary Search Test ***")
for i in range(1, 4):
    random_id = random.choice(all_game_ids)
    search_time, index = measure_search_time(games_list, random_id, True)
    if index is not None:
        found_game = games_list.get_game_by_index(index)
        print(f"Search number {i} (Binary):")
        print(f"Searching for {found_game.name}...")
        print(f"Single search time: {search_time} seconds.")
        print(f"Average search time: {search_time / len(all_game_ids)} seconds.\n")


print(f"Break point m = {breakpoint_m} between repeated linear searches and sort-once & multiple binary searches.")

