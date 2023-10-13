
class Stack(list):
    def push(self,value):
        self.append(value)
        return self
    def peek(self):
        return self[-1]
    def size(self):
        return len(self)

def main():
    actual = Stack()
    assert (actual == [])

if __name__ == "__main__":
    # execute as script
    main()