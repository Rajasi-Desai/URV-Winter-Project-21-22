from interview_parser import sentence_similarity as ss
from interview_parser import voice_parsing as vp

import sys

asked_questions = [
    "did you see the red car drive by",
    "which direction was it going",
    "how fast was it going",
]


if __name__ == "__main__":
    filename = sys.argv[1]
    results = vp.parse(filename)
    sentences = [s["text"] for s in results]

    while "" in sentences:
        sentences.remove("")

    print(sentences)
    parsed_questions = list()
    interview = dict()
    question_counter = 0
    sentence_counter = 0
    for s in sentences:
        if (
            question_counter < len(asked_questions)
            and ss.compare_sentences(s, asked_questions[question_counter]) > 0.9
        ):
            parsed_questions.append(sentence_counter)
            question_counter += 1
        sentence_counter += 1

    q = -1
    for s in range(len(sentences)):
        if s in parsed_questions:
            q = s
            interview[sentences[q]] = []
        else:
            interview[sentences[q]].append(sentences[s])

    print(interview)
