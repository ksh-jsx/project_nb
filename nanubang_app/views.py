import json
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.views import generic
from .forms import UserCreationForm,UserChangeForm,Room_infosForm,TagsForm,call_fileForm
from .models import User,Room_infos,Tags,Like,Connect,call_file,Complete_contract,Complete_contract_infos
from django.db.models import Count
from django.contrib.auth import views as auth_views
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect,HttpResponse

#이메일 인증에 필요한 것들
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text
#이메일 인증에 필요한 것들

# Create your views here.

def index(request):
        print('hi')
    get_current_sales = Room_infos.objects.all().order_by('-published_date')[:8]
    get_current_sales1 = Room_infos.objects.all().order_by('-published_date')[0:8:2]
    get_current_sales2 = Room_infos.objects.all().order_by('-published_date')[1:7:2]
    
    if request.method == "POST":
        q = request.POST.get('usern', '')
        is_active = User.objects.filter(username=q).values('active', 'username')
        if is_active[0]['active']:
            return redirect('register_index')
        
        else:
            return render(request, 'index.html', {'user_info': is_active[0]['active'],'current_sales': get_current_sales,'range': zip(get_current_sales1,get_current_sales2)})
    else:
        return render(request, 'index.html', {'user_info': 'none', 'current_sales': get_current_sales, 'range': zip(get_current_sales1,get_current_sales2) })

 
def check_authenticate(request):
    is_active = User.objects.filter(username=request.user.username).values('active', 'username')
    if is_active[0]['active']:
        message = "True"
    else:
         message = "False"
    context = {'message': message}

    return HttpResponse(json.dumps(context), content_type="application/json")

@login_required
def mail_authenticate(request):
    user = User.objects.filter(username=request.user.username).values('auto_increment_id','email')
    print(user)
    current_site = get_current_site(request) 
    message = render_to_string('account/user_activate_email.html',{
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user[0]['auto_increment_id'])).decode('utf-8'),
        'token': account_activation_token.make_token(user),
    })
    mail_subject = "나누방 인증 메일입니다."
    user_email = user[0]['email']
    email = EmailMessage(mail_subject, message, to=[user_email])
    email.send()
    return HttpResponse(
        '<div style="font-size: 40px; width: 100%; height:100%; display:flex; text-align:center; '
        'justify-content: center; align-items: center;">'
        '입력하신 이메일<span>로 인증 링크가 전송되었습니다.</span>'
        '</div>'
    )

@login_required
def activate(request, uid64, token):

    uid = force_text(urlsafe_base64_decode(uid64))
    user = User.objects.filter(auto_increment_id=uid).values('active', 'username')
    print(user)
    if user is not None :
        post = get_object_or_404(User, auto_increment_id=uid)
        post.active = True
        post.save()
        return HttpResponse(
        '<a href="/" id="goto_main" style="display:none">test</a>'
        '<script>'
        '   alert("인증되었습니다");'
        '   document.getElementById("goto_main").click();'
        '</script>'
    )
    else:
        return HttpResponse('비정상적인 접근입니다.')

def nanubang(request):
    return render(request, 'nanu_contract_desc.html')

def search_univ(request):
    q = request.GET.get('q', '')
    get_tag = Tags.objects.all().values('tag','univ').filter(univ=q).annotate(total=Count('tag')).order_by('-total')[:5]
    
    if request.user.is_authenticated:
        like = Like.objects.filter(author=request.user)
    else:
        like = 'none'

    if request.method == "POST":
        univ = request.POST.get('univ', None)
        cost1 = request.POST.get('sort1_1', None)
        cost2 = request.POST.get('sort1_2', None)
        cost3 = request.POST.get('sort2_1', None)
        cost4 = request.POST.get('sort2_2', None)
        date1 = request.POST.get('sort3_1', None)
        date2 = request.POST.get('sort3_2', None)
        tags = request.POST.get('tags', None)
        list_tag = tags.split(',')
        
        lat_left = request.POST.get('lat_left', None)
        lat_right = request.POST.get('lat_right', None)
        lng_left = request.POST.get('lng_left', None)
        lng_right = request.POST.get('lng_right', None)        

        if univ == '서울':
            item = Room_infos.objects.filter(desired_deposit__range = (cost1, cost2), desired_monthly__range =(cost3, cost4), start_date__gte = date1,  end_date__lte = date2, latitude__range = (lat_left, lat_right), longitude = (lng_left,lng_right) ).exclude(state = 4)
            count = item.count()
        else:
            item = Room_infos.objects.filter(univ=univ, desired_deposit__range = (cost1, cost2), desired_monthly__range =(cost3, cost4), start_date__gte = date1,  end_date__lte = date2, tag__in=list_tag).exclude(state = 4)
            count = item.count()
        return render(request, 'sales_sort.html', {'info': univ, 'item':item, 'like':like, 'count':count})


    else:    
        if q == '':
            item = Room_infos.objects.all().exclude(state = 4)
            count = item.count()    
            return render(request, 'view_sales.html', {'info': '서울', 'item':item, 'like':like, 'count':count, 'tags':get_tag})
        else:
            item = Room_infos.objects.filter(univ=q).exclude(state = 4)
            count = item.count()
            return render(request, 'view_sales.html', {'info': q, 'item':item, 'like':like, 'count':count, 'tags':get_tag})

@login_required
@require_POST # 해당 뷰는 POST method 만 받는다.
def post_like(request):
    pk = request.POST.get('pk', None) # ajax 통신을 통해서 template에서 POST방식으로 전달
    item = get_object_or_404(Room_infos, pk=pk)
    post_like, post_like_created = item.like_set.get_or_create(author=request.user)

    if not post_like_created:
        post_like.delete()
        message = "좋아요 취소"
    else:
        message = "좋아요"

    context = {'message': message}

    return HttpResponse(json.dumps(context), content_type="application/json")
    # context를 json 타입으로

def room_detail(request):
    get_id = request.GET.get('item_id', '')
    get_room = Room_infos.objects.all().filter(auto_increment_id = get_id)
    if request.session.keys(): 
	    get_connect = Connect.objects.all().filter(Room_buyer = request.user)
    else:
        get_connect = None
    get_like = Like.objects.all().filter(room_info = get_room[:1]).count()
    return render(request, 'view_detail.html',{'get_info':get_room,'like':get_like,'connect':get_connect})

def room_detail_temp(request):
    return render(request, 'view_detail_tmp.html')

@login_required
def register_index(request):
    room_count = Room_infos.objects.all().filter(author = request.user).count() #내가 올린 방 1개 이상이면 뒤로가게 해야댐
    return render(request, 'register_index.html', {'room_count': room_count})

@login_required
def register(request):
    if request.method == "POST":
        form = Room_infosForm(request.POST, request.FILES)
        form2 = TagsForm()
        if form.is_valid():
            temp = form.save(commit=False)
            temp.author = request.user
            temp.publish()
            temp.save()
            get_roomInfo = Room_infos.objects.order_by('-created_date')[:1]
            form2 = TagsForm()
            temp2 = form2.save(commit=False)
            for roomInfo in get_roomInfo:
                temp2.key = roomInfo
                temp2.tag = roomInfo.tag
                temp2.univ = roomInfo.univ
            temp2.save()
            return redirect('register_complete')
    else:
        get_tag = Tags.objects.all().values('tag','univ').annotate(total=Count('tag')).order_by('-total')[:5]
        form = Room_infosForm()
        count = get_tag.count()
        return render(request, 'register.html',{'form' : form, 'tags':get_tag,'count':count})

@login_required
def register_complete(request):
    room = Room_infos.objects.all().filter(author = request.user)[:1]
    return render(request, 'register_complete.html', {'room': room})

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('signup_success')
    template_name = 'registration/signup.html'



@login_required
def mypage(request):
    get_page = request.GET.get('page', '')
    #1
    user = UserChangeForm()
    user_info = User.objects.all().filter(username = request.user)

    #2
    item = Room_infosForm()
    get_tag = Tags.objects.all().values('tag','univ').annotate(total=Count('tag')).order_by('-total')[:5]
    count = get_tag.count()
    item_info = Room_infos.objects.all().filter(author = request.user)

    #3
    like = Room_infos.objects.all().filter(like_user_set = request.user)

    #4
    get_connect_info = User.objects.all().filter(username = request.user)[0]
    get_complete_contract1 = Complete_contract.objects.all().filter(Room_seller = request.user)
    get_complete_contract2 = Complete_contract.objects.all().filter(Room_buyer = request.user)

    if(get_connect_info.connector):
        get_connector_name = user_info[0].connector
        if not user_info[0].connector :
            get_connector_name = request.user
        get_connector = User.objects.all().filter(username = get_connector_name)[0]
        get_room_id = Room_infos.objects.all().filter(author = get_connector)
        if not get_room_id:
            get_room_id = Room_infos.objects.all().filter(author = request.user)  
        buyer_phone = get_connector.phone1 + ' - ' + get_connector.phone2 + ' - ' + get_connector.phone3
        seller_phone = get_connector.phone1 + ' - ' + get_connector.phone2 + ' - ' + get_connector.phone3
        print(seller_phone)
        connect_buyer = None
        connect_seller = None
        if User.objects.all().filter(username = request.user)[0].payment:
            connect_buyer = Connect.objects.all().filter(Room_buyer = request.user, Room_seller = get_connector)
            connect_seller = Connect.objects.all().filter(Room_seller = request.user, Room_buyer = get_connector)
            print('asdasd')
            get_room_id = None
    else:
        connect_buyer = Connect.objects.all().filter(Room_buyer = request.user)
        connect_seller = Connect.objects.all().filter(Room_seller = request.user)
        get_room_id = None
        buyer_phone = None
        seller_phone = None
        if not connect_buyer and not connect_seller:
            connect_buyer = 'x'
            connect_seller = 'x'
            

    if request.method == "POST":
        get_num = request.POST.get('mypage_num', '')
        if get_num == '1':
            item = get_object_or_404(Room_infos, author=request.user)
            form = Room_infosForm(request.POST, request.FILES, instance=item)
            if form.is_valid():
                form.save()
                return redirect('mypage')

        elif get_num == '2':
            user = get_object_or_404(User, username=request.user.username)
            form = UserChangeForm(request.POST, instance=user)
            if form.is_valid():
                temp = form.save(commit=False)
                if user_info[0].email.strip() != request.POST['email'].strip():
                    temp.active = False
                print(request.POST['password1'])
                if request.POST['password1'] != '0':
                    temp.set_password(request.POST['password1'].strip())
                temp.save()
                return redirect('mypage')


    else:
        return render(request, 'mypage.html',{'page':get_page,'form1' : user,'user_info' : user_info, 'form2':item,'item_info':item_info,'tags':get_tag,'count':count,'like':like,'id':get_room_id,'seller_phone':seller_phone,'buyer_phone':buyer_phone,'seller':connect_seller ,'buyer':connect_buyer,'complete_contract1':get_complete_contract1,'complete_contract2':get_complete_contract2})    

def delete_user(request):
    if request.method == "POST":
	    user = get_object_or_404(User, username=request.user.username)
	    user.delete()
	    message = '유저 삭제'
	    context = {'message': message}
    return HttpResponse(json.dumps(context), content_type="application/json")

def delete_item(request):
    delete_contract = Room_infos.objects.get(author = request.user)
    print(delete_contract)
    insert_info = delete_contract(
        author = complete_contract.author,
        auto_increment_id = complete_contract.auto_increment_id,
        created_date = complete_contract.created_date,
        published_date = complete_contract.published_date,
        address =  complete_contract.address,
        address_detail = complete_contract.address_detail,
        univ = complete_contract.univ,
        tag = complete_contract.tag,
        room_type = complete_contract.room_type,
        deposit = complete_contract.deposit,
        monthly_cost = complete_contract.monthly_cost,
        deposit_necessity = complete_contract.deposit_necessity,
        desired_deposit = complete_contract.desired_deposit,
        desired_monthly = complete_contract.desired_monthly,
        management_cost_include = complete_contract.management_cost_include,
        management_cost = complete_contract.management_cost,
        start_date = complete_contract.start_date,
        end_date = complete_contract.end_date,
        floor = complete_contract.floor,
        sublessee_type1 = complete_contract.sublessee_type1,
        sublessee_type2 = complete_contract.sublessee_type2,
        room_options = complete_contract.room_options,
        sublessor_type1 = complete_contract.sublessor_type1,
        sublessor_type2 = complete_contract.sublessor_type2,
        latitude = complete_contract.latitude,
        longitude = complete_contract.longitude,
		
        room_desc = complete_contract.room_desc,
        room_size = complete_contract.room_size,
        is_duplex = complete_contract.is_duplex,
        window = complete_contract.window,

        photo1 = complete_contract.photo1,
        photo2 = complete_contract.photo2,
        photo3 = complete_contract.photo3,
        photo4 = complete_contract.photo4,
        pano_photo = complete_contract.pano_photo,
        Room_seller = '미판매',
        Room_buyer = '미판매'
    )
    insert_info.save()  
    complete_contract.delete()
    message = '아이템 삭제'
    context = {'message': message}
    return HttpResponse(json.dumps(context), content_type="application/json")

def cust_service(request):
    return render(request, 'service.html')

def cust_service(request, page=0):
    return render(request, 'service.html',{'page':page})

@login_required
def contract_desc(request):
    
    if request.method == "GET":
        get_id = request.GET.get('item_id', '')
        if get_id and not get_id.isspace() :
            return render(request, 'contract_desc.html',{'id':get_id})      
        else :
            return redirect('index')
        
    else:
        get_id = request.POST.get('item_id', '')
        get_room = Room_infos.objects.filter(auto_increment_id = get_id).values('auto_increment_id','author')    
        get_owner = User.objects.all().filter(auto_increment_id = get_room[0]['author'])
        if get_id and not get_id.isspace() :
            is_connected = Connect.objects.filter(Room_buyer = request.user, Room_seller = get_owner[0])
            if not is_connected:
                data = Connect(Room_buyer = request.user, Room_seller = get_owner[0])
                data.save()
                room = get_object_or_404(Room_infos, auto_increment_id = get_id)
                room.state = 1
                room.save()
                return redirect('mypage')
            else : 
                return HttpResponse(

                '<script>'
                '   alert("이미 거래를 신청한 방입니다.");'
                '   history.back();'
                '</script>'
                )
        else:
            return redirect('index')

@login_required
def contract1(request):
    get_id = request.POST.get('item_id', '')
    get_type = User.objects.all().filter(username = request.user)
    if get_id and not get_id.isspace() :
        return render(request, 'contract1.html',{'id':get_id,'get_type':get_type})      
    else :
        return redirect('index')

@login_required
def contract_type(request):
    get_id = request.POST.get('item_id', '')
    get_type = request.POST.get('contract_type', '')

    get_room_buyer = User.objects.filter(connector = request.user.username).values('username')
    
    if get_id and not get_id.isspace() :
        post1 = get_object_or_404(User, username=request.user)
        post2 = get_object_or_404(User, username=get_room_buyer[0]['username'])
        room1 = get_object_or_404(Room_infos, auto_increment_id = get_id)
        #room1.state = 2
        #post1.user_type = '판매자, '+get_type
        #post2.user_type = '구매자, '+get_type
        #post1.connector = get_room_buyer[0]['username']
        #post2.connector = request.user.username
        #post1.save()
        #post2.save()
        #room1.save()

        connect1 = get_object_or_404(Connect, Room_seller=post1, Room_buyer=post2)
        get_connect2 = Connect.objects.all().filter(Room_seller = post1)
        get_connect3 = Connect.objects.all().filter(Room_buyer = post2)
        for i in get_connect2:
            connect2 = get_object_or_404(Connect, Room_seller=i)
            connect2.delete()

        for i in get_connect3:
            connect3 = get_object_or_404(Connect, Room_buyer=i)
            connect3.delete()

        connect1.save()
        message = get_type
        context = {'message': message}
        return HttpResponse(json.dumps(context), content_type="application/json")


@login_required
def contract_confirm(request):
    get_user = Connect.objects.all().filter(Room_seller = request.user)[0].Room_seller
    get_id = Room_infos.objects.all().filter(author = request.user)

    if request.method == "POST":
        get_buyer = Connect.objects.all().filter(Room_seller = request.user)[0].Room_buyer
        room = get_object_or_404(Room_infos, auto_increment_id = get_id[0].auto_increment_id)
        room.state = 2 
        room.save()
        post1 = get_object_or_404(User, username=request.user)
        post2 = get_object_or_404(User, username=get_buyer)
        post1.user_type = '판매자, type0'
        post2.user_type = '구매자, type0'
        post1.connector = get_buyer.username
        post2.connector = request.user.username
        post1.save()
        post2.save()
        connect1 = get_object_or_404(Connect, Room_seller=post1, Room_buyer=post2)
        get_connect2 = Connect.objects.all().filter(Room_seller = post1).delete()
        get_connect3 = Connect.objects.all().filter(Room_buyer = post2).delete()
        connect1.save()
        return render(request, 'contract_confirm.html',{'room_state':room.state,'room':get_id}) 
    else:
        if get_user:
            return render(request, 'contract_confirm.html',{'room':get_id})      
        else:
            return redirect('index')

@login_required
def payment(request):
    get_id = request.GET.get('item_id', '')
    get_type = request.POST.get('contract_type', '')

    if get_id and not get_id.isspace() :
        item_info = Room_infos.objects.all().filter(auto_increment_id = get_id)
        user_info = User.objects.all().filter(username = request.user)
        return render(request, 'payment.html', {'payment_info': item_info,'user_info':user_info})
    else :
        return redirect('index')

@login_required
def payment_check(request):
    post = get_object_or_404(User, username=request.user)
    post.payment = True
    post.save()
    
    message = "결제함"

    context = {'message': message}

    return HttpResponse(json.dumps(context), content_type="application/json")

@login_required
def contract2(request):

    get_buyer = User.objects.filter(username = request.user.username).values('payment','username','name','phone1','phone2','phone3')
    get_seller = User.objects.filter(connector = request.user.username).values('payment','username','name','phone1','phone2','phone3')
    
    if get_buyer[0]['payment'] and get_seller[0]['payment'] : 
        return redirect('contract3')

    elif get_buyer[0]['payment']:
        return render(request, 'contract2.html', {'user_info':get_seller})
    elif get_seller[0]['payment']:
        return render(request, 'contract2.html', {'user_info':get_buyer})
    else:
        return redirect('index')

def contract4(request):
    return render(request, 'contract4.html')

def save_file(request):
    
    form = call_fileForm(request.POST, request.FILES)
    if form.is_valid():
        temp = form.save(commit=False)
        temp.author = request.user
        temp.save()
        print('저장성공')
    return render(request, 'save_file.html')

@login_required
def contract3(request):
    import requests

    get_myInfo = User.objects.filter(username = request.user.username).values('payment','username','user_type')
    get_yourInfo = User.objects.filter(connector = request.user.username).values('payment','username','user_type')
    if not get_myInfo[0]['payment'] or not get_yourInfo[0]['payment'] : 
        print('hihi')        
        return redirect('index')
    else : 

        if get_myInfo[0]['user_type'].strip().split(',')[0] == '판매자':
            room_state = get_object_or_404(Room_infos, author=request.user).state
            return render(request, 'contract3.html', {'users': get_myInfo,'state':room_state})
        elif get_myInfo[0]['user_type'].strip().split(',')[0] == '구매자':

            return render(request, 'contract3_buyer.html', {'users': get_myInfo})

def send_contract1(request):
    import requests

    get_myInfo = User.objects.filter(username = request.user.username).values('payment','username','user_type','phone1','phone2','phone3','name')
    get_yourInfo = User.objects.filter(connector = request.user.username).values('payment','username','user_type','phone1','phone2','phone3','name')
    
    myInfo_arr = get_myInfo[0]['user_type'].strip().split(',')
    if myInfo_arr[0] == '판매자':
        buyer_phone = get_yourInfo[0]['phone1']+get_yourInfo[0]['phone2']+get_yourInfo[0]['phone3']
        buyer_name = get_yourInfo[0]['name']
        seller_phone = get_myInfo[0]['phone1']+get_myInfo[0]['phone2']+get_myInfo[0]['phone3']
        seller_name = get_myInfo[0]['name']
    else:
        buyer_phone = get_myInfo[0]['phone1']+get_myInfo[0]['phone2']+get_myInfo[0]['phone3']
        buyer_name = get_myInfo[0]['name']
        seller_phone = get_yourInfo[0]['phone1']+get_yourInfo[0]['phone2']+get_yourInfo[0]['phone3']
        seller_name = get_yourInfo[0]['name']
    
    get_type = request.POST.get('type', '')
    get_owner_name = request.POST.get('owner_name', '')
    get_owner_phone = request.POST.get('owner_phone', '')

    print(seller_name)
    print(seller_phone)
    print(buyer_name)
    print(buyer_phone)
    print(get_owner_name)
    print(get_owner_phone)

    url1 = 'https://docs.esignon.net/api/Testapi/login'
    url2 = 'https://docs.esignon.net/api/Testapi/startsimple'

    data1 = { 
        "header" : { 
            "request_code" : "1001Q",  
            "request_msg" : "인증코드 요청을 합니다.", 
            "session_id" : "thread_023" 
            
        }, 
            "body" : { 
                "comp_id" : "Testapi", 
                "memb_email" : "shkim061198@gmail.com",  
                "memb_pwd" : "testapi1!", 
                "client_id" : "*C9E7513F88CF918AC0C393B3CF14F9CF26F70017" 
                
            } 
        
    }

    data2_contract = {
        "header": 
        {
                "request_code": "5005Q",
                "api_name": "start api",
                "session_id": "S1001",
                "version": "1.1.58"
        },
        "body": 
        {
                "comp_id": "Testapi",
                "biz_id": "0",
                "client_id": "*C9E7513F88CF918AC0C393B3CF14F9CF26F70017",
                "memb_email": "shkim061198@gmail.com",
                "workflow_name": "전대차 계약서",
                "doc_id": "74",
                "language": "ko-KR",
                "player_list": 
                [
                    {
                        "field_owner": "1",
                        "email": seller_phone,
                        "id_type": "Mobile",
                        "name": seller_name,
                        "language": "ko-KR",
                        "enable_mobile_cert": "true",
                        "mobile_number": seller_phone
                    },
                    {
                        "field_owner": "2",
                        "email": buyer_phone,
                        "id_type": "Mobile",
                        "name": buyer_name,
                        "language": "ko-KR",
                        "enable_mobile_cert": "true",
                        "mobile_number": buyer_phone
                    }
                    
                ],
                "field_list": 
                [
                    {
                        "doc_id": "74",
                        "field_name": "근로자 이름",
                        "field_value": "홍길동"
                    }
                ],

                "export_api_info": 
                {
                    "api_type": "",
                    "url": "",
                    "enable": "",
                    "request_code": "",
                    "clientid": "",
                    "request_params": 
                    [
                        {
                                "param_id": "",
                                "param_value": "",
                                "fields": []
                        }
                    ],
                    "response_params": []
                },
                "comment": ""
        }
    }
    
    data2_agree = {
        "header": 
        {
                "request_code": "5005Q",
                "api_name": "start api",
                "session_id": "S1001",
                "version": "1.1.58"
        },
        "body": 
        {
                "comp_id": "Testapi",
                "biz_id": "0",
                "client_id": "*C9E7513F88CF918AC0C393B3CF14F9CF26F70017",
                "memb_email": "shkim061198@gmail.com",
                "workflow_name": "전대 동의서",
                "doc_id": "75",
                "language": "ko-KR",
                "player_list": 
                [
                    {
                        "field_owner": "1",
                        "email": seller_phone,
                        "id_type": "Mobile",
                        "name": seller_name,
                        "language": "ko-KR",
                        "enable_mobile_cert": "true",
                        "mobile_number": seller_phone
                    },
                    {
                        "field_owner": "2",
                        "email": buyer_phone,
                        "id_type": "Mobile",
                        "name": buyer_name,
                        "language": "ko-KR",
                        "enable_mobile_cert": "true",
                        "mobile_number": buyer_phone
                    },
                    {
                        "field_owner": "3",
                        "email": get_owner_phone,
                        "id_type": "Mobile",
                        "name": get_owner_name,
                        "language": "ko-KR",
                        "enable_mobile_cert": "true",
                        "mobile_number": get_owner_phone
                    }
                ],
                "field_list": 
                [
                    {
                        "doc_id": "75",
                        "field_name": "근로자 이름",
                        "field_value": "홍길동"
                    }
                ],

                "export_api_info": 
                {
                    "api_type": "",
                    "url": "",
                    "enable": "",
                    "request_code": "",
                    "clientid": "",
                    "request_params": 
                    [
                        {
                                "param_id": "",
                                "param_value": "",
                                "fields": []
                        }
                    ],
                    "response_params": []
                },
                "comment": ""
        }
    }
    
    if get_myInfo[0]['payment'] and get_yourInfo[0]['payment'] : 
        headers1 = {'Content-Type': 'application/json; charset=utf-8', 'User-Agent' : 'esignonapi'}
        
        jsonString1 = json.dumps(data1, indent=4, ensure_ascii=False)
        if get_type.strip() =='type2':
            jsonString2 = json.dumps(data2_contract, indent=4, ensure_ascii=False)
        elif get_type.strip() =='type1':
            jsonString2 = json.dumps(data2_agree, indent=4, ensure_ascii=False)

        if request.method == "POST" :
            
            r1=requests.post(url1, data=jsonString1.encode('utf-8'), headers=headers1)
            temp = json.loads(r1.text)
            accees_token = temp['body']['access_token']
            headers2 = {'Content-Type': 'application/json; charset=utf-8', 'Authorization' : 'esignon '+accees_token, 'User-Agent' : 'esignonapi'}    
            r2=requests.post(url2, data=jsonString2.encode('utf-8'), headers=headers2)

            if get_type.strip() =='type2':
                contract_connector = User.objects.all().filter(connector = request.user.username)
                room = get_object_or_404(Room_infos, author=request.user)
                room.state = 4
                room.save()
                
                complete_contract = Room_infos.objects.get(author = request.user)
                insert_info = Complete_contract_infos.objects.create(
                    author = complete_contract.author,
                    auto_increment_id = complete_contract.auto_increment_id,
                    created_date = complete_contract.created_date,
                    published_date = complete_contract.published_date,
                    address =  complete_contract.address,
                    address_detail = complete_contract.address_detail,
                    univ = complete_contract.univ,
                    tag = complete_contract.tag,
                    room_type = complete_contract.room_type,
                    deposit = complete_contract.deposit,
                    monthly_cost = complete_contract.monthly_cost,
                    deposit_necessity = complete_contract.deposit_necessity,
                    desired_deposit = complete_contract.desired_deposit,
                    desired_monthly = complete_contract.desired_monthly,
                    management_cost_include = complete_contract.management_cost_include,
                    management_cost = complete_contract.management_cost,
                    start_date = complete_contract.start_date,
                    end_date = complete_contract.end_date,
                    floor = complete_contract.floor,
                    sublessee_type1 = complete_contract.sublessee_type1,
                    sublessee_type2 = complete_contract.sublessee_type2,
                    room_options = complete_contract.room_options,
                    sublessor_type1 = complete_contract.sublessor_type1,
                    sublessor_type2 = complete_contract.sublessor_type2,
                    latitude = complete_contract.latitude,
                    longitude = complete_contract.longitude,
                    
                    room_desc = complete_contract.room_desc,
                    room_size = complete_contract.room_size,
                    is_duplex = complete_contract.is_duplex,
                    window = complete_contract.window,

                    photo1 = complete_contract.photo1,
                    photo2 = complete_contract.photo2,
                    photo3 = complete_contract.photo3,
                    photo4 = complete_contract.photo4,
                    pano_photo = complete_contract.pano_photo,
                    Room_seller = request.user.username,
                    Room_buyer = contract_connector[0].username
                )
                insert_info.save() 
                complete_contract.delete()

                connect_model1 = Connect.objects.get(Room_seller = request.user)
                connect_model1.delete()
                connect_user1 = User.objects.get(username = request.user)
                connect_user1.user_type = ''
                connect_user1.connector = ''
                connect_user1.payment = False
                connect_user1.save()
                connect_user2 = User.objects.get(username = contract_connector[0])
                connect_user2.user_type = ''
                connect_user2.connector = ''
                connect_user2.payment = False
                connect_user2.save()
            elif get_type.strip() =='type1':
                room = get_object_or_404(Room_infos, author=request.user)
                room.state = 3
                room.save()


            message = '전송됨'
            return HttpResponse(json.dumps(message), content_type="application/json")


    
    
