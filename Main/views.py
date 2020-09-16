from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import *
from Coursera.settings import EMAIL_HOST_USER
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import FormMixin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseNotAllowed, HttpResponse
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .forms import *


class CourseListView(ListView):
    model = Courses
    template_name = 'courses.html'
    ordering = '-date'
    paginate_by = 6
    context_object_name = 'courses'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cats = Category.objects.all()
        context['cats'] = cats
        return context

class CourseDetailView(DetailView):
    model = Courses
    template_name = 'course_detail.html'

class OrderSummaryView(LoginRequiredMixin ,View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            cats = Category.objects.all()
            context = {'object':order, 'cats':cats}
            return render(self.request, 'order_summary.html', context=context)
        except ObjectDoesNotExist:
            messages.error(self.request, 'You do not have an active order!')
            return redirect('/')


def CourseFilterView(request, category, pk):
    courses = Courses.objects.filter(category=pk)
    context = {'courses':courses, 'pk':category}
    return render(request, 'course_category.html', context)
    
@login_required
def add_to_cart(request, slug):
    course = get_object_or_404(Courses, slug=slug)
    order_course, created= OrderCourse.objects.get_or_create(course=course, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.course.filter(course__slug = slug).exists():
            messages.info(request, 'You already have a course!')
        else:
            messages.info(request, 'This course was added to your cart!')
            order.course.add(order_course)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.course.add(order_course)
        messages.info(request, 'This course was added to your cart!')
    return redirect('order-summary')

@login_required
def remove_from_cart(request, slug):
    course = get_object_or_404(Courses, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.course.filter(course__slug = slug).exists():
            order_course = OrderCourse.objects.filter(course=course, user=request.user, ordered=False)[0]    
            order.course.remove(order_course)
            messages.info(request, 'This course was removed from your cart!')
            return redirect('order-summary')
        else:
            messages.info(request, 'This course was not in your cart!')
            return redirect('course-detail', slug=slug)
    else:
        messages.info(request, 'You do not have an active order!')
        return redirect('course-detail', slug=slug)    
    return redirect('course-detail', slug=slug)


class EnrollView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            code = Coupon.objects.all()
            form = StudentAddForm()
            couponform = CouponForm()
            context = {'form':form, 'object':order, 'couponform':couponform, 'code':code}
            return render(self.request, 'enroll.html', context)

        except ObjectDoesNotExist:
            messages.info(self.request, 'You do not have an active order!')
            return redirect('user-enroll')

    def post(self, *args, **kwargs):
        form = StudentAddForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                your_name = form.cleaned_data.get('your_name')
                father = form.cleaned_data.get('father')
                email = form.cleaned_data.get('email')
                phone_no = form.cleaned_data.get('phone_no')
                address = form.cleaned_data.get('address')
                address2 = form.cleaned_data.get('address2')
                batch = form.cleaned_data.get('batch')
                batch_time = form.cleaned_data.get('batch_time')
                serial_no = form.cleaned_data.get('serial_no')

                details = Student_Details(
                    user = self.request.user,
                    your_name = your_name,
                    father = father,
                    email = email,
                    phone_no = phone_no,
                    address = address,
                    address2 = address2,
                    batch = batch,
                    batch_time = batch_time,
                    serial_no = serial_no
                )
                details.save()
                messages.success(self.request, 'Your form has been submited!')
                return redirect('main-home')
            messages.warning(self.request, '')
            return redirect('order-summary')
        except ObjectDoesNotExist:
            messages.error(self.request, 'Sorry, Please try again!')
            return redirect('order-summary')


class PostListView(ListView):
    model = Post
    template_name = 'blog.html'
    context_object_name = 'posts'
    paginate_by = 2
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cats = Category.objects.all()
        context['cats'] = cats
        return context

class PostDetailViex(FormMixin, DetailView):
    model = Post
    template_name = 'post_detail.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('detail-post', kwargs={'pk':self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cats = Category.objects.all()
        context['cats'] = cats
        form = CommentForm()
        context['form'] = form
        return context
     
    def post(self, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        post = self.object
        form.instance.post = post
        name = self.request.user
        form.instance.name = name
        form.save()
        return super(PostDetailViex, self).form_valid(form)
              
        

def PostFilterView(request, category, pk):
    posts = Post.objects.filter(category=pk)
    context = {'posts':posts, 'pk':category}
    return render(request, 'post_category.html', context)

def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.likes.add(request.user)
    return HttpResponseRedirect(reverse('detail-post', args=[str(pk)]))

def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, 'This coupon dose not exist!')
        return redirect('user-enroll')

class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(user=self.request.user, ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.info(self.request, 'Successfully added coupon')
                return redirect('user-enroll')

            except ObjectDoesNotExist:
                messages.info(self.request, 'You do not have an active order!')
                return redirect('user-enroll')
    
class IndexView(View):
    def get(self, *args, **kwargs):
        categories = Category.objects.all()
        courses = Courses.objects.all()

        context = {'cats':categories, 'courses':courses}
        return render(self.request, 'index.html', context)

def about(request):
    return render(request, 'about.html')

def team(request):
    return render(request, 'team.html')

class QuestionListView(ListView):
    model = Question
    template_name = 'faq.html'
    paginate_by = 5
    ordering = ['-date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cats'] = Category.objects.all()
        return context

class AnswerView(FormMixin, DetailView):
    model = Question
    template_name = 'answer.html'
    form_class = AnswerForm
    
    def post(self, *args, **kwargs):
        self.object = self.get_object()
        form = AnswerForm(self.request.POST)
        if form.is_valid():
            form.instance.question = self.object
            form.instance.name = self.request.user
            form.save()
            return HttpResponseRedirect(reverse('faq-ans', kwargs={'pk':self.object.id}))
        else:
            messages.warning(self.request, "Sorry, Please Try again!")
            return HttpResponseRedirect(reverse('faq-ans', kwargs={'pk':self.object.pk}))
        
def QuestionFilterView(request, category, pk):
    question = Question.objects.filter(category=pk)
    context = {'question':question, 'pk':category}
    return render(request, 'question_category.html', context)

def QuestionFormView(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')
            description_2 = form.cleaned_data.get('description_2')
            category = form.cleaned_data.get('category')
            data = Question(
                title = title,
                description = description,
                description_2 = description_2,
                category = category
            )
            data.save()
            messages.success(request, "Your question has been submited!")
    else:
        form = QuestionForm()
    return render(request, 'question.html', {'form':form})
    
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            if not User.objects.filter(email=form.cleaned_data.get('email')).exists():
                form.save()
                email = form.cleaned_data.get('email')
                messages.success(request, f"Your account has been created!  You are now able to login")
                subject = 'Welcome to Study-HQ'
                msg = 'Hope your enjoying our Blog.'
                recepient = str(form['email'].value())
                send_mail(subject, msg, EMAIL_HOST_USER, [recepient], fail_silently=False)
                return redirect('user-login') 
            messages.warning(request, 'Email is already taken, Please try again with other email!')
       
    else:
        form = UserRegistrationForm()
    return render(request, 'registration.html', {'form':form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        img_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid() and img_form.is_valid():
            form.save()
            img_form.save()
            messages.success(request, f"Your Account Has Been Updated!")
            return redirect('user-profile')
    else:
        form = UserUpdateForm(instance=request.user)
        img_form = ProfileUpdateForm(instance=request.user.profile)
        cats = Category.objects.all()
    return render(request, 'profile.html', {'form':form, 'img_form':img_form, 'cats':cats})


def contact(request):
    if request.method == 'POST':
        form = ContectUsForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            subject = form.cleaned_data.get('subject')
            message = form.cleaned_data.get('message')
            details = ContactUs(name = name,
                                email = email,
                                subject = subject,
                                message = message)
            details.save()
            messages.success(request, 'Your message has been send!')
    else:
        form = ContectUsForm()
        cats = Category.objects.all()
    return render(request, 'contact.html', {'form':form, 'cats':cats})

