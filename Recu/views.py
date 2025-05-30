from itertools import chain

from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.core import serializers
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.views import APIView

from Recu.models import Usuario,Player,Weapons,Boss,Summoner,Recipes, Materials, Biome, NPCs, Mobs

import json



#GETS
@csrf_exempt
class Boss_status(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        boss = Boss.objects.filter(pk=id)
        data = {"id": boss.id, "nombre": boss.name, "estado": boss.status}
        return JsonResponse(data)



class Show_Recipes(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, m_name, page):

        if request.method == "GET":
            limite = int(request.GET.get("limite", 3))
            pagina = int(request.GET.get("página", page))
            material = Materials.objects.get(material_name=m_name)
            recipes = (Recipes.objects.filter(id_material=material)
                       .select_related('id_s', 'id_w', 'id_material'))

            print(recipes)

            paginator = Paginator(recipes, limite)

            try:
                recipes_page = paginator.page(pagina)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=400)

            data = []
            for recipe in recipes_page:
                data.append(
                    {
                        "id" : recipe.id,
                        "weapon" : recipe.id_w.name if recipe.id_w else None,
                        "summoner" : recipe.id_s.name if recipe.id_s else None,
                        "material" : recipe.id_material.material_name
                    }
                )

            return JsonResponse({"recipes": data, "total": paginator.count, "page": pagina, "pages": paginator.num_pages})

        else :
            return JsonResponse({"message":"Error: El método debe ser GET"})



#POSTS
class Register (APIView):
    def post(self, request):
        data = json.loads(request.body)
        if (data["usertype"] != "admin" and data["usertype"] != "player"):
            return JsonResponse({"error" : "El usuario solo puede ser admin(Administrador) o player(Jugador)"})
        else:
            user = Usuario.objects.create_user(
                username = data["username"],
                password = data["password"],
                email = data["email"],
                usertype = data["usertype"]
            )
            return JsonResponse({"id": user.pk, "mensaje": "Usuario creado con exito"})



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
class boss_beated(APIView):
    def patch(request, id):
        if request.method == "PATCH":
            data = json.loads(request.body)
            boss = Boss.objects.get(pk=id)
            boss.status = data.get("status", boss.status)
            return JsonResponse({"mensaje": "Jefe actualizado"})
        else :
            return JsonResponse({"message": "Error: El método debe ser PATCH"})


#DELETES
class EsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.usertype == 'admin'

class del_Boss(APIView):
    permission_classes = [EsAdmin]

    def delete(self, request, id):

        boss = Boss.objects.get(pk=id)
        print(boss.name)
        boss.delete()
        return JsonResponse({"mensaje": "Jefe eliminado"})




