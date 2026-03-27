class Node:
    def __init__(self,value):
        self.value = value
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def traverse(self):
        current = self.head
        while current is not None:
            print(current.value)
            current = current.next

# Build the list
node1 = Node(10)
node2 = Node(20)
node3 = Node(30)

node1.next = node2
node2.next = node3

ll = LinkedList()
ll.head = node1

ll.traverse()

