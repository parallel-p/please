import base
class Statements(base.Base):
    LATEX = 0
    def __init__(self):
        super(Statements, self).__init__({
            Statements.LATEX : ["tex"]
        })

if __name__ == "__main__":
    p = Statements()
    print(p.extensions(Statements.ALL))
    print(p.extensions(Statements.LATEX))
