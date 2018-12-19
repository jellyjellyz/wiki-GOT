from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

from .models import CharacterInfo, CharacterFamilyTie, CharacterAliase, CharacterTitle


# Create your views here.
def index(request):
    return HttpResponse("Hello, world.")


class AboutPageView(generic.TemplateView):
    template_name = 'gameofthrones/about.html'


class HomePageView(generic.TemplateView):
    template_name = 'gameofthrones/home.html'


class MainCharacterListView(generic.ListView):
    model = CharacterInfo
    context_object_name = 'characters'
    template_name = 'gameofthrones/main_character.html'

    def get_queryset(self):
        return CharacterInfo.objects\
            .filter(is_main_character=1).all()\
            .order_by('full_name')


class AllCharacterListView(generic.ListView):
    model = CharacterInfo
    context_object_name = 'characters'
    template_name = 'gameofthrones/all_character.html'
    paginate_by = 60

    def get_queryset(self):
        return CharacterInfo.objects\
            .all()\
            .order_by('full_name')


class CharacterDetailView(generic.DetailView):
    model = CharacterInfo
    context_object_name = 'character'
    template_name = 'gameofthrones/character_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tocharacter = CharacterInfo.objects.get(
            character_id=self.object.character_id).character2.all()
        context['toCharacters'] = {}
        for c in tocharacter:
            family_tie = CharacterFamilyTie.objects.get(character1__character_id=self.object.character_id,
                                                        character2__character_id=c.character_id)
            relation = ''
            biological = ''
            if family_tie.relation_type:
                relation = family_tie.relation_type.relation_type_name

            if family_tie.biological_type:
                biological = family_tie.biological_type.biological_type_name

            if relation != '':
                if  relation in context['toCharacters']:
                    context['toCharacters'][relation].append(
                        {'character': c, 'biological': biological})
                else:
                    context['toCharacters'][relation] = [
                        {'character': c, 'biological': biological}]
        # print(context['toCharacters'])

        temp = []
        titles = CharacterTitle.objects.filter(
            character_id=self.object.character_id).all()
        for t in titles:
            temp.append(t.title_name)

        context['titles'] = (', ').join(temp)

        temp = []
        aliases = CharacterAliase.objects.filter(
            character_id=self.object.character_id).all()
        for a in aliases:
            temp.append(a.aliase)
        context['aliases'] = (', ').join(temp)
        return context
