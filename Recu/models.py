
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import CharField


class Usuario(AbstractUser):
    type = [
        ('admin', 'Administrador'),
        ('player', 'Jugador')
    ]
    usertype = models.CharField(max_length=20, choices=type, default='player')
    def __str__(self):
        return self.username
class Weapons(models.Model):
    name = models.CharField(max_length=20)
    dmg = models.DecimalField
    crit_rate = models.DecimalField
    wep_rarity = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Player(models.Model):
    role = [
        ('invocador', 'Invocador'),
        ('melee', 'Melee'),
        ('mago', 'Mago'),
        ('tirador', 'Tirador')
    ]
    name = models.CharField(max_length=20)
    clase = models.CharField(max_length=20, choices=role, default='melee')
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    weapon = models.ForeignKey(Weapons, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Summoner(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=200)

class Boss(models.Model):
    name = models.CharField(max_length=20)
    summoner_id = models.OneToOneField(Summoner, on_delete=models.CASCADE)
    status = models.BooleanField
    f_creac = models.DateTimeField


class Biome(models.Model):
    name = models.CharField(max_length=20)
    difficulty = models.CharField(max_length=20)

class NPCs(models.Model):
    use = [
        ('vendedor', 'Vendedor'),
        ('mejorar', 'Mejorar'),
        ('curar', 'Curar'),
        ('misiones', 'Misiones')
    ]
    name = models.CharField(max_length=20)
    utility = models.CharField(max_length=20, choices=use, default='misiones')
    fav_biome = models.ForeignKey(Biome, on_delete=models.CASCADE)
    happyness = models.IntegerField(validators=[MaxValueValidator(10), MinValueValidator(1)])


class Materials(models.Model):
    material_rarity = CharField(max_length=20)
    id_biome = models.ForeignKey(Biome, on_delete=models.CASCADE)

class Recipes(models.Model):
    id_s = models.ForeignKey(Summoner, on_delete=models.CASCADE)
    id_w = models.ForeignKey(Weapons, on_delete=models.CASCADE)
    id_material = models.ForeignKey(Materials, on_delete=models.CASCADE)

class Mobs(models.Model):
    name = models.CharField(max_length=20)
    dmg = models.DecimalField
    biome_id = models.ForeignKey(Biome, on_delete=models.CASCADE)
