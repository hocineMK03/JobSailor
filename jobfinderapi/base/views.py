from django.shortcuts import render,redirect
from django.http import JsonResponse
import json
import uuid
import base64
import re
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
from django.core.cache import cache
from datetime import datetime, timedelta
from .models import Theuser, Session_model ,Job_listing,Theuser_conversation,Theuser_messages,Job_Category,Theuser_notifications,Job_accepted,Job_pending,Tokenhandlin,Theuser_worker,Theuser_Company
from django.core.paginator import Paginator
from django.http import HttpRequest

def validthetype(request):
    if(request.method=='GET'):
        session_id=request.GET.get('session_id',20)
        print(session_id)
        
        authent=False
        u=""

        print(session_id)
        if session_id is not None:
            try:
                sessioncust = Session_model.objects.get(session_id=session_id)
                authent = True
                
                u = sessioncust.user
                print(u,"u")
                return JsonResponse({'message':'informations about the user','id':u.id,'type':u.is_worker,'name':u.name})
                
            except Session_model.DoesNotExist as e:
                print("Session not found:", str(e))
            except Exception as e:
                print("An error occurred:", str(e))
            return JsonResponse({'message':'cant authent this user'},status=400)
    else:
        return JsonResponse({'message':'request method false'},status=405)

def paginatingforbrowser(request):
    
    

    if(request.method=='GET'):
        page_num = int(request.GET.get('page', 0))
        session_id=request.GET.get('session_id',20)
        print(session_id)
        authent=False
        u=""
    
        
        if session_id is not None:
            try:
                sessioncust = Session_model.objects.get(session_id=session_id)
                authent = True
                
                u = sessioncust.user
            

                
            except:
                u=None
                print("not logged in")
                print("u",u)
            print("pagenump",page_num)
            # Calculate the starting and ending indices for pagination based on page_num
            per_page =2
            start_idx = (page_num - 1) * per_page
            end_idx = page_num * per_page
            print("start_idx",start_idx,"end_idx",end_idx)
            
            if(u!=None):
                print("here")
                ordered_posts = Job_listing.objects.all().exclude(job_pending__pending_id=u).exclude(job_accepted__accepted_id=u).order_by('-posted_at')[start_idx:end_idx]
                print(ordered_posts)
            else:
                print("here1")
                ordered_posts = Job_listing.objects.all().order_by('-posted_at')[start_idx:end_idx]
            
            
            print(ordered_posts)
            
            job_list = [job.to_dict() for job in ordered_posts]
            job_listing_count = Job_listing.objects.count()
            pages=job_listing_count/per_page
            return JsonResponse({'items': job_list,"pages":pages})
    else:
        return JsonResponse({'message':'huh'})

def paginateforpendings(request):
    ordered_requests=""
    if(request.method=='GET'):
        session_id=request.GET.get('session_id',20)
        typeof=int(request.GET.get('type',3))
        authent=False
        u=""
        print("session id",session_id)
        
        if session_id is not None:
            try:
                sessioncust = Session_model.objects.get(session_id=session_id)
                authent = True
                
                u = sessioncust.user
            

                
            except:
                u=None
                print("not logged in")
                return JsonResponse({'message':'youre not authenticated'},status=400)
        print(u.id,"u.id")
        if(typeof !=1 and typeof !=2):
            return JsonResponse({'message':'error happenned'},status=400)
        elif(typeof==1):
            #means pending adn requests
            print("no")
            if(u.is_worker):
                ordered_requests=Job_pending.objects.filter(pending_id=u)
                print("worker")
            else:
                print("organisation")
            
            job_pending = [job.to_dict() for job in ordered_requests]
            return JsonResponse({'items': job_pending})
        
        elif(typeof==2):
            #means accepts
            print("n")
            if(u.is_worker):
                ordered_requests=Job_accepted.objects.filter(accepted_id=u)
                print("worker")
            else:

                print("organisation")
            print(ordered_requests)
            
            job_list = [job.to_dict() for job in ordered_requests]
            return JsonResponse({'items': job_list})
        
        
    else:
            return JsonResponse({'message':'huh1'})

    

def debugchecktime(time_start):
    time_now=timezone.now()
    time_dif=time_now-time_start
    seconds = time_dif.total_seconds()
    return seconds

def assigntoken(token_user):
    time_start=timezone.now()
    print("assign1",debugchecktime(time_start))
    try: 
        th=Tokenhandlin.objects.all()
    except Tokenhandlin.DoesNotExist:
        print("okay")
    except:
        return JsonResponse({'message':'something happened'},status=500)
    print("assign2",debugchecktime(time_start))
    thlength=len(th)
    # print("length",thlength)
    if(thlength<10):
        token_rand=str(uuid.uuid4())
        tokenhandlin=Tokenhandlin()
        tokenhandlin.token_rand=token_rand
        tokenhandlin.token_user=token_user
        tokenhandlin.save()
        print("assign3",debugchecktime(time_start))
        return True
    else:
        return False
def collecttoken(token_user):
    try:
        th=Tokenhandlin.objects.filter(token_user=token_user)
        th.delete()
        return True
    except:
        return JsonResponse({'message':'something happened'},status=500)

        
def check_rate_limit(request):
    user_identifier = request.META.get('REMOTE_ADDR')  # You can use another unique identifier if needed
    # print(user_identifier)
    rate_limit_key = f'rate_limit:{user_identifier}'
    rate_limit_window = 30  # Time window for rate limiting in seconds
    rate_limit_count = 10  # Number of requests allowed in the time window

    # Get the current timestamp
    current_time = int(timezone.now().timestamp())

    # Get the rate limit data from the cache
    rate_limit_data = cache.get(rate_limit_key)

    if rate_limit_data is None:
        # If no data is in the cache, initialize it
        rate_limit_data = {'requests': 1, 'window_start': current_time}
        cache.set(rate_limit_key, rate_limit_data, rate_limit_window)
    else:
        # If data exists, check if the rate limit has been exceeded
        if current_time - rate_limit_data['window_start'] <= rate_limit_window:
            rate_limit_data['requests'] += 1
        else:
            # If the time window has passed, reset the data
            rate_limit_data = {'requests': 1, 'window_start': current_time}

        if rate_limit_data['requests'] > rate_limit_count:
            return False  # Rate limit exceeded

        cache.set(rate_limit_key, rate_limit_data, rate_limit_window)

    return True  # Request is within the rate limit

def hashingalgorithme(text):
    original_string = text

                                # Encode the string to base64
    encoded_bytes = base64.b64encode(original_string.encode('utf-8'))
    encoded_string = encoded_bytes.decode('utf-8')
    # print(encoded_string)
    encoded_string.capitalize()
    return encoded_string

def validatingemail(email):
        pattern = r'^[a-zA-Z0-9]+([_.+%-]?[a-zA-Z0-9]+)*@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        match = re.match(pattern, email)
        return bool(match)

def check(request):
    u=""
    session_id = request.COOKIES.get('session_id')
    if session_id is not None:
        try:
            sessioncust = Session_model.objects.get(session_id=session_id)
            authent = True
            
            u = sessioncust.user
            return u
        except:
            print("not logged in")
            authent="notauthent"

    return authent

def create_session(theuser):  
    
    
    while True:
        session_id = str(uuid.uuid4())
        try:
            session = Session_model.objects.get(session_id=session_id)
            
            
        except:
            session = Session_model.objects.create(session_id=session_id, user=theuser)
            session.save()
            return session_id
        
    
        
def get_csrf_token(request):
    # Retrieve the CSRF token and send it as a JSON response
    csrf_token = get_token(request)
    print(csrf_token)
    return JsonResponse({'csrf_token': csrf_token})

def heropage(request):
    authent=False
    u=""
    session_id = request.COOKIES.get('session_id')
    if session_id is not None:
        try:
            sessioncust = Session_model.objects.get(session_id=session_id)
            authent = True
            
            u = sessioncust.user
            print(u.id)
        
            return redirect('home')
        except:
            print("not logged in")

    
    context={
        'authent':authent,
        'u':u,
    }
    return render(request,'heropage.html',context)



def home(request):
    u=""
    session_id = request.COOKIES.get('session_id')
    if session_id is not None:
        try:
            sessioncust = Session_model.objects.get(session_id=session_id)
            authent = True
            
            u = sessioncust.user
            print(u.id)
        except:
            print("not logged in")
    
    

def log_view(request):
    # csrf_token = get_token(request)
    # print("first",csrf_token)
    # print(request.method)
    return render(request,'login.html')

def log(request):
    time_start=timezone.now()
    print("time1",debugchecktime(time_start))
    
    csrf_token = get_token(request)
    # print(csrf_token)
    if(not check_rate_limit(request)):
        return JsonResponse({'message':'you cant sir'})
    authent = False
    # print("ee1"+request.method)
    http_method = request.META.get('REQUEST_METHOD')
    # print("ee"+http_method)
    if (request.method == 'POST'):
        # Use json.loads() to parse JSON from a string
        try:
            data = json.loads(request.body.decode('utf-8'))
            name = data.get('name')
            password = data.get('password')
            tmp = hashingalgorithme(password)
            tmp1=hashingalgorithme(name)
            # print(name,password)
            
            print("time2",debugchecktime(time_start))
                
            
            try:
                theuser = Theuser.objects.get(name=name, password=password)
            except Theuser.DoesNotExist:
                return JsonResponse({'message':'account is invalid'},status=400)
            print("time3",debugchecktime(time_start))
            if(assigntoken(theuser)):
                print("time4",debugchecktime(time_start))
                session_id=create_session(theuser)
                collecttoken(theuser)
                response = JsonResponse({'message': 'successfully login', 'csrf_token': csrf_token,'type':'1'})
                response.set_cookie('session_id', session_id)
                print("time5",debugchecktime(time_start))
                return response
            else:
                collecttoken(theuser)
                return JsonResponse({'message':'there is no space for you , try again later'},status=400)
        except json.JSONDecodeError as e:
            return JsonResponse({'message': 'Invalid JSON data'},status=400)
    else:
        return JsonResponse({'message': 'Invalid aa'}, status=405)
def register_view(request):
    # csrf_token = get_token(request)
    # print("first",csrf_token)
    # print(request.method)
    return render(request,'register.html')

def reg(request):
    csrf_token = get_token(request)
    print(csrf_token)
   
    print("ee1"+request.method)
    http_method = request.META.get('REQUEST_METHOD')
    print("ee"+http_method)
    if(not check_rate_limit(request)):
        return JsonResponse({'message':'you cant sir'})
    
    if (request.method == 'POST'):
        try:
                data = json.loads(request.body.decode('utf-8'))
                name = data.get('name')
                password = data.get('password')
                email=data.get('email')
                username=data.get('username')
                worker=bool(data.get('worker'))
                bio=data.get('bio')
                skills=data.get('skills')
                location=data.get('location')
                description=data.get('description')

                if(validatingemail(email)==False):
                    return JsonResponse({'message':'something happened1'},status=400)

                tmpuser=Theuser()
                tmpuser.name=name
                tmpuser.username=username
                tmpuser.email=email
                tmpuser.password=password
                tmpuser.is_worker=worker
                tmpuser.save()
                print(data)
                try:
                    tmpuser1=Theuser.objects.get(name=name,password=password)
                    print(tmpuser,worker)
                except:
                    return JsonResponse({'message':'something happenned2'},status=400)
                
                if(worker==True):
                    try:
                        print("here")
                        tmpworker=Theuser_worker()
                        tmpworker.theuser=tmpuser1
                        print("here2")
                        tmpworker.bio=bio
                        print("here3")
                        
                        tmpworker.location=location
                        
                        tmpworker.save()
                        print("is worker")
                    except:
                        return JsonResponse({'message':'somethin happened3'},status=400)
                    

                elif(worker==False):
                    try:
                        tmpcompany=Theuser_Company()
                        tmpcompany.name=tmpuser1
                        tmpcompany.description=description
                        tmpcompany.location=location
                        tmpcompany.save()
                        print("is not worker")
                    except:
                        return JsonResponse({'message':'somethin happened4'},status=400)
                    
                    
                    
                    
                if(assigntoken(tmpuser)):
                
                    session_id=create_session(tmpuser)
                    collecttoken(tmpuser)
                    response = JsonResponse({'message': 'Successfully registered'})
                    response.set_cookie('session_id', session_id)
                    return response
                else:
                    collecttoken(tmpuser)
                    return JsonResponse({'message':'there is no space for you , try again later'})

                
                return JsonResponse({'message': 'v'})
        except json.JSONDecodeError as e:
            return JsonResponse({'message': 'Invalid JSON data'},status=400)
    else:
        return JsonResponse({'message': 'Invalid aa'}, status=405)
                        
def out(request):
    session_id = request.COOKIES.get('session_id')
    print(session_id)
    
    if session_id:
        try:
            session = Session_model.objects.get(session_id=session_id)
            session.delete()

            # Create a JSON response indicating success and delete the cookie
            response = JsonResponse({'message': 'deleted'})
            response.delete_cookie('session_id')  # Remove the session_id cookie
            return response

        except Session_model.DoesNotExist:
            return JsonResponse({'message': 'Session not found'}, status=400)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)

    return JsonResponse({'message': 'No session_id cookie found'}, status=400)
#jobs
def addjob(request):
    csrf_token = get_token(request)
    print(csrf_token)
    u=""
    session_id = request.COOKIES.get('session_id')
    if session_id is not None:
        try:
            sessioncust = Session_model.objects.get(session_id=session_id)
            authent = True
            
            u = sessioncust.user
            print(u.id)
        except:
            print("not logged in")
            # return redirect('home')
  
    if(request.method=='POST'):
        try:

            data = json.loads(request.body)
            print(data)
            name=data.get('name')
            category=data.get('category')
            description=data.get('description')
            salary=data.get('salary')
            posted_by=data.get('posted_by')
            try:
                theuser = Theuser.objects.get(id=posted_by)
                
                
            except Theuser.DoesNotExist:
                return JsonResponse({'message':'account invalid'},status=400)


            try:
                c = Job_Category.objects.get(category_name=category)
                print(c)
            except Job_Category.DoesNotExist:
                c=""
                return JsonResponse({'message': 'Category does not exist'}, status=400)
            except:
                print("dont care")
                c=""
            try:

                test=Job_listing.objects.filter(name=name,posted_by=theuser).last()
                db_time=test.posted_at
                
                time_now=timezone.now()
                print(db_time,time_now)
                time_dif=time_now-db_time
                seconds = time_dif.total_seconds()

                print("here",seconds)
                if(seconds<150):
                    return JsonResponse({'message':'you already made a request','seconds':seconds})
            except:
                print("valid")

            if(assigntoken(theuser)):
                job_listing=Job_listing()
                job_listing.name=name
                job_listing.category=c
                
                job_listing.description=description
                job_listing.salary=salary
                job_listing.posted_by=theuser
                
                
                job_listing.save()
                collecttoken(theuser)
                return JsonResponse({'message': 'job added succesfully'})
            else:
                return JsonResponse({'message':'there is no space for you , try again later'})
             
        except json.JSONDecodeError as e:
            return JsonResponse({'message': 'Invalid JSON data'},status=400)

    else:
        return JsonResponse({'message': 'Invalid aa'}, status=405)


def deletejob(request):
    csrf_token = get_token(request)
    print(csrf_token)
    u=""
    session_id = request.COOKIES.get('session_id')
    if session_id is not None:
        try:
            sessioncust = Session_model.objects.get(session_id=session_id)
            authent = True
            
            u = sessioncust.user
            print(u.id)
        except:
            print("not logged in")
    
    if(request.method=='POST'):
        try:

            data = json.loads(request.body)
            job_id=data.get('job_id')
            user_id=data.get('user_id')
            try:
                u=Theuser.objects.get(id=user_id)
            except:
                return JsonResponse({'message':'user does not exist'})
            if(assigntoken(u)):
                try:
                    job_listing=Job_listing.objects.get(id=job_id,posted_by=u)
                    job_listing.delete()
                    response = JsonResponse({'message': 'Successfully deleted'})
                    collecttoken(u)
                    return response
                except:
                    collecttoken(u)
                    return JsonResponse({'message': 'cant find the job'}, status=400) 
            else:
                    collecttoken(u)
                    return JsonResponse({'message':'there is no space for you , try again later'})
        
        except json.JSONDecodeError as e:
            return JsonResponse({'message': 'Invalid JSON data'},status=400)
    else:
        return JsonResponse({'message': 'Invalid aa'}, status=405)
        
def editjob(request):
    u=""
    session_id = request.COOKIES.get('session_id')
    if session_id is not None:
        try:
            sessioncust = Session_model.objects.get(session_id=session_id)
            authent = True
            
            u = sessioncust.user
            print(u.id)
        except:
            print("not logged in")
    
    if(request.method=='POST'):
        try:

            data = json.loads(request.body)
            job_id=data.get('job_id')
            name=data.get('name')
            category=data.get('category')
            description=data.get('description')
            salary=data.get('salary')
            validation=True
            user_id=data.get('user_id')
            try:
                u=Theuser.objects.get(id=user_id)
            except:
                return JsonResponse({'message':'user does not exist'})
            try:
                c = Job_Category.objects.get(category_name=category)
                print(c)
            except Job_Category.DoesNotExist:
                return JsonResponse({'message': 'Category does not exist'}, status=400)
            except:
                c=""
            if(assigntoken(u)):

                try:
                    job_listing=Job_listing.objects.get(id=job_id,posted_by=u)
                    if(job_listing.edited==False):
                                job_listing.name=name
                                job_listing.category=c
                                job_listing.description=description
                                job_listing.salary=salary
                                job_listing.edited=True
                                job_listing.save()
                                collecttoken(u)
                                response = JsonResponse({'message': 'Successfully edited'})
                                
                                return response
                    else:
                                collecttoken(u)
                                return JsonResponse({'message': 'cant edit two times'})
                except:
                    return JsonResponse({'message': 'cant find the job'}, status=400)
                            
            else:
                return JsonResponse({'message':'there is no space for you , try again later'})
                    
                        
              
        except json.JSONDecodeError as e:
            return JsonResponse({'message': 'Invalid JSON data'},status=400)
        
    else:
        return JsonResponse({'message': 'Invalid aa'}, status=405)

def acceptjoboffer(request):
    u=""
    session_id = request.COOKIES.get('session_id')
    if session_id is not None:
        try:
            sessioncust = Session_model.objects.get(session_id=session_id)
            authent = True
            
            u = sessioncust.user
            print(u.id)
        except:
            return JsonResponse({'message':'youre not authenticated'},status=400)
    if(request.method=='POST'):
        try:
            data = json.loads(request.body)
            accepted_id=data.get('accepted_id')
            Job_id=data.get('Job_id')
            try:
                u1=Theuser.objects.get(id=accepted_id)
            except:
                return JsonResponse({'message':'user does not exist'})
            
            try:
                    ja=Job_accepted.objects.get(accepted_id=accepted_id,Job_id=Job_id)
                    return JsonResponse({'message':'user already accepted'})
            except:
                    print("okay")

            try:
                applyer=Job_pending.objects.get(pending_id=accepted_id)
            
            except:
                return JsonResponse({'message':'user not in pending'})

            try:
                joblist=Job_listing.objects.get(id=Job_id)
            except:
                return JsonResponse({'message':'cant find the job'},status=400)
            if(assigntoken(u)):

                job_accepted=Job_accepted()
                job_accepted.accepted_id=u1
                job_accepted.Job_id=joblist
                job_accepted.save()
                deletejobpending(joblist,u1)
                collecttoken(u)
                return JsonResponse({'message': 'Successfully accepted'})
            else:
                collecttoken(u)
                return JsonResponse({'message':'there is no space for you , try again later'})
        except json.JSONDecodeError as e:
            return JsonResponse({'message': 'Invalid JSON data'},status=400)
    else:
        return JsonResponse({'message': 'Invalid aa'}, status=405)

def deletejobpending(Job_id,theuser):
    
    try:
        print("hi",Job_id,theuser)
        pendingjob=Job_pending.objects.get(Job_id=Job_id,pending_id=theuser)
        print(pendingjob)
        pendingjob.delete()
        
        return True
    except:
        print("here")
        return JsonResponse({'message':'something happened when deleting the pending post'},status=400)
def deletependingandaccepts(request):
    u=""
    session_id = request.COOKIES.get('session_id')
    if session_id is not None:
        try:
            sessioncust = Session_model.objects.get(session_id=session_id)
            authent = True
            
            u = sessioncust.user
            print(u.id)
        except:
            return JsonResponse({'message':'youre not authenticated'},status=400)
    csrf_token = get_token(request)
    if(u.is_worker==False):
        return JsonResponse({'message':'organisations cant apply'},status=400)
    if(request.method=='POST'):
        try:
            data=json.loads(request.body)
            Job_id=data.get('Job_id')
            calltype=int(data.get('calltype'))

            if(calltype==1):
                try:

                    tmp1=Job_pending.objects.get(Job_id=Job_id,pending_id=u)
                    tmp1.delete()
                except:
                    return JsonResponse({'message':'something happened'},status=400)
            elif(calltype==2):
                try:

                    tmp1=Job_accepted.objects.get(Job_id=Job_id,accepted_id=u)
                    tmp1.delete()
                except:
                    return JsonResponse({'message':'something happened'},status=400)

            return JsonResponse({'message':'finished'})
        except json.JSONDecodeError as e:
            return JsonResponse({'message': 'Invalid JSON data'},status=400)

        
    else:
        return JsonResponse({'message','messgaemessage'},status=405)
def addordeletepending(request):
    u=""
    session_id = request.COOKIES.get('session_id')
    if session_id is not None:
        try:
            sessioncust = Session_model.objects.get(session_id=session_id)
            authent = True
            
            u = sessioncust.user
            print(u.id)
        except:
            return JsonResponse({'message':'youre not authenticated'},status=400)
    csrf_token = get_token(request)
    if(u.is_worker==False):
        return JsonResponse({'message':'organisations cant apply'},status=400)
    if(request.method=='POST'):
        try:
            data = json.loads(request.body)
            Job_id=data.get('Job_id')
            
            offered=data.get('applied')
            if(offered==True):

                new_request = HttpRequest()
                new_request.method = 'POST'
                new_request._body = json.dumps({
                    "pending_id": u.id,
                    "Job_id": Job_id
                }).encode('utf-8')
                new_request._stream = None

                # Call the other endpoint with the new request
                response = pendingjobapply(new_request)
                
                print(response)
                return JsonResponse({'message':'meesage11','jobid':Job_id,'offered':offered})
            else:
                theuser=check(request)
                if(theuser!="notauthent"):
                    deletejobpending(Job_id,theuser)
                    return JsonResponse({'message':'meesage','jobid':Job_id,'offered':offered})
                
        except json.JSONDecodeError as e:
            return JsonResponse({'message': 'Invalid JSON data'},status=400)
    else:
        return JsonResponse({'message','messgaemessage'},status=405)
def pendingjobapply(request):
   
    if(request.method=='POST'):
        try:
            data = json.loads(request.body)
            Job_id=data.get('Job_id')
            pending_id=data.get('pending_id')

            try:
                u1=Theuser.objects.get(id=pending_id)
            except:
                return JsonResponse({'message':'user does not exist'})
            
            try:
                    ja=Job_accepted.objects.get(accepted_id=pending_id,Job_id=Job_id)
                    return JsonResponse({'message':'user already accepted'})
            except:
                    print("okay")

            try:
                    jp=Job_pending.objects.get(pending_id=pending_id,Job_id=Job_id)
                    return JsonResponse({'message':'user already in pending'})
            except:
                    print("okay")

            try:
                joblist=Job_listing.objects.get(id=Job_id)
            except:
                return JsonResponse({'message':'cant find the job'},status=400)
            job_pending=Job_pending()
            job_pending.Job_id=joblist
            job_pending.pending_id=u1
            job_pending.save()
            return JsonResponse({'message':'request added successfully'})
        except json.JSONDecodeError as e:
            return JsonResponse({'message': 'Invalid JSON data'},status=400)
    else:
        return JsonResponse({'message': 'Invalid aa'}, status=405)

def showjobappliers(request):
    u=""
    session_id = request.COOKIES.get('session_id')
    if session_id is not None:
        try:
            sessioncust = Session_model.objects.get(session_id=session_id)
            authent = True
            
            u = sessioncust.user
            print(u.id)
        except:
            return JsonResponse({'message':'youre not authenticated'},status=400)
    if(request.method=='POST'):
        try:
            data = json.loads(request.body)
            Job_id=data.get('Job_id')
            try:
                joblist=Job_listing.objects.get(id=Job_id)
            except:
                return JsonResponse({'message':'cant find the job'},status=400)
            try:
                if(assigntoken(u)):

                    print(joblist)
                    pendings=Job_pending.objects.filter(Job_id=joblist)
                    pending_data = list(pendings.values())
                    
                    collecttoken(u)
                    return JsonResponse({'data':pending_data})
                else:
                    collecttoken(u)
                    return JsonResponse({'message':'there is no space for you , try again later'})
            except:
                return JsonResponse({'message':'there is no appliers to this job'})
        except json.JSONDecodeError as e:
            return JsonResponse({'message': 'Invalid JSON data'},status=400)
    else:
        return JsonResponse({'message': 'Invalid aa'}, status=405)
    

#messages
def messagedisplay(request):
    validation=True
    valid=True
    u=""
    session_id = request.COOKIES.get('session_id')
    if session_id is not None:
        try:
            sessioncust = Session_model.objects.get(session_id=session_id)
            authent = True
            
            u = sessioncust.user
            print(u.id)
        except:
            print("not logged in")
            return redirect('home')
    
    if(request.method=='POST'):
        try:

            data=json.load(request.body.decode('utf-8'))
            conversation_identifier=data.get('conversation_identifier')
            message_sender=data.get('message_sender')
            message_receiver=data.get('message_receiver')
            message_body=data.get('message_body')
            
            try:
                ms=Theuser.objects.get(id=message_sender.id)
            except:
                validation=False
            try:
                mr=Theuser.objects.get(id=message_receiver.id)
            except:
                valid=False
            
            if(validation and valid):

                try:
                    theuser_conversation=Theuser_conversation.objects.get(conversation_identifier=conversation_identifier)
                    theuser_messages1=Theuser_messages.objects.filter(message_sender=message_sender,message_receiver=message_receiver)
                    theuser_messages2=Theuser_messages.objects.filter(message_sender=message_receiver,message_receiver=message_sender)
                    #merge   
                    return JsonResponse({'message':'conversation is loaded'})  #add conversation id next   
                except:
                    return JsonResponse({'message':'a new conversation is loaded'})#add conversation id next 
            elif(validation and not valid):
                return JsonResponse({'message':'receiver doesnt exist'})
            elif(not validation and valid):
                return JsonResponse({'message':'sender invalid'})
        except json.JSONDecodeError as e:
            return JsonResponse({'message': 'Invalid JSON data'},status=400)
    else:
        return JsonResponse({'message': 'Invalid aa'}, status=405)
        
            


def messageadd(request):
    validation=True
    valid=True
    authent=False
    u=""
    session_id = request.COOKIES.get('session_id')
    if session_id is not None:
        try:
            sessioncust = Session_model.objects.get(session_id=session_id)
            authent = True
            
            u = sessioncust.user
            print(u.id)
        except:
            print("not logged in")
    
    if(request.method=='POST'):
        try:

            data=json.load(request.body.decode('utf-8'))
            conversation_identifier=data.get('conversation_identifier')
            message_sender=data.get('message_sender')
            message_receiver=data.get('message_receiver')
            message_body=data.get('message_body')
            try:
                ms=Theuser.objects.get(id=message_sender.id)
            except:
                validation=False
            try:
                mr=Theuser.objects.get(id=message_receiver.id)
            except:
                valid=False
            
            if(message_body is None):
                return JsonResponse({'message': 'body shouldnt be empty '})
            if(validation and valid):

                try:
                    theuser_conversation=Theuser_conversation.objects.get(conversation_identifier=conversation_identifier)
                    theuser_messages=Theuser_messages()
                    theuser_messages.message_sender=message_sender
                    theuser_messages.message_receiver=message_receiver
                    theuser_messages.message_body=message_body
                    theuser_messages.message_belongto=conversation_identifier
                    theuser_messages.save()
                       
                    return JsonResponse({'message':'conversation is loaded'})  #add conversation id next   
                except:
                    return JsonResponse({'message':'a new conversation is loaded'})#add conversation id next             
            elif(validation and not valid):
                return JsonResponse({'message':'receiver doesnt exist'})
            elif(not validation and valid):
                return JsonResponse({'message':'sender invalid'})
        except json.JSONDecodeError as e:
            return JsonResponse({'message': 'Invalid JSON data'},status=400)
    else:
        return JsonResponse({'message': 'Invalid aa'}, status=405)


def messagedelete(request):
    theuser_messages=""
    u=""
    session_id = request.COOKIES.get('session_id')
    if session_id is not None:
        try:
            sessioncust = Session_model.objects.get(session_id=session_id)
            authent = True
            
            u = sessioncust.user
            print(u.id)
        except:
            print("not logged in")
    if(request.method=='POST'):
        try:

            data=json.load(request.body.decode('utf-8'))
            # message_sender=data.get('message_sender')
            # message_receiver=data.get('message_receiver')
            message_body=data.get('message_body')
            message_id=data.get('message_id')
            try:
                theuser_messages=Theuser_messages(id=message_id.id)
            except:
                return JsonResponse({'message':'message cant be found'})
            if(theuser_messages.message_body_isempty):
                return JsonResponse({'message':'message already deleted'})
            else:

                theuser_messages.message_body=""
                theuser_messages.message_body_isempty=True
                theuser_messages.save()
                return JsonResponse({'message': 'message Successfully deleted'})
        

        except json.JSONDecodeError as e:
            return JsonResponse({'message': 'Invalid JSON data'},status=400)

    else:
        return JsonResponse({'message': 'Invalid aa'}, status=405)





#profil

def profildisplay(request,name):
    
    u=""
    thestyling="color=#050505;"
    session_id = request.COOKIES.get('session_id')
    istheuser=False
    if session_id is not None:
        try:
            sessioncust = Session_model.objects.get(session_id=session_id)
            
            
            u = sessioncust.user
            print(u.id)
        except:
            
            print("not logged in")
        
        
        try:
            profiluser=Theuser.objects.get(name=name)
            if(u.name==name):
                istheuser=True

            if(profiluser.is_worker):
                profiluser_worker=Theuser_worker.objects.get(theuser=profiluser)
                return JsonResponse({'profildata':profiluser_worker,'istheuser':istheuser})
            else:
                profiluser_company=Theuser_Company.objects.get(name=profiluser)
                return JsonResponse({'profildata':profiluser_company,'istheuser':istheuser})


                
        except:
            return JsonResponse({'message':'something happenned'},status=400)

    else:
        return JsonResponse({'message':'something happenned'},status=400)



#to fix
#handling api calls
#json responses still doesn't send data
#handling deleting accounts
#handling trafic
#pagination for displaying messages or using a delete system after 24 h
#pagination for displaying joboffers