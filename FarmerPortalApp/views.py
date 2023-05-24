from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
import pymysql
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import os
from datetime import date
from Blockchain import *
from Block import *

blockchain = Blockchain()
if os.path.exists('blockchain_contract.txt'):
    with open('blockchain_contract.txt', 'rb') as fileinput:
        blockchain = pickle.load(fileinput)
    fileinput.close()

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})    

def BrowseProducts(request):
    if request.method == 'GET':
        output = '<tr><td><font size="" color="black">Product&nbsp;Name</font></td><td><select name="t1">'
        for i in range(len(blockchain.chain)):
            if i > 0:
                b = blockchain.chain[i]
                data = b.transactions[0]
                data = base64.b64decode(data)
                decrypt = blockchain.decrypt(data)
                decrypt = decrypt.decode("utf-8")
                arr = decrypt.split("#")
                if arr[0] == 'addproduct':
                    output+='<option value='+arr[2]+'>'+arr[2]+'</option>'
        output+="</select></td></tr>"
        context= {'data1':output}
        return render(request, 'BrowseProducts.html', context)

def Login(request):
    if request.method == 'GET':
       return render(request, 'Login.html', {})
    
def ViewOrders(request):
    if request.method == 'GET':
        user = ''
        with open("session.txt", "r") as file:
            for line in file:
                user = line.strip('\n')
        file.close()
        output = '<table border=1 align=center>'
        output+='<tr><th><font size=3 color=black>Product Name</font></th>'
        output+='<th><font size=3 color=black>Customer Name</font></th>'
        output+='<th><font size=3 color=black>Contact No</font></th>'
        output+='<th><font size=3 color=black>Email ID</font></th>'
        output+='<th><font size=3 color=black>Address</font></th>'
        output+='<th><font size=3 color=black>Ordered Date</font></th></tr>'
        for i in range(len(blockchain.chain)):
            if i > 0:
                b = blockchain.chain[i]
                data = b.transactions[0]
                data = base64.b64decode(data)
                decrypt = blockchain.decrypt(data)
                decrypt = decrypt.decode("utf-8")
                arr = decrypt.split("#")
                if arr[0] == 'bookorder':
                    print(arr[2]+" "+user)
                    details = arr[3].split(",")
                    pid = arr[1]
                    user = arr[2]
                    book_date = arr[4]
                    output+='<tr><td><font size=3 color=black>'+pid+'</font></td>'
                    output+='<td><font size=3 color=black>'+user+'</font></td>'
                    output+='<td><font size=3 color=black>'+details[0]+'</font></td>'
                    output+='<td><font size=3 color=black>'+details[1]+'</font></td>'
                    output+='<td><font size=3 color=black>'+details[2]+'</font></td>'
                    output+='<td><font size=3 color=black>'+str(book_date)+'</font></td></tr>'
        output+="</table><br/><br/><br/><br/><br/><br/>"
        context= {'data':output}
        return render(request, 'ViewOrders.html', context)     

def Register(request):
    if request.method == 'GET':
       return render(request, 'Register.html', {})

def AddProduct(request):
    if request.method == 'GET':
       return render(request, 'AddProduct.html', {})

def BookOrder(request):
    if request.method == 'GET':
        pid = request.GET['crop']
        user = ''
        with open("session.txt", "r") as file:
            for line in file:
                user = line.strip('\n')
        file.close()
        details = ''
        for i in range(len(blockchain.chain)):
            if i > 0:
                b = blockchain.chain[i]
                data = b.transactions[0]
                data = base64.b64decode(data)
                decrypt = blockchain.decrypt(data)
                decrypt = decrypt.decode("utf-8")
                arr = decrypt.split("#")
                if arr[0] == "signup":
                    if arr[1] == user:
                        details = arr[3]+","+arr[4]+","+arr[5]
                        break
        today = date.today()            
        data = "bookorder#"+pid+"#"+user+"#"+details+"#"+str(today)
        enc = blockchain.encrypt(str(data))
        enc = str(base64.b64encode(enc),'utf-8')
        blockchain.add_new_transaction(enc)
        hash = blockchain.mine()
        b = blockchain.chain[len(blockchain.chain)-1]
        blockchain.save_object(blockchain,'blockchain_contract.txt')
        print("Previous Hash : "+str(b.previous_hash)+" Block No : "+str(b.index)+" Current Hash : "+str(b.hash))
        bc = "Previous Hash : "+str(b.previous_hash)+"<br/>Block No : "+str(b.index)+"<br/>Current Hash : "+str(b.hash)
        output = 'Your Order details Updated<br/>'+bc
        context= {'data':output}
        return render(request, 'ConsumerScreen.html', context)      

def UpdateQuantity(request):
    if request.method == 'GET':
        output = ''
        user = ''
        with open("session.txt", "r") as file:
            for line in file:
                user = line.strip('\n')
        file.close()        
        output = '<tr><td><font size="" color="black">Product&nbsp;Name</font></td><td><select name="t1">'
        for i in range(len(blockchain.chain)):
            if i > 0:
                b = blockchain.chain[i]
                data = b.transactions[0]
                data = base64.b64decode(data)
                decrypt = blockchain.decrypt(data)
                decrypt = decrypt.decode("utf-8")
                arr = decrypt.split("#")
                if arr[0] == 'addproduct':
                    if arr[1] == user:
                        output+='<option value='+arr[2]+'>'+arr[2]+'</option>'
        output+="</select></td></tr>"
        context= {'data':output}
        return render(request, 'UpdateQuantity.html', context)       
        

def SearchProductAction(request):
    if request.method == 'POST':
        ptype = request.POST.get('t1', False)
        output = '<table border=1 align=center>'
        output+='<tr><th><font size=3 color=black>Farmer Name</font></th>'
        output+='<th><font size=3 color=black>Crop Name</font></th>'
        output+='<th><font size=3 color=black>Price</font></th>'
        output+='<th><font size=3 color=black>Quantity</font></th>'
        output+='<th><font size=3 color=black>Description</font></th>'
        output+='<th><font size=3 color=black>Image</font></th>'
        output+='<th><font size=3 color=black>Purchase Crop</font></th></tr>'
        for i in range(len(blockchain.chain)):
            if i > 0:
                b = blockchain.chain[i]
                data = b.transactions[0]
                data = base64.b64decode(data)
                decrypt = blockchain.decrypt(data)
                decrypt = decrypt.decode("utf-8")
                arr = decrypt.split("#")
                if arr[0] == 'addproduct':
                    if arr[2] == ptype:
                        output+='<tr><td><font size=3 color=black>'+arr[1]+'</font></td>'
                        output+='<td><font size=3 color=black>'+arr[2]+'</font></td>'
                        output+='<td><font size=3 color=black>'+str(arr[3])+'</font></td>'
                        output+='<td><font size=3 color=black>'+str(arr[4])+'</font></td>'
                        output+='<td><font size=3 color=black>'+arr[5]+'</font></td>'
                        output+='<td><img src=/static/products/'+arr[6]+' width=200 height=200></img></td>'
                        output+='<td><a href=\'BookOrder?farmer='+arr[1]+'&crop='+arr[2]+'\'><font size=3 color=black>Click Here</font></a></td></tr>'
        output+="</table><br/><br/><br/><br/><br/><br/>"
        context= {'data':output}
        return render(request, 'SearchProducts.html', context)              
        
    
def QuantityUpdateAction(request):
    if request.method == 'POST':
        pname = request.POST.get('t1', False)
        qty = request.POST.get('t2', False)
        user = ''
        with open("session.txt", "r") as file:
            for line in file:
                user = line.strip('\n')
        file.close()
        index = 0
        record = 'none'
        for i in range(len(blockchain.chain)):
            if i > 0:
                b = blockchain.chain[i]
                data = b.transactions[0]
                data = base64.b64decode(data)
                decrypt = blockchain.decrypt(data)
                decrypt = decrypt.decode("utf-8")
                arr = decrypt.split("#")
                if arr[0] == 'addproduct':
                    if arr[1] == user and arr[2] == pname:
                        tot_qty = int(arr[4])
                        tot_qty = tot_qty + int(qty)
                        index = i
                        record = arr[0]+"#"+arr[1]+"#"+arr[2]+"#"+arr[3]+"#"+str(tot_qty)+"#"+arr[5]+"#"+arr[6]
                        break
        output = "Error in updating quantity"
        if record != 'none':
            blockchain.chain.pop(index)
            enc = blockchain.encrypt(str(record))
            enc = str(base64.b64encode(enc),'utf-8')
            blockchain.add_new_transaction(enc)
            hash = blockchain.mine()
            b = blockchain.chain[len(blockchain.chain)-1]
            print("Previous Hash : "+str(b.previous_hash)+" Block No : "+str(b.index)+" Current Hash : "+str(b.hash))
            bc = "Previous Hash : "+str(b.previous_hash)+"<br/>Block No : "+str(b.index)+"<br/>Current Hash : "+str(b.hash)
            output = 'Product Quantity Details Updated in Supply Chain Block<br/>'+bc
            blockchain.save_object(blockchain,'blockchain_contract.txt')
        context= {'data':output}
        return render(request, 'SupplierScreen.html', context)
          
                    
      

def AddProductAction(request):
    if request.method == 'POST':
        cname = request.POST.get('t1', False)
        qty = request.POST.get('t2', False)
        price = request.POST.get('t3', False)
        desc = request.POST.get('t4', False)
        image = request.FILES['t5']
        imagename = request.FILES['t5'].name
        user = ''
        with open("session.txt", "r") as file:
            for line in file:
                user = line.strip('\n')
        file.close()
        data = "addproduct#"+user+"#"+cname+"#"+price+"#"+qty+"#"+desc+"#"+imagename
        enc = blockchain.encrypt(str(data))
        enc = str(base64.b64encode(enc),'utf-8')
        blockchain.add_new_transaction(enc)
        hash = blockchain.mine()
        b = blockchain.chain[len(blockchain.chain)-1]
        print("Encrypted Data : "+str(b.transactions[0])+" Previous Hash : "+str(b.previous_hash)+" Block No : "+str(b.index)+" Current Hash : "+str(b.hash))
        bc = "Encrypted Data : "+str(b.transactions[0])+" Previous Hash : "+str(b.previous_hash)+"<br/>Block No : "+str(b.index)+"<br/>Current Hash : "+str(b.hash)
        blockchain.save_object(blockchain,'blockchain_contract.txt')
        fs = FileSystemStorage()
        filename = fs.save('FarmerPortalApp/static/products/'+imagename, image)
        context= {'data':'Signup process completd and record saved in Blockchain with below hashcodes.<br/>'+bc}
        context= {'data':'Crop details added.<br/>'+bc}
        return render(request, 'AddProduct.html', context)
        
   
def Signup(request):
    if request.method == 'POST':
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        contact = request.POST.get('contact', False)
        email = request.POST.get('email', False)
        address = request.POST.get('address', False)
        usertype = request.POST.get('type', False)
        record = 'none'
        for i in range(len(blockchain.chain)):
            if i > 0:
                b = blockchain.chain[i]
                data = b.transactions[0]
                data = base64.b64decode(data)
                decrypt = blockchain.decrypt(data)
                decrypt = decrypt.decode("utf-8")
                arr = decrypt.split("#")
                if arr[0] == "signup":
                    if arr[1] == username:
                        record = "exists"
                        break
        if record == 'none':
            data = "signup#"+username+"#"+password+"#"+contact+"#"+email+"#"+address+"#"+usertype
            enc = blockchain.encrypt(str(data))
            enc = str(base64.b64encode(enc),'utf-8')
            blockchain.add_new_transaction(enc)
            hash = blockchain.mine()
            b = blockchain.chain[len(blockchain.chain)-1]
            print("Encrypted Data : "+str(b.transactions[0])+" Previous Hash : "+str(b.previous_hash)+" Block No : "+str(b.index)+" Current Hash : "+str(b.hash))
            bc = "Encrypted Data : "+str(b.transactions[0])+" Previous Hash : "+str(b.previous_hash)+"<br/>Block No : "+str(b.index)+"<br/>Current Hash : "+str(b.hash)
            blockchain.save_object(blockchain,'blockchain_contract.txt')
            context= {'data':'Signup process completd and record saved in Blockchain with below hashcodes.<br/>'+bc}
            return render(request, 'Register.html', context)
        else:
            context= {'data':username+'Username already exists'}
            return render(request, 'Register.html', context)    



def UserLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        usertype = request.POST.get('type', False)
        status = 'none'
        for i in range(len(blockchain.chain)):
            if i > 0:
                b = blockchain.chain[i]
                data = b.transactions[0]
                data = base64.b64decode(data)
                decrypt = blockchain.decrypt(data)
                decrypt = decrypt.decode("utf-8")
                arr = decrypt.split("#")
                if arr[0] == "signup":
                    if arr[1] == username and arr[2] == password and arr[6] == usertype:
                        status = 'success'
                        break
        if status == 'success' and usertype == 'Farmer':
            file = open('session.txt','w')
            file.write(username)
            file.close()
            context= {'data':"Welcome "+username}
            return render(request, 'SupplierScreen.html', context)
        elif status == 'success' and usertype == 'Consumer':
            file = open('session.txt','w')
            file.write(username)
            file.close()
            context= {'data':"Welcome "+username}
            return render(request, 'ConsumerScreen.html', context)
        else:
            context= {'data':'Invalid login details'}
            return render(request, 'Login.html', context)            


        
        



        
            
