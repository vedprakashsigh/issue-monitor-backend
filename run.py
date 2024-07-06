from flask import Flask
from app import create_app


app: Flask = create_app()

if __name__ == "__main__":
    isDev: bool = True
    app.run(debug=isDev)
