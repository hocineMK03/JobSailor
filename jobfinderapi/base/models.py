from django.utils import timezone

from django.db import models

# Create your models here.

class Theuser(models.Model):
    name=models.TextField(null=False,unique=True,max_length=70)
    username=models.TextField(null=True,max_length=70) #optionel
    email= models.EmailField(null=False, max_length=254)
    password=models.TextField(max_length=254)
    is_worker=models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    last_accessed = models.DateTimeField(auto_now=True)
    

class Theuser_skills(models.Model):
    skill_name=models.TextField(max_length=70)
class Theuser_worker(models.Model):
    theuser=models.ForeignKey(Theuser,on_delete=models.CASCADE)
    #details
    bio=models.TextField(null=True)
    # skills=models.ForeignKey(Theuser_skills,on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    # websitelink=models.URLField(null=True)
    # resume = models.FileField(upload_to="resumes/", null=True) 
class Theuser_Company(models.Model):
    name=models.ForeignKey(Theuser,on_delete=models.CASCADE)
    description = models.TextField()
    location = models.CharField(max_length=255)
    # logo=models.ImageField(upload_to="logo/")
    # websitelink=models.URLField(null=True)




class Tokenhandlin(models.Model):
    token_rand=models.TextField(primary_key=True)
    token_user=models.ForeignKey(Theuser,on_delete=models.CASCADE)
    posted_at = models.DateTimeField(auto_now_add=True)
    


class Session_model(models.Model):
    session_id = models.CharField(max_length=40, primary_key=True)
    user = models.ForeignKey(Theuser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_accessed = models.DateTimeField(auto_now=True)

    # def check_session(self,session_id):
    #     u=""
    #     session_id = self.COOKIES.get('session_id')
    #     if session_id is not None:
    #         try:
    #             sessioncust = Session_model.objects.get(session_id=session_id)
    #             authent = True
                
    #             u = sessioncust.user
    #             print(u.id)
    #         except:
    #             print("not logged in")
    #             authent=False

    #     return authent

    

class Job_Category(models.Model):
    category_name=models.TextField(null=True,max_length=70)

class Job_listing(models.Model):
    name=models.TextField(null=False,max_length=70)
    category=models.ForeignKey(Job_Category,on_delete=models.CASCADE,null=True,blank=True)
    description = models.TextField()
    salary=models.IntegerField(default=0)
    
    posted_by=models.ForeignKey(Theuser,on_delete=models.CASCADE)
    edited=models.BooleanField(default=False)
   
    posted_at = models.DateTimeField(default=timezone.now)

    offered=models.BooleanField(default=False)
    #nu_appllierss=models.IntegerField(default=0)
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category.category_name,
            'description': self.description,
            'posted_by': self.posted_by.name,
            'posted_at': self.posted_at,
            'offered':self.offered
            # Add more fields as needed
        }
# class Job_listing(models.Model):
#     name=models.TextField(null=False,max_length=70)
#     category=models.ForeignKey(Job_Category,on_delete=models.CASCADE)
#     description = models.TextField()
#     salary=models.IntegerField(default=0)
#     edited=models.BooleanField(default=False)
#     posted_by=models.ForeignKey(Theuser,on_delete=models.CASCADE)
#     posted_at = models.DateTimeField(auto_now_add=True)
#     offered=models.BooleanField(default=False)

class Job_accepted(models.Model):
    Job_id=models.ForeignKey(Job_listing,on_delete=models.CASCADE)
    accepted_id=models.ForeignKey(Theuser,on_delete=models.CASCADE)
    posted_at = models.DateTimeField(auto_now_add=True)
    def to_dict(self):
        return {
            'Job_id': self.Job_id.id,
            'Job_name':self.Job_id.name,
            'accepted_name': self.Job_id.posted_by.name,
            'posted_at': self.posted_at,
            
        }
class Job_pending(models.Model):
    Job_id=models.ForeignKey(Job_listing,on_delete=models.CASCADE)
    pending_id=models.ForeignKey(Theuser,on_delete=models.CASCADE)
    posted_at = models.DateTimeField(auto_now_add=True)

    def to_dict(self):
        return {
            'Job_id': self.Job_id.id,
            'Job_name':self.Job_id.name,
            'accepted_name': self.Job_id.posted_by.name,
            'posted_at': self.posted_at,
        }








class Theuser_conversation(models.Model):
    conversation_identifier=models.TextField(primary_key=True)
    
class Theuser_messages(models.Model):
    #didn't handle user deleting the account
    message_belongto=models.ForeignKey(Theuser_conversation,on_delete=models.CASCADE)
    message_sender=models.ForeignKey(Theuser,on_delete=models.DO_NOTHING,related_name="sender")
    message_receiver=models.ForeignKey(Theuser,on_delete=models.DO_NOTHING,related_name="receiver")
    message_body=models.TextField(null=True) 
    message_body_isempty=models.BooleanField(default=False)
    posted_at = models.DateTimeField(auto_now_add=True)









class Theuser_notifications_type(models.Model):
    notification_types=models.TextField(null=False,max_length=256)
    #types of notifications 
# apply , accepted , declined,
class Theuser_notifications(models.Model):
    notification_sender=models.ForeignKey(Theuser,on_delete=models.CASCADE,related_name="notifsender")
    notification_receiver=models.ForeignKey(Theuser,on_delete=models.CASCADE,related_name="notifreceiver")
    notification_header=models.TextField(max_length=256,null=False,blank=False)
    notification_body=models.TextField(max_length=256,null=False,blank=False)
    isread=models.BooleanField(default=False)
    post_linked=models.ForeignKey(Job_listing,on_delete=models.CASCADE) #so he can access
    posted_at = models.DateTimeField(auto_now_add=True)
    

