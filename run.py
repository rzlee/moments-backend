import os
from app import app
port = int(os.environ.get("PORT", 5000))
app.debug = True
app.csrf = False
app.run(host='0.0.0.0', port=port)
