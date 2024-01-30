from rest_framework.views import APIView, Response, Request, status
from groups.models import Group
from traits.models import Trait
from .models import Pet
from .serializers import PetSerializer
from rest_framework.pagination import PageNumberPagination

class PetView(APIView, PageNumberPagination):
    def post(self, request: Request) -> Response:
        serializer = PetSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        group = serializer.validated_data.pop("group")
        traits = serializer.validated_data.pop("traits")
        
        verify_group = Group.objects.filter(scientific_name__iexact = group["scientific_name"])
        if len(verify_group) == 0:
           verify_group = Group.objects.create(**group)
        else:
            verify_group = verify_group[0]

        traits_obj = []
        for trait_data in traits:
            verify_trait = Trait.objects.filter(name__iexact = trait_data["name"])

            if len(verify_trait) == 0:
                newTrait = Trait.objects.create(**trait_data)
                traits_obj.append(newTrait)
            else:
                traits_obj.append(verify_trait[0])

        pet = Pet.objects.create(**serializer.validated_data, group=verify_group)
        pet.traits.set(traits_obj)
        serializer_2 = PetSerializer(Pet.objects.get(id=pet.id))

        return Response(serializer_2.data, status.HTTP_201_CREATED)

    def get(self, request: Request) -> Response:
        trait_name = request.query_params.get("trait", None)
        if trait_name is None:
            pet = Pet.objects.all()
        else:
            pet = Pet.objects.filter(traits__name__iexact = trait_name)
        petsPerPage = self.paginate_queryset(pet, request, view=self)
        serializer = PetSerializer(petsPerPage, many=True)
        return self.get_paginated_response(serializer.data)

class PetDetailView(APIView):
    def get(self, request: Request, pet_id: int) -> Response:
        try:
            pet = Pet.objects.get(pk=pet_id)
        except Pet.DoesNotExist:
            return Response({'detail': 'Not found.'}, status.HTTP_404_NOT_FOUND)
        serializer = PetSerializer(pet)
        return Response(serializer.data)
    
    def delete(self, request: Request, pet_id: int) -> Response:
        try:
            pet = Pet.objects.get(pk=pet_id)
        except Pet.DoesNotExist:
            return Response({'detail': 'Not found.'}, status.HTTP_404_NOT_FOUND)
        pet.delete()
        return Response(status=204)
    
    def patch(self, request: Request, pet_id: int) -> Response:    
        try:
            pet = Pet.objects.get(pk=pet_id)
        except Pet.DoesNotExist:
            return Response({'detail': 'Not found.'}, status.HTTP_404_NOT_FOUND)

        serializer = PetSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        group = serializer.validated_data.pop("group", '')
        if group:
            verify_group = Group.objects.filter(scientific_name__iexact = group["scientific_name"])
            if len(verify_group) == 0:
                verify_group = Group.objects.create(**group)
                pet.group = verify_group
            else:
                verify_group = verify_group[0]

        traits_obj = []
        traits = serializer.validated_data.pop("traits", '')
        if traits:
            for trait in traits:
                verify_trait = Trait.objects.filter(name__iexact = trait["name"])
                if len(verify_trait) == 0:
                    newTrait = Trait.objects.create(**trait)
                    traits_obj.append(newTrait)
                else:
                    traits_obj.append(verify_trait[0])

        for key, value in serializer.validated_data.items():
            setattr(pet, key, value)
        pet.save()

        serializer = PetSerializer(pet)

        return Response(serializer.data, status.HTTP_200_OK)


    

