import numpy as np
from collections import defaultdict
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

class MovieRecommender:
    def __init__(self):
        self.movies = {}  # movie_id -> {title, genre, description}
        self.ratings = defaultdict(dict)  # user_id -> {movie_id -> rating}
        self.user_similarity = None
        self.movie_content_similarity = None
        self.movie_features = None
        
    def add_movie(self, movie_id, title, genre, description):
        """Add a movie to the system."""
        self.movies[movie_id] = {
            'title': title,
            'genre': genre,
            'description': description
        }
        
    def add_rating(self, user_id, movie_id, rating):
        """Add a user rating for a movie."""
        if movie_id in self.movies:
            self.ratings[user_id][movie_id] = rating
            
    def build_user_similarity_matrix(self):
        """Build user similarity matrix for collaborative filtering."""
        users = list(self.ratings.keys())
        n_users = len(users)
        
        # Create user-movie rating matrix
        rating_matrix = np.zeros((n_users, len(self.movies)))
        for i, user in enumerate(users):
            for movie_id, rating in self.ratings[user].items():
                rating_matrix[i, movie_id] = rating
                
        # Calculate user similarity using cosine similarity
        self.user_similarity = cosine_similarity(rating_matrix)
        return self.user_similarity
    
    def build_content_similarity_matrix(self):
        """Build movie content similarity matrix for content-based filtering."""
        movies_data = [
            f"{self.movies[mid]['title']} {self.movies[mid]['genre']} {self.movies[mid]['description']}"
            for mid in sorted(self.movies.keys())
        ]
        
        # Create TF-IDF matrix
        tfidf = TfidfVectorizer(stop_words='english')
        self.movie_features = tfidf.fit_transform(movies_data)
        
        # Calculate movie similarity using cosine similarity
        self.movie_content_similarity = cosine_similarity(self.movie_features)
        return self.movie_content_similarity
    
    def get_collaborative_recommendations(self, user_id, n_recommendations=5):
        """Get recommendations based on collaborative filtering."""
        if user_id not in self.ratings:
            return []
            
        if self.user_similarity is None:
            self.build_user_similarity_matrix()
            
        # Find similar users
        user_idx = list(self.ratings.keys()).index(user_id)
        similar_users = np.argsort(self.user_similarity[user_idx])[::-1][1:6]  # top 5 similar users
        
        # Get movies rated by similar users but not by target user
        recommendations = defaultdict(float)
        for similar_user_idx in similar_users:
            similar_user = list(self.ratings.keys())[similar_user_idx]
            similarity = self.user_similarity[user_idx][similar_user_idx]
            
            for movie_id, rating in self.ratings[similar_user].items():
                if movie_id not in self.ratings[user_id]:
                    recommendations[movie_id] += similarity * rating
                    
        # Sort and return top N recommendations
        sorted_recommendations = sorted(recommendations.items(), 
                                     key=lambda x: x[1], 
                                     reverse=True)[:n_recommendations]
        return [(self.movies[movie_id]['title'], score) 
                for movie_id, score in sorted_recommendations]
    
    def get_content_recommendations(self, movie_id, n_recommendations=5):
        """Get recommendations based on content similarity."""
        if movie_id not in self.movies:
            return []
            
        if self.movie_content_similarity is None:
            self.build_content_similarity_matrix()
            
        # Find similar movies
        movie_idx = list(self.movies.keys()).index(movie_id)
        similar_movies = np.argsort(self.movie_content_similarity[movie_idx])[::-1][1:n_recommendations+1]
        
        return [(self.movies[list(self.movies.keys())[idx]]['title'],
                self.movie_content_similarity[movie_idx][idx])
                for idx in similar_movies]
    
    def get_hybrid_recommendations(self, user_id, n_recommendations=5):
        """Get recommendations using both collaborative and content-based filtering."""
        collaborative_recs = self.get_collaborative_recommendations(user_id, n_recommendations)
        
        # Get a recently rated movie for content-based recommendations
        recent_movie_id = None
        if user_id in self.ratings and self.ratings[user_id]:
            recent_movie_id = list(self.ratings[user_id].keys())[-1]
            
        if recent_movie_id:
            content_recs = self.get_content_recommendations(recent_movie_id, n_recommendations)
        else:
            content_recs = []
            
        # Combine and weight recommendations
        hybrid_recs = {}
        for title, score in collaborative_recs:
            hybrid_recs[title] = score * 0.7  # 70% weight to collaborative filtering
            
        for title, score in content_recs:
            if title in hybrid_recs:
                hybrid_recs[title] += score * 0.3  # 30% weight to content-based
            else:
                hybrid_recs[title] = score * 0.3
                
        # Sort and return top N recommendations
        sorted_recommendations = sorted(hybrid_recs.items(), 
                                     key=lambda x: x[1], 
                                     reverse=True)[:n_recommendations]
        return sorted_recommendations

# Example usage
def demo_recommendation_system():
    # Create recommender
    recommender = MovieRecommender()
    
    # Add some sample movies
    sample_movies = [
        (0, "The Shawshank Redemption", "Drama", "Two imprisoned men bond over a number of years."),
        (1, "The Godfather", "Crime Drama", "The aging patriarch of an organized crime dynasty transfers control."),
        (2, "The Dark Knight", "Action", "Batman fights against the Joker terrorizing Gotham City."),
        (3, "Inception", "Sci-Fi Action", "A thief who steals corporate secrets through dreams."),
        (4, "Pulp Fiction", "Crime Drama", "Various interconnected stories of criminals in Los Angeles."),
        (5, "Fight Club", "Drama", "An insomniac office worker and a soap maker form an underground fight club.")
    ]
    
    for movie_id, title, genre, desc in sample_movies:
        recommender.add_movie(movie_id, title, genre, desc)
    
    # Add some sample ratings
    sample_ratings = [
        (1, 0, 5.0),  # User 1 rates Shawshank
        (1, 1, 4.5),  # User 1 rates Godfather
        (1, 2, 4.0),  # User 1 rates Dark Knight
        (2, 0, 4.0),  # User 2 rates Shawshank
        (2, 2, 5.0),  # User 2 rates Dark Knight
        (2, 3, 4.5),  # User 2 rates Inception
        (3, 1, 5.0),  # User 3 rates Godfather
        (3, 4, 4.5),  # User 3 rates Pulp Fiction
    ]
    
    for user_id, movie_id, rating in sample_ratings:
        recommender.add_rating(user_id, movie_id, rating)
    
    # Get recommendations
    print("\nCollaborative Filtering Recommendations for User 1:")
    print(recommender.get_collaborative_recommendations(1))
    
    print("\nContent-based Recommendations for Movie 0 (Shawshank Redemption):")
    print(recommender.get_content_recommendations(0))
    
    print("\nHybrid Recommendations for User 1:")
    print(recommender.get_hybrid_recommendations(1))

if __name__ == "__main__":
    demo_recommendation_system()
