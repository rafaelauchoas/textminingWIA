import spacy
from spacy.matcher import PhraseMatcher

text = """I like tomtom and I cannot lie. In computer science, artificial intelligence (AI), sometimes called machine intelligence, is intelligence demonstrated by machines, unlike the natural intelligence displayed by humans and animals.  Leading AI textbooks define the field as the study of "intelligent agents": any device that perceives its  environment and takes actions that maximize its chance of successfully achieving its goals.[1] Colloquially,  the term "artificial intelligence" is often used to describe machines (or computers) that mimic "cognitive"  functions that humans associate with the human mind, such as "learning" and "problem solving".[2] """

nlp = spacy.load("en_core_web_sm")

phrase_matcher = PhraseMatcher(nlp.vocab)
phrases = ['omtom and I cannot', 'science, artificial intelligence (AI), sometimes called machine']
patterns = [nlp(text) for text in phrases]
phrase_matcher.add('AI', None, *patterns)

doc = nlp(text)

for sent in doc.sents:
    for match_id, start, end in phrase_matcher(nlp(sent.text)):
        if nlp.vocab.strings[match_id] in ["AI"]:
            print(sent.text)