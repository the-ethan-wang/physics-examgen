import random
from river import get_river_question, get_straight_boat_question
from latex_classes import Section, document

random.seed(1)

sec = Section("Ferry travelling across a river")
sec.add_questions(get_river_question, 5)

sec2 = Section("Ferry travelling straight across a river")
sec2.add_questions(get_straight_boat_question, 5)

doc = document(filename="dev/questions/kinematics/river_exam", title="River Test", solution_title="RAWERIHAWERHIAR")
doc.add_section(sec)
doc.add_section(sec2)

doc.compile(answer_pdf=False)
doc.compile(answer_pdf=True)