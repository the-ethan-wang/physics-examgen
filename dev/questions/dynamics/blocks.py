from pathlib import Path
import os
import json

from typing import Optional, Union
import random

NICE_MEDIUM_NUMBERS = list(range(1,11))+[12, 15, 16, 18, 20, 24, 25]
NICE_LARGE_NUMBERS = [67, 676767677, 2**16-1, 2**31-1, 314159265358979323846264338327950]

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

def generate_block_q():
    question_base = "The diagram shows {0} blocks in contact on a smooth surface. A {1}N force acts on block {2} from the {3}, and the surface can be considered frictionless. Calculate:"
    question_parts = [
        "The acceleration of the system",
        "The acceleration of each block",
        "The net force on each block",
        "The contact forces for each block"
    ]
    system_acceleration = get_nice()*random.choice([-1, 1])
    number_of_blocks = random.randint(2, 4)
    weights=[]
    net_forces=[]
    for _ in range(number_of_blocks):
        mass = get_nice("M")
        force = mass * system_acceleration
        weights.append(mass)
        net_forces.append(force)
    net_force = sum(weights) * system_acceleration
    block_exerted_on = 1 if net_force>0 else number_of_blocks
    dir_from = "left" if net_force>0 else "right"
    filled_question = question_base.format(*[number_of_blocks, abs(net_force), block_exerted_on, dir_from])

    marks = 6
    mark_distribution = [1, 1, 2, 2]
    acceleration_answer = f"The acceleration of the system is ${system_acceleration}\\,\\mathrm{{m s^{{-2}}}}$"
    each_acc_answer = f"Each block has an acceleration of ${system_acceleration}\\,\\mathrm{{m s^{{-2}}}}$"
    each_block_nf_base = "Block {0} has a net force of {1}N"
    each_block_net_force_answer = []
    for i, nf in enumerate(net_forces):
        this_block_ans = each_block_nf_base.format(i+1, nf)
        each_block_net_force_answer.append(this_block_ans)
    each_block_net_force_answer = "\n\n".join(each_block_net_force_answer)
    forces = block_forces(weights, net_force, system_acceleration)
    assert forces
    forces = forces["forces"]
    each_block_f_base = "{0} has {1} force{2} acting on it. They are: \n\n{3}"
    each_force_base = "{0}N {1}"
    each_block_forces_answer = []
    for force in forces:
        block_ans = each_block_f_base.format(force["name"], len(force["forces"]), "s" if len(force["forces"])!=1 else "", ", ".join([each_force_base.format(x[1],x[0]) for x in force["forces"]]))
        each_block_forces_answer.append(block_ans)
    each_block_forces_answer="\n\n".join(each_block_forces_answer)
    question_data = {
        "marks": marks,
        "mark_distribution": mark_distribution,

        "question": filled_question,
        "question_parts": question_parts,
        "diagram_data": { # TODO: Include a function for drawing the diagram in here, so the main class can call qd["diagram_data"]["generator"](qd["diagram_data"])
            "weights": weights,
            "net_force": net_force
        },
        
        "answer": None,
        "answer_parts": [
            acceleration_answer,
            each_acc_answer,
            each_block_net_force_answer,
            each_block_forces_answer
        ]
    }
    return question_data

def block_forces(weights: list[Union[float,int]], net_force: Optional[Union[float,int]], net_acceleration: Optional[Union[float,int]]):
    """Returns list of every force acting on each object. Assumes force is applied to the side of the weights."""
    for weight in weights:
        if weight<0:
            print("Weights must be non-negative.")
            return
        
    if len(weights)<1:
        print("Must include at least 1 block.")
        return

    total_mass=sum(weights)

    if net_acceleration is not None and net_force is not None:
        if net_force!=net_acceleration*total_mass:
            print("Net force conflicts with net acceleration")
            return
    elif net_acceleration is not None:
        net_force=net_acceleration*total_mass
    elif net_force is not None:
        net_acceleration=net_force/total_mass
    else:
        print("Not enough information")
        return
    
    ans={"forces": [], 'net acceleration': net_acceleration, 'net force': net_force}
    n=len(weights)
    net_forces=[net_acceleration*x for x in weights]
    contacts=[]
    for i in range(n - 1):
        right_mass=sum(weights[i+1:])
        contact_force=right_mass * net_acceleration
        contacts.append(contact_force)
    for i, weight in enumerate(weights):
        obj_net_force=net_forces[i]
        obj_data = {
            "name": f"Block {i+1}",
            "weight": weight,
            "forces": [],
            "net force": obj_net_force
        }
        if i==0:
            if net_force>=0:
                obj_data["forces"].append(["Applied Force", net_force])
                obj_data["forces"].append([f"Contact Force from block {i+2}", obj_net_force-net_force])
            else:
                obj_data["forces"].append([f"Contact Force from block {i+2}", obj_net_force])
        elif i==n-1:
            if net_force<0:
                obj_data["forces"].append(["Applied Force", net_force])
                obj_data["forces"].append([f"Contact Force from block {i}", obj_net_force-net_force])
            else:
                obj_data["forces"].append([f"Contact Force from block {i}", obj_net_force])
        else:
            obj_data["forces"].append([f"Contact Force from block {i}", -1*ans['forces'][i-1]['forces'][-1][1]]) # FIXME: HACK:
            obj_data["forces"].append([f"Contact Force from block {i+2}", obj_net_force-obj_data['forces'][0][1]])
        ans['forces'].append(obj_data)
    print(contacts)
    return ans

if __name__ == "__main__":
    a = generate_block_q()
    print(a)
    datapath = os.path.join(Path(__file__).resolve().parent, "blocks.json")
    with open(datapath, "w") as f:
        json.dump(a, f, indent=4)