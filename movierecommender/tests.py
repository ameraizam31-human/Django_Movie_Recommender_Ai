from .models import Movie
from django.shortcuts import render

def generate_movies_context():
    context = {}
    # Mencari bilangan movie yang ditanda sebagai 'recommended'
    recommended_count = Movie.objects.filter(recommended=True).count()
    
    # Jika tiada yang ditanda, ambil 30 movie paling popular
    if recommended_count == 0:
        movies = Movie.objects.filter(watched=False).order_by('-vote_count')[:30]
    else:
        # Jika ada, ambil movie yang belum ditonton dan disyorkan
        movies = Movie.objects.filter(watched=False).filter(recommended=True)
        
    context['movie_list'] = movies
    return context

def movie_recommendation_view(request):
    if request.method == "GET":
      # Memanggil fungsi context yang dicipta di atas
      context = generate_movies_context()
      # Menghantar data ke template movie_list.html
      return render(request, 'movierecommender/movie_list.html', context)