import random
from blocks import get_block_question
from latex_classes import Section, document

random.seed(1)

sec = Section("Blocks")

sec.add_questions(get_block_question, 10)

doc = document("dev/questions/dynamics/block_exam", "Dynamics Test")
doc.add_section(sec)

answer_doc = document("dev/questions/dynamics/block_exam_answers", "Dynamics Test Answers")
answer_doc.add_section(sec)

doc.compile(show_answers=False)
answer_doc.compile(show_answers=True)