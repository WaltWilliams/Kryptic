from Node import Node


class EnDecryptWheel:
    def __init__(self):
        self.head = None

    def build_list(self):
        # Starting values.
        letter = "A"
        number = 0
        # Starting with the first node.
        a_node = Node(letter, number)
        # Setting head and mobile (roving) pointers.
        rover = a_node
        self.head = rover
        # Incrementing the 2 values for the next added node before going into the while loop.
        number += 1
        letter = chr(ord(letter) + 1)
        # Adding a node for each letter.
        while number != 26:
            a_node = Node(letter, number)
            rover.next = a_node
            rover = rover.next
            # Incrementing the 2 values for the next added node.
            number += 1
            letter = chr(ord(letter) + 1)
        # Making it circular
        rover.next = self.head

    def increment(self):
        rover = self.head
        rover = rover.next
        return rover.letter

    def find_letter(self, char):
        count = 0
        rover = self.head
        while count != char:
            rover = rover.next
            count += 1
        return rover.letter

    def find_letter_number(self, letter):
        rover = self.head
        while rover.letter != letter:
            n = rover.number
            l = rover.letter
            rover = rover.next
        return rover.number

    def change_letter_encrypt(self, msg_letter, pad_letter):
        m = self.find_letter_number(msg_letter)
        p = self.find_letter_number(pad_letter)
        if (m + p) < 26:
            new_letter = self.find_letter(m + p)
        else:
            new_letter = self.find_letter(m + p - 26)
        return new_letter

    def change_letter_decrypt(self, msg_letter, pad_letter):
        m = self.find_letter_number(msg_letter)
        p = self.find_letter_number(pad_letter)
        letter = self.find_letter((m-p)%26)
        return letter