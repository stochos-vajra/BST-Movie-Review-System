from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Movie
from . import bst


@receiver([post_save, post_delete], sender=Movie)
def rebuild_tree(sender, **kwargs):
    bst.build_tree()