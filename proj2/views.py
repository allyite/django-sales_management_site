from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.template import loader
from django.db.models import Avg,Count,Sum,Min,Max


from django.urls import reverse
from datetime import datetime
from django.contrib.auth.decorators import login_required,permission_required
from django.core.exceptions import PermissionDenied
import logging
logger = logging.getLogger(__name__) # Get an instance of a logger


def parent_url_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('homeview'))
    else:
        return HttpResponseRedirect(reverse('login'))

@login_required()
def homeview(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        '''
        # create a form instance and populate it with data from the request:
        form = InvItemForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            
            fd= form.cleaned_data
            iis= Inv_item.objects.all().order_by("-isno")
            if len(iis)==0:
                fd["isno"]= 1
            else:
                fd["isno"]= iis[0].isno + 1
            ii= Inv_item(**fd)
            ii.save()
            
            # update product units avail in prod table
            prd= ii.iprod
            prd.pua += ii.iu
            prd.save()
            
            invitems= Inv_item.objects.all()
            prdids= [item["iprod"] for item in invitems.values('iprod')]
            pu={}
            for prdid in prdids:
                f= invitems.filter(iprod__id=prdid).aggregate(f1=Sum('iu'))
                tunits= f['f1']
                pu[prdid]=  tunits
                prd= Product.objects.get(id=prdid)
                prd.pua= tunits
                prd.save()
            
            
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('app1:manage_inv'))
        '''
        pass

    # if a GET (or any other method) 
    else:

        uid= request.user.id

        s= r"http://127.0.0.1:8000/"
        lproj= [ ("Logout",s+"logout"),("Login",s+"login"),("Home",s+"home") ]

        s= r"http://127.0.0.1:8000/a1/"
        lapp1= [ ("Manage inventory",s+"minv"),
                 ("Track inventory",s+"tinv"),
                 ("Sales orders",s+"orders"),
                 ("Product info",s+"prod/1"),
                 ]

        s= r"http://127.0.0.1:8000/a2/"
        lapp2= [ ("Manage users",s+"users"),
                 ("View profile",s+"users/profile/"+str(uid)),
                 ]

        links=[lproj, lapp1, lapp2]    #links= [ [(title,link),] , ]
                  
        context= {"links":links} 
        return render(request, 'proj/home.html', context )
        
