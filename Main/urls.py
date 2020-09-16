from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='main-home'),
    path('courses/', CourseListView.as_view(), name='courses-list'),
    path('course-detail/<slug>/', CourseDetailView.as_view(), name='course-detail'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('category/<str:category>/<int:pk>', CourseFilterView, name='category'),
    path('post/', PostListView.as_view(), name='admin-post'),
    path('post/<int:pk>/', PostDetailViex.as_view(), name='detail-post'),
    path('post/<str:category>/<int:pk>/', PostFilterView, name='post-category'),
    path('enroll-user/', EnrollView.as_view(), name='user-enroll'),
    path('enroll-coupon/', AddCouponView.as_view(), name='user-coupon'),
    path('like/<int:pk>/', LikeView, name='like_post'),
    path('team/', team, name='main-team'),
    path('about/', about, name='main-about'),
    path('FAQ/', QuestionListView.as_view(), name='main-faq'),
    path('answer/<int:pk>', AnswerView.as_view(), name='faq-ans'),
    path('ask-question/', QuestionFormView, name='question-form'),
    path('question/<str:category>/<int:pk>/', QuestionFilterView, name='question-category'),

    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='user-login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='user-logout'),
    path('register/', register, name='user-register'),
    path('profile/', profile, name='user-profile'),
    path('contact/', contact, name='user-contact'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
