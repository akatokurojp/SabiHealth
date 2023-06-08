import sys
import nltk

TERMINALS = """
Adj -> "plenty" | "warm" | "over-the-counter" | "sore" | "humidifier" | "saline" | "nasal" | "sinus" | "face" | "pressure" | "decongestants" | "irritants" | "throat" | "fluids" | "hydration" | "cough" | "smoke" | "secondhand" | "irrigation" | "sprays" | "antihistamines" | "soup" | "voice" | "straining" | "lozenges" | "asthma" | "medications" | "inhalers" | "nebulizers" | "attacks" | "action" | "plan" | "triggers" | "symptoms" | "affected"
Adv -> "plenty" | "warm" | "over-the-counter" | "like"
N -> "sinuses" | "face" | "pressure" | "irritants" | "throat" | "fluids" | "hydration" | "cough" | "smoke" | "secondhand" | "irrigation" | "sprays" | "antihistamines" | "soup" | "voice" | "straining" | "lozenges" | "medications" | "inhalers" | "nebulizers" | "attacks" | "action" | "plan" | "triggers" | "symptoms" | "ear" | "objects" | "healthcare" | "professional" | "evaluation" | "treatment" | "you" | "saltwater" | "night"
P -> "to" | "for" | "at" | "like"
V -> "avoid" | "use" | "consult" | "drink" | "gargle" | "identify" | "take" | "follow" | "rest" | "maintain" | "apply" | "inserting" | "exposure" | "covering" | "need"
Det -> "the" | "your" | "a" | "good"
Conj -> "and" | "or"
"""




NONTERMINALS = """
S -> VP | VP P NP | VP Conj VP | VP Conj S | VP P NP Conj VP | NP VP
NP -> Det N | Det Adj N | Det N Conj NP | Det N | Det N PP | N 
VP -> V | V NP | V NP P NP | V NP P NP P NP | V NP P NP Conj VP | Det N | Det N PP | N
PP -> P NP
"""

def main():
    # Create the grammar and parser
    grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
    parser = nltk.ChartParser(grammar)

    # Example sentences
    sentences = [
        "You need to gargle saltwater at night.",
    ]

    for sentence in sentences:
        print("Sentence:", sentence)

        # Preprocess the sentence
        s = preprocess(sentence)

        # Parsing the sentence
        try:
            trees = list(parser.parse(s))
        except ValueError as e:
            print(e)
            continue

        if not trees:
            print("Could not parse sentence.")
            continue

        # Print each tree with noun phrase chunks
        for tree in trees:
            tree.pretty_print()

            # Print noun phrase chunks
            print("Noun Phrase Chunks:")
            np_chunks = get_np_chunks(tree)
            for np in np_chunks:
                print(" ".join(np.flatten()))

        print()  # Add a blank line between sentences


def preprocess(sentence):
    """
    Convert the sentence to a list of words.
    Preprocessing is done by converting the characters to lowercase
    and removing words that do not have at least 1 alphabetical character.
    """
    sentence = sentence.lower()
    tokens = nltk.word_tokenize(sentence)
    tokens = filter(lambda string: any(c.isalpha() for c in string), tokens)
    return tokens


def get_np_chunks(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as a subtree of the sentence tree
    with the label "NP" that does not contain
    another noun phrase chunk as its subtree.
    """
    chunks_list = []

    for subtree in tree.subtrees():
        if subtree.label() == 'NP' and not any(s.label() == 'NP' for s in subtree.subtrees(lambda t: t != subtree)):
            chunks_list.append(subtree)

    return chunks_list


if __name__ == "__main__":
    main()
