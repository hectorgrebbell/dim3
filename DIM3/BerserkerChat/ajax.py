from django.template import Context, loader, RequestContext
from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from chatrooms.models import Room
from django.shortcuts import render
import random, string
from chatrooms.utils.decorators import room_check_access
from chatrooms import views


@dajaxice_register
def getPrivateRoom(request, name):
    if (name != ""):
        request.session['guest_name'] = name
    rooms = Room.objects.all()
    new_name = ''.join(random.choice(string.ascii_lowercase) for x in range(2))+str(rooms.count())
    r = Room(name=new_name, slug=new_name, allow_anonymous_access=True)

    r.save()
    r = Room.objects.get(slug=new_name)
    t = loader.get_template('chatrooms/room.html')

    return simplejson.dumps({'name': new_name})


@dajaxice_register
def getRoom(request, name, room):
    print "room :" + room
    if (name != ""):
        request.session['guest_name'] = name
    r, created = Room.objects.get_or_create(name=room, slug=room, allow_anonymous_access=True)
    if (created):
        r.save()
        r = Room.objects.get(name=room)
    c = RequestContext(request, {'user':request.user,'room': r })
    t = loader.get_template('chatrooms/room.html')
    page = t.render(c)
    print page
    return simplejson.dumps({'name': "Public(" + room + ")", 'tab':page})

@dajaxice_register
def createGuestName(request, name):
    request.session['guest_name'] = name
    print name
    return name