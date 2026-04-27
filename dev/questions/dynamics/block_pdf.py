import random
from blocks import generate_block_q
from latex_classes import Question, Section, document

random.seed(1)

sec = Section("Blocks")

for _ in range(10):
    qd = generate_block_q()
    q = Question(
        prompt=qd["question"],
        parts=qd["question_parts"],
        marks=qd["marks"],
        answers=qd["answer_parts"]
    )
    sec.add_question(q)

doc = document("dev/questions/dynamics/block_exam", "Dynamics Test")
doc.add_section(sec)
answer_doc = document("dev/questions/dynamics/block_exam_answers", "Dynamics Test Answers")
answer_doc.add_section(sec)

doc.compile(show_answers=False)
answer_doc.compile(show_answers=True)