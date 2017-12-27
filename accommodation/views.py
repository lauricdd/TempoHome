from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.forms import modelformset_factory

from .models import Room, Picture
from .forms import RoomForm, PictureForm

def dashboard(request):
    return render(request, 'accommodation/dashboard.html')

# @login_required
def create_room(request):
    # formsets allow the user to store several pictures at once
    PicureFormSet = modelformset_factory(Picture, form=PictureForm)

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request
        room_form = RoomForm(request.POST)
        picture_formset = PicureFormSet(request.POST, request.FILES, queryset=Picture.objects.none())

        # check whether it's valid
        if room_form.is_valid() and picture_formset.is_valid():
            new_room = room_form.save(commit=False)
            new_room.user = request.user
            new_room.save()

            for form in picture_formset.cleaned_data:
                picture = Picture(picture=form['picture'], room=new_room)
                picture.save()

            return HttpResponseRedirect('/accommodation/rooms')
        else:
            print room_form.errors, picture_formset.errors

    # return blank forms
    else:
        room_form = RoomForm()
        picture_formset = PicureFormSet(queryset=Picture.objects.none())

    return render(request, 'accommodation/room_form.html', {'room_form': room_form, 'picture_formset': picture_formset})


class RoomList(ListView):
   model = Room