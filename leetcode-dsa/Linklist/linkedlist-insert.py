class Node:
    def __init__(self,value):
        self.value = value
        self.next = None

class Linkedlist:
    def __init__(self):
        self.head = None

    def traverse(self):
        current = self.head
        while current is not None:
            print(current.value)
            current = current.next

    # Insert at the beginning
    def insert_at_head(self,value):
        new_node = Node(value)                  # Create new node
        new_node.next = self.head               # Point it to current head
        self.head = new_node                    # new node becomes the head

    # Insert at the end
    def insert_at_tail(self,value):
        new_node = Node(value)

        if self.head is None:                   # empty list - new node is the head
            self.head = new_node
            return
        
        current = self.head
        while current.next is not None:              # Walk to the last node
            current = current.next

        current.head = new_node

    # Insert after a specific value
    def insert_after(self,target,value):
        current = self.head

        while current is not None:
            if current.value == target:         # found the target node
                new_node = Node(value)
                new_node.next = current.next    # point new node to what comes after
                current.next = new_node          # point target to new node   
                return
            current = current.next

        print(f"{target} not found")

    def delete(self, value):
        # Case 1 — empty list
        if self.head is None:
            print("List is empty")
            return

        # Case 2 — delete the head
        if self.head.value == value:
            self.head = self.head.next   # second node becomes new head
            return

        # Case 3 — delete middle or tail
        current = self.head
        while current.next is not None:
            if current.next.value == value:       # found the node to delete
                current.next = current.next.next  # skip over it
                return
            current = current.next

        print(f"{value} not found")

ll = Linkedlist()

ll.insert_at_tail(10)
ll.insert_at_tail(20)
ll.insert_at_tail(30)
ll.insert_at_tail(40)

print("Original:")
ll.traverse()

ll.delete(20)
print("\nAfter deleting 20:")
ll.traverse()

ll.delete(10)
print("\nAfter deleting head 10:")
ll.traverse()

ll.delete(40)
print("\nAfter deleting tail 40:")
ll.traverse()