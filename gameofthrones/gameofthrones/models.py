# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class BiologicalType(models.Model):
    biological_type_id = models.AutoField(primary_key=True)
    biological_type_name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'biological_type'
        verbose_name = 'biological type'
        verbose_name_plural = 'biological types'
        ordering = ['biological_type_name']
    def __str__(self):
        return self.biological_type_name


class CharacterAliase(models.Model):
    character_aliase_id = models.AutoField(primary_key=True)
    character = models.ForeignKey('CharacterInfo', models.DO_NOTHING)
    aliase = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'character_aliase'
        verbose_name = 'character aliase'
        verbose_name_plural = 'character aliases'
        ordering = ['character', 'aliase']
    def __str__(self):
        return ':'.join([self.character, self.aliase])


class CharacterFamilyTie(models.Model):
    family_tie_id = models.AutoField(primary_key=True)
    character1 = models.ForeignKey('CharacterInfo', models.DO_NOTHING, related_name='from_character')
    character2 = models.ForeignKey('CharacterInfo', models.DO_NOTHING, related_name='to_character')
    relation_type = models.ForeignKey('RelationType', models.DO_NOTHING, blank=True, null=True)
    biological_type = models.ForeignKey(BiologicalType, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'character_family_tie'
        verbose_name = 'character family tie'
        verbose_name_plural = 'character family ties'
        ordering = ['character1', 'character2']
    def __str__(self):
        return ','.join([self.character1, self.character2, self.relation_type, self.biological_type])


class CharacterInfo(models.Model):
    character_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=100)
    is_male = models.IntegerField()
    is_main_character = models.IntegerField()
    brief_intro = models.TextField(blank=True, null=True)
    full_intro = models.TextField()
    character_url = models.CharField(unique=True, max_length=255)
    character_img_file_name = models.CharField(unique=True, max_length=100, blank=True, null=True)
    house = models.ForeignKey('House', models.DO_NOTHING, blank=True, null=True)
    culture = models.ForeignKey('Culture', models.DO_NOTHING, blank=True, null=True)

    # intermediate model ()
    character2 = models.ManyToManyField('self', through='CharacterFamilyTie', symmetrical=False, related_name='related_to')

    class Meta:
        managed = False
        db_table = 'character_info'
        verbose_name = 'character'
        verbose_name_plural = 'characters'
        ordering = ['full_name']
    def __str__(self):
        return self.full_name


class CharacterTitle(models.Model):
    character_title_id = models.AutoField(primary_key=True)
    character = models.ForeignKey(CharacterInfo, models.DO_NOTHING)
    title_name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'character_title'
        verbose_name ='character title'
        verbose_name_plural = 'character titles'
        ordering = ['character', 'title_name']
    def __str__(self):
        return ':'.join([self.character, self.title_name])


class Culture(models.Model):
    culture_id = models.AutoField(primary_key=True)
    culture_name = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'culture'
        verbose_name = 'culture'
        verbose_name_plural = 'cultures'
        ordering = ['culture_name']
    def __str__(self):
        return self.culture_name


class Episode(models.Model):
    episode_id = models.AutoField(primary_key=True)
    episode_name = models.CharField(unique=True, max_length=100)
    season_num = models.IntegerField()
    episode_num = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'episode'
        verbose_name = 'episode'
        verbose_name_plural = 'episodes'
        ordering = ['season_num', 'episode_num']
    def __str__(self):
        return self.episode_name


class House(models.Model):
    house_id = models.AutoField(primary_key=True)
    house_name = models.CharField(unique=True, max_length=100)
    house_img_file_name = models.CharField(unique=True, max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'house'
        verbose_name = 'house'
        verbose_name_plural = 'houses'
        ordering = ['house_name']
    def __str__(self):
        return self.house_name


class RelationType(models.Model):
    relation_type_id = models.AutoField(primary_key=True)
    relation_type_name = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'relation_type'
        verbose_name = 'relation type'
        verbose_name_plural = 'relation types'
        ordering = ['relation_type_name']
    def __str__(self):
        return self.relation_type_name
