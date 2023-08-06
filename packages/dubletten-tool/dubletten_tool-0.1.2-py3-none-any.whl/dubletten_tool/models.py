from django.db import models
from apis_core.apis_entities.models import Person




class PersonProxy(models.Model):
    # todo: __gpirgie__ rename to Deduplication Proxy or something like that
    status_choices = [
        ("candidate", "Candidate"),
        ("single", "Single"),
        ("merged", "Merged"),
    ]
    person = models.OneToOneField(Person, null=False, blank=False, on_delete=models.CASCADE)
    status = models.CharField(max_length=300, choices=status_choices, default="single")


    @property
    def alt_names(self):
        nach = ["alternative name", "alternativer Nachname", "Nachname verheiratet", "Nachname alternativ verheiratet", "Nachname alternativ vergeiratet"]
        return [l[0] for l in self.person.label_set.filter(label_type__name__in=nach).values_list("label")]

    @property
    def name_verheiratet(self):
        ver = ["Nachname verheiratet", "Nachname alternativ verheiratet", "Nachname alternativ vergeiratet"]
        return [l[0] for l in self.person.label_set.filter(label_type__name__in=ver).values_list("label")]

    @property 
    def alt_first_names(self):
        return [l[0] for l in self.person.label_set.filter(label_type__name="alternativer Vorname").values_list("label")]

    @property
    def names_list(self):
        name = self.person.name
        alt_names = self.alt_names
        alt_names.append(name)
        return alt_names

    @property
    def first_names_list(self):
        first_name = self.person.first_name
        alt_first_names = self.alt_first_names
        alt_first_names.append(first_name)
        return alt_first_names

    @property
    def names_set(self):
        return set(self.names_list)

    @property
    def first_names_set(self):
        return set(self.first_names_list)

    


class Group(models.Model):
    """Group: A collection of Person-Instances storing possible duplicates. 
    Each group should run through several filter, split and add processes to finally be merged into one entity. 
    A Group holds GroupingCandidates, which serve as proxies for the actual Person-instances.

    Args:
        models (_type_): 
        
    Fields:
    """
    status_choices_group = [
        ("unchecked", "unchecked"),
        ("checked group", "checked group"),
        ("checked for other groups", "checked for other groups"),
        ("checked all members", "checked all members"),
        ("ready to merge", "ready to merge"),
        ("merged", "merged")
    ]
    name = models.CharField(max_length=600, blank=True)
    members = models.ManyToManyField(PersonProxy, blank=True)
    status = models.CharField(max_length=300, choices=status_choices_group, default="unchecked")

    @property
    def count(self):
        return self.members.all().count()


#     removed = models.ManyToManyField(GroupingCandidate, blank=True, null=True)
#     added = models.ManyToManyField(GroupingCandidate, blank=True, null=True)




    




