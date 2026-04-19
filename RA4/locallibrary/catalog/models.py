from django.db import models

from django.urls import reverse # S'utilitza per generar URLs invertint els patrons d'URL

import uuid # Requerit per a instàncies de llibres úniques



class Genre(models.Model):

    """Model que representa un gènere literari (p. ex. Ciència-ficció)."""

    name = models.CharField(max_length=200, help_text='Introdueix un gènere de llibre (p. ex. Ciència-ficció)')



    def __str__(self):

        return self.name



class Book(models.Model):

    """Model que representa un llibre (però no una còpia específica)."""

    title = models.CharField(max_length=200)

    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    summary = models.TextField(max_length=1000, help_text='Escriu una breu descripció del llibre')

    isbn = models.CharField('ISBN', max_length=13, unique=True, help_text='13 Caràcters <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    

    # ManyToManyField s'utilitza perquè un gènere pot tenir molts llibres i un llibre molts gèneres.
    genre = models.ManyToManyField(Genre, help_text='Selecciona un gènere per a aquest llibre')

    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)



    def __str__(self):

        return self.title



    def get_absolute_url(self):

        """Retorna l'URL per accedir a una instància detallada d'aquest llibre."""

        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):

        """Creates a string for the Genre. This is required to display genre in Admin."""

        return ', '.join([ genre.name for genre in self.genre.all()[:3] ])

    display_genre.short_description = 'Genre'



class BookInstance(models.Model):

    """Model que representa una còpia específica d'un llibre (que es pot prestar)."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='ID únic per a aquest llibre a tota la biblioteca')

    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)

    imprint = models.CharField(max_length=200)

    due_back = models.DateField(null=True, blank=True)



    LOAN_STATUS = (

        ('m', 'Manteniment'),

        ('o', 'En préstec'),

        ('a', 'Disponible'),

        ('r', 'Reservat'),

    )



    status = models.CharField(

        max_length=1,

        choices=LOAN_STATUS,

        blank=True,

        default='m',

        help_text='Disponibilitat del llibre',

    )



    class Meta:

        ordering = ['due_back']



    def __str__(self):
        return f'{self.id} ({self.book.title})'

class Author(models.Model):
    """Model que representa un autor."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Mort', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Retorna l'URL per accedir a una instància d'autor específica."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """Cadena per representar l'objecte del Model."""
        return f'{self.last_name}, {self.first_name}'

class Language(models.Model):
    """Model que representa un llenguatge (p. ex. Anglès, Francès, Japonès, etc.)"""
    name = models.CharField(max_length=200, help_text="Introdueix el llenguatge natural del llibre (p. ex. Anglès, Francès, Japonès, etc.)")

    def __str__(self):
        """String que representa l'objecte Model (en el lloc d'Administració, etc.)"""
        return self.name
