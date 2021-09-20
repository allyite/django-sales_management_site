from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.template import loader
from django.db.models import Avg,Count,Sum,Min,Max

from .models import Product,Inv_item,SOrder_item
from .forms import InvItemForm,SOrderItemForm

from django.urls import reverse
from datetime import datetime
from django.contrib.auth.decorators import login_required,permission_required
from django.core.exceptions import PermissionDenied
import logging
logger = logging.getLogger(__name__) # Get an instance of a logger
from django.core.paginator import Paginator


@login_required()
@permission_required('app1.upd_inv', raise_exception=True)
def mng_inv(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = InvItemForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            
            fd= form.cleaned_data
            ii= Inv_item(**fd)
            ii.save()
            
            # update product units avail in prod table
            prd= ii.iprod
            prd.pua += ii.iu
            prd.save()
            '''
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
            '''
            
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('app1:manage_inv'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = InvItemForm()

        invitems= Inv_item.objects.all().order_by("id")
        invitems= list(zip(range(1,len(invitems)+1),invitems))
        
        #context= {"form":form, "items":invitems}
        
        paginator = Paginator(invitems, 4) # Show 25 contacts per page.
        pgno= request.GET.get('page')
        page_number = pgno if pgno else 1
        page_obj = paginator.get_page(page_number)
        if len(page_obj)==0: #needed or not? check after removing with 0 items
            page_obj= None 
        context= {"form":form, "page_obj":page_obj}
        
        return render(request, 'app1/mng_inv.html', context )
        ##orig indent= inline with if-else ##test

@login_required()
def trck_inv(request):
    if request.method == 'GET':
        '''form = InvItemForm()
        invitems= Inv_item.objects.all()
        prdids= [item["iprod"] for item in invitems.values('iprod')]
        prds= Product.objects.filter(id__in=prdids).order_by("psno")'''
        prds= Product.objects.all().order_by("id")
        context= {"items":zip(range(1,len(prds)+1),prds)}
        return render(request, 'app1/trck_inv.html', context )

@login_required()
def s_orders(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SOrderItemForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            
            fd= form.cleaned_data
            fp= int(fd["sprod"].pmrp * ((100-fd["sdisc"])/100))
            fd["sfp"]= fp
            soi= SOrder_item(**fd)
            soi.save()
            
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('app1:sales_orders'))
            
    # if a GET (or any other method) we'll create a blank form
    else:
        logger.error("Log: s_orders: GET:\n"+str(request.GET))
        
        form = SOrderItemForm()
        #logger.error("zz:"+str(fprices)) 

        sortoptions={"Order Id":"order_id","Customer Name":"cust_name",
                     "Product":"prod_name","Discount":"disc",
                     "Final Price":"fprice"}
        sortvalues={"order_id":"id","cust_name":"scust__cname",
                     "prod_name":"sprod__pname","disc":"sdisc",
                     "fprice":"sfp"}

        sortorder=""
        if request.GET.get("sortfield"):
            sortby= sortvalues[request.GET["sortfield"]]
            sorder= request.GET["sortorder"]  #asc/desc
            sortorder="-" if sorder=="desc" else sortorder
            sortkey=[request.GET.get("sortfield"),request.GET["sortorder"]]
        else:
            sortby= "id"
            sortkey= ["order_id","asc"]
        oitems= SOrder_item.objects.filter(ssold=False).order_by(sortorder+sortby)

        if request.GET.get("editid"):
            edit_oid= int(request.GET.get("editid"))
            edit_form= SOrderItemForm(instance=SOrder_item.objects.get(id=edit_oid))
        else:
            edit_oid= 0; edit_form=None
            
        context= {"form":form, "items":oitems,
                  "sortoptions":sortoptions, "sortkey":sortkey,
                  "edit_oid":edit_oid, "edit_form":edit_form}
        return render(request, 'app1/sorders.html', context )
        ##orig indent= inline with if-else ##test

@login_required()
@permission_required('app1.mng_order', raise_exception=True)
def mng_order(request,oaction,oid):
    if request.method == 'POST':
        #if not request.user.has_perm("app1.mng_order"):
        #    raise PermissionDenied()
        
        if oaction=="sell":
            oitem= SOrder_item.objects.get(id=oid)
            prod= oitem.sprod
            if prod.pua == 0:
                msg= "Product quantity available= 0.   "
                msg+= "Please go back & choose a different product.."
                return(HttpResponse(msg))
            prod.pua-=1
            prod.plpd= datetime.now()
            prod.save()
            
            cust= oitem.scust
            cust.clb= datetime.now()
            cust.clba= oitem.sfp
            cust.save()

            oitem.ssold= True
            oitem.save()
            '''
            # update product units avail in prod table
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
         '''            
        elif oaction=="del":
            oitem= SOrder_item.objects.get(id=oid)
            oitem.delete()

        elif oaction=="upd":
            #logger.error("Log: mgn_order: upd:\n"+str(request.POST))
            '''d= request.POST.dict()
            d2= request.POST
            upd_id= d["upd_id"]
            del d["upd_id"]'''
            
            d2= request.POST
            upd_id= oid

            #logger.error("Log: mgn_order: upd: usno="+str(upd_sno)+"\n"+str(d)) 
            #logger.error("Log: mgn_order: upd:"+ str(request.POST.get("upd_sno")))
            
            form = SOrderItemForm(d2)
            if form.is_valid():
                fd= form.cleaned_data
                oitems= SOrder_item.objects.filter(id=upd_id)
                #logger.error("Log: mgn_order: upd: oitems:"+str(oitems)+"\n"+str(fd))
                ### update() only works for queryset
                ### so manually ensure uniqueness by filtering on pk or checking len
                if(len(oitems)>1):
                    logger.error("Log: mgn_order: upd: Error Not Unique")
                    return HttpResponseRedirect(reverse('app1:sales_orders'))
                ### You cannot call update() on a QuerySet that has had a slice taken
                ### or can otherwise no longer be filtered.
                ### "Slice taken" means don't include any line of code
                ### such as qs[0] or qs[:5], in btw obtaining qs (model.objects.filter())
                ### and calling qs.update()
                oitems.update(**fd)
                #logger.error("Log: mgn_order: upd: n="+str(n))
                oitem= oitems[0]
                fp= int(oitem.sprod.pmrp * ((100-oitem.sdisc)/100))
                oitem.sfp= fp
                oitem.save()
            else:
                logger.error("Log: mgn_order: upd: invalid form") 
            
        logger.error("Log: mng_order: "+oaction+" "+str(oid))  
        return HttpResponseRedirect(reverse('app1:sales_orders'))
            
@login_required()
def prod(request, prodid):
    #return HttpResponse("You looked for product no-"+str(prodid))
    try:
        prd= Product.objects.get(id=prodid)
    except Product.DoesNotExist:
        raise Http404("Product id does not exist")
    #prd = get_object_or_404(Product, psno=prodid)
    '''
    pstrs= []
    for objd in Product.objects.values():
        pstr=""
        for key in objd:
            pstr+= str(objd[key]) + " "
        pstr= pstr[:-1]
        pstrs.append(pstr)
    out= "\n".join(pstrs)
    return HttpResponse(out)
    '''
    context = {
        "prd": prd,
    }
    template = loader.get_template('app1/product.html')
    return HttpResponse(template.render(context, request))
    #either above 2 lines, or below one
    #return render(request, 'app1/mng_inv.html', context)
    
        
