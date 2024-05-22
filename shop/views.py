from django.shortcuts import render, redirect
from .models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from .models import Car, Order
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm
from .forms import ChangePasswordForm

from .models import FAQ
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .forms import FeedbackForm
from .models import Feedback
from .models import Order
from django.contrib import messages
from decimal import Decimal, InvalidOperation






# Create your views here.
def contact_view(request):
    # messages.success(request, "contact page pe h aap!")
    if request.method == 'POST':
        # extract info from the form
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        if len(name)> 0 and len(email)> 0 and len(subject)> 0 and len(message)> 0:
            # save the data to the database
            contact = Contact(name=name, email=email, subject=subject, message=message)
            contact.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact')
        else:
            messages.error(request, "Please fill in all the fields!")
    return render(request, 'contact.html')


from django.core.mail import send_mail

def register(request):
    if request.method == "POST":
        name = request.POST['name']
        username = request.POST['username']
        number = request.POST['number']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if User.objects.filter(username = username).first():
            messages.error(request,"Username already taken")
            return redirect('register')
        if User.objects.filter(email = email).first():
            messages.error(request,"Email already taken")
            return redirect('register')

        if password != password2:
            messages.error(request,"Passwords do not match")
            return redirect('register')

        myuser = User.objects.create_user(username=username,email=email,password=password)
        myuser.name = name
        myuser.save()

        send_mail(
            'Welcome to our website',
            'Hi ' + username + ',\n\n' + 'Thank you for registering in our website. We are glad to have you here. We hope you have a great experience with us.\n\n' + 'Regards,\nTeam CarPool',
            'navneetyadv6034@digipodium.com',
            [email],
            fail_silently=False,
        )

        messages.success(request,"Your account has been successfully created!")
        return redirect('signin')

    else:
        print("error")
        return render(request,'register.html')
    

def signin(request):
    if request.method == "POST":
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username = loginusername,password = loginpassword)
        if user is not None:
            login(request, user)
            # messages.success(request,"Successfully logged in!")
            return redirect('home')
        else:
            messages.error(request,"Invalid credentials")
            return render(request,'login.html',{"error":True})

    else:
        print("error")
        return render(request,'login.html')

def signout(request):
        logout(request)
        # messages.success(request,"Successfully logged out!")
        return redirect('home')

def vehicles(request):
    cars = Car.objects.all()
    # print(cars)
    params = {'car':cars}
    return render(request,'vehicles.html ',params)

def bill(request):
    cars = Car.objects.all()
    params = {'cars':cars}
    return render(request,'bill.html',params)

def faq_page(request):
    faqs = FAQ.objects.all()
    return render(request, 'faq.html', {'faqs': faqs})

def bill_view(request):
    context = {
        'user': request.user,

        # ... other context variables ...

    }
    return render(request, 'bill.html', context)

def order(request):

    
    if request.method == "POST":
         
        billname = request.POST.get('billname','')
        billemail = request.POST.get('billemail','')
        billphone = request.POST.get('billphone','')
        billaddress = request.POST.get('billaddress','')
        billcity = request.POST.get('billcity','')
        cars11 = request.POST.get('cars11')
        if cars11 is None:
            messages.error(request, 'Please Fill The Details.')
            return redirect('bill')
        
        dayss = request.POST.get('dayss','')
        date = request.POST.get('date','')
        fl = request.POST.get('fl','')
        tl = request.POST.get('tl','')

        # print(request.POST['cars11'])
        
        order = Order(name = billname,email = billemail,phone = billphone,address = billaddress,city=billcity,cars = cars11,days_for_rent = dayss,date = date,loc_from = fl,loc_to = tl,user = request.user)
        order.save()
        send_mail(
        'Booking Confirmation',
        'Hi ' + billname + ',\n\n' +
        'Thank you for your booking. Here are your order details:\n' +
        'Order ID: ' + str(order.order_id) + '\n' +
        'Car: ' + cars11 + '\n' +
        'Days: ' + dayss + '\n' +
        'Date: ' + date + '\n' +
        'From: ' + fl + '\n' +
        'To: ' + tl + '\n',
        'navneetyadv6034@digipodium.com',
        [billemail],
        fail_silently=False,
    )
        messages.success(request, "Successful booking!")
        return redirect('final')
    else:
        print("error")
        return render(request,'bill.html')


import json
from django.conf import settings
import stripe
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


    # views.py
   
@login_required
def profile_view(request):
    orders = Order.objects.filter(user=request.user)
    profile = Profile.objects.filter(user=request.user).first()
    if not profile:
        return redirect('profile_update')

    return render(request, 'profile.html', {
        'profile': profile,
        'orders': orders

    })

@login_required
def profile_update_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        gender =  request.POST.get('gender')
        age = request.POST.get('age')
        photo = request.FILES.get('photo')
        number=request.POST.get('number')
         
      
        if name and email:
            profile = Profile(
                name=name, 
                email=email,
                gender = gender,
                age = age,
                image = photo,
                number=number,
               
                user = request.user
            )
            profile.save()
            messages.success(request, "Profile created successfully")
            return redirect('profile')
        else:
            messages.error(request, "Please fill in all the fields")
    return render(request, 'profile_form.html')

@login_required
def profile_edit_view(request):
    profile = Profile.objects.filter(user=request.user).first()
    try:
        form = ProfileForm(instance=profile)
        if request.method == 'POST':
            form = ProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request,"Profile updated")
                return redirect('profile')
        return render(request, 'profile_edit.html', {
            'form' : form
        })
    except Exception as e:
        print(e)
        return redirect('profile_update')
    


from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

class ChangePasswordView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('profile')
    template_name = 'change_password.html'
    def form_valid(self, form):
        messages.success(self.request, 'Your password was successfully updated!')
        return super().form_valid(form)
    
    

#order_details
@login_required
def order_detail(request, order_id):
    # Use order_id to get the order details
    order = Order.objects.get(order_id=order_id)  # Replace 'Order' and 'id' with your actual model and field names
    feedback=Feedback.objects.filter(order=order).first()

    # Pass the order details to the template
    context = {
        'order': order,
        'feedback': feedback,
        # ... other context variables ...
    }
    return render(request, 'order_detail.html', context)
#cancel_order
@login_required
def cancel_order(request, order_id):
    try:
        order = Order.objects.get(order_id=order_id)
    except Order.DoesNotExist:
        messages.error(request, 'No order found with the given ID.')
        return redirect('profile')  # Replace 'order_list' with the name of the view you want to redirect to

    order.delete()
    send_mail(
        'Order Cancellation',
        'Hi ' + request.user.username + ',\n\n' +
        'Your order with ID: ' + str(order_id) + ' has been cancelled.',
        'navneetyadv6034@digipodium.com',
        [request.user.email],
        fail_silently=False,
    )
    messages.success(request, 'Order cancelled successfully!')
    return redirect('profile')  # Replace 'order_list' with the name of the view you want to redirect to


@login_required
def submit_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST, user=request.user)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            messages.success(request, 'Your feedback has been submitted.')
            return redirect('profile')  # Redirect to the same page or another relevant page
    else:
        form = FeedbackForm(user=request.user)
    return render(request, 'feedback_form.html', {'form': form})

def final_view(request):
    return render(request, 'final.html')


from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from .forms import CustomPasswordResetForm

class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset_form.html'
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'