from django.db import models
from datetime import datetime

class Product(models.Model):
    pname= models.CharField(max_length=200)
    pmf= models.CharField(max_length=200)
    pmrp= models.IntegerField(default=-1)
    plpd= models.DateTimeField(help_text='last purchased date',default=datetime(1900,1,1))
    pua= models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.id)+": "+str(self.pname)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['pname', 'pmf'], name='unique_prod')
            ]

    
    #pub_date = models.DateTimeField('date published')
    #question = models.ForeignKey(Question, on_delete=models.CASCADE)

class Distributor(models.Model):
    dname= models.CharField(max_length=200)
    daddr= models.CharField(max_length=200)
    dcp= models.CharField(max_length=200)
    dcn= models.CharField(max_length=200)
    
    def __str__(self):
        return str(self.id)+": "+str(self.dname)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['dname'], name='unique_distrib')
            ]

class Customer(models.Model):
    cname= models.CharField(max_length=200)
    ccn= models.CharField(max_length=200)
    cmail= models.CharField(max_length=200)
    clb= models.DateTimeField(help_text='last billed date',default=datetime(1900,1,1))
    clba= models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.id)+": "+str(self.cname)

class Inv_item(models.Model):
    iprod= models.ForeignKey(Product, on_delete=models.CASCADE) #pname/pmf/pmrp
    idist= models.ForeignKey(Distributor, on_delete=models.CASCADE) #dname
    iu= models.IntegerField(default=0)
    idd= models.DateTimeField('delivered date')

    def __str__(self):
        return "Inv item id: "+ str(self.id)

    class Meta:
        permissions = [
            ("upd_inv", "manage inventory"),
        ]

class SOrder_item(models.Model):
    scust= models.ForeignKey(Customer, on_delete=models.CASCADE) #cname,ccn,ccmail
    sprod= models.ForeignKey(Product, on_delete=models.CASCADE) #pname/pmf/pmrp(apply sdisc)
    sdisc= models.IntegerField(default=0)
    sfp= models.IntegerField(default=-1)
    ssold= models.BooleanField(default=False)

    def __str__(self):
        return "SOrder id: "+ str(self.id)

    class Meta:
        permissions = [
            ("mng_order", "sell/del/edit sales order"),
        ]



    
    
    

