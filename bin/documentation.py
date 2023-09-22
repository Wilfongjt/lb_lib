import settings
import code.git_commands
import code.git_script
import code.project_script
import code.utility_script
import code.lb_doc_comments
import code.lb_recorder

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