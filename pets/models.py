from django.db import models

class SexOfPets(models.TextChoices):
    MALE = "Male"
    FEMALE = "Female"
    NOT_INFORMED = "Not Informed"

class Pet(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(
        max_length=20,
        choices=SexOfPets.choices,
        default=SexOfPets.NOT_INFORMED
    )
    group = models.ForeignKey(
        "groups.Group", related_name="pets", on_delete=models.PROTECT
    )