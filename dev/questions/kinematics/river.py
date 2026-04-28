
"""
Relative motion

2 types

Type 1:
Boat's heading is across the river relative to the water, but the river is flowing. Find the resultant vector, time taken, displacement, distance travelled up/downstream
Variables:
- boat speed relative to water
- river speed relative to stable ground
- width of river

- resultant vector
- time taken
- displacement
- distance travelled

Type 2:
Boat wants a resultant vector of perpendicular to the riverbank relative to stable ground(straight line path to opposite shore), but the river is flowing. Find the required angle and time taken to reach the opposite shore


More:
Water speed isn't NESW, at an angle
Water speed isn't a constant(a function of time))
Man wants to cross the river and reach a point x metres higher at the opposite side of the shore. He can swim at V_a and run on ground at V_b.
"""

import random
import math
from latex_classes import Question

NICE_MEDIUM_NUMBERS = list(range(1,11))+[12, 15, 16, 18, 20, 24, 25]
NICE_LARGE_NUMBERS = [67, 676767677, 2**16-1, 2**31-1, 314159265358979323846264338327950]

def generate_wonky_boat_tikz():
    return ""

def get_nice(size="S"):
    match size:
        case "S":
            return random.randint(1,10)
        case "M":
            return random.choice(NICE_MEDIUM_NUMBERS)
        case "L":
            return random.choice(NICE_LARGE_NUMBERS)
        case _:
            return get_nice()

def get_river_question() -> Question:
    qd = generate_river_q()
    q = Question(
        prompt=qd["question"]+"\n\n"+qd["diagram_data"]["tikz"],
        parts=qd["question_parts"],
        marks=qd["marks"],
        answers=qd["answer_parts"]
    )
    return q

def generate_river_q():
    question_base = "A ferry is crossing a river that is {0}m wide at a velocity of ${1}\\,\\mathrm{{m s^{{-2}}}}$ right relative to the water. However, the water is travelling at ${2}\\,\\mathrm{{m s^{{-2}}}}$ {3} relative to the ground. Calculate:"
    question_parts = [
        "The resultant velocity of the ferry relative to the ground",
        "The time taken to cross the river",
        "The displacement of the boat",
        "The vertical displacement of the boat"
    ]
    water_velocity = get_nice("S")
    ferry_velocity = get_nice("M")
    river_width = ferry_velocity*get_nice("S")

    filled_question = question_base.format(*[river_width, ferry_velocity, abs(water_velocity), "up" if water_velocity>0 else "down"])

    marks = 4
    mark_distribution = [1, 1, 1, 1]
    question_data = {
        "marks": marks,
        "mark_distribution": mark_distribution,

        "question": filled_question,
        "question_parts": question_parts,
        "diagram_data": {
            "river_width": river_width,
            "water_velocity": water_velocity,
            "ferry_velocity": ferry_velocity,
            "tikz": generate_wonky_boat_tikz()
        },
        
        "answer": None,
        "answer_parts": [

        ]
    }
    return question_data

def solve_river(river_width, water_velocity, ferry_velocity):
    # Solve river problems for resultant velocity, time taken to cross the river, displacement of boat, vertical displacement of boat
    resultant_velocity_magnitude = math.sqrt(water_velocity**2 + ferry_velocity**2)
    resultant_velocity_angle = math.degrees(math.atan(abs(water_velocity)/ferry_velocity))
    time_taken = river_width / ferry_velocity
    vertical_displacement = time_taken * water_velocity
    horizontal_displacement = river_width
    displacement_magnitude = math.sqrt(vertical_displacement**2 + horizontal_displacement**2)
    displacement_angle = resultant_velocity_angle

    return {
        "resultant_velocity_mag"
    }