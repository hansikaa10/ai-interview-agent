# questions.py
import random

BANK = {
    "python": {
        "easy": [
            "What is a variable in Python?",
            "What is the difference between a list and a tuple?"
        ],
        "medium": [
            "Explain data types in Python and how mutability works.",
            "What are list comprehensions and how do you use them?"
        ],
        "hard": [
            "Explain Python memory management, including garbage collection.",
            "What are decorators and how do you implement a custom one?"
        ]
    },
    "oop": {
        "easy": [
            "What is a class and an object?",
            "What is the basic definition of encapsulation?"
        ],
        "medium": [
            "What is inheritance and how do you use super()?",
            "Explain the difference between abstract classes and interfaces."
        ],
        "hard": [
            "Explain polymorphism and method overriding with a clean example.",
            "What are dunder (magic) methods in Python OOP?"
        ]
    },
    "basics": {
        "easy": ["What is an expression vs a statement?"],
        "medium": ["How does exception handling work using try-except blocks?"],
        "hard": ["Explain the global interpreter lock (GIL) in Python."]
    },
    "loops": {
        "easy": ["What is a for loop?"],
        "medium": ["What is the difference between a for loop and a while loop?"],
        "hard": ["Explain nested loops and how to break out of them cleanly."]
    },
    "functions": {
        "easy": ["What is a function parameter?"],
        "medium": ["What is the difference between return and print?", "What are *args and **kwargs?"],
        "hard": ["Explain variable scope (LEGB rule) inside nested functions."]
    }
}

def get_question(topic, difficulty):
    # Safe fallback if a topic or difficulty is missing during edge cases
    if topic not in BANK:
        topic = "basics"
    if difficulty not in BANK[topic]:
        difficulty = "easy"
        
    return random.choice(BANK[topic][difficulty])
