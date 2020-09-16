from django.db import models

from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from PIL import Image

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger'),
)

class Category(models.Model):
    category = models.CharField(max_length=20)
    
    def __str__(self):
        return self.category

class Courses(models.Model):
    title = models.CharField(max_length=200)
    actual_price = models.IntegerField()
    offer_price = models.IntegerField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    course_img = models.ImageField(default='default.png', upload_to='Courses Img')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('course-detail', kwargs={'slug':self.slug})

    def get_add_to_cart_url(self):
        return reverse('add-to-cart', kwargs={'slug':self.slug})

    def get_remove_from_cart_url(self):
        return reverse('remove-from-cart', kwargs={'slug':self.slug})

    def get_category_url(self):
        return reverse('category', kwargs={'category':self.category.id})


class OrderCourse(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False) 
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.course.title}'

    def get_total_saving(self):
        return self.course.actual_price - self.course.offer_price

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ManyToManyField(OrderCourse)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    coupon = models.ForeignKey('Coupon', default=1, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    def get_final_price(self):
        total = 0
        for ord_course in self.course.all():
            if ord_course.course.offer_price:      
                total += ord_course.course.offer_price
            else:
                total += ord_course.course.actual_price
        return total 

    def coupon_price(self):
        total = self.get_final_price()
        total -= self.coupon.amount
        return total


class Student_Details(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    your_name = models.CharField(max_length=100)
    father = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100, blank=True, null=True)
    batch = models.CharField(max_length=100)
    batch_time = models.CharField(max_length=100)
    serial_no = models.CharField(max_length=100)

    def __str__(self):
        return self.your_name


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    thumbnail = models.ImageField(default='default.png', upload_to='Thumbnails')
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='blog_posts')

    def __str__(self):
        return self.title
        
    def total_likes(self):
        return self.likes.count()

    def save(self):
        super().save()
        img = Image.open(self.thumbnail.path)
        if img.height > 300 or img.width > 300:
            output_size = (750, 375)
            img.thumbnail(output_size)
            img.save(self.thumbnail.path)

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.post.title, self.name)


class Coupon(models.Model):
    code = models.CharField(max_length=20)
    amount = models.FloatField(default=1)

    def __str__(self):
        return self.code

class ContactUs(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')

    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self):
        super().save()
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Question(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    description_2 = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.title

class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    answer = models.TextField()
    name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.answer