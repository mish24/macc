from django.core.exceptions import ObjectDoesNotExist

from pcsa.models import PcsaPost

from signup.models import Pcuser


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

def create_post(owner, title, description):
    """
    Creates a post when the owner, title and
    description all three are provided. 
    """
    post = None

    if owner and title and description:
        #create an object of the model only
        #all the three parameters are present
        post = PcsaPost.objects.create(owner=owner,
                    title=title,
                    description=description
                    )
        post.save()

    return post

def search_post(username, title, description):
    """
    Searches for a typical post by any of the three parameters
    If none is provided, entire list of posts is returned.
    Any part of the description of the title might be provided
    """
    search_query = PcsaPost.objects.all()

    if username:
        search_query = search_query.filter(owner=Pcuser.objects.filter(user__username__contains=username))
    if title:
        search_query = search_query.filter(title__contains=title)
    if description:
        search_query = search_query.filter(description__contains=description)

    return search_query

def count_number_of_posts(username):
    """
    Returns the total number of posts by any user.
    In case no parameter is given, it returns a list of all
    the posts in the pcsa model
    """
    search_query = PcsaPost.objects.all()
    if username:
        search_query = search_query.filter(owner=Pcuser.objects.filter(user__username__contains=username))

    count = search_query.count()

    return count

def delete_posts(username):
    """
    This function deletes the post by any user altogether
    In case no parameter is given, it deletes all the posts
    """
    search_query = PcsaPost.objects.all()

    if username:
        search_query = search_query.filter(owner=Pcuser.objects.filter(user__username__contains=username))

    search_query.delele()

    