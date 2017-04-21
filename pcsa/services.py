from django.core.exceptions import ObjectDoesNotExist

from pcsa.models import PcsaPost


def create_post_from_form(form, owner):

    post = None
    if form and owner:
        post = form.save(commit=False)
        post.owner = owner
        post.save()
    return post


def delete_post_by_id(post_id):

    is_deleted = False
    try:
        post = PcsaPost.objects.get(pk=post_id)
        post.delete()
        is_deleted = True
    except ObjectDoesNotExist:
        pass

    return is_deleted


def get_post_by_id(post_id):

    post = None
    try:
        post = PcsaPost.objects.get(pk=post_id)
    except ObjectDoesNotExist:
        pass

    return post

def search_post(username, title, description):
    search_query = ghnPost.objects.all()
    """
    This function searches for the posts created by some
    particular user, title or description
    """
    if username:
        search_query = search_query.filter(owner=Pcuser.objects.filter(user__username__contains=username))
    if title:
        search_query = search_query.filter(title__contains=title)
    if description:
        search_query = search_query.filter(description__contains=description)

    return search_query

def count_posts_by_pcuser(username):

    search_query = ghnPost.objects.all()
    """
    This returns the number of total posts added
    by the Pcuser.
    In case no username is provided, it will just
    return the total number of post objects present 
    in the database
    """
    if username:
        search_query = search_query.filter(owner=Pcuser.objects.filter(user__username__contains=username))

    count = search_query.count()

    return count

def delete_posts(username):
    """
    It doesn't make sense to delete a post
    by title or username
    This can delete posts by any user, all posts by default.
    """
    search_query = ghnPost.objects.all()

    if username:
        search_query = search_query.filter(owner=Pcuser.objects.filter(user__username__contains=username))


