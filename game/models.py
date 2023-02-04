from django.db import models
from django.contrib.auth.models import User
import uuid

def get_code():
    return 'H_'+uuid.uuid4().hex[:8].upper()

def get_qr():
    return 'QR_'+uuid.uuid4().hex[:9].upper()

# Create your models here.
class QRScan(models.Model):
    code = models.CharField(max_length=400,default=get_qr(),unique=True)
    sponsor = models.CharField(max_length=200,default="")
    points_max = models.IntegerField(default=50)
    points_mid = models.IntegerField(default=15)
    points_min = models.IntegerField(default=10)
    count  = models.IntegerField(default=0)
    location = models.TextField()
    def __str__(self) -> str:
        return "QR code at "+self.location +"| QR_VAL="+self.code

class Gamer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=14)
    college = models.CharField(max_length=300)
    referral_code = models.TextField(blank=True,null=True)
    points = models.IntegerField(default=0)
    share_code = models.CharField(max_length=8,blank=True,default=get_code(),unique=True)
    def __str__(self) -> str:
        return self.user.email + ' share-code: '+self.share_code
    
    @property
    def get_total_points(self):
        scans_list = SuccessfullScan.objects.all().filter(gamer=self)
        qr_points = 0
        for scan in scans_list:
            qr_points+=scan.points_given
        total_points = self.points + qr_points
        return total_points

class ClubMember(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    def __str__(self) -> str:
        return 'Club Member' + self.user.email

class SuccessfullScan(models.Model):
    gamer = models.ForeignKey(Gamer,on_delete=models.CASCADE)
    qr_code_id = models.IntegerField()
    points_given = models.IntegerField(default=0)
    scanned_at = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return "scanned by " + self.gamer.user.email + " at " + self.scanned_at.isoformat()
    
    @property
    def get_qr_code(self):
        return QRScan.objects.get(id=self.qr_code_id)