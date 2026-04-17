from django.core.management.base import BaseCommand
from movierecommender.models import Movie

# Fungsi untuk pastikan data genre sah (tak kosong atau cuma 'na')
def check_valid_genres(genres: str) -> bool:
    if bool(genres) and isinstance(genres, str) and not genres.isspace() and genres != 'na':
        return True
    else:
        return False

# Langkah Matematik: Kira persamaan antara dua set genre
def jaccard_similarity(list1: list, list2: list) -> float:
    s1 = set(list1)
    s2 = set(list2)
    # Formula: (A ricih B) / (A kesatuan B)
    return float(len(s1.intersection(s2)) / len(s1.union(s2)))

# Fungsi untuk bandingkan dua filem
def similarity_between_movies(movie1: Movie, movie2: Movie) -> float:
    if check_valid_genres(movie1.genres) and check_valid_genres(movie2.genres):
        # Kita split string genre jadi list (contoh: "Action Adventure" -> ["Action", "Adventure"])
        m1_generes = movie1.genres.split()
        m2_generes = movie2.genres.split()
        return jaccard_similarity(m1_generes, m2_generes)
    else:
        return 0

class Command(BaseCommand):
    help = 'Generate movie recommendations based on watched movies'

    def handle(self, *args, **kwargs):
        # Threshold 0.8 bermaksud 80% genre kena sama baru kita recommend
        THRESHOLD = 0.8
        
        # Ambil data dari database
        watched_movies = Movie.objects.filter(watched=True)
        unwatched_movies = Movie.objects.filter(watched=False)
        
        self.stdout.write(f'Mula menjana cadangan berdasarkan {watched_movies.count()} filem yang ditonton...')

        for unwatched_movie in unwatched_movies:
            max_similarity = 0
            will_recommend = False
            
            for watched_movie in watched_movies:
                similarity = similarity_between_movies(unwatched_movie, watched_movie)
                if similarity > max_similarity:
                    max_similarity = similarity
                
                # Kalau dah capai threshold, tak payah banding dengan filem lain lagi
                if max_similarity >= THRESHOLD:
                    break
            
            # Tentukan kalau movie ni layak di-recommend
            if max_similarity >= THRESHOLD:
                will_recommend = True
                print(f"Jumpa padanan: {unwatched_movie.original_title} (Score: {max_similarity})")
            
            # Update database
            unwatched_movie.recommended = will_recommend
            unwatched_movie.save()

        self.stdout.write(self.style.SUCCESS('Settle! Semua cadangan telah dikemaskini.'))