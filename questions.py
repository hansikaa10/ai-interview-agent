
import random

BANK = {
    "python": {
        "easy": [
            "What is a variable in Python?",
            "What is the difference between a list and a tuple?",
            "What is a dictionary in Python?",
            "What is the purpose of indentation in Python?",
            "What is the difference between == and = ?"
        ],
        "medium": [
            "Explain data types in Python and how mutability works.",
            "What are list comprehensions and how do you use them?",
            "Explain the difference between shallow copy and deep copy.",
            "What is exception handling in Python?",
            "What are Python modules and packages?"
        ],
        "hard": [
            "Explain Python memory management, including garbage collection.",
            "What are decorators and how do you implement a custom one?",
            "Explain generators and the yield keyword.",
            "What are context managers and why are they useful?",
            "Explain multithreading vs multiprocessing in Python."
        ]
    },

    "oop": {
        "easy": [
            "What is a class and an object?",
            "What is encapsulation?",
            "What is the purpose of a constructor?",
            "What is an instance variable?",
            "How do you create an object in Python?"
        ],
        "medium": [
            "What is inheritance and how do you use super()?",
            "Explain the difference between abstract classes and interfaces.",
            "What is method overriding?",
            "Explain polymorphism with an example.",
            "What is composition in OOP?"
        ],
        "hard": [
            "Explain polymorphism and method overriding with a clean example.",
            "What are dunder (magic) methods in Python OOP?",
            "Explain multiple inheritance and the Method Resolution Order (MRO).",
            "What is operator overloading?",
            "Explain SOLID principles in object-oriented programming."
        ]
    },

    "basics": {
        "easy": [
            "What is an expression versus a statement?",
            "What is a keyword in Python?",
            "What are comments used for?",
            "What is the difference between syntax errors and runtime errors?",
            "What is the purpose of input()?"
        ],
        "medium": [
            "How does exception handling work using try-except blocks?",
            "Explain the difference between mutable and immutable objects.",
            "What is variable scope in Python?",
            "What are lambda functions?",
            "Explain type casting."
        ],
        "hard": [
            "Explain the Global Interpreter Lock (GIL) in Python.",
            "What is monkey patching?",
            "Explain Python's object model.",
            "How does Python import modules internally?",
            "Explain reference counting."
        ]
    },

    "loops": {
        "easy": [
            "What is a for loop?",
            "What is a while loop?",
            "When would you use a loop?",
            "How do you stop a loop?",
            "What does the range() function do?"
        ],
        "medium": [
            "What is the difference between a for loop and a while loop?",
            "Explain break and continue with examples.",
            "What is loop nesting?",
            "How do you iterate through a dictionary?",
            "How do enumerate() and zip() simplify loops?"
        ],
        "hard": [
            "Explain nested loops and how to break out of them cleanly.",
            "Discuss the time complexity of nested loops.",
            "What are infinite loops and how can you avoid them?",
            "How do generator expressions work in loops?",
            "How would you optimize inefficient loops?"
        ]
    },

    "functions": {
        "easy": [
            "What is a function?",
            "What is a function parameter?",
            "What is a function argument?",
            "Why do we use functions?",
            "How do you call a function in Python?"
        ],
        "medium": [
            "What is the difference between return and print?",
            "What are *args and **kwargs?",
            "What are default arguments?",
            "Explain keyword arguments.",
            "Can a function return multiple values?"
        ],
        "hard": [
            "Explain variable scope (LEGB rule) inside nested functions.",
            "What are closures in Python?",
            "Explain recursion with an example.",
            "What are lambda functions?",
            "How do decorators work with functions?"
        ]
    }
}


def get_question(topic, difficulty):
    if topic not in BANK:
        topic = "basics"

    if difficulty not in BANK[topic]:
        difficulty = "easy"

    return random.choice(BANK[topic][difficulty])

