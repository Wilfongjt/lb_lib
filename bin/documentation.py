import settings
import _lib.git_commands
import _lib.git_script
import _lib.project_script
import _lib.utility_script
import _lib.lb_doc_comments
import _lib.lb_recorder

import lb_project

def main():
    git_commands.main_document()
    git_script.main_document()
    project_script.main_document()
    utility_script.main_document()
    lb_doc_comments.main_document()
    lb_recorder.main_document()

    lb_project.main_document()

if __name__ == "__main__":
    # execute as script
    main()