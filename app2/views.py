from django.shortcuts import render

from django.urls import reverse
from datetime import datetime
from django.contrib.auth.decorators import login_required,permission_required
from django.core.exceptions import PermissionDenied
import logging
logger = logging.getLogger(__name__) # Get an instance of a logger
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,Http404

from app2.admin import UserChangeForm as UserForm
from app2.models import User1
# Create your views here.


@login_required()
@permission_required('app2.mng_users', raise_exception=True)
def users(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        '''
        # create a form instance and populate it with data from the request:
        form = SOrderItemForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            
            fd= form.cleaned_data
            so= SOrder_item.objects.all().order_by("-ssno")
            if len(so)==0:
                fd["ssno"]= 1
            else:
                fd["ssno"]= so[0].ssno + 1
            fp= int(fd["sprod"].pmrp * ((100-fd["sdisc"])/100))
            fd["sfp"]= fp
            soi= SOrder_item(**fd)
            soi.save()
        '''
        # redirect to a new URL:
        return HttpResponseRedirect(reverse('app2:users'))
            
    # if a GET (or any other method) we'll create a blank form
    else:
        uitems= User1.objects.all().order_by("username")
        snos= range(1,len(uitems)+1)

        context= {"items":zip(snos,uitems)}
        return render(request, 'app2/upd_users.html', context )
        ##orig indent= inline with if-else ##test


@login_required()
def mng_user(request,uaction,uid):
    logger.error(uaction+str(uid)+str(request.user.id))
    if request.method == 'POST':
        logger.error(uaction+str(uid)+str(request.user.id))
        req_user= User1.objects.get(id=request.user.id)
        prof_user= User1.objects.get(id=uid)
        if req_user.has_perm("app2.mng_users"):
            if(uaction=="Activate"):
                prof_user.is_active= True; prof_user.save()
            elif(uaction=="Deactivate"):
                prof_user.is_active= False; prof_user.save()
            elif(uaction=="Change_Pwd"):
                prof_user.set_password(request.POST["new_pwd"])
                prof_user.save()
        elif request.user.id==uid:
            if(uaction=="Change_Pwd"):
                if prof_user.check_password(request.POST["old_pwd"]):
                    prof_user.set_password(request.POST["new_pwd"])
                    prof_user.save()
                else:
                    return HttpResponse("Wrong current-password entered..!")
        else:
            raise PermissionDenied()

        nexturl=request.POST.get("next_url")
        if nexturl:
            nurl= nexturl.split("|")[0]; nargs= nexturl.split("|")[1:]
            return HttpResponseRedirect(reverse(nurl,args=nargs))
        else:
            return HttpResponseRedirect(reverse('app2:users'))

@login_required()
def view_prof(request,uid):
    if request.method == 'GET':
        req_user= User1.objects.get(id=request.user.id)
        prof_user= User1.objects.get(id=uid)
        '''user= User1.objects.get(id=uid)
        if request.user.has_perm("app2.view_profile",obj=user):'''
        if uid==request.user.id or req_user.has_perm("app2.mng_users"):
            context={"user":prof_user}
            return render(request, 'app2/view_profile.html', context )
        else:
            raise PermissionDenied()
            
    
    
