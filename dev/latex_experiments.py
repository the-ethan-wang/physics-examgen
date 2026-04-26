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

sample=document("dev/test", "Maths test 1(12 marks)", False)
sample.add(r"\section{Section 1(4 marks)}")
sample.add(r"Hello. This is a test line")
sample.add(r"\vspace{1em}")
sample.add(r"For each of the following: Convert to form $y = mx + b$ to find the gradient:")
sample.add(r"\begin{enumerate}")
sample.add(r"\item pretend i put a linear equation here")
sample.add(r"\item pretend i put a linear equation here")
sample.add(r"\item pretend i put a linear equation here")
sample.add(r"\item pretend i put a linear equation here")
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
sample.add(r"\item For each of the following, solve using the quadratic equation(4 marks)")
sample.add(r"\begin{enumerate}[label=(\alph*)]")
sample.add(r"\item pretend i put a quadratic here")
sample.add(r"\item pretend i put a quadratic here")
sample.add(r"\item pretend i put a quadratic here")
sample.add(r"\item pretend i put a quadratic here")
sample.add(r"\end{enumerate}")
sample.add(r"\end{enumerate}")

sample.compile()