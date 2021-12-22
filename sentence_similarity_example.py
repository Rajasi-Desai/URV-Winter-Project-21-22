import spacy

# pip install spacy
# python -m spacy download en_core_web_lg
nlp = spacy.load("en_core_web_lg")
# nlp = spacy.load("en_core_web_md")


doc1 = nlp(u"the person wear red T-shirt")
doc2 = nlp(u"this person is walking")
doc3 = nlp(u"the boy wear red T-shirt")


print(doc1.similarity(doc2))
print(doc1.similarity(doc3))
print(doc2.similarity(doc3))
