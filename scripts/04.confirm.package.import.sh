#!/bin/sh
cd ..

python3 -c "from lb_lib.lb_script import LbScript; LbScript().hello_world()"

python3 -c "from lb_lib.lb_recorder import LbRecorder; LbRecorder().hello_world()"
