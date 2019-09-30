
import collections


class Node:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.freq = 1
        self.prev = None
        self.next = None

# DLinkedList => Doubly-Linked-List


class DoublyLinkedList:
    def __init__(self):
        # naming convention for private member variables
        self._sentinel = Node(None, None)
        # '.next' points to head of linkedlist
        self._sentinel.next = self._sentinel
        # '.prev' points to tail of linkedlist
        self._sentinel.prev = self._sentinel
        self._size = 0

    def __len__(self):
        return self._size

    def append(self, node):
        # NOTE: append at tail of linked list
        node.next = self._sentinel
        node.prev = self._sentinel.prev
        node.next.prev = node
        node.prev.next = node
        self._size += 1

    def pop(self, node=None):
        # NOTE: popleft; pop from the head of the queue
        if self._size == 0:
            return
        if not node:
            node = self._sentinel.next

        node.prev.next = node.next
        node.next.prev = node.prev
        self._size -= 1
        return node

    # NOTE:not for popLeft version; below is for popRight
    # NOTE:below two functions are redundant
    # to show interviewer
    # combine these two functions into pop()
    # remove a node from the linked list
    # remove the last item in the linked list
    # Dont use these functions below
    def removeFromLinkedList(self, node):
        if not node:
            return
        node.prev.next = node.next
        node.next.prev = node.prev
        self._size -= 1
        return node

    def popTail(self):
        if self._size == 0:
            return
        # pointing to tail
        node = self.sentinel._prev

        node.prev.next = node.next
        node.next.prev = node.prev
        self._size -= 1

        # even if the linkedlist only has one element
        # would not require any checks bcos
        # it will just go back to the original form
        # i.e. during init
        return node
# NOTE: similar idea to LRU


# TWO dictionary
# dict 1) to store the frequency
#   - within each frequency the value is a linked list
#   - for those keys that have the same frequency
# dict 2) to store the number as key
#   - and the value-of-the-key pointing to node itself i.e. similar to memory pointer


class LFUCache:
    def __init__(self, capacity):
        self._size = 0
        self._capacity = capacity
        self._node = dict()
        self._freq = collections.defaultdict(DoublyLinkedList)

        self._minfreq = 0

    def _update(self, node):
        freq = node.freq
        self._freq[freq].pop(node)

        if self._minfreq == freq and not self._freq[freq]:
            self._minfreq += 1

        node.freq += 1
        self._freq[node.freq].append(node)

    def get(self, key):

        if key not in self._node:
            # key doesnt exist in the dict
            return -1
        node = self._node[key]
        self._update(node)
        return node.val

    def put(self, key, value):

        if self._capacity == 0:
            return
        if key in self._node:
            node = self._node[key]
            self._update(node)
            node.val = value
        else:  # key not in dict
            if self._size == self._capacity:
                node = self._freq[self._minfreq].pop()
                # remove the key from the dict
                del self._node[node.key]
                self._size -= 1

            node = Node(key, value)
            self._node[key] = node
            # new minimum key in the dict
            self._freq[1].append(node)
            # reset min freq
            self._minfreq = 1
            self._size += 1
