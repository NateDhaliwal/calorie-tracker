import os
os.system("gunicorn -w 4 'main:app' --reload")
