from feanor import BaseBuilder

class Builder(BaseBuilder):
    def Setup(self):
        self.addDirectory("src")
        self.venv().install("pyinstaller")

    def Build(self):
        self.venv().runExecutable(f"pyinstaller --onefile src/pack.py")
        self.exportFolderContents("dist")
        self.exportFile("dist/pack.spec")
        