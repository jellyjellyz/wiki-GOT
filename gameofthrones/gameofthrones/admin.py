from django.contrib import admin
import gameofthrones.models as models

# Register your models here.

@admin.register(models.BiologicalType)
class BiologicalTypeAdmin(admin.ModelAdmin):
    fields = [
        'biological_type_name'
    ]
    list_display = [
        'biological_type_name'
    ]
    ordering = [
        'biological_type_name'
    ]

@admin.register(models.CharacterAliase)
class CharacterAliaseAdmin(admin.ModelAdmin):
    fields = ['character', 'aliase']
    list_display = ['character', 'aliase']
    ordering = ['character']




@admin.register(models.CharacterTitle)
class CharacterTitleAdmin(admin.ModelAdmin):
	fields = ['character', 'title_name']
	list_display = ['character', 'title_name']
	ordering = ['character']

# admin.site.register(models.CharacterTitle)


class CharacterFamilyTieInline(admin.TabularInline):
	model = models.CharacterFamilyTie
	fk_name = 'character1'


# admin.site.register(models.CharacterFamilyTie)


@admin.register(models.CharacterInfo)
class CharacterInfoAdmin(admin.ModelAdmin):
	fieldsets = (
		(None, {
			'fields': (
				'full_name',
                'is_male',
                'is_main_character',
				'house',
				'culture',
                'brief_intro',
                'full_intro'
			)
		}),
		('URL', {
			'fields': [
				'character_url',
				'character_img_file_name'
			]
		})
	)

	list_display = (
		'full_name',
		'house',
		'culture',
		'brief_intro'
	)

	list_filter = (
		'is_main_character',
		'is_male',
        'house',
        'culture'
	)

	inlines = [
		CharacterFamilyTieInline,
	]

# admin.site.register(models.CharacterInfo)


@admin.register(models.Culture)
class CultureAdmin(admin.ModelAdmin):
	fields = ['culture_name']
	list_display = ['culture_name']
	ordering = ['culture_name']

# admin.site.register(models.Culture)


@admin.register(models.House)
class HouseAdmin(admin.ModelAdmin):
	fields = ['house_name', 'house_img_file_name']
	list_display = ['house_name', 'house_img_file_name']
	ordering = ['house_name']

# admin.site.register(models.House)


@admin.register(models.RelationType)
class RelationTypeAdmin(admin.ModelAdmin):
	fields = ['relation_type_name']
	list_display = ['relation_type_name']
	ordering = ['relation_type_name']

# admin.site.register(models.RelationType)


