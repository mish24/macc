from django.core.exceptions import ObjectDoesNotExist
from pcsa_GHN.models import ghnPost, Contact


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
        post = ghnPost.objects.get(pk=post_id)
        post.delete()
        is_deleted = True
    except ObjectDoesNotExist:
        pass

    return is_deleted


def get_post_by_id(post_id):

    post = None
    try:
        post = ghnPost.objects.get(pk=post_id)
    except ObjectDoesNotExist:
        pass

    return post
    
    
def create_contact_from_form(form):

    contact = None
    if form:
        contact = form.save(commit=True)
        contact.owner = owner
        contact.save()
    return contact


def delete_contact_by_id(contact_id):

    is_deleted = False
    try:
        contact = Contact.objects.get(pk=contact_id)
        contact.delete()
        is_deleted = True
    except ObjectDoesNotExist:
        pass

    return is_deleted


def get_contact_by_id(contact_id):

    contact = None
    try:
        contact = Contact.objects.get(pk=contact_id)
    except ObjectDoesNotExist:
        pass

    return contact
