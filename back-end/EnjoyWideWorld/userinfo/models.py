from django.db import models


# 用户信息
class UserInfo(models.Model):
    username = models.CharField(max_length = 32)
    username.primary_key = True # 主键
    password = models.CharField(max_length = 32)
    profile_picture = models.ImageField(upload_to='./user/', default = None) # 用户头像
    
    # optional 
    gender = models.CharField(max_length = 2, default = "其他") # 男性、女性、其他
    description = models.TextField(default = "宅呀宅呀宅呀宅～～～") # 用户简介
    birthday = models.DateField(default = None) # 用户生日
    email = models.EmailField(max_length=75, default = None) # 用户邮箱
    phone = models.CharField(max_length = 32, default = None) # 用户电话
    
    position = models.CharField(max_length = 32, default = None) # 用户居住地
    
    create_time = models.DateField(default = None) # 用户创建时间
    
    update_time = models.DateField(default = None) # 用户最后一次修改时间
    
    def __str__(self):
        return self.username
    
# 宠物信息
class Pet(models.Model):
    username = models.CharField(max_length = 32)
    petname = models.CharField(max_length = 32)
    level = models.PositiveIntegerField(default = 0) # 等级
    experience = models.PositiveIntegerField(default = 0) # 经验值 
    weight = models.PositiveIntegerField(default = 0) # 体重
    gender = models.CharField(max_length = 2, default = "无性") # 雄性、雌性、无性
    
    pet_picture =  models.ImageField(upload_to='./pet/', default = None) # 宠物头像
    
    birthday = models.DateField(default = None) # 宠物生日
    
    update_time = models.DateField(default = None) # 宠物最后一次修改时间
    
    description = models.TextField(default = "我是主人的小棉袄") # 宠物简介
    
    def __str__(self):
        return "{0}.{1}".format(self.username, self.petname)

# 地点信息  
class Position(models.Model):
    username = models.CharField(max_length = 32) # 用户名
    petname = models.CharField(max_length = 32) # 宠物名
    position_name = models.CharField(max_length = 32) # 地点名
    longitude = models.DecimalField(max_digits=20, decimal_places = 15) # 经度
    latitude = models.DecimalField(max_digits=20, decimal_places = 15) # 纬度
    position_picture =  models.ImageField(upload_to='./position/', default = None) # 地点图片
    time = models.DateField(default = None) # 打卡时间
    notes = models.TextField(default = "到此一游") # 地点随记
    
    def __str__(self):
        return "{0}.{1}.{2}".format(self.username, self.petname, self.position_name)