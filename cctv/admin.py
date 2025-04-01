from django.contrib import admin
from .models import UserProfile,Notification
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.urls import reverse

# Register your models here.


admin.site.site_header = "CRC@Surveillance Administration Panel"
admin.site.site_title = "Administration Panel"
admin.site.index_title = "Welcome to CRC@Surveillance  "

admin.site.unregister(Group)

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'  # Incluir todos los campos excepto "groups"
        exclude = ['groups']




class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm


    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Information', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.unregister(User)

admin.site.register(User, CustomUserAdmin)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["password1"].required = True
        self.fields["password2"].required = True

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if not password1:
            raise forms.ValidationError("The password cannot be empty!")
        return password1


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm  # Usar el formulario personalizado

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    def add_view(self, request, form_url='', extra_context=None):
        """
        Sobrescribe la vista de agregar usuario para asegurarse de que
        la autenticación basada en contraseña siempre esté activada.
        """
        if request.method == "POST":
            form = self.add_form(request.POST)
            if form.is_valid():
                user = form.save()
                return redirect(reverse('admin:auth_user_changelist'))  # Redirige a la lista de usuarios
        return super().add_view(request, form_url, extra_context)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

class UserProfileAdmin(admin.ModelAdmin):
   
    list_display = ('user', 'location')
    search_fields = ('user__username', 'location__location', 'user__email',)
    empty_value_display = "-empty-"

admin.site.register(UserProfile,UserProfileAdmin)

class NotificationAdmin(admin.ModelAdmin):
     list_display = ('location','user')
     search_fields = ('user__username', 'location__location')
     empty_value_display = "-empty-"
admin.site.register(Notification,NotificationAdmin)
