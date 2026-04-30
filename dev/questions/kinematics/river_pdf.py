import random
from river import get_river_question, get_straight_boat_question
from latex_classes import Section, document

random.seed(1)

sec = Section("Ferry travelling across a river")
sec.add_questions(get_river_question, 5)

sec2 = Section("Ferry travelling straight across a river")
sec2.add_questions(get_straight_boat_question, 5)

doc = document("dev/questions/kinematics/river_exam", "River Test")
doc.add_section(sec)
doc.add_section(sec2)

answer_doc = document("dev/questions/kinematics/river_exam_answers", "River Test Answers")
answer_doc.add_section(sec)
answer_doc.add_section(sec2)

doc.compile(show_answers=False)
answer_doc.compile(show_answers=True)