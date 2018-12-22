from gameofthrones.models import BiologicalType, CharacterAliase, CharacterFamilyTie, CharacterInfo, \
	CharacterTitle, Culture, House, RelationType
from rest_framework import response, serializers, status


class BiologicalTypeSerializer(serializers.ModelSerializer):

	class Meta:
		model = BiologicalType
		fields = ('biological_type_id', 'biological_type_name')


class CultureSerializer(serializers.ModelSerializer):

	class Meta:
		model = Culture
		fields = ('culture_id', 'culture_name')


class HouseSerializer(serializers.ModelSerializer):

	class Meta:
		model = House
		fields = ('house_id', 'house_name', 'house_img_file_name')


class RelationTypeSerializer(serializers.ModelSerializer):

	class Meta:
		model = RelationType
		fields = ('relation_type_id', 'relation_type_name')


class CharacterFamilyTieSerializer(serializers.ModelSerializer):
    character1_id = serializers.ReadOnlyField(source='character_info.character_id')
    character2_id = serializers.ReadOnlyField(source='character_info.character_id')
    relation_type = RelationTypeSerializer(many=False, read_only=True)
    biological_type = BiologicalTypeSerializer(many=False, read_only=True)

    class Meta:
        model = CharacterFamilyTie
        fields = ('character1_id', 'character2_id', 'relation_type', 'biological_type')


class CharacterInfoSerializer(serializers.ModelSerializer):

    full_name = serializers.CharField(
        allow_blank=False,
        max_length=100
    )
    is_male = serializers.IntegerField(
        allow_null=False
    )
    is_main_character = serializers.IntegerField(
        allow_null=False
    )
    brief_intro = serializers.CharField(
        allow_null=True
    )
    full_intro = serializers.CharField(
        allow_blank=False
    )
    character_url = serializers.CharField(
        allow_null=True
    )
    character_img_file_name = serializers.CharField(
        allow_null=True
    )
    house = HouseSerializer(
        many=False,
        read_only=True
    )
    house_id = serializers.PrimaryKeyRelatedField(
        allow_null=False,
        many=False,
        write_only=True,
        queryset=House.objects.all(),
        source='house'
    )
    culture = CultureSerializer(
        many=False,
        read_only=True
    )
    culture_id = serializers.PrimaryKeyRelatedField(
        allow_null=False,
        many=False,
        write_only=True,
        queryset=Culture.objects.all(),
        source='culture'
    )
    character_family_tie = CharacterFamilyTieSerializer(
        source='character_family_tie_set', # Note use of _set
        many=True,
        read_only=True
    )
    character_family_ties = serializers.ListField(
        write_only=True,
        source='character_family_tie'
    )

    class Meta:
        model = CharacterInfo
        fields = (
            'character_id',
            'full_name',
            'is_male',
            'is_main_character',
            'brief_intro',
            'full_intro',
            'character_url',
            'character_img_file_name',
            'house',
            'house_id',
            'culture',
            'culture_id',
            'character_family_tie',
            'character_family_ties'
        )

    def create(self, validated_data):
        """
        This method persists a new HeritageSite instance as well as adds all related
        countries/areas to the heritage_site_jurisdiction table.  It does so by first
        removing (validated_data.pop('heritage_site_jurisdiction')) from the validated
        data before the new HeritageSite instance is saved to the database. It then loops
        over the heritage_site_jurisdiction array in order to extract each country_area_id
        element and add entries to junction/associative heritage_site_jurisdiction table.
        :param validated_data:
        :return: site
        """

        # print(validated_data)

        characters = validated_data.pop('character_family_tie')
        character = CharacterInfo.objects.create(**validated_data)
        character_id = character.character_id

        if characters is not None:
        	for character in characters:
        		CharacterFamilyTie.objects.create(
        			character1_id=character_id,
        			character2_id=character['character2_id'],
                    relation_type_id=character['relation_type_id'],
                    biological_type_id=character['biological_type_id']
        		)

        return character

    def update(self, instance, validated_data):
        character_id = instance.character_id
        characters = validated_data.pop('character_family_tie')

        instance.full_name = validated_data.get(
            'full_name',
            instance.full_name
        )
        instance.is_male = validated_data.get(
            'is_male',
            instance.is_male
        )
        instance.is_main_character = validated_data.get(
            'is_main_character',
            instance.is_main_character
        )
        instance.brief_intro = validated_data.get(
            'brief_intro',
            instance.brief_intro
        )
        instance.full_intro = validated_data.get(
            'full_intro',
            instance.full_intro
        )
        instance.character_url = validated_data.get(
            'character_url',
            instance.character_url
        )
        instance.house_id = validated_data.get(
            'house_id',
            instance.house_id
        )
        instance.culture_id = validated_data.get(
            'culture_id',
            instance.culture_id
        )
        instance.character_img_file_name = validated_data.get(
            'character_img_file_name',
            instance.character_img_file_name
        )
        instance.save()

        # If any existing country/areas are not in updated list, delete them
        new_ids = []
        old_ids = CharacterFamilyTie.objects \
            .values_list('character2_id', flat=True) \
            .filter(character1_id=character_id)

        # Insert new unmatched country entries
        for character in characters:
            new_id = character['character2_id']
            new_ids.append(new_id)
            if new_id in old_ids:
                continue
            else:
                CharacterFamilyTie.objects.create(
                    character1_id=character_id,
                    character2_id=new_id,
                    relation_type_id = character['relation_type_id'],
                    biological_type_id = character['biological_type_id']
                )

        # Delete old unmatched country entries
        for old_id in old_ids:
            if old_id in new_ids:
                continue
            else:
                CharacterFamilyTie.objects.filter(
                    character1_id=character_id,
                    character2_id=old_id
                ).delete()

        return instance

class CharacterAliaseSerializer(serializers.ModelSerializer):
    character = CharacterInfoSerializer(many=False, read_only=True)
    class Meta:
        model = CharacterAliase
        fields = ('character_aliase_id', 'character', 'aliase')


class CharacterTitleSerializer(serializers.ModelSerializer):
    character = CharacterInfoSerializer(many=False, read_only=True)
    class Meta:
        model = CharacterTitle
        fields = ('character_title_id', 'character', 'title_name')

