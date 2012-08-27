'''Classes representing information about test file.'''

class BaseTestFile:
    def __init__(self, desc):
        self.desc = desc

    def write(self, filename):
        '''Write a test to a given filename.'''
        raise NotImplementedError('Not supported for abstract test file')

class StrTestFile(BaseTestFile):
    def __init__(self, s, desc):
        self.str = str(s)
        super().__init__(desc)

    def write(self, filename):
        with open(filename, 'w') as f:
            f.write(self.str.replace(chr(13),''))


    def contents(self):
        return self.str

    def __eq__(self, other):
        return other == self.str

    def __hash__(self):
        return hash(self.str)

    def __repr__(self):
        return 'StrTestFile({!r}, {})'.format(self.str, self.desc)

class FileTestFile(BaseTestFile):
    import shutil

    def __init__(self, file, desc):
        self.filename = file
        super().__init__(desc)

    def write(self, filename):
        self.shutil.copy(self.filename, filename)

    def contents(self):
        with open(self.filename, 'r') as f:
            return f.read()

    def __eq__(self, other):
#        return samefile(self.filename, other.filename)
        return other == self.filename

    def __hash__(self):
        return hash(self.filename)

    def __repr__(self):
        return 'FileTestFile({})'.format(self.filename)
