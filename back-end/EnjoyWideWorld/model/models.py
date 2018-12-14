# This file includes all models i.e. database tables.
# ZHOU Kunpeng, 14 Dec 2018

from django.db import models

# 物品信息
class Item(models.Model):
    id = models.AutoField(primary_key = True)  # Auto increment ID
    name = models.CharField(max_length = 32, null = True)    # Name
    description = models.TextField(null = True)    # Description
    addHealth = models.PositiveIntegerField(default = 0) # 加生命值
    addAttack = models.PositiveIntegerField(default = 0) # 加攻击力
    addDefend = models.PositiveIntegerField(default = 0) # 加防御力
    addSpeed = models.PositiveIntegerField(default = 0) # 加速度
    addDodgeRate = models.PositiveIntegerField(default = 0) # 加闪避率

    def __str__(self):
        return "{0},{1}".format(self.id, self.name)

# 地点信息
class Position(models.Model):
    id = models.AutoField(primary_key = True)  # Auto increment ID
    name = models.CharField(max_length = 32, null = True)   # Position name
    longitude = models.DecimalField(max_digits = 20, decimal_places = 15) # 经度
    latitude = models.DecimalField(max_digits = 20, decimal_places = 15) # 纬度
    position_picture =  models.ImageField(upload_to='./position/', default = None, null = True) # 地点图片
    description = models.TextField(default = "到此一游", null = True) # 地点简介

    # The item that the user obtains when checking in this position.
    itemLinked = models.ForeignKey(Item, null = True, on_delete = models.SET_NULL)

    def __str__(self):
        return "{0},{1}".format(self.id, self.name)

# 用户信息
class User(models.Model):
    wechatId = models.CharField(max_length = 32, primary_key = True) # 主键

    # Many-to-one field to Pet. Related name: pets

    # Many-to-may fields are linked to CheckInRecord
    checkInPositions = models.ManyToManyField(Position, through = "CheckInRecord")

    # Many-to-may fields are linked to LikeRecord
    # Related name: likes - beingLikeds
    likes = models.ManyToManyField('User', through = "LikeRecord")

    def __str__(self):
        return self.wechatId

# 宠物信息
class Pet(models.Model):
    id = models.AutoField(primary_key = True)  # Auto increment ID

    master = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'pets')  # 主人: Many-to-one for now

    name = models.CharField(max_length = 32)    # 昵称
    experience = models.PositiveIntegerField(default = 0) # 经验值

    health = models.PositiveIntegerField(default = 0) # 生命值
    attack = models.PositiveIntegerField(default = 0) # 攻击力
    defend = models.PositiveIntegerField(default = 0) # 防御力
    speed = models.PositiveIntegerField(default = 0) # 速度
    dodgeRate = models.PositiveIntegerField(default = 0) # 闪避率
    # updateTime = models.DateField(default = None) # 宠物最后一次修改时间

    def __str__(self):
        return "{0},{1}".format(self.id, self.name)


# 打卡信息
class CheckInRecord(models.Model):
    id = models.AutoField(primary_key = True)  # Auto increment ID
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    point = models.ForeignKey(Position, on_delete = models.CASCADE)

    def __str__(self):
        return "{0}:({1}, {2})".format(self.id, self.user.wechatId, self.point.name)


# 点赞信息
class LikeRecord(models.Model):
    id = models.AutoField(primary_key = True)  # Auto increment ID
    userFrom = models.ForeignKey(User, on_delete = models.CASCADE)
    userTo = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "beingLikeds")

    def __str__(self):
        return "{0}:({1}, {2})".format(self.id, self.userFrom.wechatId, self.userTo.wechatId)
