from django.shortcuts import render
from django.http import HttpResponse
from .models import Product,Contact,Orders,OrderUpdate
from math import ceil
# from PayTm import Checksum
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
# def index(request):
#   products=Product.objects.all()
#   print(products)
#   n=len(products)
#   nSlides=n//4+ceil((n/4)-(n//4))
#   allProds=[[products,range(1,nSlides),nSlides],[products,range(1,nSlides),nSlides]]
#   # params={'no_of_slides':nSlides,'range':range(1,nSlides),'product':products}
#   params={'allProds':allProds}
#   return render(request, 'shop/index.html',params)

def index(request):
    allProds=[]
    catProds=Product.objects.values('category','id')
    cats={item['category'] for item in catProds}
    for cat in cats:
        prod=Product.objects.filter(category=cat)
        n=len(prod)
        nSlides=n//4+ceil((n/4)-(n//4))
        allProds.append([prod,range(1,nSlides),nSlides])
    params={'allProds':allProds}
    return render(request,'shop/index.html',params)

def searchMatch(query,item):
    if query in item.product_desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query=request.GET.get('search')
    allProds=[]
    catProds=Product.objects.values('category','id')
    cats={item['category'] for item in catProds}
    for cat in cats:
        prodtemp=Product.objects.filter(category=cat)
        prod=[item for item in prodtemp if searchMatch(query,item)]
        n=len(prod)
        nSlides=n//4+ceil((n/4)-(n//4))
        if len(prod)!=0:
            allProds.append([prod,range(1,nSlides),nSlides])
    params={'allProds':allProds,'msg':""}
    if len(allProds)==0 or len(query)<4:
        params={'msg':"Please make sure to enter relevant search query"}
    return render(request,'shop/search.html',params)


def prodview(request,myid):
    product=Product.objects.filter(id=myid)
    print(product)
    return render(request,'shop/prodview.html',{'product':product[0]})

def about(request):
    return render(request,'shop/about.html')

def checkout(request):
    if request.method=='POST':
        items_json1=request.POST.get('itemsJson','')
        name1=request.POST.get('name','')
        email1=request.POST.get('email','')
        amount=request.POST.get('amount','')
        address1=request.POST.get('address1','')+" "+request.POST.get('address2',' ')
        state1=request.POST.get('state','')
        city1=request.POST.get('city','')
        zip1=request.POST.get('zip','')
        phone1=request.POST.get('phone','')
        order=Orders(items_json=items_json1,name=name1,email=email1,address=address1,state=state1,city=
            city1,zip_code=zip1,phone=phone1,amount=amount)
        order.save()
        update=OrderUpdate(order_id=order.order_id,update_desc="The order has been placed")
        update.save()
        id=order.order_id
        thank=True
        return render(request,'shop/checkout.html',{'thank':thank,'id':id})
    return render(request,'shop/checkout.html')

def contact(request):
    if request.method=='POST':
        name1=request.POST.get('name','')
        email1=request.POST.get('email','')
        phone1=request.POST.get('phone','')
        desc1=request.POST.get('desc','')
        print(name1,email1,phone1,desc1)
        contact=Contact(name=name1,email=email1,phone=phone1,desc=desc1)
        contact.save()
        thank=True
        id=order.order_id
    return render(request, 'shop/contact.html',{'thank':thank,'id':id})


def tracker(request):
    if request.method=='POST':
        orderId=request.POST.get('orderId','')
        email=request.POST.get('email','')       
        try:
            order=Orders.objects.filter(order_id=orderId,email=email)
            if len(order)>0:
                update=OrderUpdate.objects.filter(order_id=orderId)
                updates=[]
                for item in update:
                    updates.append({'text':item.update_desc,'time':item.timestamp})
                    response=json.dumps({'status':'success','updates':updates,'itemsjson':order[0].items_json},default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')


    return render(request,'shop/tracker.html')