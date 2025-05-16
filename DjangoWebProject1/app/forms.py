"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import Comment, Blog

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Имя пользователя'}))
    password = forms.CharField(label=_("Пароль"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Пароль'}))

class FeedbackForm(forms.Form):
    """Форма для сбора отзывов посетителей сайта"""
    
    name = forms.CharField(
        label='Ваше имя', 
        max_length=100, 
        min_length=2,
        widget=forms.TextInput({'class': 'form-control'})
    )
    email = forms.EmailField(
        label='Email', 
        widget=forms.EmailInput({'class': 'form-control'})
    )
    
    # Оценка сайта 
    site_rating = forms.ChoiceField(
        label='Как вы оцениваете наш сайт?',
        choices=[
            ('5', 'Отлично'),
            ('4', 'Хорошо'),
            ('3', 'Удовлетворительно'),
            ('2', 'Плохо'),
            ('1', 'Очень плохо')
        ],
        widget=forms.RadioSelect
    )
    
    # Выпадающий список
    visit_frequency = forms.ChoiceField(
        label='Как часто вы посещаете наш сайт?',
        choices=[
            ('daily', 'Ежедневно'),
            ('weekly', 'Еженедельно'),
            ('monthly', 'Ежемесячно'),
            ('rarely', 'Редко'),
            ('first', 'Впервые')
        ],
        widget=forms.Select({'class': 'form-control'})
    )
    
    improvements = forms.MultipleChoiceField(
        label='Что бы вы хотели улучшить на сайте?',
        required=False,
        choices=[
            ('design', 'Дизайн'),
            ('content', 'Содержание'),
            ('navigation', 'Навигацию'),
            ('speed', 'Скорость работы'),
            ('mobile', 'Мобильную версию')
        ],
        widget=forms.CheckboxSelectMultiple
    )
    
    # Числовое поле с ограничениями
    age = forms.IntegerField(
        label='Ваш возраст',
        min_value=10,
        max_value=120,
        required=False,
        widget=forms.NumberInput({'class': 'form-control'})
    )
    
    # область для отзыва
    message = forms.CharField(
        label='Ваши пожелания и комментарии',
        min_length=10,
        max_length=2000,
        required=False,
        widget=forms.Textarea({'class': 'form-control', 'rows': 5})
    )
    
    # Принятие условий 
    accept_terms = forms.BooleanField(
        label='Я согласен с обработкой моих персональных данных',
        widget=forms.CheckboxInput({'class': 'form-check-input'})
    )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {
            'text': 'Комментарий',
        }
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'description', 'content', 'image',)
        labels = {
            'title': 'Заголовок',
            'description': 'Краткое содержание',
            'content': 'Полное содержание',
            'image': 'Картинка'
        }
