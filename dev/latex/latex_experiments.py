import os

def base_document(title="", author="Ethan Wang"):
    header=r"""
    \documentclass{article}
    \usepackage{amsmath,eso-pic,indentfirst,enumitem}
    \begin{document}""" + r"\title{" + title + r"}\author{" + author + r"""}
    \date{\today}
    \maketitle"""
    footer=r"\end{document}"
    return header, footer

class document(object):
    def __init__(self, filename, title="", generator = base_document):
        self.start, self.end = generator(title)
        self.main = []
        self.filename = filename

    def add(self, code):
        self.main.append(code)

    def compile(self, remove_aux=True):
        main = '\n\n'.join(self.main)
        doc = '\n'.join([self.start, main, self.end])
        tex_path = f"{self.filename}.tex"
        dir_name = os.path.dirname(tex_path) or "."
        base_name = os.path.basename(self.filename)
        tex_file = f"{dir_name}/{base_name}.tex"
        with open(tex_file, "w") as f:
            f.write(doc)
        os.system(f"cd {dir_name} && pdflatex {base_name}.tex")
        if remove_aux:
            os.remove(f"{dir_name}/{base_name}.aux")
            os.remove(f"{dir_name}/{base_name}.log")
        os.remove(tex_file)

sample=document("dev/latex/test", "Dynamics test(12 marks)")
sample.add(r"\section{Blocks(12 marks)}")
sample.add(r"\subsection{Question 1(4 marks)}")
sample.add(r"The diagram shows two blocks in contact on a smooth surface. A 48N force acts on block 1, and the surface can be considered frictionless. Calculate:")
sample.add(r"\vspace{1em}")
sample.add(r"\begin{enumerate}[label=(\alph*)]")
sample.add(r"\item The acceleration of the system")
sample.add(r"\item The acceleration of each block")
sample.add(r"\item The net force on each block")
sample.add(r"\item The contact forces for each block")
sample.add(r"\end{enumerate}")

sample.add(r"\section{Section 2(8 marks)}")
sample.add(r"This is another sample set.")
sample.add(r"\vspace{1em}")
sample.add(r"Behold, nested questions.")
sample.add(r"\begin{enumerate}")
sample.add(r"\item For each of the following, solve by completing the square(4 marks)")
sample.add(r"\begin{enumerate}[label=(\alph*)]")
sample.add(r"\item pretend i put a quadratic here")
sample.add(r"\item pretend i put a quadratic here")
sample.add(r"\item pretend i put a quadratic here")
sample.add(r"\item pretend i put a quadratic here")
sample.add(r"\end{enumerate}")
sample.add(r"\item For each of the following, solve using the quadratic formula(4 marks)")
sample.add(r"\begin{enumerate}[label=(\alph*)]")
sample.add(r"\item pretend i put a quadratic here")
sample.add(r"\item pretend i put a quadratic here")
sample.add(r"\item pretend i put a quadratic here")
sample.add(r"\item pretend i put a quadratic here")
sample.add(r"\end{enumerate}")
sample.add(r"\end{enumerate}")

sample.compile()