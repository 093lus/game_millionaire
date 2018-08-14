from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.views import View
from authentication.forms import UserForm


class UserLoginView(View):
    def get(self, request):
        return render_to_response('login.html', {})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
               login(request, user)
               return redirect('index')
            else:
                return HttpResponse("Your account is disabled.")

        else:
            return HttpResponse("Invalid login details supplied.")



class RegisterView(View):
    def get(self, request):
        return render_to_response('register.html', {})

    def post(self, request):
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            user.set_password(user.password)
            user.save()
            login(request, user)
            return redirect('index')

        else:
            return HttpResponse(user_form.errors)
            return redirect('index')
