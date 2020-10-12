import os

class Config(object):

    # Secret key
    SECRET_KEY = os.environ.get("SECRET_KEY")

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # File transition
    QR_CODE_DIRECTORY = r"C:\FILES\Workspace\SummerLesson\APP\QR_code"
    TEMP_UPLOAD_DIRECTORY = r"C:\MYFILES\Workspace\SummerLesson\APP\Temp_upload"

    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")