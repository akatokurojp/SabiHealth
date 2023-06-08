from flask import Flask, render_template, request
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
import Sastrawi
from nltk.corpus import stopwords
import spacy
nlp = spacy.load('en_core_web_sm')
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

app = Flask(__name__)

class ChatBot:
    def __init__(self):
        self.bot_response = ""
        self.nlp = nlp

    def generate_bot_response(self, user_query):
        self.bot_response = "I'm sorry, I didn't understand. Could you please rephrase your query?"

        # Tokenization
        tokens = word_tokenize(user_query.lower())

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
        pos_tags = [(token.text, token.pos_) for token in self.nlp(user_query)]

        # Update the bot response based on user query
        if "diagnose" in user_query.lower():
            self.bot_response = "I'm sorry, but I cannot diagnose medical conditions. " \
                                "It's always best to consult with a qualified healthcare professional for an accurate diagnosis."
        elif "hi" in user_query.lower() or "hello" in user_query.lower():
            self.bot_response = "Hi welcome to sabi Health. This app is specifically designed for ENT use only (Ear Nose And Throat)." \
                                "\nType in How to heal 'insert symptomps here' to get a reply on how to heal your specific ENT Problem."\
                                "\nType in How to cure 'insert conditiions here' to get a suggestion on what is the most suitable medicine for your condition. \n do note you might need doctor prescription for heavier conditions."
        elif "list-symptomps" in user_query.lower():
            self.bot_response = "tinnitus\n" \
                                "bronkitis\n"\
                                "sinusitis\n"\
                                "rhinitis\n"
        elif "list-cure" in user_query.lower():
            self.bot_response = "headache\n" \
                                "fever\n"\
                                "cough\n"
        elif "heal" in user_query.lower() or "self-care" in user_query.lower():
            self.bot_response = self.get_self_healing_methods(user_query)
        elif "cure" in user_query.lower() or "medication" in user_query.lower():
            self.bot_response = self.get_medicine_options(user_query)

        return self.bot_response

    def get_self_healing_methods(self, user_query):
        symptoms = [token.text for token in self.nlp(user_query) if token.pos_ == "NOUN"]
        self_healing_methods = {
            "tinnitus": [
                "Avoid loud noises and use ear protection when necessary.",
                "Manage stress levels through relaxation techniques.",
                "Try background noise or soothing music to mask the tinnitus.",
                "Avoid caffeine and nicotine, as they can worsen tinnitus.",
                "Consult a healthcare professional for further evaluation and treatment."
            ],
            "otitis media": [
                "Keep the ear dry and avoid water exposure.",
                "Apply warm compresses to the affected ear.",
                "Use over-the-counter pain relievers like acetaminophen or ibuprofen.",
                "Avoid inserting objects into the ear.",
                "Consult a healthcare professional for further evaluation and treatment."
            ],
            "otitis eksterna": [
                "Keep the ear dry and avoid water exposure.",
                "Use ear drops prescribed by a healthcare professional.",
                "Apply warm compresses to the affected ear.",
                "Avoid inserting objects into the ear.",
                "Consult a healthcare professional for further evaluation and treatment."
            ],
            "tinnitus": [
                "Avoid loud noises and use ear protection when necessary.",
                "Manage stress levels through relaxation techniques.",
                "Try background noise or soothing music to mask the tinnitus.",
                "Avoid caffeine and nicotine, as they can worsen tinnitus.",
                "Consult a healthcare professional for further evaluation and treatment."
            ],
            "gangguan pendengaran": [
                "Avoid exposure to loud noises and use ear protection.",
                "Maintain good ear hygiene and avoid inserting objects into the ear.",
                "Follow a balanced diet rich in essential nutrients.",
                "Consider hearing aids or other assistive devices if necessary.",
                "Consult a healthcare professional for further evaluation and treatment."
            ],
            "infeksi saluran pernapasan": [
                "Get plenty of rest and drink fluids to stay hydrated.",
                "Use over-the-counter pain relievers and fever reducers if needed.",
                "Gargle with warm saltwater to soothe a sore throat.",
                "Use a humidifier to add moisture to the air.",
                "Consult a healthcare professional for further evaluation and treatment."
            ],
            "bronkitis": [
                "Get plenty of rest and drink fluids to stay hydrated.",
                "Use over-the-counter cough suppressants if needed.",
                "Avoid smoking and exposure to secondhand smoke.",
                "Use a humidifier to moisten the air.",
                "Consult a healthcare professional for further evaluation and treatment."
            ],
            "sinusitis": [
                "Use saline nasal irrigation to flush out the sinuses.",
                "Apply warm compresses to the face to relieve pain and pressure.",
                "Use over-the-counter decongestants if needed.",
                "Keep the nasal passages moist with a humidifier or steam inhalation.",
                "Consult a healthcare professional for further evaluation and treatment."
            ],
            "rhinitis": [
                "Avoid allergens and irritants that trigger symptoms.",
                "Use over-the-counter antihistamines or nasal sprays for relief.",
                "Keep the nasal passages clean with saline nasal rinses.",
                "Use a humidifier to add moisture to the air.",
                "Consult a healthcare professional for further evaluation and treatment."
            ],
            "faringitis": [
                "Gargle with warm saltwater to soothe a sore throat.",
                "Drink warm fluids like tea or soup to relieve discomfort.",
                "Use over-the-counter pain relievers if needed.",
                "Get plenty of rest and maintain good hydration.",
                "Consult a healthcare professional for further evaluation and treatment."
            ],
            "tonsilitis": [
                "Gargle with warm saltwater to soothe a sore throat.",
                "Use over-the-counter pain relievers if needed.",
                "Get plenty of rest and drink fluids to stay hydrated.",
                "Avoid irritants like smoke and spicy foods.",
                "Consult a healthcare professional for further evaluation and treatment."
            ],
            "laringitis": [
                "Rest your voice and avoid straining it.",
                "Drink warm fluids and use throat lozenges for relief.",
                "Avoid irritants like smoke and dry air.",
                "Use a humidifier to add moisture to the air.",
                "Consult a healthcare professional for further evaluation and treatment."
            ],
            "asma": [
                "Identify and avoid triggers that worsen your asthma symptoms.",
                "Take prescribed asthma medications as directed.",
                "Use inhalers or nebulizers for immediate relief during asthma attacks.",
                "Follow a written asthma action plan provided by a healthcare professional.",
                "Consult a healthcare professional for further evaluation and treatment."
            ]
        }


        self_healing_methods_found = [method for symptom in symptoms for method in self_healing_methods.get(symptom, [])]
        if self_healing_methods_found:
            self.bot_response = "Here are some self-healing methods for your symptoms:\n\n"
            self.bot_response += "\n".join(self_healing_methods_found)
        else:
            self.bot_response = "I'm sorry, I don't have self-healing methods for those symptoms."

        return self.bot_response

    def get_medicine_options(self, user_query):
        conditions = [token.text for token in self.nlp(user_query) if token.pos_ == "NOUN"]
        medicine_options = {
            "headache": [
                "Ibuprofen",
                "Acetaminophen",
                "Aspirin"
            ],
            "fever": [
                "Acetaminophen (Tylenol)",
                "Ibuprofen (Advil, Motrin)",
                "Naproxen (Aleve)"
            ],
            "cough": [
                "Dextromethorphan (Robitussin DM, Delsym)",
                "Guaifenesin (Mucinex, Robitussin)",
                "Codeine"
            ],
            "sore throat": [
                "Lozenges containing benzocaine or menthol",
                "Sprays containing phenol or benzocaine",
                "Acetaminophen or ibuprofen for pain relief"
            ],
            "congestion": [
                "Decongestant nasal sprays (e.g., Afrin)",
                "Oral decongestants (e.g., pseudoephedrine)",
                "Antihistamines with decongestant combination (e.g., Claritin-D)"
            ],
            "earache": [
                "Over-the-counter pain relievers (e.g., acetaminophen, ibuprofen)",
                "Ear drops for pain relief (e.g., benzocaine, hydrocortisone)",
                "Antibiotic ear drops (if prescribed by a healthcare professional)"
            ],
            "sinus headache": [
                "Decongestants (oral or nasal)",
                "Saline nasal sprays or rinses",
                "Pain relievers such as acetaminophen or ibuprofen"
            ],
            "postnasal drip": [
                "Decongestants to reduce nasal congestion",
                "Antihistamines to reduce mucus production",
                "Guaifenesin to thin and loosen mucus"
            ],
            "tonsillitis": [
                "Acetaminophen or ibuprofen for pain relief",
                "Antibiotics (if prescribed by a healthcare professional)",
                "Throat sprays or lozenges for temporary relief"
            ],
            "hoarseness": [
                "Voice rest and hydration",
                "Warm beverages or throat lozenges",
                "Prescription medications for underlying causes (if necessary)"
            ],
            "ear infection": [
                "Over-the-counter pain relievers (e.g., acetaminophen, ibuprofen)",
                "Antibiotics (if prescribed by a healthcare professional)",
                "Ear drops to relieve pain or treat infection (if prescribed)"
            ],
            "stuffy nose": [
                "Decongestant nasal sprays or drops",
                "Oral decongestants (e.g., pseudoephedrine)",
                "Saline nasal sprays or rinses"
            ],
            "swimmer's ear": [
                "Ear drops with acetic acid or alcohol to help dry the ear",
                "Pain relievers for discomfort",
                "Antibiotic ear drops (if prescribed by a healthcare professional)"
            ],
            "deviated septum": [
                "Nasal decongestants or nasal strips for temporary relief",
                "Saline nasal sprays or rinses",
                "Prescription medications or surgical options (if necessary)"
            ],
            "snoring": [
                "Anti-snoring devices or mouthpieces",
                "Nasal strips or dilators",
                "Lifestyle changes such as weight loss or sleeping position adjustment"
            ],
            "epistaxis (nosebleed)": [
                "Pinching the nostrils and leaning forward",
                "Nasal saline sprays or rinses",
                "Cauterization or nasal packing (for severe cases)"
            ],
            "laryngitis": [
                "Voice rest and hydration",
                "Warm beverages or throat lozenges",
                "Prescription medications for underlying causes (if necessary)"
            ],
            "earwax buildup": [
                "Over-the-counter ear drops for wax removal",
                "Ear irrigation kits for gentle flushing",
                "Consultation with a healthcare professional for removal"
            ]
        }


        medicine_options_found = [medicine for condition in conditions for medicine in medicine_options.get(condition, [])]
        if medicine_options_found:
            self.bot_response = "Here are some medicine options for your condition:\n\n"
            self.bot_response += "\n".join(medicine_options_found)
        else:
            self.bot_response = "I'm sorry, I don't have medicine options for that condition."

        return self.bot_response

@app.route('/analyze', methods=['POST'])
def analyze():
    bot_response = request.form.get('bot_response')
    
    # Tokenization
    tokens = word_tokenize(bot_response.lower())
    
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
    pos_tags = [(token.text, token.pos_) for token in nlp(bot_response)]
    
    # Prepare analysis results
    analysis = {
        'Tokenized': ', '.join(tokens),
        'Removed Punctuation': ', '.join(filtered_tokens),
        'Stemmed': ', '.join(stemmed_tokens),
        'Lemmatized': ', '.join(lemmatized_tokens),
        'Part-of-Speech Tagging': ', '.join([f'{token}/{pos}' for token, pos in pos_tags])
    }
    
    return {'analysis': analysis}

# Create an instance of ChatBot
chatbot = ChatBot()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_query = request.form['user_query']

    # Generate bot response
    bot_response = chatbot.generate_bot_response(user_query)

    return {'response': bot_response}

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
