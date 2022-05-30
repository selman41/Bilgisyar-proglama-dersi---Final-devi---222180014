from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes,APIView
from rest_framework.response import Response
from .models import Wallet
from .serializers import WalletSerializer
import string,random,hashlib,datetime,hmac,base64,json
from django.utils import timezone
from django.shortcuts import render
import dateutil.parser


@api_view(['GET', 'POST'])
def WalletList(request,format = None):
    if request.method == 'GET':
        objs = Wallet.objects.all()
        serializer = WalletSerializer(objs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = WalletSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def WalletDetail(request, pk,format = None):

    try:
        obj = Wallet.objects.filter(wallet2store_details= pk)
    except Wallet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = WalletSerializer(obj,many=True)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = WalletSerializer(obj, data=request.data,many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def updateHMAC(obj):
    
    '''
    msg = hashlib.md5()
    msg.update(str(obj.id))
    msg.update(str(obj.transaction_amount))
    msg.update(str(obj.transaction_time))
    msg.update(str(obj.wallet2store_details))
    #Personal salt
    msg.update('x7lsvtrl^&*')
    obj.hmac_or_checksum = msg.hexdigest()
    obj.save()
    '''
    
    message = (str(obj.id) + str(obj.transaction_amount) + str(obj.transaction_time) + str(obj.wallet2store_details)).encode('utf-8')
    secret = (str('x7lsvtrl^&*')).encode('utf-8')
    signature = base64.b64encode(hmac.new(secret, message, digestmod=hashlib.sha256).digest())
    obj.hmac_or_checksum = signature
    obj.save()


@api_view(['GET','POST'])
def getAmountinWalletforStore(request,format = None):
    if request.method == 'GET':
        return Response('Current amount available page. Data fields for POST are: store_id')
    elif request.method == 'POST':
        print "Inside"
        received_json_data = json.loads(request.body)
        try:
            store_id = received_json_data["store_id"]
            wallet_list = Wallet.objects.filter(wallet2store_details = store_id,debit_or_credit = False)
        except :
            return Response("ERROR! Invalid data field sent in POST. Please try again")
        
        print wallet_list
        current_amount = 0
        curr_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for obj in wallet_list:
            t=(obj.expiry_time_of_credited_amount).strftime("%Y-%m-%d %H:%M:%S")
            if(obj.debit_or_credit == False and str(t) > str(curr_date)):
                print "Loop"
                current_amount += obj.curr_available_amount_if_credit_row
        json_data = {}
        json_data['current_time'] = curr_date
        json_data['current_amount'] = current_amount
        return Response(json_data)
    else:
        pass


def transaction_id(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def createWalletRecord(debit_or_credit,amount,method,remarks,store_id,obj,expiry_date=None):
    new_wallet_obj = Wallet()
    new_wallet_obj.debit_or_credit = debit_or_credit
    new_wallet_obj.transaction_amount = amount
    if(debit_or_credit == False):
        new_wallet_obj.curr_available_amount_if_credit_row = amount
    else:
        new_wallet_obj.curr_available_amount_if_credit_row = 0.0
    if remarks == None or remarks == "":
        remarks = 'Transaction'
    new_wallet_obj.remarks = remarks
    new_wallet_obj.transaction_method_record_unique_id = transaction_id()
    if expiry_date != None:
        new_wallet_obj.expiry_time_of_credited_amount = expiry_date

    new_wallet_obj.wallet_debit_record2wallet_credit_record = obj
    new_wallet_obj.wallet2store_details = store_id
    new_wallet_obj.hmac_or_checksum = "temp_HMAC"
    new_wallet_obj.is_deleted = 0
    new_wallet_obj.save()
  
    updateHMAC(new_wallet_obj)



def createDebitCreditrecord(amount,method,remarks,store_id,expiry_date=None):
    if method == 'Credit' or method == 'credit':
        debit_or_credit = False
        createWalletRecord(debit_or_credit,amount,method,remarks,store_id,None,expiry_date)
        return str("Credit Successful")
    #*************************************************
    #DEBIT TRANSACTION METHOD
    #*************************************************
    elif method == 'Debit' or method == 'debit':
        debit_or_credit = True
        available_amount = 0
        amount_to_debit = float(amount)
        print store_id
        wallet_list = Wallet.objects.filter(wallet2store_details= store_id,debit_or_credit = False).order_by('expiry_time_of_credited_amount')
        print wallet_list

        for obj in wallet_list:
            if(obj.is_deleted == "0" and obj.curr_available_amount_if_credit_row > 0.0):
                available_amount += obj.curr_available_amount_if_credit_row

        print available_amount,amount_to_debit
        if (float(available_amount) > float(amount_to_debit)):
            for obj in wallet_list:
                    print "INSIDE"
                    if(amount_to_debit == 0.0):
                        return
                    if(obj.curr_available_amount_if_credit_row >= amount_to_debit):
                        obj.curr_available_amount_if_credit_row -= amount_to_debit
                        obj.save()
                  
                        
                        new_amount = amount_to_debit
                        createWalletRecord(debit_or_credit,new_amount,method,remarks,store_id,obj)
                        amount_to_debit = 0.0
                    else:
                        amount_to_debit -= obj.curr_available_amount_if_credit_row
                        createWalletRecord(debit_or_credit,obj.curr_available_amount_if_credit_row,method,remarks,store_id,obj)
                        obj.curr_available_amount_if_credit_row = 0.0
                        obj.save()
        else:
            return str('Insufficient Funds!')
        if(amount_to_debit == 0.0):
            return str('Debit Successful!')
        else:
            return str('ERROR!')



@api_view(['GET', 'POST'])
def debitView(request,format = None):
    if request.method == 'GET':
        return Response('You have arrived at the transaction page. Fields to send the post data to are:'
                        'Store ID, '
                        'amount, '
                        'method, '
                        'remarks '
                        'expiry_date(ONLY for CREDIT)'
                        )

    elif request.method == 'POST':
        received_json_data = json.loads(request.body)
        try:
            store_id = received_json_data["ID"]
            amount = received_json_data["amount"]
            method = received_json_data["method"]
            remarks = received_json_data["remarks"]
        except:
            return Response("ERROR! Invalid data sent.Please try again!")
        try:
            recv_date = received_json_data["expiry_date"]
            expiry_date = dateutil.parser.parse(recv_date)
        except:
            if method == 'credit' or method == 'Credit':
                expiry_date = datetime.datetime(year=2030, month=1, day=1, hour=00, minute=00,second=00)
                response = str(createDebitCreditrecord(amount,method,remarks,store_id,expiry_date))
            else:
                response = str(createDebitCreditrecord(amount,method,remarks,store_id))


        return Response(response)
    else:
        pass
