import os
from typing import Callable, Optional

def base_document(title="", author="Ethan Wang"):
    header=r"""
    \documentclass[addpoints]{exam}
    \printanswers
    \usepackage{amsmath,eso-pic,indentfirst,enumitem,tikz,multicol}
    """ + r"\title{\vspace{-2cm}" + title + r"}\author{" + author + r"""}
    \date{\today}
    \begin{document}
    \maketitle
    \begin{questions}"""
    footer=r"""\end{questions}
    \end{document}"""
    return header, footer

class Question:
    def __init__(self, prompt, parts=None, marks=0, answers=None):
        self.prompt = prompt
        self.parts = parts or []
        self.marks = marks
        self.answers = answers or []

    def to_latex(self, show_answers=False):
        out = []
        out.append(rf"\question[{self.marks}] {self.prompt}")
        if self.parts:
            out.append(r"\begin{parts}")
            for i, p in enumerate(self.parts):
                out.append(rf"\part {p}")
                if show_answers and i < len(self.answers):
                    out.append(r"\begin{solution}")
                    out.append(self.answers[i])
                    out.append(r"\end{solution}")
            out.append(r"\end{parts}")
        return "\n".join(out)
    
class Section:
    def __init__(self, title, marks=0):
        self.title = title
        self.marks = marks
        self.questions = []

    def add_question(self, q):
        self.questions.append(q)
        self.marks += q.marks

    def add_questions(self, gen: Callable, count):
        for _ in range(count):
            q = gen()
            self.questions.append(q)
            self.marks += q.marks

    def to_latex(self, show_answers=False):
        out = [rf"\section*{{{self.title}({self.marks} points)}}"]
        for q in self.questions:
            out.append(q.to_latex(show_answers))
        return "\n\n".join(out)

class document(object):
    def __init__(self, filename: str, title="", solution_filename=None, solution_title=None, generator=base_document):
        self.start, self.end = generator(title)
        self.sections = []
        self.filename = filename
        self.title = title
        if solution_filename:
            self.solution_filename = solution_filename
        else:
            self.solution_filename = self.filename + "_answers"
        if solution_title:
            self.solution_title = solution_title
        else:
            self.solution_title = title + " answers"

    def change_title(self, newtitle):
        l_oldtex = self.start.split(r"\title{\vspace{-2cm}")
        l_oldtex2 = self.start.split(r"}\author{")
        newtex = l_oldtex[0] + r"\title{\vspace{-2cm}" + newtitle + r"}\author{" + l_oldtex2[1]
        self.start = newtex

    def add_section(self, section):
        self.sections.append(section)

    def compile(self, answer_pdf=False, remove_aux=True):
        if answer_pdf:
            self.change_title(self.solution_title)
        else:
            self.change_title(self.title)

        main = "\n\n".join(section.to_latex(answer_pdf) for section in self.sections)
        doc = "\n".join([self.start, main, self.end])
        if answer_pdf:
            tex_path = f"{self.solution_filename}.tex"
            dir_name = os.path.dirname(tex_path) or "."
            base_name = os.path.basename(self.solution_filename)
            tex_file = f"{dir_name}/{base_name}.tex"
        else:
            tex_path = f"{self.filename}.tex"
            dir_name = os.path.dirname(tex_path) or "."
            base_name = os.path.basename(self.filename)
            tex_file = f"{dir_name}/{base_name}.tex"

        with open(tex_file, "w") as f:
            f.write(doc)
        os.system(f"cd {dir_name} && pdflatex {base_name}.tex")
        if remove_aux:
            try:
                os.remove(f"{dir_name}/{base_name}.aux")
                os.remove(f"{dir_name}/{base_name}.log")
            except FileNotFoundError:
                pass
        os.remove(tex_file)