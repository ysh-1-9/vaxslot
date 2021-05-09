from vaxslot import app
from vaxslot.scripts.automator import automate
from vaxslot.scripts.db_imports_exports import initialize

DEBUG = True
PORT = 8080

if __name__ == "__main__":
    initialize()
    # automate()                   #multithread
    app.run(host='0.0.0.0',debug = DEBUG, port = PORT)

