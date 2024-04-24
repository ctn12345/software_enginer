# views.py
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt
from django.db import connections
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
import os
from .models import *
import json
from datetime import datetime

@csrf_exempt
@require_POST
def login(request):
    if request.method == "POST":
        # 从POST数据中获取用户名和密码
        customer_data = json.loads(request.body)
        is_root=customer_data.get('is_root')
        print(is_root)
        if(is_root=='false'):
            username = customer_data.get('username',False)
            password = customer_data.get('password',False)
            print(username)
            try:
                user = Travel_agencies.objects.get(account=username)
            except Travel_agencies.DoesNotExist:
                user = None
            print(user)
            if user is not None:
                if user.password==password:
                    print("登录成功")
                    return JsonResponse({'status': 'success',
                                         'accout':user.account,
                                         'phone_number':user.phone_number,
                                         'password':user.password,
                                         'travel_name':user.travel_name,
                                         'is_root':False
                                         })
                else :
                    print("密码错误")
                    return JsonResponse({
                                         'status': 'failed',
                                         'message':'password fail'
                                         })
            else:
                print("账号不存在")
                return JsonResponse({'status': 'failed',
                                     'message': 'account do not exist'
                                     })
            # User not found, return an error response
            # return JsonResponse({'status': 'error', 'message': 'Invalid login credentials'})
        # 将数据转换为 JSON 格式
        # serialized_data = [{'id': item.id} for item in data]
        # 返回 JSON 响应
        # return HttpResponse('successful')
        # return JsonResponse({'status': 'success', 'data': serialized_data})
        else:
            username = customer_data.get('username', False)
            password = customer_data.get('password', False)
            print(username)
            try:
                user = root_user.objects.get(account=username)
            except root_user.DoesNotExist:
                user = None
            if user is not None:
                if user.password == password:
                    print("登录成功")
                    return JsonResponse({'status': 'success',
                                         'accout': user.account,
                                         'name': user.name,
                                         'password': user.password,
                                         'work': user.work,
                                         'is_root': True
                                         })
                else:
                    print("密码错误")
                    return JsonResponse({
                        'status': 'failed',
                        'message': 'password fail'
                    })
            else:
                print("账号不存在")
                return JsonResponse({'status': 'failed',
                                     'message': 'account do not exist'
                                     })
    # 如果不是 GET 请求，返回错误响应
    else:
        return JsonResponse({'status': 'failed'})


@csrf_exempt
@require_POST
def flight_search(request):
    print(request.method)
    if request.method == 'POST':
       customer_data = json.loads(request.body)
       travel_name = customer_data.get('travel_name')
       from_location = customer_data.get('from_location')
       destination = customer_data.get('destination')
       departure_time = customer_data.get('departureTime')
       departure_time = departure_time.split('T')[0]
       print('location ',from_location,' desti', destination, ' time ', departure_time)
       try:
            departure_date = datetime.fromisoformat(departure_time).date()
       except ValueError:
            return JsonResponse({'error': 'Invalid date format'}, status=400)
       
       # 查询数据库，获取符合条件的航班
       matching_flights = flight.objects.filter(from_date__date=departure_date,from_location=from_location,destination=destination).values()
       if matching_flights.exists():
            
            flights_data = list(matching_flights)
            for flight_temp in flights_data:
                flight_temp['status'] = "success"
                flight_temp['travel_name'] = travel_name
            # dic_flights_data = flights_data[0]
            return JsonResponse(flights_data,
                                json_dumps_params={'default': str},
                                safe=False,
                                encoder=DjangoJSONEncoder)    
       else:
           print("no")
           flights_data = [{'status':'not exist', 'from_date':departure_time,'from_location':from_location,'destination':destination}]
           return JsonResponse(flights_data,
                                json_dumps_params={'default': str},
                                safe=False,
                                encoder=DjangoJSONEncoder)
    return HttpResponse('successful')

@csrf_exempt
@require_POST
def select(request):
    if request.method == "POST":
        customer_data = json.loads(request.body)
        travel_agency_name = customer_data.get('travel_agency_name')
        from_date_str = customer_data.get('from_date')
        # travel_agency_name = customer_data.get('travel_agency_name',False)
        # from_date_str = customer_data.get('from_date',False)
        print('tra ',travel_agency_name)
        print('date',from_date_str)
        query = """SELECT myapp_guest.name, myapp_reserve_tickets.identify_card,myapp_reserve_tickets.flight_number, myapp_reserve_tickets.is_ticket 
        FROM myapp_guest JOIN myapp_reserve_tickets ON myapp_guest.identify_card = myapp_reserve_tickets.identify_card 
        JOIN myapp_flight ON myapp_reserve_tickets.flight_number = myapp_flight.flight_number 
        WHERE  myapp_guest.travel_name = '"""+travel_agency_name+'''' and DATE(myapp_flight.from_date) ="'''+from_date_str+'''"; '''

        result = execute_raw_sql(query)
        if result  is  None:
            print("can not select")
            return JsonResponse({
                'status': 'failed'})
        else:
            processed_data = []
            for row in result:
                name, identify_card, flight_number, is_ticket = row
                data_dict = {
                    'name': name,
                    'identify_card': identify_card,
                    'flight_number': flight_number,
                    'is_ticket': is_ticket
                }
                processed_data.append(data_dict)
            print("success")
            return JsonResponse({'data': processed_data,
                                 'status':'success'})
    else:
        return JsonResponse({
                             'status': 'failed'})

def execute_raw_sql(query):
    with connections['default'].cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    return result

@csrf_exempt
@require_POST
def register(request):
    print("in register")
    if request.method == 'POST':
        # 从POST数据中获取用户名和密码
        customer_data = json.loads(request.body)
        travel_name  = customer_data.get('travel_name',False)
        account  = customer_data.get('account', '1111213')
        phone_number  = customer_data.get('phone_number', False)
        password  = customer_data.get('password', False)

        print("travel_name:", travel_name)
        print("account:",account)
        print("phone_number:",phone_number)
        print("password:",password)

        # Validate data (you can add more validation as needed)
        if not (travel_name and account and phone_number and password):
            print("incomplete data")
            return JsonResponse({'status': 'Incomplete data'})

        # Check if the account already exists
        if Travel_agencies.objects.filter(account=account).exists():
            print("exist")
            return JsonResponse({'status': 'Account already exists'})
        
        # Create a new Travel_agencies instance
        new_travel_agency = Travel_agencies(
            travel_name=travel_name,
            account=account,
            phone_number=phone_number,
            password=password
        )

        # Save the new instance to the database
        new_travel_agency.save()

        print("done that right")

        
        # return JsonResponse({'success': 'Registration successful'})
        return JsonResponse({'status':'success' , 'travel_name': travel_name, 'account':account, 'phone_number': phone_number, 'password':password } ) 
    else:
        # 如果不是 GET 请求，返回错误响应
        return JsonResponse({'status': 'failed'})



@csrf_exempt
@require_POST
def search_order(request):
    if request.method == 'POST':
        customer_data = json.loads(request.body)
        travel_name = customer_data.get('travel_name', False)
        selectDate = customer_data.get('selectdate', False)
        selectDate = datetime.fromisoformat(selectDate).date()
        print("travel_name:", travel_name)
        print("selectDate: ",selectDate)
        if not travel_name or not selectDate:
            return JsonResponse({'status':'failed','message': 'Incomplete data'})
        # 得到旅行社成员
        queryset_travelname = guest.objects.filter(travel_name=travel_name).values()
        # 得到航班号
        queryset_flight = flight.objects.filter(from_date__date=selectDate).values_list('flight_number', flat=True)
        flight_info = flight.objects.filter(from_date__date=selectDate).values()
        # 得到订票信息
        queryset_temp = reserve_tickets.objects.all().values()
        # print(queryset_temp)
        result_info = []
        for reserver_info in queryset_temp:
            # 精确到日的所有乘客
            if reserver_info['flight_number_id'] in queryset_flight:
                flag = False
                for member in queryset_travelname:
                    if member['identify_card'] == reserver_info['identify_card_id']:
                        flag = True
                        break
                if flag:
                    is_ticket = "False"
                    if reserver_info['is_ticket']:
                        is_ticket = 'True'
                    price = ""
                    for i in flight_info:
                        if i['flight_number'] == reserver_info['flight_number_id']:
                            price = i['price']
                            break
                    result_info.append({"name":member['name'],
                                        'identify_card':member["identify_card"],
                                        "flight_number":reserver_info['flight_number_id'],
                                        'phone_number':member['phone_number'],
                                        'price':price,
                                        "is_ticket":is_ticket,
                                        "seat_number":reserver_info['seat_number']})
        print('result ',result_info)
        return JsonResponse(result_info,
                                json_dumps_params={'default': str},
                                safe=False,
                                encoder=DjangoJSONEncoder)
    return JsonResponse({"status":"get method not allowed!!"})


@csrf_exempt
@require_POST
def get_customers_info(request):
    if request.method == 'POST':
        cusomer_data = json.loads(request.body)
        travel_name = cusomer_data.get('travel_name',False)
        flight_number = cusomer_data.get('flight_number',False)
        print("travel_name:",travel_name)
        print('flight number ',flight_number)
        matching_guests = guest.objects.filter(travel_name=travel_name).values()
        already_buy_ticket = reserve_tickets.objects.filter(flight_number_id=flight_number).values_list('identify_card_id')
        already_buy_ticket = list(already_buy_ticket)
        already_buy = []
        for i in already_buy_ticket:
            already_buy.append(i[0])
        print('already ',already_buy)
        # 检查是否有符合条件的记录
        if matching_guests.exists():
            # 将QuerySet转换为列表
            matching_guests_list = list(matching_guests)
            matching_guests_list_result = []
            print(matching_guests_list)
            # 遍历所有记录，可以进一步处理每条记录
            for dic_guest_data in matching_guests_list:
                if dic_guest_data['identify_card'] not in already_buy:
                    dic_guest_data.pop('id', None)  # 删除 'id' 项
                    dic_guest_data.pop('travel_name', None)  # 删除 'travel_name' 项
                    dic_guest_data.pop('work', None)  # 删除 'work' 项
                    dic_guest_data.pop('sex', None)  # 删除 'sex' 项
                    dic_guest_data['status'] = 'exist'
                    matching_guests_list_result.append(dic_guest_data.copy())

            
            print(matching_guests_list_result)
            return JsonResponse(matching_guests_list_result, safe=False)
        else:
            # 处理没有符合条件的情况
            return JsonResponse({'status':'failed','message':'no matching guest'})
    else:
        return JsonResponse({'status':'failed'})


@csrf_exempt
@require_POST
def insert_customer(request):
    if request.method == 'POST':
        customer_data = json.loads(request.body)
        name = customer_data.get('name',False)
        identify_card = customer_data.get('identify_card',False)
        phone_number = customer_data.get('phone_number',False)
        sex = customer_data.get('sex',False)
        work = customer_data.get('work',False)
        travel_name = customer_data.get('travel_name',False)

        print("name:",name)
        print("identify_card:",identify_card)
        print("phone_number:",phone_number)
        print("sex:",sex)
        print("work:",work)
        print("travel_name:",travel_name)

        if guest.objects.filter(identify_card=identify_card).exists():
            print("exist")
            return JsonResponse({'status': '该用户已经订购机票啦!!!'})

        if not (travel_name and name and identify_card and phone_number and sex and work):
            print("incomplete data")
            return JsonResponse({'status': 'Incomplete data'})
        
        if guest.objects.filter(identify_card=identify_card).exists():
            print("exist")
            return JsonResponse({'status': '该用户已经订购机票啦!!!'})
        
        # 获取旅行社实例
        travel_agency_instance = Travel_agencies.objects.get(travel_name=travel_name)

        new_guest = guest(
            name=name,
            identify_card=identify_card,
            phone_number=phone_number,
            sex=sex,
            work=work,
            travel_name=travel_agency_instance  # 将实例赋给 travel_name
        )

        new_guest.save()

        print("done that right")
        return JsonResponse({'status':'success' , 'name': name, 'identify_card':identify_card, 'phone_number': phone_number, 'sex':sex,'work':work,'travel_name':travel_name } )
    
    else:
        return JsonResponse({'status':'failed'})
    

@csrf_exempt
@require_POST
def is_ticket(request):
    if request.method == 'POST':
        customer_data = json.loads(request.body)
        flight_number = customer_data.get('flight_number',False)
        identify_card = customer_data.get('identify_card',False)
        print("flight_number:",flight_number)
        print("identify_card:",identify_card)

        if not (flight_number and identify_card):
            print("incomplete data")
            return JsonResponse({'status': 'Incomplete data'})
        
        if reserve_tickets.objects.filter(identify_card=identify_card, flight_number = flight_number).exists():
            print("already exist buy ticket")
            return JsonResponse({'status': 'falied', 'message':'repeated order'})
        
        else:
            print("buying ticket...")
            remaining_tickets = flight.objects.filter(flight_number=flight_number).values('avilable_seat')

            # 票从后往前买
            take_seat = remaining_tickets[0]['avilable_seat']
            print("remaining_tickets:",remaining_tickets)
            print("take_seat:",take_seat)
            if take_seat > 0:
                guest_instance = guest.objects.get(identify_card=identify_card)
                flight_instance = flight.objects.get(flight_number=flight_number)
                new_reserve = reserve_tickets(
                    flight_number = flight_instance,
                    identify_card = guest_instance,
                    seat_number = take_seat,
                    is_ticket = False
                )
                new_reserve.save()
                flight.objects.filter(flight_number=flight_number).update(avilable_seat=take_seat-1)
                print("buying ticket successfully")
                return JsonResponse({'status':'success'})
            else:
                print("no ticket")
                return JsonResponse({'status':'failed', 'message':'票已经卖完了!!!'})
    else:
        return JsonResponse({'status':'failed'})


@csrf_exempt
@require_POST
def select_date_travelname(request):
    customer_data = json.loads(request.body)
    from_date = customer_data.get('from_date')
    from_date = from_date.split('T')[0]
    travel_agency = customer_data.get('travel_agency_name')
    print(travel_agency)
    result = {'data':[]}
    guest_info_id = guest.objects.filter(travel_name=travel_agency).values_list('identify_card', flat=True)
    guest_info = guest.objects.filter(travel_name=travel_agency).values()

    reserve_info = reserve_tickets.objects.all().values()
    # from_date = datetime.fromisoformat(from_date).date()
    print(from_date)
    flight_info_number = flight.objects.filter(from_date__date=from_date).values_list('flight_number', flat=True)
    flight_info = flight.objects.filter(from_date__date=from_date).values()

    for per_info in reserve_info:
        for index_flight,per_flight in enumerate(flight_info_number):
            if per_flight == per_info['flight_number_id']:
                for index_id,per_guest in enumerate(guest_info_id):
                    if per_guest == per_info['identify_card_id']:
                        print('enter')
                        result['data'].append({'name':guest_info[index_id]['name'],
                                       'identify_card':guest_info[index_id]['identify_card'],
                                       'flight_number':flight_info[index_flight]['flight_number'],
                                       'is_ticket':per_info['is_ticket'],
                                       'seat_number':per_info['seat_number']})      
    # print(guest_info)
    print(result)
    return JsonResponse(result,
                                json_dumps_params={'default': str},
                                safe=False,
                                encoder=DjangoJSONEncoder)
    
@csrf_exempt
@require_POST
def update_is_ticket(request):
    customer_data = json.loads(request.body)
    flight_number = customer_data.get('flight_number')
    identify_card = customer_data.get('identify_card')
    if flight_number is None or identify_card is None:
        return JsonResponse({'status','Incomplete data!!'})
    reserve_tickets.objects.filter(flight_number_id=flight_number,identify_card_id=identify_card).update(is_ticket=True)
    return JsonResponse({'status':'success'})


@csrf_exempt
@require_POST
def insert_flight(request):
    # Get data from the request
    customer_data = json.loads(request.body)
    flight_number = customer_data.get('flight_number')
    from_date = customer_data.get('from_date')
    arrived_date = customer_data.get('arrived_date')
    print('arrived date ',arrived_date)
    print('departure date ',from_date)


    price = customer_data.get('price')
    destination = customer_data.get('destination')
    from_location = customer_data.get('from_location')
    available_seat = customer_data.get('available_seat')
    
    from_date_hour = from_date.split(' ')[1].split(':')[0]
    arrived_date_hour = arrived_date.split(' ')[1].split(':')[0]
    if arrived_date_hour == '24':
        arrived_date = arrived_date[:11] + '00' + arrived_date[13:]
    if from_date_hour == '24':
        from_date = from_date[:11] + '00' + from_date[13:]
    if from_date > arrived_date:
        print('time error')
        return JsonResponse({'status': 'failed',
                             'msg': '航班到达时间应该晚于出发时间!!!'
                             })
    else:
        try:
            flight2 = flight.objects.get(flight_number=flight_number)
        except flight.DoesNotExist:
            flight2 = None
        # Validate the user (you should implement your authentication logic here)
        if flight2 is not None:
            print("failed")
            return JsonResponse({'status': 'failed',
                                 'msg':'航班已经存在'
                                 })
        else:
            # Create a new Flight object
            flight1 = flight(
                flight_number=flight_number,
                from_date=from_date,
                arrived_date=arrived_date,
                price=price,
                from_location=from_location,
                destination=destination,
                avilable_seat=available_seat
            )

            # Save the Flight object to the database
            flight1.save()
            print("success")
            # Return a success response
            return JsonResponse({'status': 'success'})

@csrf_exempt
@require_POST
def delete_flight(request):
    customer_data = json.loads(request.body)
    flight_number = customer_data.get('flight_number')
    try:
        flight2 = flight.objects.get(flight_number=flight_number)
    except flight.DoesNotExist:
        flight2 = None
    # Validate the user (you should implement your authentication logic here)
    if flight2 is not None:
        flight2.delete()
        print("delete success")
        return JsonResponse({'status': 'success'
                             })
    else:
        print("failed .not exist")
        # Return a success response
        return JsonResponse({'status': 'failed',
                             'msg': 'conflicted'
                             })

@csrf_exempt
@require_POST
def update_flight(request):
    # Get data from the request
    customer_data = json.loads(request.body)
    old_flight_number = customer_data.get("old_flight_number")
    # old_from_date = customer_data.get('old_item[from_date]')
    # old_arrived_date = customer_data.get('old_item[arrived_date]')
    # old_price = customer_data.get('old_item[price]')
    # old_destination = customer_data.get('old_item[destination]')
    # old_from_location = customer_data.get('old_item[from_location]')
    # old_available_seat = customer_data.get('old_item[available_seat]')

    flight_number = customer_data.get('flight_number')
    from_date = customer_data.get('from_date')
    arrived_date = customer_data.get('arrived_date')
    price = customer_data.get('price')
    destination = customer_data.get('destination')
    from_location = customer_data.get('from_location')
    available_seat = customer_data.get('available_seat')
    if from_date is not None and arrived_date is not None and from_date > arrived_date:
        print('time error')
        return JsonResponse({'status': 'failed',
                             'msg': 'conflicted'
                             })
    else:
        try:
            flight2 = flight.objects.get(flight_number=old_flight_number)
        except flight.DoesNotExist:
            flight2 = None
        # Validate the user (you should implement your authentication logic here)
        if flight2 is not None:
            if old_flight_number!=flight_number:
                flight2.flight_number=flight_number
                print("flight_number change")
            if from_date is not None:
                flight2.from_date=from_date
                print("from_date change")
            if arrived_date is not None:
                flight2.arrived_date=arrived_date
                print("arrived_date change")
            if price is not None:
                flight2.price=price
                print("price change")
            if destination is not None:
                flight2.destination=destination
                print("destination change")
            if from_date is not None:
                flight2.from_location=from_location
                print("from_location change")
            if available_seat is not None:
                flight2.available_seat=available_seat
                print("available_seat change")
            print("success")
            return JsonResponse({'status': 'success'
                                 })
        else:
            print("failed")
            return JsonResponse({'status': 'failed',
                                 'msg': 'conflicted'
                                 })
@csrf_exempt
@require_POST
def search_flight(request):
    # Get data from the request
    customer_data = json.loads(request.body)
    flight_number = customer_data.get('flight_number')
    try:
        flight2 = flight.objects.get(flight_number=flight_number)
    except flight.DoesNotExist:
        flight2 = None
    # Validate the user (you should implement your authentication logic here)
    if flight2 is not None:
        print("success")
        print({
            'flight_number': flight2.flight_number,
            'from_date': flight2.from_date,
            'arrived_date': flight2.arrived_date,
            'price': flight2.price,
            'available_seat': flight2.avilable_seat,
            'from_location': flight2.from_location,
            'destination': flight2.destination
        })
        return JsonResponse({'status': 'success',
                             'flight_number':flight2.flight_number,
                             'from_date':flight2.from_date,
                             'arrived_date':flight2.arrived_date,
                             'price':flight2.price,
                             'available_seat':flight2.avilable_seat,
                             'from_location':flight2.from_location,
                             'destination':flight2.destination
                             })
    else:
        print("not find")
        return JsonResponse({'status': 'failed'})

@csrf_exempt
@require_POST
def is_ticket_simple(request):
    if request.method == 'POST':
        customer_data = json.loads(request.body)
        flight_number = customer_data.get('flight_number',False)
        identify_card = customer_data.get('identify_card',False)
        print("flight_number:",flight_number)
        print("identify_card:",identify_card)
        if not (flight_number and identify_card):
            print("incomplete data")
            return JsonResponse({'status': 'Incomplete data'})
        
        if reserve_tickets.objects.filter(identify_card=identify_card, flight_number = flight_number).exists():
            print("already exist buy ticket")
            return JsonResponse({'status': 'falied', 'message':'repeated order'})
        return JsonResponse({'status':'success'})



@csrf_exempt
@require_POST
def get_all_travelname(request):
    all_data = Travel_agencies.objects.values('travel_name')
    # print(all_data.values())
    travel_name = []
    for travel_agency in all_data:
        travel_name.append({'travel_name':travel_agency['travel_name']})
    # print(travel_name)
    return JsonResponse(travel_name,
                                json_dumps_params={'default': str},
                                safe=False,
                                encoder=DjangoJSONEncoder)