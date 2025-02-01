
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Model, ImageField, CharField, IntegerField, IntegerChoices, ForeignKey, CASCADE, \
    SmallIntegerField, DecimalField, TextChoices


# Create your models here.


class Book(Model):
    class NumberType(IntegerChoices):
        ONE = 1 , '1'
        TWO = 2 , '2'
        THREE = 3 , '3'
        FOUR = 4 , '4'
        FIVE = 5 , '5'
        SIX = 6 , '6'
    name = CharField(max_length=255)
    image = ImageField(upload_to='images/books/')
    number = IntegerField(choices=NumberType)

class Unit(Model):
    book = ForeignKey('essential.Book' , CASCADE , related_name='units')
    number = SmallIntegerField(validators=[MaxValueValidator(30) , MinValueValidator(1)])
    name = CharField(max_length=255)


class Word(Model):
    class WorkType(TextChoices):
        NOUN = "noun" , 'Noun'
        PRONOUN = 'pronoun' , 'Pronoun'
        VERB = 'verb' , 'Verb'
        ADJECTIVE = 'adjective' , 'Adjective'
        ADVERB = 'adverb' , 'Adverb'
    uz = CharField(max_length=255)
    en = CharField(max_length=255)
    pronunciation = CharField(max_length=255)
    type = CharField(max_length=255 , choices=WorkType)
    definition = CharField(max_length=400)
    sentence = CharField(max_length=500)
    image = ImageField(upload_to='images/words/')
    unit = ForeignKey('essential.Unit' , CASCADE , related_name='words')
