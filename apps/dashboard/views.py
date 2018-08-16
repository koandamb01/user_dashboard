from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request, 'dashboard/index.html')

# render the sign in page form
def signin_page(request):
    return render(request, 'dashboard/signin_page.html')

# Log user out 
def logout(request):
    request.session.clear()
    return redirect('/')

# render the sign in page form
def register_page(request):
    return render(request, 'dashboard/register_page.html')

# render the users dashbord
def dashboard(request):
    # check if user id exist in session
    if 'user_id' not in request.session:
        return redirect('/')
    try:
        mydata = User.objects.get(id = request.session['user_id']) # get the logged in user data
    except:
        return redirect('/')
    users = User.objects.all() # get all users data

    if mydata.user_level == 9:
        return render(request, 'dashboard/admin_dashboard.html', {'users': users, 'mydata': mydata})
    else:
        return render(request, 'dashboard/user_dashboard.html', {'users': users, 'mydata': mydata})


# render the add new user in page form
def new_user_page(request):
    # return render(request, 'dashboard/user_dashboard.html')
    return render(request, 'dashboard/new_user_page.html')

# render the edit profile form
def edit_profile_page(request, id):
    try:
        user = User.objects.get(id = id)
    except:
        messages.error(request, "An error accurred during your request!")
        return redirect('/dashboard')
    return render(request, 'dashboard/profile_page.html', {'user': user})


# update the user first, last, email
def update_personal(request):
    # check if this is a POST request
    if request.method != 'POST':
        return redirect('/')
    # get the user object
    try:
        user = User.objects.get(id = int(request.POST['id']))
    except:
        messages.error(request, "An erro occurred while processing your request!")
        return redirect('/')
    
    user.first_name = request.POST['first_name']
    user.last_name = request.POST['last_name']
    user.email = request.POST['email']
    user.save()

    messages.success(request, "User information has successfully updated!", 'personal')
    return redirect('/edit_profile/'+request.POST['id'])

# update the user password
def update_password(request):
    # check if this is a POST request
    if request.method != 'POST':
        return redirect('/')
    # get the user objects
    try:
        user = User.objects.get(id = int(request.POST['id']))
    except:
        messages.error(request, "An erro occurred while processing your request!")
        return redirect('/')

    errors = User.objects.basic_validator(request.POST)
    # check if any errors exist
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value, key)
        return redirect('/edit_profile/'+request.POST['id'])
    
    hash_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    user.password = hash_pw
    user.save()
    messages.success(request, "User password has successfully updated!", 'password')
    return redirect('/edit_profile/'+request.POST['id'])


# update the user description
def update_description(request):
    # check if this is a POST request
    if request.method != 'POST':
        return redirect('/')
    # get the user object
    try:
        user = User.objects.get(id = int(request.POST['id']))
    except:
        messages.error(request, "An erro occurred while processing your request!")
        return redirect('/')

    user.desc = request.POST['desc']
    user.save()

    messages.success(request, "User description has successfully updated!", 'description')
    return redirect('/edit_profile/'+request.POST['id'])


# show the user information and messages
def show(request, id):
    # check if the user is login
    if 'user_id' not in request.session:
        return redirect('/')
    
    user = User.objects.get(id = id) # get the user information

    user_messages = user.received_messages.all() # get the user received messages
    
    messages_with_comments = [] # list to get all the messages with thier comments
    
    for msg in user_messages: # loop through each message object to be able to get their comments
        m = Message.objects.get(id = msg.id) # get this message object
        comments = m.message_comments.all() # use the message object to get all its comments
        
        # get the user that send the message name
        u = User.objects.get(sent_messages = msg)

        # fetch through the comments to get the commenter information
        new_comments = []
        for comment in comments:
            u = User.objects.get(post_comments = comment) # get the user who post this comment
            # make a new comment with the commenter user first and last name
            tem_comment = {
                'comment': comment.comment,
                'commenter_id': u.id,
                'commenter_first_name': u.first_name,
                'commenter_last_name': u.last_name,
                'created_at': comment.created_at
            }
            new_comments.append(tem_comment)

        # append this message with all its comments to the list
        messages_with_comments.append(
            {
                'id': msg.id,
                'message': msg.message,
                'sender_id': msg.sender_id,
                'sender_first_name': u.first_name,
                'sender_last_name': u.last_name,
                'receiver_id': msg.receiver_id,
                'created_at': msg.created_at,
                'updated_at': msg.updated_at,
                'comments': new_comments
            }
        )
    return render(request, 'dashboard/show.html', {'user': user, 'messages_with_comments': messages_with_comments})



# admin only method to remove a user from the database 
def destroy(request, id):
    # check if the user login
    if 'user_id' not in request.session:
        return redirect('/')
    try:
        user = User.objects.get(id = id)
    except:
        return redirect('/dashboard')
    user.delete()

    messages.success(request, "A user has been successfully remove from the system")
    return redirect('/dashboard')



############## REGISTRATION #################
def register_me(request):
    # check if this was a post request
    if request.method != 'POST':
        return redirect('/')
    
    errors = User.objects.basic_validator(request.POST)
    # check if any errors exist
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value, key)

            # record form data to sessions
            request.session['first_name'] = request.POST['first_name']
            request.session['last_name'] = request.POST['last_name']
            request.session['email'] = request.POST['email']
        
        # check if the user is login or not, if the user is login, that mean it an admin user
        if 'user_id' not in request.session:
            return redirect('/register')
        else:
            return redirect('/new')
    else:
        # check email already exist in the database
        user = User.objects.filter(email = request.POST['email'])
        if user:
            messages.error(request, '*Email already exist', 'email')
            request.session['first_name'] = request.POST['first_name']
            request.session['last_name'] = request.POST['last_name']
            request.session['email'] = request.POST['email']
            return redirect('/')
        
        # Hash the user password first
        hash_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects # create an object of the user table
        user.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hash_pw
        )
    
    # New a user has been successfully register
    messages.success(request, 'You have successfull register', 'register')
    
    # check if it is the admin creating a new user
    if 'user_id' not in request.session:
        request.session.clear()
        request.session['user_id'] = user.last().id
        return redirect('/dashboard')
    return redirect('/dashboard')


# sign in the user
def login(request):
    if request.method != 'POST':
        messages.error(request, '*You must logged in first', 'login')
        return redirect('/')
    
    # no validation error, so fetch the user data
    user = User.objects.filter(email = request.POST['email'])
    if not user: # if the user email doesn't exist redirect it back with error
        messages.error(request, '*Email or password is invalid', 'login')
        return redirect('/signin')

    user = user[0] # since it is a list with only one element, get the first element
    if not bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        # password did not match so redirect the user back to fix the error
        messages.error(request, '*Email or password is invalid', 'login')
        return redirect('/signin')
        
    # password match so logged the user in 
    request.session['user_id'] = user.id
    return redirect('/dashboard')



############## SEND A MESSAGES ####################
def send_message(request):
    # check if this post method
    if request.method != 'POST':
        request.session.clear()
        return redirect('/')

    sender = User.objects.get(id = int(request.POST['sender_id'])) # get the sender object from the database models
    receiver = User.objects.get(id = int(request.POST['receiver_id'])) # get the receiver object from the database models

    # Send the message now 
    Message.objects.create(message=request.POST['message'], sender=sender, receiver=receiver)
    messages.success(request, 'Message sent!')
    return redirect('/show/'+request.POST['receiver_id'])


############# POST A COMMENT #################
def post_comment(request):
    # check if this post method
    if request.method != 'POST':
        request.session.clear()
        return redirect('/')
    
    commenter = User.objects.get(id = int(request.POST['commenter_id'])) # the commenter object from the database models
    message = Message.objects.get(id = int(request.POST['message_id'])) # the message being commented on object from the database models

    # Post the comment now
    Comment.objects.create(comment=request.POST['comment'], message=message, commenter=commenter)
    messages.success(request, 'Comment Post!')
    return redirect('/show/'+request.POST['receiver_id'])

