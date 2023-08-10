from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from .models import Todo
from django.conf import settings
from email.mime.text import MIMEText
import smtplib
# Create your views here.

class TodoForm(ModelForm):
    class Meta:
        model = Todo
        fields = ["task", "completed"]

def send_email(body):
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = "koushikromel@gmail.com"
    msg = MIMEText(body)
    msg['Subject'] = "New Task Created"
    msg['From'] = from_email
    msg['To'] = to_email

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    server.sendmail(from_email, [to_email], msg.as_string())
    server.quit()
    return redirect("/")

def list_todos(request):
    todo = Todo.objects.all()
    context = {"tasks": todo}
    return render(request, "list_todos.html", context)

def create_todo(request):
    form = TodoForm(request.POST or None)
    if form.is_valid():
        form.save()
        send_email(f"Task is created as: {form['task'].value()} and the completed is: {form['completed'].value()}")
        return redirect("/")
    context = {"form": form}
    return render(request, "create_todo.html", context)

def list_todo(request, pk):
    todo = Todo.objects.get(pk=pk)
    return render(request, "list_todo.html", {"todo": todo})

def update_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    form = TodoForm(request.POST or None, instance=todo)
    if form.is_valid():
        form.save()
        return redirect("/")
    return render(request, "update_todo.html", {"form": form})

def delete_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == "POST":
        todo.delete()
        return redirect("/")
    return render(request, "delete_todo.html", {"todo": todo})