from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django_filters.views import FilterView

from .models import CharacterInfo, CharacterFamilyTie, CharacterAliase, CharacterTitle
from .forms import CharacterInfoForm, RelationForm
from .filters import CharacterFilter

# Create your views here.
def index(request):
    return HttpResponse("Hello, world.")


class AboutPageView(generic.TemplateView):
    template_name = 'gameofthrones/about.html'


class HomePageView(generic.TemplateView):
    template_name = 'gameofthrones/home.html'

class CharacterFilterView(FilterView):
	filterset_class = CharacterFilter
	template_name = 'gameofthrones/character_filter.html'


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

@method_decorator(login_required, name='dispatch')
class CharacterCreateView(generic.View):
	model = CharacterInfo
	form_class = CharacterInfoForm
	success_message = "Character created successfully"
	template_name = 'gameofthrones/character_new.html'
	# field = '__all__' <-- superseded by form_class

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def post(self, request):
		form = CharacterInfoForm(request.POST)
		if form.is_valid():
			character = form.save(commit=False)
			character.save()
			# for country in form.cleaned_data['country_area']:
			# 	CharacterFamilyTie.objects.create(character1=site, country_area=country)
			return HttpResponseRedirect(reverse_lazy('characters'))
		else:
			print(form.errors)
		return render(request, 'gameofthrones/character_new.html', {'form': form})
	
	def get(self, request):
		form = CharacterInfoForm()
		return render(request, 'gameofthrones/character_new.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class CharacterUpdateView(generic.UpdateView):
	model = CharacterInfo
	form_class = CharacterInfoForm
	context_object_name = 'character'
# 	# pk_url_kwarg = 'site_pk'
	success_message = "Character updated successfully"
	template_name = 'gameofthrones/character_update.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def form_valid(self, form):
		character = form.save(commit=False)
		character.save()

		return HttpResponseRedirect(character.get_absolute_url())


@method_decorator(login_required, name='dispatch')
class CharacterDeleteView(generic.DeleteView):
    model = CharacterInfo
    success_message = "Character deleted successfully"
    success_url = reverse_lazy('characters')
    context_object_name = 'character'
    template_name = 'gameofthrones/character_delete.html'

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        # # Delete Character_family_tie entries
        CharacterFamilyTie.objects \
        	.filter(character1=self.object.character_id) \
        	.delete()

        self.object.delete()

        return HttpResponseRedirect(self.get_success_url())

@method_decorator(login_required, name='dispatch')
class RelationCreateView(generic.View):
    model = CharacterFamilyTie
    form_class = RelationForm
    success_message = "Relation created successfully"
    template_name = 'gameofthrones/relationship_new.html'
    
    # field = '__all__' <-- superseded by form_class
    # success_url = reverse_lazy('heritagesites/site_list')

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        form = RelationForm(request.POST)
        if form.is_valid():
            relation = form.save(commit=False)
            relation.save()
            print(form.cleaned_data)
            return HttpResponseRedirect(reverse_lazy('characters'))
        return render(request, 'gameofthrones/relationship_new.html', {'form': form})

    def get(self, request):
        form = RelationForm()
        return render(request, 'gameofthrones/relationship_new.html', {'form': form})


