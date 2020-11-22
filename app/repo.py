from .models import *
from django.db.models import Q
class FamilyRepo():
    def __init__(self,user):
        self.user=user
        self.objects=Family.objects
    def add_child(self,family_id,first_name):
        family=self.family(family_id=family_id)
        if family is not None:
            if family.father is not None:
                last_name=family.father.last_name
            else:
                last_name=family.mother.last_name
            child=Person(first_name=first_name,last_name=last_name)
            child.save()
            family.childs.add(child)
            family.save()
            return family

    def family_of_person(self,person_id):
        person=PersonRepo(self.user).person(person_id=person_id)
        ids= []
        for family in person.family_childs.all():
            ids.append(family.id)

        for family in person.family_fathers.all():
            ids.append(family.id)
            for family in family.child_families():
                ids.append(family.id)
                for family2 in family.child_families():
                    ids.append(family2.id)
                    for family in family.child_families():
                        ids.append(family.id)

        for family in person.family_mothers.all():
            ids.append(family.id)
            for family in family.child_families():
                ids.append(family.id)
                for family in family.child_families():
                    ids.append(family.id)
                    for family in family.child_families():
                        ids.append(family.id)
        # print(ids)
        families= self.objects.filter(Q(id__in=ids))
        # families= self.objects.filter(Q(father=person)|Q(mother=person))
        # print(families)
        return families
    def family(self,family_id):
        try:
            return self.objects.get(pk=family_id)
        except:
            return None
    def roots(self):
        # return self.objects.filter(Q(father=None)|Q(mother=None))
        return self.objects.all()
class PersonRepo():
    def __init__(self,user):
        self.user=user
        self.objects=Person.objects
    def persons_of_person(self,person_id):
        person=self.person(person_id=person_id)
        persons=[]
        persons.append(person)
        ids=[person.id]
        if person.father() is not None:
            ids.append(person.father().id)
        if person.mother() is not None:
            ids.append(person.mother().id)
        if person.husbands() is not None:
            for husband in person.husbands():
                ids.append(husband.id)
        if person.wives() is not None:
            for wife in person.wives():
                ids.append(wife.id)
        if person.father() is not None:
            for person1 in person.father().childs():
                ids.append(person1.id)
        if person.mother() is not None:
            for person1 in person.mother().childs():
                ids.append(person1.id)
        for person1 in person.childs():
            ids.append(person1.id)

            for husband in person1.husbands():
                ids.append(husband.id)
            for wife in person1.wives():
                ids.append(wife.id)

            if person1.childs() is not None:
                for child in person1.childs():
                    ids.append(child.id)
        persons=self.objects.filter(id__in=ids)
        return persons


    def add_person(self,first_name,last_name,birthdate,deathdate):
        person=Person(first_name=first_name,last_name=last_name,birthdate=birthdate,deathdate=deathdate)
        person.save()
        return person
    def search(self,search_for):
        persons=self.objects.filter(Q(first_name__contains=search_for)|Q(last_name__contains=search_for)|Q(first_name__contains=search_for))
        return persons
    def person(self,person_id):        
        try:
            return self.objects.get(pk=person_id)
        except:
            return None
    def persons(self):
        return self.objects.all()
    def delete(self,person_id):        
        person=self.person(person_id=person_id)
        if person is not None:
            person.delete()
            return self.persons()