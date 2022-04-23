from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
univ_list = (
                ('건국대학교 서울캠퍼스','건국대학교 서울캠퍼스'),
                ('경희대학교 서울캠퍼스','경희대학교 서울캠퍼스'),
                ('고려대학교 서울캠퍼스','고려대학교 서울캠퍼스'),
                ('광운대학교','광운대학교'),
                ('국민대학교','국민대학교'),
                ('덕성여자대학교 쌍문캠퍼스','덕성여자대학교 쌍문캠퍼스'),
                ('덕성여자대학교 종로캠퍼스','덕성여자대학교 종로캠퍼스'),
                ('동국대학교 서울캠퍼스','동국대학교 서울캠퍼스'),
                ('동덕여자대학교','동덕여자대학교'),
                ('삼육대학교','삼육대학교'),

                ('상명대학교 서울캠퍼스','상명대학교 서울캠퍼스'),
                ('서강대학교','서강대학교'),
                ('서경대학교','서경대학교'),
                ('서울과학기술대학교','서울과학기술대학교'),
                ('서울대학교 관악캠퍼스','서울대학교 관악캠퍼스'),
                ('서울대학교 연건캠퍼스','서울대학교 연건캠퍼스'),
                ('서울시립대학교','서울시립대학교'),
                ('서울여자대학교','서울여자대학교'),
                ('성공회대학교','성공회대학교'),
                ('성균관대학교 인문사회캠퍼스','성균관대학교 인문사회캠퍼스'),

                ('성신여자대학교 수정캠퍼스','성신여자대학교 수정캠퍼스'),
                ('성신여자대학교 운정그린캠퍼스','성신여자대학교 운정그린캠퍼스'),
                ('세종대학교','세종대학교'),
                ('숙명여자대학교','숙명여자대학교'),
                ('숭실대학교','숭실대학교'),
                ('연세대학교 신촌캠퍼스','연세대학교 신촌캠퍼스'),
                ('이화여자대학교','이화여자대학교'),
                ('중앙대학교 서울캠퍼스','중앙대학교 서울캠퍼스'),
                ('한국외국어대학교 서울캠퍼스','한국외국어대학교 서울캠퍼스'),
                ('한국체육대학교','한국체육대학교'),

                ('한국성서대학교','한국성서대학교'),
                ('한성대학교','한성대학교'),
                ('한양대학교 서울캠퍼스','한양대학교 서울캠퍼스'),
                ('홍익대학교 서울캠퍼스','홍익대학교 서울캠퍼스'),
        )

class User(AbstractUser):
    # default : username, password, firstname, lastname, emaill
    GENDER_CHOICES = (
            ('남자', '남자'),
            ('여자', '여자')
    )

    USER_TYPE = (
            ('구매자', '구매자'),
            ('판매자', '판매자')
    )

    CIGA_CHOICES = (
            ('흡연', '흡연'),
            ('비흡연', '비흡연')
    )

    MEET_PATH_CHOICES = (
            ('SNS', 'SNS'),
            ('Inschool_Promotion', '교내홍보물'),
            ('Naver_PR', '네이버 광고'),
            ('KaKao_OpenChat', '오픈카톡방'),
            ('School_Community', '학교 커뮤니티'),
            ('etc', '기타')
    )

    name = models.CharField(verbose_name='이름', max_length=255, blank=True)

    phone1 = models.CharField(verbose_name='휴대전화1', max_length=140, null=True)
    phone2 = models.CharField(verbose_name='휴대전화2', max_length=140, null=True)
    phone3 = models.CharField(verbose_name='휴대전화3', max_length=140, null=True)

    gender = models.CharField(verbose_name='성별', max_length=80)

    ciga = models.CharField(verbose_name='흡연 여부', max_length=80)

    mail_agree = models.BooleanField(verbose_name='메일 수신', default=False)

    sms_agree = models.BooleanField(verbose_name='SMS', default=False)

    meet_path = models.CharField(verbose_name='나누방을 접한 경로', max_length=50, choices=MEET_PATH_CHOICES)

    active = models.BooleanField(default=False)
    auto_increment_id = models.AutoField(primary_key=True)
    payment = models.BooleanField(default=False)
    user_type = models.CharField(verbose_name='이용자 타입', max_length=80,  blank=True,null=True)
    connector = models.CharField(verbose_name='관계인', max_length=140, null=True,  blank=True)

class Connect(models.Model):
    Room_seller = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='판매자',related_name='sell', on_delete=models.CASCADE, null=True) 
    Room_buyer = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='구매자',related_name='buy', on_delete=models.CASCADE, null=True) 

class Room_infos(models.Model):

        floor = (
                ('7층↑','7층↑'),
                ('7층','7층'),
                ('6층','6층'),
                ('5층','5층'),
                ('4층','4층'),
                ('3층','3층'),
                ('2층','2층'),
                ('1층','1층'),
                ('반지하','반지하'),
                ('지하 1층','지하 1층'),
                ('지하 2층','지하 2층'),
                ('지하 2층↓','지하 2층↓'),
        )

        window = (
                ('0','0'),
                ('1','1'),
                ('2','2'),
                ('3','3'),
                ('4','4'),
                ('5','5'),
                ('6','6'),
                ('7','7'),
                ('7↑','7↑'),
        )
        author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

        auto_increment_id = models.AutoField(primary_key=True,blank=False)
        created_date = models.DateTimeField(default=timezone.now)
        published_date = models.DateTimeField(blank=True, null=True)
        address =  models.CharField(verbose_name = '주소',max_length=255,blank=False)
        address_detail = models.CharField(verbose_name = '상세주소',max_length=255,blank=False)
        univ = models.CharField(verbose_name='대학', max_length=15, choices=univ_list,blank=False)
        tag = models.CharField(verbose_name='태그', max_length=10,blank=False)
        room_type = models.CharField(verbose_name='방종류', max_length=6,blank=False)
        deposit = models.IntegerField(verbose_name='내고 있는 보증금')
        monthly_cost = models.IntegerField(verbose_name='내고 있는 월세')
        deposit_necessity = models.CharField(verbose_name='보증금 여부', max_length=6 ,blank=False)
        desired_deposit = models.IntegerField(verbose_name='받을 보증금')
        desired_monthly = models.IntegerField(verbose_name='받을 월세')
        management_cost_include = models.CharField(verbose_name='관리비 포함 여부', max_length=6 ,blank=False)
        management_cost = models.IntegerField(verbose_name='관리비')
        start_date = models.DateField(verbose_name='입실희망날짜', max_length=15 ,blank=False)
        end_date = models.DateField(verbose_name='퇴실희망날짜', max_length=15 ,blank=False)
        floor = models.CharField(verbose_name='층수', max_length=15, choices=floor,blank=False)
        sublessee_type1 = models.CharField(verbose_name='흡연여부', max_length=5 ,blank=False)
        sublessee_type2 = models.CharField(verbose_name='성별', max_length=5 ,blank=False)
        room_options = models.CharField(verbose_name='옵션', max_length=500 ,blank=True, null=True)
        sublessor_type1 = models.CharField(verbose_name='판매자 정보 표시 유형', max_length=10 ,blank=False)
        sublessor_type2 = models.CharField(verbose_name='판매자정보', max_length=30 ,blank=False)
        latitude = models.DecimalField(verbose_name='위도',max_digits=33, decimal_places=30)
        longitude = models.DecimalField(verbose_name='경도',max_digits=33, decimal_places=30)
        
        room_desc = models.CharField(verbose_name='방상세설명', max_length=300 ,blank=True, null=True)
        room_size = models.CharField(verbose_name='면적', max_length=10 ,blank=True, null=True)
        is_duplex = models.BooleanField(verbose_name='복층여부', default=False)
        window = models.CharField(verbose_name='창문수', max_length=300,choices=window ,blank=True, null=True)

        photo1 = models.ImageField(upload_to='%Y/%m/%d',blank=True ,null=True)
        photo2 = models.ImageField(upload_to='%Y/%m/%d',blank=True ,null=True, default='./default/img_icon_temp.png')
        photo3 = models.ImageField(upload_to='%Y/%m/%d',blank=True ,null=True, default='./default/img_icon_temp.png')
        photo4 = models.ImageField(upload_to='%Y/%m/%d',blank=True ,null=True, default='./default/img_icon_temp.png')
        pano_photo = models.ImageField(upload_to='%Y/%m/%d', blank=True ,null=True)

        like_user_set = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name='like_user_set',through='Like')

        state = models.IntegerField(verbose_name='거래 상태' ,blank=True, null=True, default=0)

        @property
        def like_count(self):
                return self.like_user_set.count()

        def publish(self):
                self.published_date = timezone.now()
                self.save()

class call_file(models.Model):
        author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
        file1 = models.FileField(upload_to='call_files/%Y/%m/%d',blank=True ,null=True)

class Like(models.Model):
        room_info = models.ForeignKey('Room_infos', on_delete=models.CASCADE)
        author = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        class Meta:
                unique_together = (
                        ('author', 'room_info')
                )

class Tags(models.Model):
        key = models.ForeignKey('Room_infos', on_delete=models.CASCADE, null=True)
        univ = models.CharField(verbose_name='대학', max_length=15, choices=univ_list,blank=False)
        tag = models.CharField(max_length=10)  
        
class Complete_contract(models.Model):
        room_info = models.ForeignKey('Room_infos', on_delete=models.CASCADE)
        Room_seller = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='저자',related_name='sell_complete', on_delete=models.CASCADE, null=True) 
        Room_buyer = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='계약자',related_name='buy_complete', on_delete=models.CASCADE, null=True) 

class Complete_contract_infos(models.Model):
        floor = (
                        ('7층↑','7층↑'),
                        ('7층','7층'),
                        ('6층','6층'),
                        ('5층','5층'),
                        ('4층','4층'),
                        ('3층','3층'),
                        ('2층','2층'),
                        ('1층','1층'),
                        ('반지하','반지하'),
                        ('지하 1층','지하 1층'),
                        ('지하 2층','지하 2층'),
                        ('지하 2층↓','지하 2층↓'),
        )

        window = (
                        ('0','0'),
                        ('1','1'),
                        ('2','2'),
                        ('3','3'),
                        ('4','4'),
                        ('5','5'),
                        ('6','6'),
                        ('7','7'),
                        ('7↑','7↑'),
        )
        author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

        auto_increment_id = models.AutoField(primary_key=True,blank=False)
        created_date = models.DateTimeField(default=timezone.now)
        published_date = models.DateTimeField(blank=True, null=True)
        address =  models.CharField(verbose_name = '주소',max_length=255,blank=False)
        address_detail = models.CharField(verbose_name = '상세주소',max_length=255,blank=False)
        univ = models.CharField(verbose_name='대학', max_length=15, choices=univ_list,blank=False)
        tag = models.CharField(verbose_name='태그', max_length=10,blank=False)
        room_type = models.CharField(verbose_name='방종류', max_length=6,blank=False)
        deposit = models.IntegerField(verbose_name='내고 있는 보증금')
        monthly_cost = models.IntegerField(verbose_name='내고 있는 월세')
        deposit_necessity = models.CharField(verbose_name='보증금 여부', max_length=6 ,blank=False)
        desired_deposit = models.IntegerField(verbose_name='받을 보증금')
        desired_monthly = models.IntegerField(verbose_name='받을 월세')
        management_cost_include = models.CharField(verbose_name='관리비 포함 여부', max_length=6 ,blank=False)
        management_cost = models.IntegerField(verbose_name='관리비')
        start_date = models.DateField(verbose_name='입실희망날짜', max_length=15 ,blank=False)
        end_date = models.DateField(verbose_name='퇴실희망날짜', max_length=15 ,blank=False)
        floor = models.CharField(verbose_name='층수', max_length=15, choices=floor,blank=False)
        sublessee_type1 = models.CharField(verbose_name='흡연여부', max_length=5 ,blank=False)
        sublessee_type2 = models.CharField(verbose_name='성별', max_length=5 ,blank=False)
        room_options = models.CharField(verbose_name='옵션', max_length=500 ,blank=True, null=True)
        sublessor_type1 = models.CharField(verbose_name='판매자 정보 표시 유형', max_length=10 ,blank=False)
        sublessor_type2 = models.CharField(verbose_name='판매자정보', max_length=30 ,blank=False)
        latitude = models.DecimalField(verbose_name='위도',max_digits=33, decimal_places=30)
        longitude = models.DecimalField(verbose_name='경도',max_digits=33, decimal_places=30)
        
        room_desc = models.CharField(verbose_name='방상세설명', max_length=300 ,blank=True, null=True)
        room_size = models.CharField(verbose_name='면적', max_length=10 ,blank=True, null=True)
        is_duplex = models.BooleanField(verbose_name='복층여부', default=False)
        window = models.CharField(verbose_name='창문수', max_length=300,choices=window ,blank=True, null=True)

        photo1 = models.ImageField(upload_to='%Y/%m/%d',blank=True ,null=True)
        photo2 = models.ImageField(upload_to='%Y/%m/%d',blank=True ,null=True, default='./default/img_icon_temp.png')
        photo3 = models.ImageField(upload_to='%Y/%m/%d',blank=True ,null=True, default='./default/img_icon_temp.png')
        photo4 = models.ImageField(upload_to='%Y/%m/%d',blank=True ,null=True, default='./default/img_icon_temp.png')
        pano_photo = models.ImageField(upload_to='%Y/%m/%d', blank=True ,null=True)
        Room_seller = models.CharField(verbose_name = '판매자',max_length=255,blank=False)
        Room_buyer = models.CharField(verbose_name = '구매자',max_length=255,blank=False)
    
    
