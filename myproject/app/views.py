from django.shortcuts import render, redirect
from .models import Movie, Review
from . import bst


def home(request):

    return render(request, "index.html", {"data": bst.tree.top_rated(5)})


def search(request):
    query = request.GET.get("search_movie", "").strip()
    results = bst.tree.search_name(query) if query else []

    return render(request, "movie_list.html", {
        "op": results,
        "query": query,
        "all_movies": sorted(bst.tree.inorder(), key=lambda m: m.name.lower()),
    })


def movies(request):
    genre = request.GET.get("genre", "")
    sort = request.GET.get("sort", "rating")

    if sort == "low":
        # in-order traversal: low -> high
        movie_list = bst.tree.inorder()
        if genre:
            movie_list = [m for m in movie_list if m.genre.lower() == genre.lower()]
    else:
        # reverse in-order: high -> low
        movie_list = bst.tree.filter_genre(genre) if genre else bst.tree.top_rated()

        if sort == "name":
            movie_list = sorted(movie_list, key=lambda m: m.name.lower())
        elif sort == "year":
            movie_list = sorted(movie_list, key=lambda m: m.year, reverse=True)
        elif sort == "old":
            movie_list = sorted(movie_list, key=lambda m: m.year)

    return render(request, "movies.html", {
        "movies": movie_list,
        "genres": bst.tree.all_genres(),
        "selected_genre": genre,
        "sort": sort,
    })
def reviews(request):
    if request.method == "POST":
        Review.objects.create(
            movie_id=request.POST["movie"],
            user=request.POST["user"],
            rating=request.POST["rating"],
            comment=request.POST["comment"],
        )
        return redirect("reviews")

    return render(request, "reviews.html", {
        "movies": Movie.objects.all(),
        "reviews": Review.objects.select_related("movie").order_by("-created"),
    })


def show(request):
    query = request.GET.get("search_movie", "").strip()
    results = bst.tree.search_name(query) if query else []
    
    return render(request, "movie_list.html", {
            "op": results,
            "query": query,
            "all_movies": sorted(bst.tree.inorder(), key=lambda m: m.name.lower()),
        })
    