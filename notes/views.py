from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Note

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST) 
        if form.is_valid():
            form.save()
            return redirect('login')   
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def notes_list(request):
    notes = Note.objects.filter(user=request.user) 
    return render(request, 'notes/notes_list.html', {'notes': notes})

@login_required
def note_create(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        image = request.FILES.get('image') 
        Note.objects.create(title=title, content=content, user=request.user, image=image)  
        return redirect('notes_list')
    return render(request, 'notes/note_form.html')

@login_required
def note_update(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        note.title = request.POST['title']
        note.content = request.POST['content']
        if 'image' in request.FILES:
            note.image = request.FILES['image']
        note.save()
        return redirect('notes_list')
    return render(request, 'notes/note_form.html', {'note': note})

@login_required
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        note.delete()
        return redirect('notes_list')
    return render(request, 'notes/note_confirm_delete.html', {'note': note})
