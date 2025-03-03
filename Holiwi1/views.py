from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie

import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64

# Create your views here.
def home(request):
    #return render(request, 'home.html')
    #return render(request, "home.html",{'name': "Juan Jacome"})
    searchTerm = request.GET.get('searchMovie')
    if  searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request,'home.html',{'searchterm': searchTerm, 'movies': movies})


def about(request):
    return render(request,'about.html')

def statistics_year_view(request):
    matplotlib.use('Agg')

    # Obtener todos los años de las películas
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('year')

    # Crear un diccionario para almacenar la cantidad de películas por año
    movie_counts_by_year = {}

    # Contar la cantidad de películas por año
    for year in years:
        if year:
            movies_in_year = Movie.objects.filter(year=year)
        else:
            movies_in_year = Movie.objects.filter(year__isnull=True)
            year = "None"

        count = movies_in_year.count()
        movie_counts_by_year[year] = count

    # Ancho de las barras y separación
    bar_width = 0.5  
    bar_positions = range(len(movie_counts_by_year))  

    # Crear la gráfica de barras
    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center')

    # Personalizar la gráfica
    plt.title('Movies per Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)

    # Ajustar el espaciado entre las barras
    plt.subplots_adjust(bottom=0.3)

    # Guardar la gráfica en un objeto BytesIO
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Convertir la gráfica a base64
    image_png = buffer.getvalue()
    buffer.close()
    graphic_year = base64.b64encode(image_png).decode('utf-8')

    return graphic_year

def statistics_genre_view(request):
    matplotlib.use('Agg')

    # Obtener todos los géneros de las películas
    genres = Movie.objects.values_list('genre', flat=True).distinct()

    # Crear un diccionario para almacenar la cantidad de películas por género
    movie_counts_by_genre = {}

    # Contar la cantidad de películas por género
    for genre_list in genres:
        if genre_list:
            # Split the genres by comma and strip whitespace
            individual_genres = [genre.strip() for genre in genre_list.split(',')]
            for genre in individual_genres:
                if genre in movie_counts_by_genre:
                    movie_counts_by_genre[genre] += 1
                else:
                    movie_counts_by_genre[genre] = 1

    # Sort genres by count and select top N
    top_n = 10  # Change this to the number of top genres you want to display
    sorted_genres = sorted(movie_counts_by_genre.items(), key=lambda x: x[1], reverse=True)[:top_n]
    movie_counts_by_genre = dict(sorted_genres)

    # Crear la gráfica de barras
    plt.figure(figsize=(12, 6))  # Adjust the size as needed
    plt.barh(list(movie_counts_by_genre.keys()), list(movie_counts_by_genre.values()), height=0.5)

    # Personalizar la gráfica
    plt.title('Movies per Genre')
    plt.xlabel('Number of Movies')
    plt.ylabel('Genre')

    # Ajustar el espaciado entre las barras
    plt.subplots_adjust(left=0.2, right=0.95, top=0.9, bottom=0.1)

    # Guardar la gráfica en un objeto BytesIO
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Convertir la gráfica a base64
    image_png = buffer.getvalue()
    buffer.close()
    graphic_genre = base64.b64encode(image_png).decode('utf-8')

    return graphic_genre

def statistics_view(request):
    graphic_year = statistics_year_view(request)
    graphic_genre = statistics_genre_view(request)

    return render(request, 'statistics.html', {'graphic_year': graphic_year, 'graphic_genre': graphic_genre})