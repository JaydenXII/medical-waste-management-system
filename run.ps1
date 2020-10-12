$env:flask_app = ".\run.py"
$env:flask_env = "development"
$env:DATABASE_URI = "sqlite:///C:\MYFILES\Workspace\SummerLesson\APP\app.db"
$env:SECRET_KEY = "SECRET_KEY"
$env:ADMIN_PASSWORD = "administration"

flask run --host=0.0.0.0