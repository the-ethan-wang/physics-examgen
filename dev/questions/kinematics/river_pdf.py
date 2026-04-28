import random
from river import get_river_question
from latex_classes import Section, document

random.seed(1)

sec = Section("Riverboat")
sec.add_questions(get_river_question, 10)

doc = document("dev/questions/kinematics/river_exam", "River Test")
doc.add_section(sec)

answer_doc = document("dev/questions/kinematics/river_exam_answers", "River Test Answers")
answer_doc.add_section(sec)

doc.compile(show_answers=False)
answer_doc.compile(show_answers=True)