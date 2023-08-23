import settings
import lb_constants
import lb_dev_env
import lb_doc_comments
import lb_doc_folders
import lb_exceptions
import lb_folders
import lb_project
import lb_recorder
import lb_step
import lb_step_list
import lb_text_file
import lb_text_file_helper
import lb_util

import script_lb_branch
import script_lb_defaults
import script_lb_rebase
import step_lb_clone_project
import step_lb_create_workspace
import step_lb_impute_project_variables
import step_lb_initialize_environment
import step_lb_save_environment
import step_lb_status
import step_lb_validate_input_variables
#import step_lb_validate_prompt_inputs

def main():
    lb_constants.main_document()
    lb_dev_env.main_document()
    lb_doc_comments.main_document()
    lb_doc_folders.main_document()
    lb_exceptions.main_document()
    lb_folders.main_document()
    lb_project.main_document()
    lb_recorder.main_document()
    lb_step.main_document()
    lb_step_list.main_document()
    lb_text_file.main_document()
    lb_text_file_helper.main_document()
    lb_util.main_document()

    script_lb_defaults.main_document()
    step_lb_clone_project.main_document()
    step_lb_create_workspace.main_document()
    step_lb_impute_project_variables.main_document()
    step_lb_initialize_environment.main_document()
    step_lb_save_environment.main_document()
    step_lb_status.main_document()
    step_lb_validate_input_variables.main_document()
    #step_lb_validate_prompt_inputs.main_document()

    script_lb_branch.main_document()
    script_lb_rebase.main_document()


if __name__ == "__main__":
    # execute as script
    main()