from rest_framework import serializers
from groups.serializes import GroupSerializer
from .models import SexOfPets
from traits.serializers import TraitSerializer 

class  PetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(
        choices=SexOfPets.choices,
        default=SexOfPets.NOT_INFORMED
    )
    group = GroupSerializer()
    traits = TraitSerializer(many=True)