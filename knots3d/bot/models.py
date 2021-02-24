from django.db import models
from django.contrib.auth.models import User


class alleknotentabelle(models.Model):

    knotenname_de = models.TextField()
    knoten_frameweite = models.TextField()
    knoten_framehoehe = models.TextField()
    knoten_frame_2d = models.TextField()
    knoten_frame_360 = models.TextField()
    knoten_count_x_2d = models.TextField()
    knoten_count_y_2d = models.TextField()
    knoten_count_x_360 = models.TextField()
    knoten_count_y_360 = models.TextField()
    knotenbild2d = models.TextField()
    knotenbild360 = models.TextField()
    knoten_typ = models.TextField()
    knotenname_eng = models.TextField()
    knotenbeschreibung_de = models.TextField()
    knoten_abok = models.TextField()
    knotenwarnung_de = models.TextField()
    knotenbeschreibung_eng = models.TextField()
    knotenbeschreibung_esp = models.TextField()
    knotenname_esp = models.TextField()
    knotenbeschreibung_ru = models.TextField()
    knotenname_ru = models.TextField()
    knotenfestigkeit = models.TextField()
    knotenname_fr = models.TextField()
    knotenbeschreibung_fr = models.TextField()
    knotenname_it = models.TextField()
    knotenbeschreibung_it = models.TextField()
    knotenname_tuek = models.TextField()
    knotenbeschreibung_tuek = models.TextField()
    knotenname_zh = models.TextField()
    knotenbeschreibung_zh = models.TextField()
    knotenname_ja = models.TextField()
    knotenbeschreibung_ja = models.TextField()
    knotenname_vi = models.TextField()
    knotenbeschreibung_vi = models.TextField()
    knotenname_pt = models.TextField()
    knotenbeschreibung_pt = models.TextField()
    knotenname_ko = models.TextField()
    knotenbeschreibung_ko = models.TextField()

    class Meta():
        verbose_name = "Knot"
        verbose_name_plural = "Knots"
