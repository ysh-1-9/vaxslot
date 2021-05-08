from vaxslot import app
from vaxslot.scripts.db_imports_exports import initialize

DEBUG = True
PORT = 8080

if __name__ == "__main__":
    initialize()
    app.run(debug = DEBUG, port = PORT)

