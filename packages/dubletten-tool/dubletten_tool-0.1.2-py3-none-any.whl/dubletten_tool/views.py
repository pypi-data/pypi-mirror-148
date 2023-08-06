from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import View, TemplateView
from django.utils.decorators import method_decorator
# Create your views here.
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required, user_passes_test
#from .grouping_script_1 import run
from .models import Group, PersonProxy
import json

#run()
@method_decorator(login_required, name="dispatch")
class getToolPage(TemplateView):
    template_name = "tool_page.html"
    print("getToolPage called")

    def get_context_data(self, **kwargs):
        #ng = get_groups()
        groups = Group.objects.all()
        #singles = PersonProxy.objects.filter(status="single")
        context = {}

        context["groups"] = groups
        #context["singles"] = singles
        return context


def get_groups(request, **kwargs):

    if request.method == "GET":
        filter = kwargs.get("val")
        filter = filter.replace("__", " ")
        print("filter was: ", filter)

        context = {}
        if not filter:
            context["groups"] = Group.objects.all()

        else: 
            groups = Group.objects.filter(name__istartswith=filter)
            context["groups"] = groups

        count = len(context["groups"])
        context["group_count"] = count

        html = render_to_string("group_list.html", context, request)

        return JsonResponse({"html": html, "group_count": count})


def get_singles(request, **kwargs):
    
    if request.method == "GET":
        #singles = {s.id: {"name":s.person.name, "first_name": s.person.first_name,"start": s.person.start_date,"end":s.person.end_date} for s in PersonProxy.objects.filter(status="single")}
        
        # text = kwargs.get("val")
        # type = kwargs.get("type")
        # print("text arrived as: ", text)
        
        # if not text:
        #     singles = [(s.person.id, s.person.name, s.person.first_name, s.person.start_date, s.person.end_date) for s in PersonProxy.objects.filter(status="single")]
        # else:
        #     print("used filtered singles")
            
        #     text = text.replace("__", " ")

        #     if type == "name":
        #         singles = [(s.person.id, s.person.name, s.person.first_name, s.person.start_date, s.person.end_date) for s in PersonProxy.objects.filter(person__name__istartswith=text).filter(status="single")]
        #     elif type == "first_name":
        #         singles = [(s.person.id, s.person.name, s.person.first_name, s.person.start_date, s.person.end_date) for s in PersonProxy.objects.filter(person__first_name__istartswith=text).filter(status="single")]

        #     print("filtered singles len: ", len(singles))

        text_name = kwargs.get("val_name")
        text_first = kwargs.get("val_first")
        print(f"Arrived as - name: {text_name}, first: {text_first}")

        if text_name == "false":
            text_name = False
        else: 
            text_name = text_name.replace("__", " ")

        if text_first == "false":
            text_first = False
        else:
            text_first = text_first.replace("__", " ")

        if not text_name and not text_first:
            singles = [(s.person.id, s.person.name, s.person.first_name, s.person.start_date, s.person.end_date) for s in PersonProxy.objects.filter(status="single")]
        elif not text_first:
            singles = [(s.person.id, s.person.name, s.person.first_name, s.person.start_date, s.person.end_date) for s in PersonProxy.objects.filter(person__name__istartswith=text_name).filter(status="single")]
        elif not text_name:
            singles = [(s.person.id, s.person.name, s.person.first_name, s.person.start_date, s.person.end_date) for s in PersonProxy.objects.filter(person__first_name__icontains=text_first).filter(status="single")]
        else:
            singles = [(s.person.id, s.person.name, s.person.first_name, s.person.start_date, s.person.end_date) for s in PersonProxy.objects.filter(person__first_name__icontains=text_first, person__name__istartswith=text_name).filter(status="single")]

        return JsonResponse({"singles":singles})

def get_group_ajax(request, **kwargs):

    if request.method == "GET":
        g_id = kwargs.get("g_id")
        group = Group.objects.get(id=g_id)
        context = {
            "group":group,
            "members": [(v.person, [r for r in v.person.personinstitution_set.all()]) for v in group.members.all()]
        }

        html = render_to_string("member_list.html", context, request)

        return JsonResponse({"html":html})
        
def get_single_ajax(request, **kwargs):

    if request.method == "GET":
        s_id = kwargs.get("s_id")
        single = PersonProxy.objects.get(person__id=s_id)
        if not single.status == "single":
            print("WAS NOT A SINGLE")
        
        context = {
            "s": single.person,
            "rels": [r for r in single.person.personinstitution_set.all()]
        }

        html = render_to_string("singles_list.html", context, request)
        return JsonResponse({"html":html})

def create_new_group(request):
    if request.method == "POST":
        d = json.loads(request.POST.get("DATA"))


        data = d.get("data")
        name = d.get("new_name")
    
        if not name:
            name = "New Group"

        new_group = Group.objects.create(name=name)
        if name == "New Group":
            new_group.name += " "+str(new_group.id)
            new_group.save()

        updates = {}
        former_singles = []
        for k, v in data.items():
            print(k, v)
            if v:
                if k != "singles":
                    group = Group.objects.get(id=k)
                   
                pers = PersonProxy.objects.filter(person__id__in=v)
                print("pers is", pers)
                for p in pers:
                    if k != "singles":
                        group.members.remove(p)
                        group.save()
                    else: 
                        p.status = "candidate"
                        former_singles.append(p.person.id)
                        p.save()
                    new_group.members.add(p)

                if k != "singles":
                    count = group.count
                    g_id = group.id
                    if count == 0:
                        print("In count == 0 gid, count", g_id, count)
                        group.delete()
                        

                    elif count == 1:
                        print("IN coutn == 1 gid, count", g_id, count)

                        per = group.members.all()[0]
                        per.status = "single"
                        per.save()
                        group.delete()
                        count = 0


                    else:
                        group.save()
               
                    updates.update({g_id:count})
                    
                new_group.save()

        print("updates is: ", updates)
        res = {"new_group_id": new_group.id, "new_group": new_group.name, "new_group_count":new_group.count, "former_singles":former_singles,"group_updates":updates}
        
        #todo: add message 
        return JsonResponse({"data":res})


def merge_groups(request):
    if request.method == "POST":
        d = json.loads(request.POST.get("DATA"))
        print(d)
        name = d.get("new_name")
        groups = d.get("groups")
        singles = d.get("singles")

        new_group = Group.objects.create(name=name)
        if groups:
            for g in groups:
                group = Group.objects.get(id=g)
                for m in group.members.all():
                    new_group.members.add(m)
                new_group.save()
                group.delete()
        if singles: 
            for s in singles:
                print("singles was true")
                print("single id was: ", s)
                pp = PersonProxy.objects.get(person__id=s)
                pp.status = "candidate"
                pp.save()
                new_group.members.add(pp)
            new_group.save()

        
        
        # todo : add message 
        return JsonResponse({"remove_groups": groups, "remove_singles":singles, "add": [new_group.id, new_group.name, new_group.count]})
            



def remove_member(request, **kwargs):
    if request.method == "GET":
        group_id = kwargs.get("group_id")
        per_id = kwargs.get("per_id")

        group = Group.objects.get(id=group_id)
        per = PersonProxy.objects.get(person__id=per_id)
        group.members.remove(per)
        per.status = "single"
        group.save()
        per.save()
        updates = {}

        count = group.count
        if count == 0:
            group.delete()
            

        elif count == 1:
            per = group.members.all()[0]
            per.status = "single"
            per.save()
            group.delete()
            count = 0

        else:
            group.save()
        
        updates.update({group_id:count})

        #todo: add message
        return JsonResponse({"data":updates})

            


