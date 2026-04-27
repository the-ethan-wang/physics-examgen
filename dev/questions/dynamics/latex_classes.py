import os

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
    def __init__(self, title):
        self.title = title
        self.questions = []

    def add_question(self, q):
        self.questions.append(q)

    def to_latex(self, show_answers=False):
        out = [rf"\section*{{{self.title}}}"]
        for q in self.questions:
            out.append(q.to_latex(show_answers))
        return "\n\n".join(out)

class document(object):
    def __init__(self, filename, title="", generator=base_document):
        self.start, self.end = generator(title)
        self.sections = []
        self.filename = filename

    def add_section(self, section):
        self.sections.append(section)

    def compile(self, show_answers=False, remove_aux=True):
        main = "\n\n".join(section.to_latex(show_answers) for section in self.sections)
        doc = "\n".join([self.start, main, self.end])
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