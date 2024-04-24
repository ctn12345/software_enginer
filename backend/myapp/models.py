from django.db import models
# Create your models here.

# 旅行社的工作人员的表
class Travel_agencies(models.Model):
    travel_name = models.CharField(primary_key=True,max_length=255)
    account = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=11)
    password = models.TextField()

    # age = models.IntegerField()
    # 其他字段...

    def __str__(self):
        return self.travel_name

# 乘客表
class guest(models.Model):
    name = models.TextField()
    identify_card = models.CharField(primary_key=True, max_length=20)
    phone_number = models.CharField(max_length=12)
    sex = models.CharField(max_length=8)
    work = models.CharField(max_length=20)
    travel_name = models.ForeignKey(Travel_agencies,on_delete=models.CASCADE)

#     def __str__(self):
#         return self.identify_card


    
# # root 用户
class root_user(models.Model):
    account = models.CharField(primary_key=True,max_length=200)
    name = models.CharField(max_length=20)
    work = models.CharField(max_length=20)
    password = models.TextField()

    def __str__(self):
        return self.name

# # 航班表
class flight(models.Model):
    flight_number = models.CharField(primary_key=True,max_length=20)
    from_date = models.DateTimeField()
    
    def formatted_date_from(self):
        return self.from_date.strftime("%y年%m月%d日%H时%M分")
    
    arrived_date = models.DateTimeField()
    def formatted_date_end(self):
        return self.arrived_date.strftime("%y年%m月%d日%H时%M分")
    
    # from_date = formatted_date_from()
    # arrived_date = formatted_date_end()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    destination = models.CharField(max_length=20)
    from_location = models.CharField(max_length=20)
    avilable_seat = models.BigIntegerField()

    def __str__(self):
        return self.flight_number

# # 订票信息
class reserve_tickets(models.Model):
    flight_number = models.ForeignKey(flight, on_delete=models.CASCADE)   
    identify_card = models.ForeignKey(guest, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)
    is_ticket = models.BooleanField()

    def __str__(self):
        return self.flight_number