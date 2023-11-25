class UnmergedKeyException(Exception):
    pass

class UnhandledMergeKeysException(Exception):
    pass

class UninitializedDataException(Exception):
    pass

class UninitializedContextException(Exception):
    pass
class FolderNotFoundException(Exception):
    pass
class BadFolderNameException(Exception):
    pass
class FolderAlreadyExistsException(Exception):
    pass

#class OverwriteOfFolderExeception(Exception):
#    pass
class SubfolderCopyException(Exception):
    pass
class FileNotFoundException(Exception):
    pass
class BadFileNameException(Exception):
    pass

def main_document():
    from dep.pylyttlebit.lb_doc_comments import LbDocComments
    print('lb_exceptions')
    folder = '/'.join(str(__file__).split('/')[0:-1])
    filename = str(__file__).split('/')[-1]
    LbDocComments().setFolder(folder).setFilename(filename).open().save()

def main():
    print('no main for lb_exceptions')
if __name__ == "__main__":
    # execute as script
    main()
    # unittest.main()