class Node:
    def __init__(self, movie):
        self.movie = movie          # Django Movie object
        self.key = (float(movie.rating), movie.name.lower())
        self.left = None
        self.right = None


class MovieBST:
    def __init__(self):
        self.root = None
        self.size = 0

    # ---------- INSERT ----------
    def insert(self, movie):
        node = Node(movie)
        if self.root is None:
            self.root = node
            self.size += 1
            return
        cur = self.root
        while True:
            if node.key < cur.key:
                if cur.left is None:
                    cur.left = node
                    break
                cur = cur.left
            elif node.key > cur.key:
                if cur.right is None:
                    cur.right = node
                    break
                cur = cur.right
            else:
                return  # same movie, skip
        self.size += 1

    # ---------- SEARCH BY NAME ----------
    # BST rating ma sorted xa, so name search ma traversal garnu parcha
    def search_name(self, text):
        text = text.lower()
        return [m for m in self.inorder() if text in m.name.lower()]

    # ---------- SEARCH BY EXACT RATING ----------
    def search_rating(self, rating):
        rating = float(rating)
        result = []
        cur = self.root
        while cur:
            r = cur.key[0]
            if rating == r:
                result.append(cur.movie)
                cur = cur.left   # same rating left ma pani hunasakcha
            elif rating < r:
                cur = cur.left
            else:
                cur = cur.right
        return result

    # ---------- IN-ORDER (low -> high) ----------
    def inorder(self):
        result, stack, cur = [], [], self.root
        while stack or cur:
            while cur:
                stack.append(cur)
                cur = cur.left
            cur = stack.pop()
            result.append(cur.movie)
            cur = cur.right
        return result

    # ---------- REVERSE IN-ORDER (high -> low) ----------
    def top_rated(self, n=None):
        result, stack, cur = [], [], self.root
        while stack or cur:
            while cur:
                stack.append(cur)
                cur = cur.right
            cur = stack.pop()
            result.append(cur.movie)
            if n and len(result) == n:
                break
            cur = cur.left
        return result

    # ---------- RANGE SEARCH (min <= rating <= max) ----------
    def range_search(self, low, high):
        low, high = float(low), float(high)
        result = []

        def walk(node):
            if not node:
                return
            r = node.key[0]
            if r > low:
                walk(node.left)
            if low <= r <= high:
                result.append(node.movie)
            if r < high:
                walk(node.right)

        walk(self.root)
        return result

    # ---------- FILTER BY GENRE ----------
    def filter_genre(self, genre):
        return [m for m in self.top_rated() if m.genre.lower() == genre.lower()]

    # ---------- OTHER ----------
    def all_genres(self):
        return sorted({m.genre for m in self.inorder()})

    def sorted_by(self, field):
        movies = self.top_rated()
        if field == 'name':
            return sorted(movies, key=lambda m: m.name.lower())
        if field == 'year':
            return sorted(movies, key=lambda m: m.year, reverse=True)
        return movies


# ---------- Global tree (server chaleko bela ek patak) ----------
tree = MovieBST()


def build_tree():
    from .models import Movie
    global tree
    tree = MovieBST()
    for m in Movie.objects.all():
        tree.insert(m)