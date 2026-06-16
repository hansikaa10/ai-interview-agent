import random

BANK = {
    "basics": {
        "easy": ["What is a variable in Python?"],
        "medium": ["Explain data types in Python."],
        "hard": ["Explain Python memory management."]
    },
    "loops": {
        "easy": ["What is a for loop?"],
        "medium": ["Difference between for and while loop?"],
        "hard": ["Explain nested loops."]
    },
    "functions": {
        "easy": ["What is a function?"],
        "medium": ["return vs print difference?"],
        "hard": ["Explain scope in functions."]
    },
    "oop": {
        "easy": ["What is a class?"],
        "medium": ["What is inheritance?"],
        "hard": ["Explain polymorphism."]
    }
}

def get_question(topic, difficulty):
    return random.choice(BANK[topic][difficulty])