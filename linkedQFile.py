from typing import Any

class Node():
    def __init__(self, value: Any) -> None:
        self.value: Any = value
        self.next: Any = None

    def __repr__(self):
        return f"{self.value}, [{self.next}]"

class Linked_Q():
    def __init__(self) -> None:
        self.__first: Node = None
        self.__last: Node = None
        self.__temp_first: Node = None
        self.__temp_last: Node = None
        self.switch: bool = True
        self.size: int = 0
    
    def __repr__(self) -> str:
        if self.__first is None:
            return "List is empty"
        output: list[str] = []
        node: Node = self.__first
        while node:
            output.append(str(node.value))
            node: Node = node.next
        return " ".join(output)

    def is_empty(self) -> bool:
        """Check if queue is empty"""
        return True if self.__first is None else False
    
    def enqueue(self, item: Any, mode: str = "D") -> None:
        """Add something to the back of the queue"""
        new_node: Node = Node(item)
        if mode == "D":
            if self.__last is not None:
                self.__last.next = new_node # Reference the new last node to the old last node, does that make sense..?
            if self.__first is None:
                self.__first: Node = new_node
            self.__last: Node = new_node
        else:
            if self.__temp_last is not None:
                self.__temp_last.next = new_node 
            if self.__temp_first is None:
                self.__temp_first: Node = new_node
            self.__temp_last: Node = new_node
        self.size += 1
    
    def peek(self) -> Any:
        """Return the first value of the queue"""
        return self.__first.value
            

    def dequeue(self) -> Any:
        """Remove something that sits in the front of the queue"""
        if self.is_empty():
            raise IndexError("Cannot dequeue an item from an empty 'list'")
        value: Any = self.__first.value
        self.__first: Node = self.__first.next  # next: Node
        if self.__first is None:  # 'next' is empty, aka list is empty
            self.__last = None
        self.size -= 1
        return value
    
    def remove(self, entry):
        """Cannot be first item"""
        current = self.__first
        outside = None
        while current:
            next = current.next
            if next:
                if next.value == entry and next.value != self.__first.value:
                    if next == self.__last.value:
                        self.__last = current
                    outside = next.next
                    current.next = outside
                    self.size -= 1
                    break
                current = current.next
            else:
                current = current.next
        
    def magic(self) -> None:
        """Does the magic trick of the century"""
        while self.__first != self.__last:
            val: Any = self.dequeue()
            self.enqueue(val, "Magic" if not self.switch else "D")
            self.switch = not self.switch
        self.enqueue(self.__first.value, "Magic")
        self.__first = self.__temp_first
        self.__last = self.__temp_last