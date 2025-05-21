from itertools import chain

from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.core import serializers
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
        return JsonResponse({"message":"Error: El método debe ser GET"})



def Show_Recipes (request, m_name):
    if request.method == "GET":
        limite = int(request.GET.get("limite", 3))
        pagina = int(request.GET.get("página", 1))
        idMaterial = Materials.objects.get(material_name=m_name)
        material = Materials.objects.get(pk=idMaterial.id)
        s_recipes = (Recipes.objects.filter(pk=material.id)
                   .select_related('id_s').all())
        w_recipes = (Recipes.objects.filter(pk=material.id)
                     .select_related('id_w').all())

        recipes = list(chain(s_recipes, w_recipes))


        paginator = Paginator(recipes, limite)

        try:
            recipes_page = paginator.page(pagina)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

        data = serializers.serialize('json', recipes_page)
        return JsonResponse({"recipes": json.loads(data), "total": paginator.count, "page": pagina, "pages": paginator.num_pages})

    else :
        return JsonResponse({"message":"Error: El método debe ser GET"})


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
        return JsonResponse({"message":"Error: El método debe ser POST"})

@csrf_exempt
@transaction.atomic
def New_Boss (request):
    if request.method == "POST":
        data = json.loads(request.body)
        if data.get("s_name", 0) == 0:
            return JsonResponse({"message": "El campo 'Nombre invocador'(s_name) no está cubierto"})
        elif data.get("description", 0) == 0:
            return JsonResponse({"message": "El campo 'Descripción invocador'(descripcion) no está cubierto"})
        elif data.get("bo_name", 0) == 0:
            return JsonResponse({"message": "El campo 'Nombre jefe'(bo_name) no está cubierto"})
        elif data.get("m_name", 0) == 0:
            return JsonResponse({"message": "El campo 'Nombre material'(m_name) no está cubierto"})
        elif data.get("m_name", 0) == 0:
            return JsonResponse({"message": "El campo 'Rareza material'(m_rarity) no está cubierto"})
        elif data.get("bi_name", 0) == 0:
            return JsonResponse({"message": "El campo 'Nombre bioma'(bi_name) no está cubierto"})

        summoner = Summoner.objects.create(
            name=data["s_name"],
            description=data["description"]
        )
        Boss.objects.create(
            name=data["bo_name"],
            summoner_id=summoner,
            status = False
        )
        try:
            material = Materials.objects.get(material_name=data["m_name"])
        except Materials.DoesNotExist:
            material = 0
        if material == 0:
            try:
                biome = Biome.objects.get(name=data["bi_name"])
            except Biome.DoesNotExist:
                return JsonResponse({"message":"Selecciona un bioma válido"})
            material = Materials.objects.create(
                material_name= data["m_name"],
                material_rarity = data["m_rarity"],
                id_biome = biome
            )
        Recipes.objects.create(
            id_s=summoner,
            id_material=material
        )
        return JsonResponse({"message":"Jefe, invocador... creado exitosamente"})
    else :
        return JsonResponse({"message":"Error: El método debe ser POST"})

#PUT/PATCH
@csrf_exempt
def boss_beated (request, id):
        if request.method == "PATCH":
            data = json.loads(request.body)
            boss = Boss.objects.get(pk=id)
            boss.status = data.get("status", boss.status)
            return JsonResponse({"mensaje": "Jefe actualizado"})
        else :
            return JsonResponse({"message": "Error: El método debe ser PATCH"})


#DELETES
@csrf_exempt
def del_boss (request, id):
    if request.method == "DELETE":
        boss = Boss.objects.get(pk=id)
        boss.delete()
        return JsonResponse({"mensaje": "Jefe eliminado"})
    else :
        return JsonResponse({"message":"Error: El método debe ser DELETE"})
