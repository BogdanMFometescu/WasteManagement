from django.shortcuts import render, redirect
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, ProfileForm, CertificateForm, MessageForm
from .utils import search_profile, paginate_profiles


def login_user(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except ValueError:
            messages.error(request, 'Username does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request, 'Username or password incorrect')
    return render(request, 'users/login-register.html')


def logout_user(request):
    logout(request)
    messages.success(request, 'User successfully logout')
    return redirect('login')


def register_user(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'Account has been created!')

            login(request, user)
            return redirect('edit-account')
        else:
            messages.error(request, 'An error has occurred during registration')

    context = {'form': form, 'page': page}
    return render(request, 'users/login-register.html', context)


def profiles(request):
    all_profiles, search_query = search_profile(request)
    custom_range, all_profiles = paginate_profiles(request, all_profiles, 6)
    context = {'profiles': all_profiles, 'search_query': search_query}
    return render(request, 'users/profiles.html', context)


def user_profile(request, pk):
    profile = Profile.objects.get(id=pk)
    top_certificates = profile.certificate_set.exclude(description__exact='')
    other_certificates = profile.certificate_set.filter(description='')

    context = {'profile': profile, 'top_certificates': top_certificates, 'other_certificates': other_certificates}
    return render(request, 'users/user-profile.html', context, )


@login_required(login_url='login')
def user_account(request):
    profile = request.user.profile

    certificates = profile.certificate_set.all()
    records = profile.record_set.all()

    context = {'profile': profile, 'certificates': certificates, 'records': records}
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def edit_account(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/profile_form.html', context)


@login_required(login_url='login')
def create_certificate(request):
    profile = request.user.profile
    form = CertificateForm()

    if request.method == 'POST':
        form = CertificateForm(request.POST)

        if form.is_valid():
            certificate = form.save(commit=False)
            certificate.owner = profile
            certificate.save()
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/certificates_form.html', context)


@login_required(login_url='login')
def edit_certificate(request, pk):
    profile = request.user.profile
    certificate = profile.certificate_set.get(id=pk)
    form = CertificateForm(instance=certificate)

    if request.method == 'POST':
        form = CertificateForm(request.POST, instance=certificate)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/certificates_form.html', context)


@login_required(login_url='login')
def delete_certificate(request, pk):
    profile = request.user.profile
    certificate = profile.certificate_set.get(id=pk)

    if request.method == 'POST':
        certificate.delete()
        return redirect('account')

    context = {'object': certificate}
    return render(request, 'delete.html', context)


@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    message_request = profile.messages.all()
    unred_count = message_request.filter(is_read=False).count()
    context = {'message_request': message_request, 'unread_count': unred_count}
    return render(request, 'users/inbox.html', context)


@login_required(login_url='login')
def view_message(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if not message.is_read:
        message.is_read = True
        message.save()

    context = {'message': message}
    return render(request, 'users/message.html', context)


def create_message(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except ValueError:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()

            messages.success(request, 'Your message was successfully sent!')
            return redirect('user-profile', pk=recipient.id)

    context = {'recipient': recipient, 'form': form}
    return render(request, 'users/message_form.html', context)
