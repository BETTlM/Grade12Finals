import subprocess

pgm_1 = r'main.py'

pgm_2 = r'trial.py'

pgm_3 = r'gui.py'

subprocess.Popen(['python',pgm_1])

subprocess.Popen(['python',pgm_2])

subprocess.Popen(['python', pgm_3])