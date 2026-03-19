from student_gmail_assistant import create_app
from livereload import Server

app = create_app()

if __name__ == "__main__":
    server = Server(app.wsgi_app)
    server.watch("static/styles.css")
    server.watch("templates/")
    server.serve(port=5000)