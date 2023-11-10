from django.apps import AppConfig
from ultralytics import YOLO

class EggsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'eggs'
    # ml_model = YOLO("repo/static/best.pt", task="detect")
    sv_model = YOLO("repo/static/sv_best.pt")
    kh_model = YOLO("repo/static/kh_best.pt")
    dh_model = YOLO("repo/static/dh_best.pt")
