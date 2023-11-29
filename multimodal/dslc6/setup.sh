#!bin/bash
sudo pip install -U dslclib
sudo pip install openai==0.28.1
sudo pip install tiktoken==0.5.1
sudo pip install timeout_decorator==0.5.0
python3 hagi_bot/hagi_run.py --main-model gpt-4 --slot-model gpt-4