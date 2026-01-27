def make_coffee():
    print("Start Machine")
    print("Make Coffee")
    print("enjoy it")

print("Wake up")
make_coffee()
print("Working for a while")
make_coffee()

#Built-in Function (Just Calling)
print(len("Python"))

# Function from libraries (Import then Call)
import math
number = 4.2
print(math.ceil(number))

# User defined Function (Define then call)
def make_coffee():
    print("Start Machine")
    print("Make Coffee")
    print("enjoy it")

make_coffee()

def clean_name(name):
    print(name.strip().lower())

clean_name("  Maria  ")
