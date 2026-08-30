class SentenceBuilder:
    def __init__(self):
        self.sentence = ""
        self.last_char = None
        
    def add_character(self, char: str):
        """
        Appends a character to the sentence.
        """
        if char and char != "nothing":
            self.sentence += char
            self.last_char = char
            
    def add_space(self):
        """Adds a space character to the sentence."""
        if not self.sentence.endswith(" "):
            self.sentence += " "
            self.last_char = " "
            
    def delete_last(self):
        """Removes the last character from the sentence."""
        if len(self.sentence) > 0:
            self.sentence = self.sentence[:-1]
            self.last_char = self.sentence[-1] if self.sentence else None
            
    def clear(self):
        """Clears the entire sentence buffer."""
        self.sentence = ""
        self.last_char = None
        
    def get_sentence(self) -> str:
        """Returns the current sentence."""
        return self.sentence
