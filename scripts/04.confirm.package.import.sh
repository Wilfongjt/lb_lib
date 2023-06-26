#!/bin/sh
cd ..
python3 -c "from lb_lib.lb_dev_env import LbDevEnv; LbDevEnv().hello_world()"
python3 -c "from lb_lib.lb_doc_comments import LbDocComments; LbDocComments().hello_world()"
python3 -c "from lb_lib.lb_doc_folders import LbDocFolders; LbDocFolders().hello_world()"
python3 -c "from lb_lib.lb_recorder import LbRecorder; LbRecorder().hello_world()"
python3 -c "from lb_lib.lb_script import LbScript; LbScript().hello_world()"
python3 -c "from lb_lib.lb_text_file import LbTextFile; LbTextFile().hello_world()"
python3 -c "from lb_lib.lb_text_file_helper import LbTextFileHelper; LbTextFileHelper().hello_world()"
