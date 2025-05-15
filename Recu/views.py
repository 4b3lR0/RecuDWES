
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction

from Recu.models import Usuario,Player,Weapons,Boss,Summoner,Recipes, Materials, Biome, NPCs, Mobs

import json



#GETS
@csrf_exempt
def Boss_status (request, id):
    if request.method == "GET":
        boss = Boss.objects.filter(pk=id)
        data = {"id": boss.id, "nombre": boss.name, "estado": boss.status}
        return JsonResponse(data)
    else :
        return "Error: El método debe ser GET"

#POSTS
@csrf_exempt
def Register (request):
    if request.method == "POST":
        data = json.loads(request.body)
        user = Usuario.objects.create(
            username=data["username"],
            password=data["password"],
            email=data["email"],
            usertype=data["usertype"]
        )
        return JsonResponse({"id": user.pk, "mensaje": "Usuario creado con exito"})
    else :
        return "Error: El método debe ser POST"

@csrf_exempt
@transaction.atomic
def New_Boss (request):
    if request.method == "POST":
        data = json.loads(request.body)
        summoner = Summoner.objects.create(
            name=data["s_name"],
            description=data["description"]
        )
        idSummoner = Summoner.objects.get(name=data["s_name"])
        boss = Boss.objects.create(
            name=data["b_name"],
            summoner_id=idSummoner
        )
        try:
            materials = Materials.objects.get(material_name=data["m_name"])
        except Materials.DoesNotExist:
            materials = 0
        if materials == 0:
            try:
                biome = Biome.objects.get(name=data["b_name"])
            except Biome.DoesNotExist:
                return "Seleccione un bioma válido"
            material = Materials.objects.create(
                material_name= data["m_name"],
                material_rarity = data["m_rarity"],
                id_biome = biome
            )
        recipes = Recipes.objects.create(
            id_s=idSummoner,
            id_material=material
        )
        summoner.save()
        boss.save()
        material.save()
        recipes.save()
        return "Jefe, invocador.... creados exitosamente"
    else :
        return "Error: El método debe ser POST"

#PUT/PATCH
@csrf_exempt
def boss_beated (request, id):
        if request.method == "PATCH":
            data = json.loads(request.body)
            boss = Boss.objects.get(pk=id)
            boss.status = data.get("status", boss.status)
            return JsonResponse({"mensaje": "Jefe actualizado"})
        else :
            return "Error: El método debe ser PATCH"

#DELETES
@csrf_exempt
def del_boss (request, id):
    if request.method == "DELETE":
        boss = Boss.objects.get(pk=id)
        boss.delete()
        return JsonResponse({"mensaje": "Jefe eliminado"})