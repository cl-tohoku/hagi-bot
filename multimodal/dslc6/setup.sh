#!bin/bash
sudo pip install -U dslclib
# python3 sample.py
# python3 dev/check_pitch.py
# python3 dev/check_pause.py
# python3 dev/check_timeout.py
# python3 dev/check_block.py
# python3 dev/check_error.py
# python3 dev/check_face.py
# python3 dev/check_motion.py
# python3 mix_model/module.py
python3 mix_model/mix_model_run.py --main-model gpt-4 --slot-model gpt-4