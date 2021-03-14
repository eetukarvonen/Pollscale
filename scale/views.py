from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import RegisterForm
from .models import Scale, Votes

def index(request):
    """
    Route for index
    """
    parents_list = Scale.objects.filter(parent_scale=None)
    details = []
    for parent in parents_list:
        dic = calulate_details(parent)
        details.append(dic)

    context = {
        'details': details
        }
    return render(request, 'index.html', context)

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

def add(request):
    """
    Route for adding new scale
    """
    if request.method == 'POST':
        title = request.POST['title']
        scale = Scale(scale_title=title)
        scale.save()
        return redirect('index')
    else:
        return render(request, 'add.html')

def add_yay(request, scale_id):
    """
    Route for adding sub-scales
    """
    if request.method == 'POST':
        title = request.POST['title']
        parent_scale = Scale.objects.get(id=scale_id)
        scale = Scale(scale_title=title, parent_scale=parent_scale, yay_or_nay_of_parent='yay')
        scale.save()
        return redirect('detail', str(scale_id))
    else:
        return render(request, 'add_yayscale.html', { 'scale_id': scale_id })

def add_nay(request, scale_id):
    """
    Route for adding sub-scales
    """
    if request.method == 'POST':
        title = request.POST['title']
        parent_scale = Scale.objects.get(id=scale_id)
        scale = Scale(scale_title=title, parent_scale=parent_scale, yay_or_nay_of_parent='nay')
        scale.save()
        return redirect('detail', str(scale_id))
    else:
        return render(request, 'add_nayscale.html', { 'scale_id': scale_id })

def detail(request, scale_id):
    """
    Route for showing details of the scale
    """
    scale = get_object_or_404(Scale, pk=scale_id)
    parent = scale.parent_scale
    details = calulate_details(scale)
    children_details = []
    children = Scale.objects.filter(parent_scale=scale)
    for child in children:
        dic = calulate_details(child)
        children_details.append(dic)

    prev_vote = 'nothing'
    user = request.user
    if user.is_authenticated:
        vote_objects = Votes.objects.filter(user=request.user)  # Votes of the user, can be empty
        for vote_object in vote_objects:                        # Loop through users votes
            if vote_object.scale.id == scale_id:                # Find the vote for this scale, could be not found
                prev_vote = vote_object.vote                    # Previous vote of the user for this scale
    

    context = {
        'details': details,
        'children_details': children_details,
        'parent':parent,
        'prev_vote': prev_vote
    }

    return render(request, 'detail.html', context)

@login_required
def vote(request, scale_id):
    """
    Handles the POST-request when user votes
    """
    if request.method == 'POST':
        user = request.user
        vote = request.POST['vote']
        prev_vote = 'nothing'
        scale = Scale.objects.get(pk=scale_id)

        # What has the user voted on this scale
        vote_objects = Votes.objects.filter(user=user)  # Votes of the user, can be empty
        for vote_object in vote_objects:                # Loop through users votes
            if vote_object.scale.id == scale_id:        # Find the vote for this scale, could be not found
                prev_vote = vote_object.vote            # Previous vote of the user for this scale
                if prev_vote != vote:
                    # Change vote in votes table
                    vote_object.vote = vote
                    vote_object.save()

                    # Change vote in scale table
                    if prev_vote == 'yay':
                        scale.yays -= 1
                        if vote == 'nay':
                            scale.nays += 1
                        scale.save()
                    elif prev_vote == 'nay':
                        scale.nays -= 1
                        if vote == 'yay':
                            scale.yays += 1
                        scale.save()
                    else:
                        if vote == 'yay':
                            scale.yays += 1
                        if vote == 'nay':
                            scale.nays += 1
                        scale.save()
                return redirect('detail', str(scale_id))

        if vote == 'nay':
            scale.nays += 1
            scale.save()
        elif vote == 'yay':
            scale.yays += 1
            scale.save()
        
        new_vote = Votes(user=user, scale=scale, vote=vote)
        new_vote.save()

    return redirect('detail', str(scale_id))

def info(request):
    return render(request, 'info.html')


def calulate_details(scale):
    """
    Calculates the vote percentages and total votes. Returns dictionary with scale details.
    """
    ident = scale.id
    title = scale.scale_title
    yay_or_nay_of_parent = scale.yay_or_nay_of_parent
    yays = scale.yays
    nays = scale.nays
    totals = yays + nays
    if totals == 0:
        yay_percentage = round(0, 2)
        nay_percentage = round(0, 2)
    else:
        yay_percentage = round((yays / totals) * 100, 2)
        nay_percentage = round((nays / totals) * 100, 2)

    dic = {
        'id': ident,
        'title': title,
        'yay_or_nay_of_parent': yay_or_nay_of_parent,
        'yays': yays,
        'nays': nays,
        'totals': totals,
        'yay_percentage': yay_percentage,
        'nay_percentage': nay_percentage
    }
    return dic
