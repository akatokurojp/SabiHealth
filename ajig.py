import tkinter as tk
from tkinter import scrolledtext, messagebox
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
import spacy
nlp = spacy.load('en_core_web_sm')


class ChatBot:
    def __init__(self):
        self.bot_response = ""
        self.nlp=nlp

    def generate_bot_response(self, user_query):
        self.bot_response = "I'm sorry, I didn't understand. Could you please rephrase your query?"

        # Tokenization
        tokens = word_tokenize(self.bot_response.lower())

        # Remove punctuation marks
        tokens = [token for token in tokens if token.isalnum()]

        # Stop Words Removal
        stop_words = set(stopwords.words("english"))
        filtered_tokens = [token for token in tokens if token not in stop_words]

        # Stemming
        stemmer = PorterStemmer()
        stemmed_tokens = [stemmer.stem(token) for token in filtered_tokens]

        # Lemmatization
        lemmatizer = WordNetLemmatizer()
        lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]

        # Part-of-Speech Tagging
        pos_tags = [(token.text, token.pos_) for token in nlp(self.bot_response)]

        if "unique recipe" in user_query.lower():
            self.bot_response = "Sure! Here's a unique recipe for you: ..."
        elif "ingredients" in user_query.lower():
            self.bot_response = "The ingredients for the recipe are: ..."
        elif "another recipe" in user_query.lower():
            self.bot_response = "Here's another recipe for you: ..."
        elif "diagnose" in user_query.lower():
            self.bot_response = "I'm sorry, but I cannot diagnose medical conditions. " \
                                "It's always best to consult with a qualified healthcare professional for an accurate diagnosis."
        elif "heal" in user_query.lower() or "self-care" in user_query.lower():
            self.bot_response = self.bot_response = self.get_self_healing_methods(user_query)
        elif "cure" in user_query.lower() or "medication" in user_query.lower():
            self.bot_response = self.bot_response = self.get_medicine_options(user_query)

        return self.bot_response

    def get_self_healing_methods(self, user_query):
        symptoms = [token.text for token in self.nlp(user_query) if token.pos_ == "NOUN"]
        self_healing_methods = {
            "sore throat": [
                "You need to gargle warm saltwater."
                "You need to drink warm liquids like tea or soup."
                "You need to suck throat lozenges."
                "You need to avoid irritants like smoke or dry air."
                "You need to get plenty of rest."
            ],
            "congestion": [
                "Use a humidifier to add moisture to the air",
                "Try nasal saline irrigation",
                "Use over-the-counter decongestants",
                "Apply a warm compress to your face",
                "Elevate your head while sleeping"
            ],
            "headache": [
                "Take a break and rest in a quiet, dark room",
                "Apply a cold or warm compress to your forehead",
                "Drink plenty of water",
                "Try relaxation techniques such as deep breathing or meditation",
                "Avoid triggers such as bright lights or loud noises"
            ],
            "cough": [
                "Drink warm fluids like herbal tea or warm water with honey",
                "Use a humidifier to add moisture to the air",
                "Try over-the-counter cough suppressants",
                "Avoid irritants like smoke or strong odors",
                "Get plenty of rest"
            ],
            "earache": [
                "Apply a warm compress to the affected ear",
                "Use over-the-counter pain relievers like acetaminophen or ibuprofen",
                "Avoid exposure to cold temperatures or drafts",
                "Try using over-the-counter ear drops",
                "Rest and avoid activities that can worsen the pain"
            ]
        }
        methods = self_healing_methods.get(" ".join(symptoms).lower(), [])
        methods = "\n".join(methods[:5])  # Limit the methods to 5
        if methods:
            return f"If you're experiencing {' '.join(symptoms)}, here are some self-healing methods you can try:\n\n{methods}"
        else:
            return "I apologize, but I couldn't find self-healing methods for the symptoms you mentioned."

    def get_medicine_options(self, user_query):
        symptoms = [token.text for token in self.nlp(user_query) if token.pos_ == "NOUN"]
        medicine_options = {
            "sore throat": [
                "Throat lozenges",
                "Pain relievers (e.g., acetaminophen, ibuprofen)",
                "Antibiotics (if prescribed by a healthcare professional)"
            ],
            "congestion": [
                "Decongestants",
                "Nasal sprays (e.g., saline nasal sprays)",
                "Antihistamines"
            ],
            "headache": [
                "Pain relievers (e.g., acetaminophen, ibuprofen)",
                "Anti-inflammatory drugs",
                "Prescription migraine medications (if prescribed by a healthcare professional)"
            ],
            "cough": [
                "Cough suppressants",
                "Expectorants",
                "Antihistamines (for cough caused by allergies)"
            ],
            "earache": [
                "Pain relievers (e.g., acetaminophen, ibuprofen)",
                "Ear drops",
                "Antibiotics (if prescribed by a healthcare professional)"
            ]
        }
        options = medicine_options.get(" ".join(symptoms).lower(), [])
        options = "\n".join(options)
        if options:
            return f"If you're experiencing {' '.join(symptoms)}, here are some medicine options you can consider:\n\n{options}"
        else:
            return "I apologize, but I couldn't find medicine options for the symptoms you mentioned."
# Create an instance of the ChatBot
chatbot = ChatBot()


# Function to open the window for displaying analysis
def open_analysis_window():
    user_input = user_entry.get()
    if user_input.strip() != "":
        bot_response = chatbot.generate_bot_response(user_input)

        analysis_window = tk.Toplevel(root)
        analysis_window.title("Analysis")

        # Analyzed Text
        analyzed_text = scrolledtext.ScrolledText(analysis_window, width=60, height=20)
        analyzed_text.insert(tk.INSERT, "Bot Response:\n\n")
        analyzed_text.insert(tk.INSERT, "User Query: " + user_input + "\n\n")
        analyzed_text.insert(tk.INSERT, "Bot Response: " + bot_response + "\n\n")

        # Tokenization
        tokens = word_tokenize(bot_response.lower())
        tokens = [token for token in tokens if token.isalnum()]
        analyzed_text.insert(tk.INSERT, "Tokenized: " + str(tokens) + "\n\n")

        # Stop Words Removal
        stop_words = set(stopwords.words("english"))
        filtered_tokens = [token for token in tokens if token not in stop_words]
        analyzed_text.insert(tk.INSERT, "Removed Stop Words: " + str(filtered_tokens) + "\n\n")

        # Stemming
        stemmer = PorterStemmer()
        stemmed_tokens = [stemmer.stem(token) for token in filtered_tokens]
        analyzed_text.insert(tk.INSERT, "Stemmed: " + str(stemmed_tokens) + "\n\n")

        # Lemmatization
        lemmatizer = WordNetLemmatizer()
        lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]
        analyzed_text.insert(tk.INSERT, "Lemmatized: " + str(lemmatized_tokens) + "\n\n")

        # Part-of-Speech Tagging
        pos_tags = [(token.text, token.pos_) for token in nlp(bot_response)]
        analyzed_text.insert(tk.INSERT, "Part-of-Speech Tagging:\n")
        for token, pos in pos_tags:
            analyzed_text.insert(tk.INSERT, f"{token} - {pos}\n")
        analyzed_text.config(state=tk.DISABLED)
        analyzed_text.pack(pady=10)

        analyzed_text.config(state=tk.DISABLED)
        analyzed_text.pack(pady=10)

    else:
        messagebox.showinfo("Error", "Please enter a message.")


# Function to send a user message and get a bot response
def send_message():
    user_input = user_entry.get()
    if user_input.strip() != "":
        chat_log.config(state=tk.NORMAL)
        chat_log.insert(tk.END, "User: " + user_input + "\n", "user")
        bot_response = chatbot.generate_bot_response(user_input)
        chat_log.insert(tk.END, "Bot: " + bot_response + "\n", "bot")
        chat_log.config(state=tk.DISABLED)
        chat_log.see(tk.END)
        user_entry.delete(0, tk.END)
    else:
        messagebox.showinfo("Error", "Please enter a message.")


# Create the main GUI window
root = tk.Tk()
root.title("ChatBot")
root.geometry("500x400")

# Chat Log
chat_log = scrolledtext.ScrolledText(root, width=60, height=20)
chat_log.config(state=tk.DISABLED)
chat_log.tag_config("user", foreground="blue")
chat_log.tag_config("bot", foreground="green")
chat_log.pack(pady=10)

# User Input
user_entry = tk.Entry(root, width=40)
user_entry.pack(pady=5)

# Send Button
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(pady=5)

# Analysis Button
analysis_button = tk.Button(root, text="View Analysis", command=open_analysis_window)
analysis_button.pack(pady=5)

# Run the GUI main loop
root.mainloop()
