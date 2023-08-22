


def main_path():
    import os
    from pathlib import Path

    print('home', Path().home())
    print('cwd ', Path().cwd())

    print('name', Path().name)
    print('stem', Path().stem)
    print('suffix', Path().suffix)
    print('anchor', Path().anchor)
    print('parent', Path().parent)

    print('file', Path(__file__))
    print('name', Path(__file__).name)
    print('stem', Path(__file__).stem)
    print('suffix', Path(__file__).suffix)
    print('anchor', Path(__file__).anchor)
    print('parent', Path(__file__).parent)
    print('parent.parent', Path(__file__).parent.parent)
    print('parts', Path(__file__).parts)

    class MPath(Path):
        def __init__(self, path_string):
            #super().__init__()
            self.development

    print('Mpath', MPath(os.getcwd()))

if __name__ == "__main__":
    # execute as script
    main_path()