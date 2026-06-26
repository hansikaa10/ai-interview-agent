
import random

BANK = {

    "python": {

        "easy": [

            {
                "question": "What is a variable in Python?",
                "answer": "A variable is a named location used to store data values in a program."
            },

            {
                "question": "What is the difference between a list and a tuple?",
                "answer": "Lists are mutable while tuples are immutable."
            },

            {
                "question": "What is a dictionary in Python?",
                "answer": "A dictionary stores data as key-value pairs."
            }

        ],

        "medium": [

            {
                "question": "Explain data types in Python and how mutability works.",
                "answer": "Python has mutable and immutable data types. Mutable objects can be modified while immutable objects cannot."
            },

            {
                "question": "What are list comprehensions?",
                "answer": "List comprehensions provide a concise way to create lists using a single expression."
            }

        ],

        "hard": [

            {
                "question": "Explain Python memory management.",
                "answer": "Python manages memory automatically using reference counting and garbage collection."
            },

            {
                "question": "What are decorators?",
                "answer": "Decorators modify or extend the behavior of functions without changing their source code."
            }

        ]
    },

    "oop": {

        "easy": [

            {
                "question": "What is a class?",
                "answer": "A class is a blueprint used to create objects."
            },

            {
                "question": "What is an object?",
                "answer": "An object is an instance of a class containing data and methods."
            },

            {
                "question": "What is encapsulation?",
                "answer": "Encapsulation bundles data and methods together while restricting direct access."
            }

        ],

        "medium": [

            {
                "question": "What is inheritance?",
                "answer": "Inheritance allows one class to inherit properties and methods from another class."
            },

            {
                "question": "Explain polymorphism.",
                "answer": "Polymorphism allows the same interface to behave differently for different objects."
            }

        ],

        "hard": [

            {
                "question": "What are magic methods?",
                "answer": "Magic methods are special Python methods beginning and ending with double underscores."
            },

            {
                "question": "Explain method overriding.",
                "answer": "Method overriding allows a child class to provide its own implementation of a parent method."
            }

        ]
    },

    "loops": {

        "easy": [

            {
                "question": "What is a for loop?",
                "answer": "A for loop repeats code for each item in an iterable."
            },

            {
                "question": "What is a while loop?",
                "answer": "A while loop repeats while a condition remains true."
            }

        ],

        "medium": [

            {
                "question": "Difference between for and while loops?",
                "answer": "A for loop is generally used when the number of iterations is known, while a while loop runs until a condition becomes false."
            }

        ],

        "hard": [

            {
                "question": "Explain nested loops.",
                "answer": "Nested loops are loops placed inside another loop and are useful for multidimensional iteration."
            }

        ]
    },

    "functions": {

        "easy": [

            {
                "question": "What is a function?",
                "answer": "A function is a reusable block of code that performs a specific task."
            },

            {
                "question": "Why do we use functions?",
                "answer": "Functions improve code reuse, readability, and maintainability."
            },

            {
                "question": "What is a function parameter?",
                "answer": "A parameter is a variable defined in a function that receives input values."
            }

        ],

        "medium": [

            {
                "question": "Difference between return and print?",
                "answer": "Return sends a value back to the caller while print only displays output."
            },

            {
                "question": "What are *args and **kwargs?",
                "answer": "They allow functions to accept a variable number of positional and keyword arguments."
            }

        ],

        "hard": [

            {
                "question": "Explain the LEGB rule.",
                "answer": "LEGB stands for Local, Enclosing, Global and Built-in variable scope."
            },

            {
                "question": "Explain recursion.",
                "answer": "Recursion is when a function calls itself until a base condition is reached."
            }

        ]
    },

    "basics": {

        "easy": [

            {
                "question": "What is an expression?",
                "answer": "An expression is a piece of code that produces a value."
            },

            {
                "question": "What is a statement?",
                "answer": "A statement performs an action but does not necessarily produce a value."
            }

        ],

        "medium": [

            {
                "question": "Explain exception handling.",
                "answer": "Exception handling uses try and except blocks to catch and handle runtime errors."
            }

        ],

        "hard": [

            {
                "question": "What is the Global Interpreter Lock?",
                "answer": "The GIL allows only one thread to execute Python bytecode at a time."
            }

        ]
    }

}


def get_question(topic, difficulty):

    if topic not in BANK:
        topic = "basics"

    if difficulty not in BANK[topic]:
        difficulty = "easy"

    q = random.choice(BANK[topic][difficulty])

    return q["question"], q["answer"]

