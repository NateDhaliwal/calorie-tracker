import os
os.system("gunicorn -w 4 -b 'main:app'")
