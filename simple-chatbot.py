import re
from datetime import datetime

class SimpleChatbot:
    def __init__(self):
        self.patterns = {
            r'\b(hi|hello|hey)\b': self.greet,
            r'\bhow are you\b': self.how_are_you,
            r'\btime\b': self.get_time,
            r'\b(bye|goodbye)\b': self.goodbye,
            r'\bweather\b': self.weather,
            r'\bname\b': self.name,
            r'\bhelp\b': self.help,
            r'\bthanks?\b': self.thanks
        }

    def process_input(self, user_input):
        # Convert input to lowercase for better matching
        user_input = user_input.lower().strip()
        
        # Check for empty input
        if not user_input:
            return "Please say something!"

        # Try to match input against patterns
        for pattern, func in self.patterns.items():
            if re.search(pattern, user_input):
                return func()

        # Default response if no pattern matches
        return self.default_response()

    def greet(self):
        import random
        greetings = [
            "Hello! How can I help you today?",
            "Hi there! Nice to meet you!",
            "Hey! What's on your mind?"
        ]
        return random.choice(greetings)

    def how_are_you(self):
        return "I'm doing well, thank you for asking! How about you?"

    def get_time(self):
        return f"The current time is {datetime.now().strftime('%H:%M')}"

    def goodbye(self):
        return "Goodbye! Have a great day!"

    def weather(self):
        return "I can't actually check the weather, but I can help you with other things!"

    def name(self):
        return "My name is ChatBot! Nice to meet you!"

    def help(self):
        return """I can help you with several things! Try asking me about:
- Time
- Basic greetings
- My name
Or just chat with me!"""

    def thanks(self):
        return "You're welcome! Let me know if you need anything else!"

    def default_response(self):
        import random
        responses = [
            "I'm not sure I understand. Could you rephrase that?",
            "Interesting! Tell me more about that.",
            "I'm still learning. Could you try asking something else?",
            "I'm not sure how to respond to that yet."
        ]
        return random.choice(responses)

def start_chat():
    bot = SimpleChatbot()
    print("ChatBot: Hello! Type 'bye' to exit.")
    
    while True:
        user_input = input("You: ")
        if user_input.lower().strip() == 'bye':
            print("ChatBot:", bot.goodbye())
            break
        
        response = bot.process_input(user_input)
        print("ChatBot:", response)

if __name__ == "__main__":
    start_chat()
