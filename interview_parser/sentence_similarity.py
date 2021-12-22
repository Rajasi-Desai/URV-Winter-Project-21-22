import spacy

# pip install spacy
# python -m spacy download en_core_web_lg
nlp = spacy.load("en_core_web_lg")


def compare_sentences(s1, s2):
    doc1 = nlp(s1)
    doc2 = nlp(s2)
    return doc1.similarity(doc2)
