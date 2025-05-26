import os
os.system("gunicorn -w 4 -b 0.0.0.0 'main:app'")
