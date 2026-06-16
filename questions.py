import random

BANK = {

    "basics": {
        "easy": [
            "What is a variable in Python?",
            "What are data types in Python?",
            "What is a string?"
        ],

        "medium": [
            "Explain data types in Python.",
            "Difference between list and tuple?",
            "What is type casting?"
        ],

        "hard": [
            "Explain Python memory management.",
            "What is dynamic typing?",
            "Explain mutable vs immutable objects."
        ]
    },

    "loops": {
        "easy": [
            "What is a for loop?",
            "What is a while loop?"
        ],

        "medium": [
            "Difference between for and while loop?",
            "When would you use a while loop?"
        ],

        "hard": [
            "Explain nested loops with example.",
            "What is loop complexity?"
        ]
    },

    "functions": {
        "easy": [
            "What is a function?",
            "Why do we use functions?"
        ],

        "medium": [
            "return vs print difference?",
            "What are function arguments?"
        ],

        "hard": [
            "Explain scope in functions.",
            "Explain local vs global variables."
        ]
    },

    "oop": {
        "easy": [
            "What is a class?",
            "What is an object?"
        ],

        "medium": [
            "What is inheritance?",
            "Why is OOP useful?"
        ],

        "hard": [
            "Explain polymorphism.",
            "Explain abstraction."
        ]
    }
}


def get_question(topic, difficulty):
    return random.choice(BANK[topic][difficulty])