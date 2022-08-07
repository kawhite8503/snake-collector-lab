from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Snake, Toy
from .forms import FeedingForm

# Create your views here.
class Home(LoginView):
  template_name = 'home.html'

def about(request):
  return render(request, 'about.html')

@login_required
def snakes_index(request):
  snakes = Snake.objects.filter(user=request.user)
  return render(request, 'snakes/index.html', { 'snakes': snakes})

@login_required
def snakes_detail(request, snake_id):
  snake = Snake.objects.get(id=snake_id)
  toys_snake_doesnt_have = Toy.objects.exclude(id__in = snake.toys.all().values_list('id'))
  feeding_form = FeedingForm()
  return render(request, 'snakes/detail.html', {
    'snake': snake, 'feeding_form': feeding_form, 'toys': toys_snake_doesnt_have })

class SnakeCreate(LoginRequiredMixin, CreateView):
  model = Snake
  fields = ['name', 'breed', 'description', 'age']
  success_url = '/snakes/'
    
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class SnakeUpdate(LoginRequiredMixin, UpdateView):
  model = Snake
  fields = ['breed', 'description', 'age']

class SnakeDelete(LoginRequiredMixin, DeleteView):
  model = Snake
  success_url = '/snakes/'

@login_required
def add_feeding(request, snake_id):
  form = FeedingForm(request.POST)
  if form.is_valid():
    new_feeding = form.save(commit=False)
    new_feeding.snake_id = snake_id
    new_feeding.save()
  return redirect('snakes_detail', snake_id=snake_id)

class ToyCreate(LoginRequiredMixin, CreateView):
  model = Toy
  fields = '__all__'

class ToyList(LoginRequiredMixin, ListView):
  model = Toy

class ToyDetail(LoginRequiredMixin, DetailView):
  model = Toy

class ToyUpdate(LoginRequiredMixin, UpdateView):
  model = Toy
  fields = ['name', 'color']

class ToyDelete(LoginRequiredMixin, DeleteView):
  model = Toy
  success_url = '/toys/'

@login_required
def assoc_toy(request, snake_id, toy_id):
  Snake.objects.get(id=snake_id).toys.add(toy_id)
  return redirect('snakes_detail', snake_id=snake_id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('cats_index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'signup.html', context)
