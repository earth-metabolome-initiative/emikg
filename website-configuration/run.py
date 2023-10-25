"""Run the website locally."""
import os
from website import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ["FLASK_PORT"]), debug=True)
