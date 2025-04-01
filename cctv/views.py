from django.shortcuts import render,  redirect
from django.views.generic import  DetailView,ListView,CreateView,UpdateView,DeleteView, RedirectView,TemplateView
from django.views import View
from .models import *
from .forms import *
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from django.http import JsonResponse,FileResponse, Http404
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import Permission
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.utils import timezone
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from django.db.models import Value, F, CharField,Count
from django.db.models.functions import Concat, Trim, Coalesce
import json



from django.db.models import ProtectedError







# Create your views here.
#login

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import LoginForm
from django.contrib.auth.decorators import login_required


@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})

class CustomLoginView(LoginView):
    form_class = LoginForm

    def get_success_url(self):
        return self.get_redirect_url() or "/"

    def get_redirect_url(self):
        return (
        self.request.GET.get("next") or
        self.request.POST.get("next") or
        self.request.GET.get("redirect_to") or
        self.request.POST.get("redirect_to")
    )

    def form_valid(self, form):
     
        remember_me = form.cleaned_data.get('remember_me')
        if remember_me:
            self.request.session.set_expiry(1209600) 
        else:
            self.request.session.set_expiry(0) 
        return super().form_valid(form)

  #User
#User***Begin

class ListUserView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
   login_url = '/accounts/login/'
   redirect_field_name = 'redirect_to' 
   template_name='user/list-user.html'
   model=User
   permission_required = 'cctv.view_user'

   def get_queryset(self):
        qs=User.objects.all()
        return qs
    
class CreateUserView(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
     login_url = '/accounts/login/'
     redirect_field_name = 'redirect_to' 
     model=User
     template_name = 'user/create-user.html'
     form_class = UserForm   
     success_url = reverse_lazy("user-list") 
     permission_required = 'cctv.add_user'
     
     def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        messages.success(self.request, "The User  was Added successfully.")
        return super(CreateUserView,self).form_valid(form)

class UpdateUserView(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
      login_url = '/accounts/login/'
      redirect_field_name = 'redirect_to' 
      model=User
      template_name = 'user/update-user.html'
      form_class = UserForm   
      success_url = reverse_lazy("user-list") 
      permission_required = 'cctv.change_user'

      def form_valid(self, form):
        messages.success(self.request, "The User  was Updated successfully.")
        return super(UpdateUserView,self).form_valid(form)

class DeleteUserView(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
       login_url = '/accounts/login/'
       redirect_field_name = 'redirect_to' 
       model=User
       context_object_name = 'user'
       template_name='user/confirm_delete.html'   
       success_url = reverse_lazy("user-list")
       permission_required = 'cctv.delete_user'
    
       def form_valid(self, form):
        messages.success(self.request, "The User  was Deleted successfully.")
        return super(DeleteUserView,self).form_valid(form)

class DetailUserView(LoginRequiredMixin,PermissionRequiredMixin,DetailView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    model = User
    context_object_name = 'user'
    template_name='user/detail-user.html'   
    success_url = reverse_lazy("user-list")
    permission_required = 'cctv.view_user'
 #User***End       
   

#UserProfile

class ListUserProfileView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
   login_url = '/accounts/login/'
   redirect_field_name = 'redirect_to' 
   template_name='user_profile/list-user_profile.html'
   model=UserProfile
   permission_required = 'cctv.view_userprofile'

   def get_queryset(self):
        qs=UserProfile.objects.all()
        return qs
     
class CreateUserProfileView(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
     login_url = '/accounts/login/'
     redirect_field_name = 'redirect_to' 
     model=UserProfile
     template_name = 'user_profile/create-user_profile.html'
     form_class = CreateUserProfileForm   
     success_url = reverse_lazy("user_profile-list") 
     permission_required = 'cctv.add_userprofile'
     
     def form_valid(self, form):
        messages.success(self.request, "The User Profile was Updated successfully.")
        return super(CreateUserProfileView,self).form_valid(form)

class UpdateUserProfileView(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
      login_url = '/accounts/login/'
      redirect_field_name = 'redirect_to' 
      model=UserProfile
      template_name = 'user_profile/update-user_profile.html'
      form_class = CreateUserProfileForm   
      success_url = reverse_lazy("user_profile-list") 
      permission_required = 'cctv.change_userprofile'

      def form_valid(self, form):
        messages.success(self.request, "The User Profile was Updated successfully.")
        return super(UpdateUserProfileView,self).form_valid(form)

class DeleteUserProfileView(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
       login_url = '/accounts/login/'
       redirect_field_name = 'redirect_to' 
       model=UserProfile
       context_object_name = 'user_profile'
       template_name='user_profile/confirm_delete.html'   
       success_url = reverse_lazy("user_profile-list")
       permission_required = 'cctv.delete_userprofile'
    
       def form_valid(self, form):
        messages.success(self.request, "The User Profile was Deleted successfully.")
        return super(DeleteUserProfileView,self).form_valid(form)

class DetailUserProfileView(LoginRequiredMixin,PermissionRequiredMixin,DetailView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    model = UserProfile
    context_object_name = 'user_profile'
    template_name='user_profile/detail-user_profile.html'   
    success_url = reverse_lazy("user_profile-list")
    permission_required = 'cctv.view_userprofile'
       
#Permission
class UserPermissionsListView(ListView):
    template_name = "permissions/user_permissions_list.html"
    context_object_name = "permissions"

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = get_object_or_404(User, pk=user_id)
        # Obtenemos los permisos asignados directamente al usuario
        return user.user_permissions.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs['user_id']
        context['user'] = get_object_or_404(User, pk=user_id)
        
        return context
 
class ManageUserPermissionsView(TemplateView):
    template_name = "permissions/manage_user_permissions.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs['user_id']
        user = get_object_or_404(User, pk=user_id)
        context['user'] = user
        context['permissions'] = user.user_permissions.all()
        context['form'] = AddPermissionForm()
        return context
    
class AddPermissionView(FormView):
    template_name = "permissions/add_permission.html"
    form_class = AddPermissionForm

    def form_valid(self, form):
        user_id = self.kwargs['user_id']
        user = get_object_or_404(User, pk=user_id)
        permission = form.cleaned_data['permission']
        user.user_permissions.add(permission)
        return super().form_valid(form)

    def get_success_url(self):
        user_id = self.kwargs['user_id']
        return reverse_lazy('manage_user_permissions', kwargs={'user_id': user_id})
    
class RemovePermissionView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        user_id = kwargs['user_id']
        permission_id = kwargs['permission_id']
        user = get_object_or_404(User, pk=user_id)
        permission = get_object_or_404(Permission, pk=permission_id)
        user.user_permissions.remove(permission)
        return reverse_lazy('manage_user_permissions', kwargs={'user_id': user_id})


#Staff list 
 
#class ListStaffView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
#   template_name='staff/list-staff.html'
 #  login_url = '/accounts/login/'
  # redirect_field_name = 'redirect_to'  
   #model=Staff
  # permission_required = 'cctv.view_staff'
   
  # def dispatch(self, request, *args, **kwargs):
   #         if not hasattr(self.request.user, 'userprofile') and not self.request.user.is_superuser:
    #            messages.error(self.request, "No profile associated with the user was found")
    #            return redirect(self.login_url)
                
     #       return super().dispatch(request, *args, **kwargs)
    
   
   #def get_queryset(self):
       # if self.request.user.is_superuser:
    #    qs=Staff.objects.all()  
       # else:
       #    qs=Staff.objects.filter(Q(location_id=3 )  | Q(location=self.request.user.userprofile.location ) )
     #   return qs

class ListStaffView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
   template_name='staff/list-staff.html'
   login_url = '/accounts/login/'
   redirect_field_name = 'redirect_to'  
   model=Staff
   permission_required = 'cctv.view_staff'
   
   def dispatch(self, request, *args, **kwargs):
            if not hasattr(self.request.user, 'userprofile') and not self.request.user.is_superuser:
                messages.error(self.request, "No profile associated with the user was found")
                return redirect(self.login_url)
                
            return super().dispatch(request, *args, **kwargs)
    

   def apply_filters(self, queryset, filters):
    """Aplica los filtros a la consulta."""
    for key, value in filters.items():
        if value:
            if key == 'id':
                queryset = queryset.filter(id__icontains=value)
            if key == 'name':
                queryset = queryset.filter(name__icontains=value)
            elif key == 'surname':
                queryset = queryset.filter(surname__icontains=value)
            elif key == 'department':
                queryset = queryset.filter(department__name__icontains=value)
            elif key == 'position':
                queryset = queryset.filter(position__name__icontains=value)
            elif key == 'location':
                queryset = queryset.filter(location__location__icontains=value)
            elif key == 'active':
                # Aplicar filtro booleano de forma consistente
                if value.lower() == 'active':  # Si es 'active', filtra True
                    queryset = queryset.filter(active=True)
                elif value.lower() == 'inactive':  # Si es 'inactive', filtra False
                    queryset = queryset.filter(active=False)

    return queryset




   def get_queryset(self):      
        queryset=self.model.objects.all()  
        search_value = self.request.GET.get('search[value]', '').strip()       
        filters = self.request.GET.get('filters', '{}')  

        try:         
         filters = json.loads(filters) if filters else {}
        except json.JSONDecodeError:         
         filters = {}  

        filters_only = self.request.GET.get('filters_only', 'false') == 'true' 
        
      

        if filters_only:
            unique_values = {}  

            if not filters:
                filters = {'id':'', 'name': '', 'surname': '', 'department': '', 'position': '', 'location': '', 'active': '' }
     
            for key in filters.keys():
                if key == 'id':
                    unique_values['id'] = list(queryset.values_list('id', flat=True).distinct().order_by('-id'))
     
                if key == 'name':
                    unique_values['name'] = list(queryset.values_list('name', flat=True).distinct())
                elif key == 'surname':
                    unique_values['surname'] = list(queryset.values_list('surname', flat=True).distinct())
                elif key == 'department':
                    unique_values['department'] = list(queryset.values_list('department__name', flat=True).distinct())
                elif key == 'position':
                    unique_values['position'] = list(queryset.values_list('position__name', flat=True).distinct())
                elif key == 'location':
                    unique_values['location'] = list(queryset.values_list('location__location', flat=True).distinct())
                elif key == 'active':
                    unique_values['active'] = list(queryset.values_list('active', flat=True).distinct())
              
            return unique_values  
      
        queryset = self.apply_filters(queryset, filters)

        if search_value:      
           queryset= queryset.filter(
                Q(id__icontains=search_value)|
                Q(name__icontains=search_value)|
                Q(surname__icontains=search_value)|
                Q(department__name__icontains=search_value)|
                Q(position__name__icontains=search_value)|
                Q(location__location__icontains=search_value)
            )
         
        
        order_colum_index=self.request.GET.get('order[0][column]','0')
     
        order_dir=self.request.GET.get('order[0][dir]','asc')
      
        column_map={
            '0':'id',
            '1':'photo',
            '2':'name',
            '3':'surname',
            '4':'department__name',
            '5':'position__name',
            '6':'location__location',
            '7':'active'

        }
        order_field=column_map.get(order_colum_index,'id')   
        if order_dir=='desc':
            order_field=f"-{order_field}"          

        queryset=queryset.order_by(order_field)     
        return queryset
   

   def render_to_response(self, context, **response_kwargs):
    if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
        draw = int(self.request.GET.get('draw', 1))
        start = int(self.request.GET.get('start', 0))
        length = int(self.request.GET.get('length', 10))      
        filters_only = self.request.GET.get('filters_only', 'false') == 'true'      

     
        if filters_only:           
                     
            unique_values = self.get_queryset()    
         
            data = []
            for key, values in unique_values.items():
                if isinstance(values, list):  # Si los valores son una lista (lo que esperamos)
                    unique_values[key] = list(set(values))  # Asegurarnos de que solo se queden los valores únicos

                    # Si la clave es 'active', convertimos True/False a 'Active'/'Inactive'
                    if key == 'active':
                        unique_values[key] = ['Active' if value else 'Inactive' for value in unique_values[key]]

                    data.append({
                        "filter": key,
                        "values": unique_values[key]  # Los valores únicos
                    })
                    
              

         
            return JsonResponse({
                "draw": draw,
                "recordsTotal": len(data),
                "recordsFiltered": len(data),
                "data": data
            })
  
        queryset = self.get_queryset()
        total_records = self.model.objects.count()
        filtered_records = queryset.count()
        staffs = queryset[start:start + length]

        data = [{
            "id": staffs.id,
            "photo": staffs.photo.url,
            "name": str(staffs.name) if staffs.name else "",
            "surname": str(staffs.surname) if staffs.surname else "",
            "department": str(staffs.department.name) if staffs.department else "",
            "position": str(staffs.position.name) if staffs.position else "",
            "location": str(staffs.location) if staffs.location else "",
            "active": "Active" if staffs.active else "Inactive",
            "detail_url": staffs.get_absolute_url(),
            "edit_url": staffs.get_edit_url(),
            "delete_url": staffs.get_delete_url(),
        } for staffs in staffs]

        return JsonResponse({
            "draw": draw,
            "recordsTotal": total_records,
            "recordsFiltered": filtered_records,
            "data": data,
        })

    return super().render_to_response(context, **response_kwargs)
 
     
class CreateStaffView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,CreateView):
     login_url = '/accounts/login/'
     redirect_field_name = 'redirect_to'
     model=Staff
     template_name = 'staff/create-staff.html'
     form_class = CreateStaffForm    
     success_url = reverse_lazy("staff-list") 
     permission_required = 'cctv.add_staff'     
     success_message = "The Staff was Added successfully."
      
     def form_valid(self, form):
        response = super().form_valid(form)
        if "save_and_continue" in self.request.POST:
            messages.success(self.request,"The Staff was Added successfully. You can continue adding.")
            return redirect('staff-create')
        return response  



class UpdateStaffView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
      login_url = '/accounts/login/'
      redirect_field_name = 'redirect_to'
      model=Staff
      template_name = 'staff/update-staff.html'
      form_class = CreateStaffForm   
      success_url = reverse_lazy("staff-list")
      permission_required = 'cctv.change_staff'
      success_message = "The Staff was Updated successfully."
      
    #  def form_valid(self, form):
     #    try:
      #      userprofile = self.request.user.userprofile.location
           
     #    except UserProfile.DoesNotExist:
               
      #          return self.form_invalid(form)          
       
      #   form.instance.location = userprofile
       
     #    return super().form_valid(form)


    #  def form_invalid(self, form):
    #    messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
    #    return super().form_invalid(form)	   

class DeleteStaffView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,DeleteView):    
       model=Staff
       context_object_name = 'staff'
       template_name='staff/confirm_delete.html'   
       success_url = reverse_lazy("staff-list")
       login_url = '/accounts/login/'
       redirect_field_name = 'redirect_to'
       permission_required = 'cctv.delete_staff'
       success_message = "The Staff was Deleted successfully."
      
       success_message = "The Staff was Deleted successfully."
       error_message = (
            "Cannot delete the Staff '{name}' because it is related to other records: {details}."
              )
       

       def post(self, request, *args, **kwargs):
                self.object = self.get_object()  # Obtener el objeto a eliminar
              
                try:
                    # Intentar eliminar el objeto
                    self.object.delete()
                    messages.success(request, self.success_message)
                    return redirect(self.success_url)
                except ProtectedError as e:
                 
                    related_objects = ', '.join(str(obj) for obj in e.protected_objects)
                    
                    error_message = self.error_message.format(name=str(self.object), details=related_objects)
                    messages.error(request, error_message)
                    return redirect(self.success_url)

class DetailStaffView(LoginRequiredMixin,PermissionRequiredMixin,DetailView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    model = Staff
    context_object_name = 'staff'
    template_name='staff/detail-staff.html'   
    success_url = reverse_lazy("staff-list")
    permission_required = 'cctv.view_staff'
#Staff****End
#Black list  CRUD and Functions

class ListBlackListView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
   login_url = '/accounts/login/'
   redirect_field_name = 'redirect_to'
   template_name='black_list/list-blacklist.html'
   model=BlackList
   permission_required = 'cctv.view_blacklist'
  
  
   def dispatch(self, request, *args, **kwargs):
            if not hasattr(request.user, 'userprofile') and not self.request.user.is_superuser:
                messages.error(self.request, "No profile associated with the user was found")
                return redirect(self.login_url)                
            return super().dispatch(request, *args, **kwargs)



   #def get_queryset(self):
      #  qs = BlackList.objects.all().exclude(duration_id=7).order_by('-id', '-date')           
     #   return qs
class ListBlackListView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
   login_url = '/accounts/login/'
   redirect_field_name = 'redirect_to'
   template_name='black_list/list-blacklist.html'
   model=BlackList
   permission_required = 'cctv.view_blacklist'
  
  
   def dispatch(self, request, *args, **kwargs):
            if not hasattr(request.user, 'userprofile') and not self.request.user.is_superuser:
                messages.error(self.request, "No profile associated with the user was found")
                return redirect(self.login_url)                
            return super().dispatch(request, *args, **kwargs)
   

   def apply_filters(self, queryset, filters):          
    for key, value in filters.items():
        if value:
            if key == 'id':
                queryset = queryset.filter(id__icontains=value)
            if key == 'date':
            
              
                formatted_search_value =datetime.datetime.strptime(value, "%d-%m-%y").strftime("%Y-%m-%d")      
                  
                queryset = queryset.filter(date__icontains=formatted_search_value)

            elif key == 'name':
                queryset = queryset.filter(name__icontains=value)
            elif key == 'surname':
                queryset = queryset.filter(surname__icontains=value)
            elif key == 'sex':
                queryset = queryset.filter(sex__sex__icontains=value)
            elif key == 'reason':
                queryset = queryset.filter(reason__reason__icontains=value)
            elif key == 'race':
                queryset = queryset.filter(race__race__icontains=value)
            elif key == 'duration':
                queryset = queryset.filter(duration__duration__icontains=value)
            elif key == 'location':
                queryset = queryset.filter(location__location__icontains=value)
    return queryset



   def get_queryset(self):
       
        queryset = self.model.objects.all().exclude(duration_id=7).order_by('-id', '-date')       
    

        search_value = self.request.GET.get('search[value]', '').strip()
        
        filters = self.request.GET.get('filters', '{}') 
        
        try:         
         filters = json.loads(filters) if filters else {}
        except json.JSONDecodeError:         
         filters = {}  

        filters_only = self.request.GET.get('filters_only', 'false') == 'true' 

        if filters_only:
            unique_values = {}  

            if not filters:
                filters = { 'id':'','date':'','name': '', 'surname': '','sex':'', 'reason': '', 'race': '', 'duration': '', 'location': '' }
     
            for key in filters.keys():
                if key == 'id':
                    unique_values['id'] = list(queryset.values_list('id', flat=True).distinct().order_by('id'))
                if key == 'date':
                    unique_values['date'] = list(queryset.values_list('date', flat=True).distinct().order_by('date'))
                elif key == 'name':
                    unique_values['name'] = list(queryset.values_list('name', flat=True).distinct().order_by('name'))
                elif key == 'surname':
                    unique_values['surname'] = list(queryset.values_list('surname', flat=True).distinct().order_by('surname'))
                elif key == 'sex':
                    unique_values['sex'] = list(queryset.values_list('sex__sex', flat=True).distinct().order_by('sex__sex'))
                elif key == 'reason':
                    unique_values['reason'] = list(queryset.values_list('reason__reason', flat=True).distinct().order_by('reason__reason'))
                elif key == 'race':
                    unique_values['race'] = list(queryset.values_list('race__race', flat=True).distinct().order_by('race__race'))
                elif key == 'duration':
                    unique_values['duration'] = list(queryset.values_list('duration__duration', flat=True).distinct().order_by('duration__duration'))
                elif key == 'location':
                    unique_values['location'] = list(queryset.values_list('location__location', flat=True).distinct().order_by('location__location'))
              
              
            return unique_values  
      
        queryset = self.apply_filters(queryset, filters)
        
        if search_value:
           try:
                formatted_search_value = datetime.datetime.strptime(search_value, "%d-%m-%Y").strftime("%Y-%m-%d")
           except ValueError:
                formatted_search_value = search_value  # En caso de error, usa el valor original
   
      
           queryset= queryset.filter(
                Q(id__icontains=search_value)|
                Q(date__icontains=formatted_search_value)|
                Q(name__icontains=search_value)|
                Q(surname__icontains=search_value)|
                Q(sex__sex__contains=search_value)|
                Q(reason__reason__icontains=search_value)|
                Q(race__race__icontains=search_value)|
                Q(duration__duration__icontains=search_value)|
                Q(location__location__icontains=search_value)
            )
        
        order_colum_index=self.request.GET.get('order[0][column]','0')
     
        order_dir=self.request.GET.get('order[0][dir]','asc')
      
        column_map={
            '0':'id',
            '1':'date',
            '2':'picture',
            '3':'name',
            '4':'surname',
            '5':'sex',
            '6':'reason__reason',
            '7':'race__race',
            '8':'duration__duration',
            '9':'location__location',
          

        }
        order_field=column_map.get(order_colum_index,'id')
        
        if order_dir=='desc':
            order_field=f"-{order_field}"  

        queryset=queryset.order_by(order_field)  

        return queryset

   def render_to_response(self, context, **response_kwargs):
            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                draw = int(self.request.GET.get('draw', 1))
                start = int(self.request.GET.get('start', 0))
                length = int(self.request.GET.get('length', 10))      
                filters_only = self.request.GET.get('filters_only', 'false') == 'true'      

            
                if filters_only:           
                            
                    unique_values = self.get_queryset()    
                
                    data = []
                    for key, values in unique_values.items():
                        if isinstance(values, list):  
                            unique_values[key] = list(set(values))                      

                            data.append({
                                "filter": key,
                                "values": unique_values[key]  # Los valores únicos
                            })
                            
                    

                
                    return JsonResponse({
                        "draw": draw,
                        "recordsTotal": len(data),
                        "recordsFiltered": len(data),
                        "data": data
                    })
        
                queryset = self.get_queryset()
                total_records = self.model.objects.count()
                filtered_records = queryset.count()
                blacklist = queryset[start:start + length]

                data = [{
                    "id": blacklist.id,
                    "picture": blacklist.picture.url,
                    "date":str(blacklist.date),
                    "name": str(blacklist.name) if blacklist.name else "",
                    "surname": str(blacklist.surname) if blacklist.surname else "",
                    "sex": str(blacklist.sex.sex) if blacklist.sex else "",
                    "reason": str(blacklist.reason.reason) if blacklist.reason else "",
                    "race": str(blacklist.race.race) if blacklist.race else "",
                    "duration": str(blacklist.duration.duration) if blacklist.duration else "",
                    "location": str(blacklist.location) if blacklist.location else "",
                 
                    "detail_url": blacklist.get_absolute_url(),
                    "edit_url": blacklist.get_edit_url(),
                    "pdf_url": blacklist.get_pdf_url(),
                } for blacklist in blacklist]

                return JsonResponse({
                    "draw": draw,
                    "recordsTotal": total_records,
                    "recordsFiltered": filtered_records,
                    "data": data,
                })

            return super().render_to_response(context, **response_kwargs)

class CreateBlackListView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,CreateView):
     login_url = '/accounts/login/'
     redirect_field_name = 'redirect_to'
     model=BlackList
     template_name = 'black_list/create-blacklist.html'
     form_class = CreateBlackListForm    
     success_url = reverse_lazy("blacklist-list") 
     permission_required = 'cctv.add_blacklist'
     success_message = "The Customer was Added successfully to the BlackList."

     def form_valid(self, form):
        response = super().form_valid(form)
        if "save_and_continue" in self.request.POST:
             messages.success(self.request,"The Customer in BlackList was Added successfully. You can continue adding.")
             return redirect('blacklist-create')
        
        return response  

     
   #  def form_valid(self, form):
       #  try:
        #    userprofile = self.request.user.userprofile.location
           
       #  except UserProfile.DoesNotExist:
                
         #       return self.form_invalid(form)          
       
        # form.instance.location = userprofile
       
       #  return super().form_valid(form)


   #  def form_invalid(self, form):
     #   messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
     #   return super().form_invalid(form)	   


class UpdateBlackListView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
      login_url = '/accounts/login/'
      redirect_field_name = 'redirect_to'
      model=BlackList
      template_name = 'black_list/update-blacklist.html'
      form_class = CreateBlackListForm   
      success_url = reverse_lazy("blacklist-list")
      permission_required = 'cctv.change_blacklist'
    

      success_message = "The Customer was Updated successfully to the BlackList."
      
     # def form_valid(self, form):
        # try:
        #    userprofile = self.request.user.userprofile.location
           
       #  except UserProfile.DoesNotExist:
        #        messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
          #      return self.form_invalid(form)          
       
       #  form.instance.location = userprofile
       
        # return super().form_valid(form)


   #   def form_invalid(self, form):
      #  messages.error(self.request, "There was an error submitting the form.")
      #  return super().form_invalid(form)	   


class DeleteBlackListView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
       login_url = '/accounts/login/'
       redirect_field_name = 'redirect_to'
       model=BlackList
       context_object_name = 'blacklist'
       template_name='black_list/confirm_delete.html'   
       success_url = reverse_lazy("blacklist-list")
       permission_required = 'cctv.delete_blacklist'
    
       success_message = "The Customer was Delete successfully to the BlackList."
      
       def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location
           
         except UserProfile.DoesNotExist:
                messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
                return self.form_invalid(form)          
       
        
       
         return super().form_valid(form)


       def form_invalid(self, form):
        messages.error(self.request, "There was an error submitting the form.")
        return super().form_invalid(form)	


class DetailBlackListView(LoginRequiredMixin,PermissionRequiredMixin,DetailView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    model = BlackList
    context_object_name = 'blacklist'
    template_name='black_list/detail-blacklist.html'   
    success_url = reverse_lazy("blacklist-list")
    permission_required = 'cctv.view_blacklist'


 #Index Main  

def magnifyin(request,id):
    img=BlackList.objects.get(id=id)
    return render (request,'black_list/magnifying.html',{"image":img} )


#EndBlackList

#Begin BlackList Reinstated


#Black list Resintated CRUD and Functions
class ListBlackListView_Reinstated(LoginRequiredMixin,PermissionRequiredMixin,ListView):
   login_url = '/accounts/login/'
   redirect_field_name = 'redirect_to'
   template_name='black_list_reinstated/list-blacklist_reinstated.html'
   model=BlackList
   permission_required = 'cctv.add_blacklist'
  
  
   def dispatch(self, request, *args, **kwargs):
            if not hasattr(request.user, 'userprofile') and not self.request.user.is_superuser:
                messages.error(self.request, "No profile associated with the user was found!")
                return redirect(self.login_url)                
            return super().dispatch(request, *args, **kwargs)
 
   def apply_filters(self, queryset, filters):          
    for key, value in filters.items():
        if value:
            if key == 'id':
                queryset = queryset.filter(id__icontains=value)
            if key == 'date':           
              
                formatted_search_value =datetime.datetime.strptime(value, "%d-%m-%y").strftime("%Y-%m-%d")    
                  
                queryset = queryset.filter(date__icontains=formatted_search_value)

            elif key == 'name':
                queryset = queryset.filter(name__icontains=value)
            elif key == 'surname':
                queryset = queryset.filter(surname__icontains=value)
            elif key == 'sex':
                queryset = queryset.filter(sex__sex__icontains=value)
            elif key == 'reason':
                queryset = queryset.filter(reason__reason__icontains=value)
            elif key == 'race':
                queryset = queryset.filter(race__race__icontains=value)
            elif key == 'duration':
                queryset = queryset.filter(duration__duration__icontains=value)
            elif key == 'location':
                queryset = queryset.filter(location__location__icontains=value)
    return queryset



   def get_queryset(self):
               
        queryset = self.model.objects.filter(duration_id=7).order_by('-id', '-date')      
    

        search_value = self.request.GET.get('search[value]', '').strip()
        
        filters = self.request.GET.get('filters', '{}') 
        
        try:         
         filters = json.loads(filters) if filters else {}
        except json.JSONDecodeError:         
         filters = {}  

        filters_only = self.request.GET.get('filters_only', 'false') == 'true' 

        if filters_only:
            unique_values = {}  

            if not filters:
                filters = { 'id':'','date':'','name': '', 'surname': '','sex':'', 'reason': '', 'race': '', 'duration': '', 'location': '' }
     
            for key in filters.keys():
                if key == 'id':
                    unique_values['id'] = list(queryset.values_list('id', flat=True).distinct().order_by('id'))
                if key == 'date':
                    unique_values['date'] = list(queryset.values_list('date', flat=True).distinct().order_by('date'))
                elif key == 'name':
                    unique_values['name'] = list(queryset.values_list('name', flat=True).distinct().order_by('name'))
                elif key == 'surname':
                    unique_values['surname'] = list(queryset.values_list('surname', flat=True).distinct().order_by('surname'))
                elif key == 'sex':
                    unique_values['sex'] = list(queryset.values_list('sex__sex', flat=True).distinct().order_by('sex__sex'))
                elif key == 'reason':
                    unique_values['reason'] = list(queryset.values_list('reason__reason', flat=True).distinct().order_by('reason__reason'))
                elif key == 'race':
                    unique_values['race'] = list(queryset.values_list('race__race', flat=True).distinct().order_by('race__race'))
                elif key == 'duration':
                    unique_values['duration'] = list(queryset.values_list('duration__duration', flat=True).distinct().order_by('duration__duration'))
                elif key == 'location':
                    unique_values['location'] = list(queryset.values_list('location__location', flat=True).distinct().order_by('location__location'))
              
              
            return unique_values  
      
        queryset = self.apply_filters(queryset, filters)
        
        if search_value:
           try:
                formatted_search_value = datetime.datetime.strptime(search_value, "%d-%m-%Y").strftime("%Y-%m-%d")
           except ValueError:
                formatted_search_value = search_value  # En caso de error, usa el valor original
   
      
           queryset= queryset.filter(
                Q(id__icontains=search_value)|
                Q(date__icontains=formatted_search_value)|
                Q(name__icontains=search_value)|
                Q(surname__icontains=search_value)|
                Q(sex__sex__contains=search_value)|
                Q(reason__reason__icontains=search_value)|
                Q(race__race__icontains=search_value)|
                Q(duration__duration__icontains=search_value)|
                Q(location__location__icontains=search_value)
            )
        
        order_colum_index=self.request.GET.get('order[0][column]','0')
     
        order_dir=self.request.GET.get('order[0][dir]','asc')
      
        column_map={
            '0':'id',
            '1':'date',
            '2':'picture',
            '3':'name',
            '4':'surname',
            '5':'sex',
            '6':'reason__reason',
            '7':'race__race',
            '8':'duration__duration',
            '9':'location__location',
          

        }
        order_field=column_map.get(order_colum_index,'id')
        
        if order_dir=='desc':
            order_field=f"-{order_field}"  

        queryset=queryset.order_by(order_field)  

        return queryset

   def render_to_response(self, context, **response_kwargs):
            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                draw = int(self.request.GET.get('draw', 1))
                start = int(self.request.GET.get('start', 0))
                length = int(self.request.GET.get('length', 10))      
                filters_only = self.request.GET.get('filters_only', 'false') == 'true'      

            
                if filters_only:           
                            
                    unique_values = self.get_queryset()    
                
                    data = []
                    for key, values in unique_values.items():
                        if isinstance(values, list):  
                            unique_values[key] = list(set(values))                      

                            data.append({
                                "filter": key,
                                "values": unique_values[key]  # Los valores únicos
                            })      
                    

                
                    return JsonResponse({
                        "draw": draw,
                        "recordsTotal": len(data),
                        "recordsFiltered": len(data),
                        "data": data
                    })
        
                queryset = self.get_queryset()
               # total_records = self.model.objects.count()
                total_records=queryset.count()
                filtered_records = queryset.count()
                blacklist = queryset[start:start + length]

                data = [{
                    "id": blacklist.id,
                    "picture": blacklist.picture.url,
                    "date":str(blacklist.date),
                    "name": str(blacklist.name) if blacklist.name else "",
                    "surname": str(blacklist.surname) if blacklist.surname else "",
                    "sex": str(blacklist.sex.sex) if blacklist.sex else "",
                    "reason": str(blacklist.reason.reason) if blacklist.reason else "",
                    "race": str(blacklist.race.race) if blacklist.race else "",
                    "duration": str(blacklist.duration.duration) if blacklist.duration else "",
                    "location": str(blacklist.location) if blacklist.location else "",                 
                    "detail_url": blacklist.get_absolute_reinstated_url(),
                    "edit_url": blacklist.get_edit_reinstated_url(),
                    "pdf_url": blacklist.get_pdf_url(),
                } for blacklist in blacklist]

                return JsonResponse({
                    "draw": draw,
                    "recordsTotal": total_records,
                    "recordsFiltered": filtered_records,
                    "data": data,
                })

            return super().render_to_response(context, **response_kwargs)
 

   

class UpdateBlackListView_Reinstated(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
      login_url = '/accounts/login/'
      redirect_field_name = 'redirect_to'
      model=BlackList
      template_name = 'black_list_reinstated/update-blacklist_reinstated.html'
      form_class = CreateBlackListForm   
      success_url = reverse_lazy("blacklist-list-reinstated")
      permission_required = 'cctv.change_blacklist'   

      success_message = "The Customer was Updated successfully to the BlackList."
      



class DetailBlackListView_Reinstated(LoginRequiredMixin,PermissionRequiredMixin,DetailView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    model = BlackList
    context_object_name = 'blacklist'
    template_name='black_list_reinstated/detail-blacklist_reinstated.html'   
    success_url = reverse_lazy("blacklist-list-reinstated")
    permission_required = 'cctv.view_blacklist'


 #Index Main  
@login_required
def magnifyin_Reinstated(request,id):
    img=BlackList.objects.get(id=id)
    return render (request,'black_list_reinstated/magnifying_reinstated.html',{"image":img} )


#EndBlackListReinsdtated


@login_required
def index(request):
    if  request.user.is_superuser or request.user.username=='manager-pos' or request.user.username=='manager-chg' or request.user.username=='manager-arg' :        
         return redirect('dashboard')          
    else:   
        return render(request, 'index.html')
 #Index Main  
@login_required
def dashboard(request):
      def get_unique_customers_count(location_id):
        total_customers = Customer.objects.filter( fk_customer__location_id=location_id,
                           location_id=location_id
                         ).distinct().count()
        return total_customers
      
      report=Report.objects.count()
      reportPOS=Report.objects.filter(location=1).count()
      reportCHG=Report.objects.filter(location=2).count()
      reportARG=Report.objects.filter(location=5).count()
      if report>0 :
            reportARGPercent=round((reportARG/report*100),0)
            reportPOSPercent=round((reportPOS/report*100),0)
            reportCHGPercent=round((reportCHG/report*100),0)  
      else:
            reportARGPercent=0
            reportPOSPercent=0
            reportCHGPercent=0


  
      transactions=Cash_Desk_Transaction.objects.count()
      trasnsactionsPOS=Cash_Desk_Transaction.objects.filter(location=1).count()
      trasnsactionsCHG=Cash_Desk_Transaction.objects.filter(location=2).count()
      trasnsactionsARG=Cash_Desk_Transaction.objects.filter(location=5).count()
      if transactions>0:
            transactionsCHGPercent=round((trasnsactionsCHG/transactions*100),0) 
            transactionsPOSPercent=round((trasnsactionsPOS/transactions*100),0) 
            transactionsARGPercent=round((trasnsactionsARG/transactions*100),0) 
      else:
            transactionsCHGPercent=0
            transactionsPOSPercent=0
            transactionsARGPercent=0



      errors=Cash_Desk_Error.objects.count()
      errorsPOS=Cash_Desk_Error.objects.filter(location=1).count()
      errorsCHG=Cash_Desk_Error.objects.filter(location=2).count()
      errorsARG=Cash_Desk_Error.objects.filter(location=5).count()
      if errors>0:
            errorsPOSPercent=round((errorsPOS/errors*100),0) 
            errorsCHGPercent=round((errorsCHG/errors*100),0)
            errorsARGPercent=round((errorsARG/errors*100),0) 
      else:
            errorsPOSPercent=0
            errorsCHGPercent=0
            errorsARGPercent=0


             
      customers=Customer.objects.count()
      customersPOS=Customer.objects.filter(location=1).count()
      customersCHG=Customer.objects.filter(location=2).count()
      customersARG=Customer.objects.filter(location=5).count()
     
      if customers>0:
            customersPOSPercent=round((customersPOS/customers*100),0) 
            customersCHGPercent=round((customersCHG/customers*100),0)
            customersARGPercent=round((customersARG/customers*100),0) 
      else:
         customersPOSPercent=0
         customersCHGPercent=0
         customersARGPercent=0


 
      blacklisted=BlackList.objects.count()
      staff=Staff.objects.count()
      counterfeit=Counterfait.objects.count()
      pokerpayout=Poker_Payout.objects.count()
      activeCustomerPOS=get_unique_customers_count(1)
      activeCutomerCHG=get_unique_customers_count(2)
      activeCutomerARG=get_unique_customers_count(5)
      totalActiveCustomer=activeCustomerPOS+activeCutomerCHG+activeCutomerARG
      if totalActiveCustomer>0:
            activePOSPercent=round((activeCustomerPOS/totalActiveCustomer*100),1) 
            activeCHGPercent=round((activeCutomerCHG/totalActiveCustomer*100),1) 
            activeARGPercent=round((activeCutomerARG/totalActiveCustomer*100),1) 
      else:
            activePOSPercent=0
            activeCHGPercent=0
            activeARGPercent=0

    
      context={'report':report,'transactions':transactions,'errors':errors,
               'customers':customers,'reportPOS':reportPOS,'reportPOSPercent':reportPOSPercent,'reportCHG':reportCHG,'reportCHGPercent':reportCHGPercent,'reportARG':reportARG,'reportARGPercent':reportARGPercent,
                                               'trasnsactionsPOS':trasnsactionsPOS,'transactionsPOSPercent':transactionsPOSPercent,'trasnsactionsCHG':trasnsactionsCHG,'transactionsCHGPercent':transactionsCHGPercent,'trasnsactionsARG':trasnsactionsARG,'transactionsARGPercent':transactionsARGPercent,
                                               'errorsPOS':errorsPOS,'errorsPOSPercent':errorsPOSPercent,'errorsCHG':errorsCHG,'errorsCHGPercent':errorsCHGPercent,'errorsARG':errorsARG, 'errorsARGPercent':errorsARGPercent,
                                               'customersPOS':customersPOS,'customersPOSPercent':customersPOSPercent,'customersCHG':customersCHG,'customersCHGPercent':customersCHGPercent,'customersARG':customersARG,'customersARGPercent':customersARGPercent,
                                               'blacklisted':blacklisted,'staff':staff,
                                               'counterfeit':counterfeit,
                                               'pokerpayout':pokerpayout,
                                               'totalActiveCustomer':totalActiveCustomer,
                                               'activeCustomerPOS':activeCustomerPOS,
                                               'activeCutomerCHG':activeCutomerCHG,
                                               'activeCutomerARG':activeCutomerARG,
                                               'activePOSPercent':activePOSPercent,
                                               'activeCHGPercent':activeCHGPercent,
                                               'activeARGPercent':activeARGPercent,                                              
                                               
                                               }

    
      return render(request, 'dashboard.html',context)
#@login_required(login_url='login')

class IndexMainView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    model = Main
    template_name = 'main/list-main.html'
    context_object_name = 'main'   
    permission_required = 'cctv.view_main'

    def dispatch(self, request, *args, **kwargs):
            if not hasattr(request.user, 'location') and not self.request.user.is_superuser:
                messages.error(self.request, "No profile associated with the user was found")
                return redirect(self.login_url)
                
            return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs=Main.objects.all().order_by('-date')        
        return qs
    

#@login_required(login_url='login')  
    
class CreateMainView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,CreateView):
     login_url = '/accounts/login/'
     redirect_field_name = 'redirect_to'
     model=Main
     template_name = 'main/create-main.html'
     form_class = CreateMainForm      
     success_url = reverse_lazy("main-index") 
     permission_required = 'cctv.add_main'
     success_message = "The Main was Added successfully to the BlackList."
      
     def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location
           
         except UserProfile.DoesNotExist:
                messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
                return self.form_invalid(form)          
       
         form.instance.location = userprofile
       
         return super().form_valid(form)


     def form_invalid(self, form):
        messages.error(self.request, "There was an error submitting the form.")
        return super().form_invalid(form)	   
 
class UpdateMainView(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
      login_url = '/accounts/login/'
      redirect_field_name = 'redirect_to'
      model=Main
      template_name = 'main/update-main.html'
      form_class = CreateMainForm   
      success_url = reverse_lazy("main-index") 
      permission_required = 'cctv.change_main'

class DeleteMainView(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
       login_url = '/accounts/login/'
       redirect_field_name = 'redirect_to' 
       model=Main
       context_object_name = 'main'
       template_name='main/confirm_delete.html'   
       success_url = reverse_lazy("main-index")
       permission_required = 'cctv.delete_main'

    
       def form_valid(self, form):
        messages.success(self.request, "The date was deleted successfully.")
        return super(DeleteMainView,self).form_valid(form)

#Token*******Begin

class ListTokenView(LoginRequiredMixin, PermissionRequiredMixin,ListView):
   login_url = '/accounts/login/'
   redirect_field_name = 'redirect_to' 
   template_name='token/list-token.html'
   model=Token
   permission_required = 'cctv.view_token'

   def dispatch(self, request, *args, **kwargs):
            if not hasattr(request.user, 'userprofile') and not self.request.user.is_superuser:
                messages.error(self.request, "No profile associated with the user was found")
                return redirect(self.login_url)
                
            return super().dispatch(request, *args, **kwargs)
  
   def get_queryset(self):
        qs=Token.objects.all()
        return qs
    
class CreateTokenView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,CreateView):
     login_url = '/accounts/login/'
     redirect_field_name = 'redirect_to' 
     model=Token
     template_name = 'token/create-token.html'
     form_class = CreateTokenForm    
     success_url = reverse_lazy("token-list") 
     permission_required = 'cctv.add_token'    
     success_message = "The Token was Added successfully."
      
     def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location
           
         except UserProfile.DoesNotExist:
               
                return self.form_invalid(form)          
       
         form.instance.location = userprofile
       
         return super().form_valid(form)


     def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
        return super().form_invalid(form)	   
class UpdateTokenView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
      login_url = '/accounts/login/'
      redirect_field_name = 'redirect_to' 
      model=Token
      template_name = 'token/update-token.html'
      form_class = CreateTokenForm   
      success_url = reverse_lazy("token-list") 
      permission_required = 'cctv.change_token'
      success_message = "The Token was Updated successfully."
      
      def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location
           
         except UserProfile.DoesNotExist:
               
                return self.form_invalid(form)          
       
         form.instance.location = userprofile
       
         return super().form_valid(form)


      def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
        return super().form_invalid(form)	   

class DeleteTokenView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
       login_url = '/accounts/login/'
       redirect_field_name = 'redirect_to' 
       model=Token
       context_object_name = 'token'
       template_name='token/confirm_delete.html'   
       success_url = reverse_lazy("token-list")
       permission_required = 'cctv.delete_token'    
 
      
       success_message = "The Token was Deleted successfully."
       error_message = (
            "Cannot delete the Token '{name}' because it is related to other records: {details}."
              )
       

       def post(self, request, *args, **kwargs):
                self.object = self.get_object()  # Obtener el objeto a eliminar
              
                try:
                    # Intentar eliminar el objeto
                    self.object.delete()
                    messages.success(request, self.success_message)
                    return redirect(self.success_url)
                except ProtectedError as e:
                 
                    related_objects = ', '.join(str(obj) for obj in e.protected_objects)
                    
                    error_message = self.error_message.format(name=str(self.object), details=related_objects)
                    messages.error(request, error_message)
                    return redirect(self.success_url)

class DetailTokenView(LoginRequiredMixin,PermissionRequiredMixin,DetailView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to' 
    model = Token
    context_object_name = 'token'
    template_name='token/detail-token.html'   
    success_url = reverse_lazy("token-list")
    permission_required = 'cctv.view_token'
#Token*****End       
#Report Type-------Begin
       
class ListReportTypeView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
   login_url = '/accounts/login/'
   redirect_field_name = 'redirect_to' 
   template_name='report_type/list-report_type.html'
   model=ReportType
   permission_required = 'cctv.view_reporttype'

   def dispatch(self, request, *args, **kwargs):
            if not hasattr(request.user, 'userprofile') and not self.request.user.is_superuser:
                messages.error(self.request, "No profile associated with the user was found")
                return redirect(self.login_url)
                
            return super().dispatch(request, *args, **kwargs)
  
   def get_queryset(self):
        qs=ReportType.objects.all()
        return qs
     
class CreateReportTypeView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,CreateView):
     login_url = '/accounts/login/'
     redirect_field_name = 'redirect_to' 
     model=ReportType
     template_name = 'report_type/create-report_type.html'
     form_class = CreateReportTypeForm    
     success_url = reverse_lazy("report_type-list") 
     permission_required = 'cctv.add_reporttype'
     success_message = "The Report Type was Added successfully to the BlackList."
      
     def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location
           
         except UserProfile.DoesNotExist:
                
                return self.form_invalid(form)          
       
         form.instance.location = userprofile
       
         return super().form_valid(form)


     def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
        return super().form_invalid(form)	   

class UpdateReportTypeView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
      login_url = '/accounts/login/'
      redirect_field_name = 'redirect_to' 
      model=ReportType
      template_name = 'report_type/update-report_type.html'
      form_class = CreateReportTypeForm   
      success_url = reverse_lazy("report_type-list") 
      permission_required = 'cctv.change_reporttype'
      success_message = "The Report Type was Updated successfully to the BlackList."
      
      def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location
           
         except UserProfile.DoesNotExist:
                
                return self.form_invalid(form)          
       
         form.instance.location = userprofile
       
         return super().form_valid(form)


      def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
        return super().form_invalid(form)	   

class DeleteReportTypeView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
       login_url = '/accounts/login/'
       redirect_field_name = 'redirect_to' 
       model=ReportType
       context_object_name = 'report_type'
       template_name='report_type/confirm_delete.html'   
       success_url = reverse_lazy("report_type-list")
       permission_required = 'cctv.delete_reporttype'
       success_message = "The Report Type was Deleted successfully to the BlackList."
      
       success_message = "The Report Type was Deleted successfully."
       error_message = (
            "Cannot delete Report Type '{name}' because it is related to other records: {details}."
              )
       

       def post(self, request, *args, **kwargs):
                self.object = self.get_object()  # Obtener el objeto a eliminar
              
                try:
                    # Intentar eliminar el objeto
                    self.object.delete()
                    messages.success(request, self.success_message)
                    return redirect(self.success_url)
                except ProtectedError as e:
                 
                    related_objects = ', '.join(str(obj) for obj in e.protected_objects)
                    
                    error_message = self.error_message.format(name=str(self.object), details=related_objects)
                    messages.error(request, error_message)
                    return redirect(self.success_url)

class DetailReportTypeView(LoginRequiredMixin,PermissionRequiredMixin,DetailView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to' 
    model = ReportType
    context_object_name = 'report_type'
    template_name='report_type/detail-report_type.html'   
    success_url = reverse_lazy("report_type-list")
    permission_required = 'cctv.view_reporttype'

#Report Type   ------End
#Customer***Begin

class ListCustomerView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Customer
    template_name = "customers/list-customers.html"
    context_object_name = "customers"
    permission_required = "cctv.view_customer"
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def get_queryset(self):
        if self.request.user.is_superuser:
             queryset = self.model.objects.all() 
          
        else:
            queryset = self.model.objects.filter(location=self.request.user.userprofile.location).order_by('customer')  
       
        search_value = self.request.GET.get('search[value]', '').strip()
        if search_value:
            queryset = queryset.filter(
                Q(id__icontains=search_value) |
                Q(customer__contains=search_value) |
                Q(location__location__contains=search_value)
            )

    
        order_column_index = self.request.GET.get('order[0][column]', '0')
        order_dir = self.request.GET.get('order[0][dir]', 'asc')

        column_map = {
            '0': 'id',
            '2': 'customer',  # Ajusta si el nombre del campo en el modelo es diferente
            '3': 'location__location',  # Si location es una ForeignKey
        }

        order_field = column_map.get(order_column_index, 'id')
        if order_dir == 'desc':
            order_field = f"-{order_field}"

        queryset = queryset.order_by(order_field)
        return queryset

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            draw = int(self.request.GET.get('draw', 1))
            start = int(self.request.GET.get('start', 0))
            length = int(self.request.GET.get('length', 10))

            queryset = self.get_queryset()
            total_records = Customer.objects.count()
            filtered_records = queryset.count()

            customers = queryset[start:start+length]

            data = [{
                "id": customer.id,
                "customer": customer.customer,
                "location": customer.location.location if customer.location else "",
                "photo": customer.photo.url if customer.photo else "",
                "detail_url": f"/customer/detail/{customer.id}/",
                "edit_url": f"/customer/update/{customer.id}/",
                "delete_url": f"/customer/delete/{customer.id}/",
            } for customer in customers]

            return JsonResponse({
                "draw": draw,
                "recordsTotal": total_records,
                "recordsFiltered": filtered_records,
                "data": data,
            })

        return super().render_to_response(context, **response_kwargs)

  
#class ListCustomerView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
#    login_url = '/accounts/login/'
#    redirect_field_name = 'redirect_to'
#    model = Customer
#    template_name = 'customers/list-customers.html'
#    context_object_name = 'customers'
#    permission_required = 'cctv.view_customer'
#    paginate_by = 10 

#    def get_paginate_by(self, queryset): 
#        paginate_by = self.request.GET.get('length', self.paginate_by)
      
     
#        try:
             
#                paginate_by = int(paginate_by)
               
#        except (ValueError, TypeError):
              
 #               paginate_by = self.paginate_by

 #       return paginate_by

 #   def get_queryset(self):
      
 #       if self.request.user.is_superuser:
 #            queryset = self.model.objects.all() 
          
  #      else:
  #           queryset = self.model.objects.filter(location=self.request.user.userprofile.location).order_by('customer')  
  #      search_query = self.request.GET.get('search', '')
  #      if search_query:         
  #          queryset = queryset.filter(
  #              Q(id__icontains=search_query) |              
  #              Q(customer__icontains=search_query) 
  #          )
        
   #     return queryset
 
    
 #   def get_context_data(self, **kwargs):
  #      context = super().get_context_data(**kwargs)     
  #      queryset = self.get_queryset()      
  #      paginate_by = self.get_paginate_by(queryset)    
 #       paginator = Paginator(queryset, paginate_by)
 #       page = self.request.GET.get('page', 1) 

  #      try:
   #         customers = paginator.page(page)
   #     except PageNotAnInteger:
  #          customers = paginator.page(1)
   #     except EmptyPage:
   #         customers = paginator.page(paginator.num_pages)
  
 #       context['customers'] = customers
  #      context['paginator'] = paginator
   #     context['paginate_by'] = paginate_by 
  #      context['total_pages'] = paginator.num_pages        
   #     context['search_query'] = self.request.GET.get('search', '')

    #    return context
   
  
     
class CreateCustomerView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,CreateView):
     login_url = '/accounts/login/'
     redirect_field_name = 'redirect_to' 
     model=Customer
     template_name = 'customers/create-customers.html'
     form_class = CreateCustomerForm    
     success_url = reverse_lazy("customer-list")
     permission_required = 'cctv.add_customer' 
     success_message = "The Customer was Added successfully."
      
     def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location
           
         except UserProfile.DoesNotExist:
                
                return self.form_invalid(form)          
       
         form.instance.location = userprofile       
         return super().form_valid(form)


     def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
        return super().form_invalid(form)	
      

class UpdateCustomerView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
      login_url = '/accounts/login/'
      redirect_field_name = 'redirect_to' 
      model=Customer
      template_name = 'customers/update-customers.html'
      form_class = CreateCustomerForm   
      success_url = reverse_lazy("customer-list") 
      permission_required = 'cctv.change_customer'
      success_message = "The Customer was Updated successfully."

      def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location
           
         except UserProfile.DoesNotExist:
                
                return self.form_invalid(form)          
       
         form.instance.location = userprofile       
         return super().form_valid(form)


      def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
        return super().form_invalid(form)	

class DeleteCustomerView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
       login_url = '/accounts/login/'
       redirect_field_name = 'redirect_to' 
       model=Customer
       context_object_name = 'customer'
       template_name='customers/confirm_delete.html'   
       success_url = reverse_lazy("customer-list")
       permission_required = 'cctv.delete_customer'

       # Mensajes personalizados
       success_message = "The Customer was successfully deleted."
       error_message = (
            "Cannot delete customer '{name}' because it is related to other records: {details}."
              )

       def post(self, request, *args, **kwargs):
            self.object = self.get_object()  # Obtener el objeto a eliminar
            try:
                # Intentar eliminar el objeto
                self.object.delete()
                messages.success(request, self.success_message)
                return redirect(self.success_url)
            except ProtectedError as e:
                # Capturar objetos relacionados que bloquean la eliminación
                related_objects = ', '.join(str(obj) for obj in e.protected_objects)
                # Personalizar el mensaje de error
                error_message = self.error_message.format(name=str(self.object), details=related_objects)
                messages.error(request, error_message)
                return redirect(self.success_url)
        
class DetailCustomerView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to' 
    model = Customer
    context_object_name = 'customer'
    template_name='customers/detail-customer.html'   
    success_url = reverse_lazy("customer-list")
    permission_required = 'cctv.view_customer' 
   
 
#Customer******End
#Casino Area
      
class ListCasinoAreaView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
   login_url = '/accounts/login/'
   redirect_field_name = 'redirect_to' 
   template_name='area/list-area.html'
   model=Area
   permission_required = 'cctv.view_area'

   def dispatch(self, request, *args, **kwargs):
            if not hasattr(request.user, 'userprofile') and not self.request.user.is_superuser:
                messages.error(self.request, "No profile associated with the user was found")
                return redirect(self.login_url)
                
            return super().dispatch(request, *args, **kwargs)

   def get_queryset(self):
        qs=Area.objects.all()
        return qs

    
class CreateCasinoAreaView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,CreateView):
     login_url = '/accounts/login/'
     redirect_field_name = 'redirect_to' 
     model=Area
     template_name = 'area/create-area.html'
     form_class = CreateCasinoAreaForm    
     success_url = reverse_lazy("area-list") 
     permission_required = 'cctv.add_area'
     success_message = "The Casino Location was Added successfully to the BlackList."
      
     def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location
           
         except UserProfile.DoesNotExist:
               
                return self.form_invalid(form)          
       
         form.instance.location = userprofile
       
         return super().form_valid(form)


     def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
        return super().form_invalid(form)	   
   
class UpdateCasinoAreaView(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
      login_url = '/accounts/login/'
      redirect_field_name = 'redirect_to' 
      model=Area
      template_name = 'area/update-area.html'
      form_class = CreateCasinoAreaForm   
      success_url = reverse_lazy("area-list") 
      permission_required = 'cctv.change_area'

      success_message = "The Casino Location was Updated successfully to the BlackList."
      
      def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location
           
         except UserProfile.DoesNotExist:
               
                return self.form_invalid(form)          
       
         form.instance.location = userprofile
       
         return super().form_valid(form)


      def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
        return super().form_invalid(form)	   

class DeleteCasinoAreaView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
       login_url = '/accounts/login/'
       redirect_field_name = 'redirect_to' 
       model=Area
       context_object_name = 'area'
       template_name='area/confirm_delete.html'   
       success_url = reverse_lazy("area-list")
       permission_required = 'cctv.delete_area'    
           
       success_message = "The Casino Location was Deleted successfully ."
       error_message = (
            "Cannot delete Casino Location  '{name}' because it is related to other records: {details}."
              )
       

       def post(self, request, *args, **kwargs):
                self.object = self.get_object()  # Obtener el objeto a eliminar
              
                try:
                    # Intentar eliminar el objeto
                    self.object.delete()
                    messages.success(request, self.success_message)
                    return redirect(self.success_url)
                except ProtectedError as e:
                 
                    related_objects = ', '.join(str(obj) for obj in e.protected_objects)
                    
                    error_message = self.error_message.format(name=str(self.object), details=related_objects)
                    messages.error(request, error_message)
                    return redirect(self.success_url)
      

class DetailCasinoAreaView(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to' 
    model = Area
    context_object_name = 'casino_area'
    template_name='area/detail-area.html'   
    success_url = reverse_lazy("area-list")
    permission_required = 'cctv.view_area' 
#Cashier Area-----Begin

class ListCashierAreaView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
   login_url = '/accounts/login/'
   redirect_field_name = 'redirect_to' 
   template_name='cashier_area/list-cashier_area.html'
   model=AreaCashier
   permission_required = 'cctv.view_areacashier'

   def dispatch(self, request, *args, **kwargs):
            if not hasattr(request.user, 'userprofile') and not self.request.user.is_superuser:
                messages.error(self.request, "No profile associated with the user was found")
                return redirect(self.login_url)
                
            return super().dispatch(request, *args, **kwargs)

   def get_queryset(self):
        qs=AreaCashier.objects.all()
        return qs
      
class CreateCashierAreaView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,CreateView):
     login_url = '/accounts/login/'
     redirect_field_name = 'redirect_to' 
     model=AreaCashier
     template_name = 'cashier_area/create-cashier_area.html'
     form_class = CreateCashierAreaForm    
     success_url = reverse_lazy("cashier_area-list") 
     permission_required = 'cctv.add_areacashier'
     success_message = "The Cashier Location was Added successfully to the BlackList."
      
     def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location
           
         except UserProfile.DoesNotExist:
             
                return self.form_invalid(form)          
       
         form.instance.location = userprofile
       
         return super().form_valid(form)


     def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
        return super().form_invalid(form)	   

class UpdateCashierAreaView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
      login_url = '/accounts/login/'
      redirect_field_name = 'redirect_to' 
      model=AreaCashier
      template_name = 'cashier_area/update-cashier_area.html'
      form_class = CreateCashierAreaForm   
      success_url = reverse_lazy("cashier_area-list") 
      permission_required = 'cctv.change_areacashier'
      success_message = "The Report Orifination was Updated successfully to the BlackList."
      
      def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location
           
         except UserProfile.DoesNotExist:
               
                return self.form_invalid(form)          
       
         form.instance.location = userprofile
       
         return super().form_valid(form)


      def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
        return super().form_invalid(form)	   

class DeleteCashierAreaView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
       login_url = '/accounts/login/'
       redirect_field_name = 'redirect_to' 
       model=AreaCashier
       context_object_name = 'area_cashier'
       template_name='cashier_area/confirm_delete.html'   
       success_url = reverse_lazy("cashier_area-list")
       permission_required = 'cctv.delete_areacashier'
       success_message = "The Report Orifination was Deleted successfully to the BlackList."
      
    
       success_message = "The Cashier Location was Deleted successfully ."
       error_message = (
            "Cannot delete Cashier Location  '{name}' because it is related to other records: {details}."
              )
       

       def post(self, request, *args, **kwargs):
                self.object = self.get_object()  # Obtener el objeto a eliminar
              
                try:
                    # Intentar eliminar el objeto
                    self.object.delete()
                    messages.success(request, self.success_message)
                    return redirect(self.success_url)
                except ProtectedError as e:
                 
                    related_objects = ', '.join(str(obj) for obj in e.protected_objects)
                    
                    error_message = self.error_message.format(name=str(self.object), details=related_objects)
                    messages.error(request, error_message)
                    return redirect(self.success_url)


class DetailCashierAreaView(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to' 
    model = AreaCashier
    context_object_name = 'area_cashier'
    template_name='cashier_area/detail-cashier_area.html'   
    success_url = reverse_lazy("area_cashier-list")
    permission_required = 'cctv.view_areacashier' 


#Cashier Area------End     

#Report Origination-----Begin

class ListReportOriginationView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
   login_url = '/accounts/login/'
   redirect_field_name = 'redirect_to' 
   template_name='report_origination/list-origination.html'
   model=ReportOrigination
   permission_required = 'cctv.view_reportorigination'

   def dispatch(self, request, *args, **kwargs):
            if not hasattr(request.user, 'userprofile') and not self.request.user.is_superuser:
                messages.error(self.request, "No profile associated with the user was found")
                return redirect(self.login_url)
                
            return super().dispatch(request, *args, **kwargs)

   def get_queryset(self):
        qs=ReportOrigination.objects.all()
        return qs
  
class CreateReportOriginationView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,CreateView):
     login_url = '/accounts/login/'
     redirect_field_name = 'redirect_to' 
     model=ReportOrigination
     template_name = 'report_origination/create-origination.html'
     form_class = CreateReportOriginationForm    
     success_url = reverse_lazy("origination-list") 
     permission_required = 'cctv.add_reportorigination'
     success_message = "The Report Orifination was Added successfully to the BlackList."
      
     def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location
           
         except UserProfile.DoesNotExist:
               
                return self.form_invalid(form)          
       
         form.instance.location = userprofile
       
         return super().form_valid(form)

     def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
        return super().form_invalid(form)	 
  
class UpdateReportOriginationView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
      login_url = '/accounts/login/'
      redirect_field_name = 'redirect_to' 
      model=ReportOrigination
      template_name = 'report_origination/update-origination.html'
      form_class = CreateReportOriginationForm   
      success_url = reverse_lazy("origination-list") 
      permission_required = 'cctv.change_reportorigination'

      success_message = "The Report Orifination was Updated successfully to the BlackList."
      
      def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location
           
         except UserProfile.DoesNotExist:
               
                return self.form_invalid(form)          
       
         form.instance.location = userprofile
       
         return super().form_valid(form)


      def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
        return super().form_invalid(form)	   

class DeleteReportOriginationView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
       login_url = '/accounts/login/'
       redirect_field_name = 'redirect_to' 
       model=ReportOrigination
       context_object_name = 'origination'
       template_name='report_origination/confirm_delete.html'   
       success_url = reverse_lazy("origination-list")
       permission_required = 'cctv.delete_reportorigination'
    
       success_message = "The Report Origination was Deleted successfully."
       error_message = (
            "Cannot delete Report Origination '{name}' because it is related to other records: {details}."
              )
       

       def post(self, request, *args, **kwargs):
                self.object = self.get_object()  # Obtener el objeto a eliminar
              
                try:
                    # Intentar eliminar el objeto
                    self.object.delete()
                    messages.success(request, self.success_message)
                    return redirect(self.success_url)
                except ProtectedError as e:
                 
                    related_objects = ', '.join(str(obj) for obj in e.protected_objects)
                    
                    error_message = self.error_message.format(name=str(self.object), details=related_objects)
                    messages.error(request, error_message)
                    return redirect(self.success_url)

class DetailReportOriginationView(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to' 
    model = ReportOrigination
    context_object_name = 'origination'
    template_name='report_origination/detail-origination.html'   
    success_url = reverse_lazy("origination-list")
    permission_required = 'cctv.view_reportorigination' 

#Report Origination--------End
#Report Title
   
class ListReportTitleView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
   login_url = '/accounts/login/'
   redirect_field_name = 'redirect_to' 
   template_name='report_title/list-report_title.html'
   model=ReportTitle
   permission_required = 'cctv.view_reporttitle'

   def dispatch(self, request, *args, **kwargs):
            if not hasattr(request.user, 'userprofile') and not self.request.user.is_superuser:
                messages.error(self.request, "No profile associated with the user was found")
                return redirect(self.login_url)
                
            return super().dispatch(request, *args, **kwargs)

   def get_queryset(self):
        qs=ReportTitle.objects.all()
        return qs
    
class CreateReportTitleView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,CreateView):
     login_url = '/accounts/login/'
     redirect_field_name = 'redirect_to' 
     model=ReportTitle
     template_name = 'report_title/create-report_title.html'
     form_class = CreateReportTitleForm    
     success_url = reverse_lazy("report_title-list") 
     permission_required = 'cctv.add_reporttitle'
     success_message = "The Report Title was Added successfully to the BlackList."
      
     def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location
           
         except UserProfile.DoesNotExist:
               
                return self.form_invalid(form)          
       
         form.instance.location = userprofile
       
         return super().form_valid(form)


     def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
        return super().form_invalid(form)	   

class UpdateReportTitleView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
      login_url = '/accounts/login/'
      redirect_field_name = 'redirect_to' 
      model=ReportTitle
      template_name = 'report_title/update-report_title.html'
      form_class = CreateReportTitleForm   
      success_url = reverse_lazy("report_title-list") 
      permission_required = 'cctv.change_reporttitle'

      success_message = "The Report Title was Updated successfully to the BlackList."
      
      def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location
           
         except UserProfile.DoesNotExist:
               
                return self.form_invalid(form)          
       
         form.instance.location = userprofile
       
         return super().form_valid(form)


      def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
        return super().form_invalid(form)	   

class DeleteReportTitleView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
       login_url = '/accounts/login/'
       redirect_field_name = 'redirect_to' 
       model=ReportTitle
       context_object_name = 'report_title'
       template_name='report_title/confirm_delete.html'   
       success_url = reverse_lazy("report_title-list")
       permission_required = 'cctv.delete_reporttitle'

       success_message = "The Report Title was Deleted successfully"
       error_message = (
            "Cannot delete Report Title  '{name}' because it is related to other records: {details}."
              )
       

       def post(self, request, *args, **kwargs):
                self.object = self.get_object()  # Obtener el objeto a eliminar
              
                try:
                    # Intentar eliminar el objeto
                    self.object.delete()
                    messages.success(request, self.success_message)
                    return redirect(self.success_url)
                except ProtectedError as e:
                 
                    related_objects = ', '.join(str(obj) for obj in e.protected_objects)
                    
                    error_message = self.error_message.format(name=str(self.object), details=related_objects)
                    messages.error(request, error_message)
                    return redirect(self.success_url)

class DetailReportTitleView(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to' 
    model = ReportTitle
    context_object_name = 'report_title'
    template_name='report_title/detail-report_title.html'   
    success_url = reverse_lazy("report_title-list")
    permission_required = 'cctv.view_reporttitle'    
#Report Title ------End  
@login_required
def LoadReportTitle(request):
     id = request.GET.get('id')  # Obtener el ID seleccionado
     titles = ReportTitle.objects.filter(type_report_id=id).values('id', 'title')
   
     return JsonResponse(list(titles), safe=False)
        
#Account_Type------Begin
class ListAccount_TypeView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
   login_url = '/accounts/login/'
   redirect_field_name = 'redirect_to' 
   template_name='account_type/list-account_type.html'
   model=AccountType
   permission_required = 'cctv.view_accounttype'

   def dispatch(self, request, *args, **kwargs):
            if not hasattr(request.user, 'userprofile') and not self.request.user.is_superuser:
                messages.error(self.request, "No profile associated with the user was found")
                return redirect(self.login_url)
                
            return super().dispatch(request, *args, **kwargs)
   
   def get_queryset(self):
        qs=AccountType.objects.all()
        return qs
     
class CreateAccount_TypeView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,CreateView):
     login_url = '/accounts/login/'
     redirect_field_name = 'redirect_to' 
     model=AccountType
     template_name = 'account_type/create-account_type.html'
     form_class = CreateAccountTypeForm    
     success_url = reverse_lazy("account_type-list")
     permission_required = 'cctv.add_accounttype'
     success_message = "The Account Type was Added successfully."
      
     def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location
           
         except UserProfile.DoesNotExist:
               
                return self.form_invalid(form)          
       
         form.instance.location = userprofile
       
         return super().form_valid(form)


     def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
        return super().form_invalid(form)	   
     
class UpdateAccount_TypeView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
      login_url = '/accounts/login/'
      redirect_field_name = 'redirect_to' 
      model=AccountType
      template_name = 'account_type/update-account_type.html'
      form_class = CreateAccountTypeForm   
      success_url = reverse_lazy("account_type-list")
      permission_required = 'cctv.change_accounttype'
      success_message = "The Account Type was Added successfully."
      
      def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location
           
         except UserProfile.DoesNotExist:
               
                return self.form_invalid(form)          
       
         form.instance.location = userprofile
       
         return super().form_valid(form)


      def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
        return super().form_invalid(form)	   
   
class DeleteAccount_TypeView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
       login_url = '/accounts/login/'
       redirect_field_name = 'redirect_to' 
       model=AccountType
       context_object_name = 'account_type'
       template_name='account_type/confirm_delete.html'   
       success_url = reverse_lazy("account_type-list")
       permission_required = 'cctv.delete_accounttype'
    
       success_message = "The Account Type was Delete successfully."
       error_message = (
            "Cannot delete the Account Type '{name}' because it is related to other records: {details}."
              )
       

       def post(self, request, *args, **kwargs):
                self.object = self.get_object()  # Obtener el objeto a eliminar
              
                try:
                    # Intentar eliminar el objeto
                    self.object.delete()
                    messages.success(request, self.success_message)
                    return redirect(self.success_url)
                except ProtectedError as e:
                 
                    related_objects = ', '.join(str(obj) for obj in e.protected_objects)
                    
                    error_message = self.error_message.format(name=str(self.object), details=related_objects)
                    messages.error(request, error_message)
                    return redirect(self.success_url)


class DetailAccount_TypeView(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to' 
    model = AccountType
    context_object_name = 'account_type'
    template_name='account_type/detail-account_type.html'   
    success_url = reverse_lazy("account_type-list")
    permission_required = 'cctv.view_accounttype'    	   
#Account_Type------End

#Shift--------Begin
class ListShiftView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
   login_url = '/accounts/login/'
   redirect_field_name = 'redirect_to' 
   template_name='shift/list-shift.html'
   model=Shift
   permission_required = 'cctv.view_shift'

   def dispatch(self, request, *args, **kwargs):
            if not hasattr(request.user, 'userprofile') and not self.request.user.is_superuser:
                messages.error(self.request, "No profile associated with the user was found")
                return redirect(self.login_url)
                
            return super().dispatch(request, *args, **kwargs)
   

   def get_queryset(self):
        qs=Shift.objects.all()
        return qs
     
class CreateShiftView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,CreateView):
     login_url = '/accounts/login/'
     redirect_field_name = 'redirect_to' 
     model=Shift
     template_name = 'shift/create-shift.html'
     form_class = CreateShiftForm    
     success_url = reverse_lazy("shift-list")
     permission_required = 'cctv.add_shift'
     success_message = "The Shift was Added successfully."
      
     def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location
           
         except UserProfile.DoesNotExist:
               
                return self.form_invalid(form)          
       
         form.instance.location = userprofile
       
         return super().form_valid(form)


     def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
        return super().form_invalid(form)	   
    
class UpdateShiftView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
      login_url = '/accounts/login/'
      redirect_field_name = 'redirect_to' 
      model=Shift
      template_name = 'shift/update-shift.html'
      form_class = CreateShiftForm   
      success_url = reverse_lazy("shift-list")
      permission_required = 'cctv.change_shift'
      success_message = "The Shift was Updated successfully."
      
      def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location
           
         except UserProfile.DoesNotExist:
               
                return self.form_invalid(form)          
       
         form.instance.location = userprofile
       
         return super().form_valid(form)


      def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
        return super().form_invalid(form)	   
    
class DeleteShiftView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
       login_url = '/accounts/login/'
       redirect_field_name = 'redirect_to' 
       model=Shift
       context_object_name = 'shift'
       template_name='shift/confirm_delete.html'   
       success_url = reverse_lazy("shift-list")
       permission_required = 'cctv.delete_shift'
       
      
       success_message = "The Shift was Updated successfully."
       error_message = (
            "Cannot delete the Shift '{name}' because it is related to other records: {details}."
              )
       

       def post(self, request, *args, **kwargs):
                self.object = self.get_object()  # Obtener el objeto a eliminar
              
                try:
                    # Intentar eliminar el objeto
                    self.object.delete()
                    messages.success(request, self.success_message)
                    return redirect(self.success_url)
                except ProtectedError as e:
                 
                    related_objects = ', '.join(str(obj) for obj in e.protected_objects)
                    
                    error_message = self.error_message.format(name=str(self.object), details=related_objects)
                    messages.error(request, error_message)
                    return redirect(self.success_url)

class  DetailShiftView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,DetailView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to' 
    model = Shift
    context_object_name = 'shift'
    template_name='shift/detail-shift.html'   
    success_url = reverse_lazy("shift-list")
    permission_required = 'cctv.view_shift'     
 #Shift--------End      


#Location------Begin
class ListLocationView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
   login_url = '/accounts/login/'
   redirect_field_name = 'redirect_to' 
   template_name='location/list-location.html'
   model=Location
   permission_required = 'cctv.view_location'

   def dispatch(self, request, *args, **kwargs):
            if not hasattr(request.user, 'userprofile') and not self.request.user.is_superuser:
                messages.error(self.request, "No profile associated with the user was found")
                return redirect(self.login_url)
                
            return super().dispatch(request, *args, **kwargs)

   def get_queryset(self):
        qs=Location.objects.all()
        return qs
     
class CreateLocationView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,CreateView):
     login_url = '/accounts/login/'
     redirect_field_name = 'redirect_to' 
     model=Location
     template_name = 'location/create-location.html'
     form_class = CreateLocationForm    
     success_url = reverse_lazy("location-list")
     permission_required = 'cctv.add_location'
     success_message = "The Branch was Added successfully."
      
     def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location
           
         except UserProfile.DoesNotExist:
               
                return self.form_invalid(form)          
       
         form.instance.location = userprofile
       
         return super().form_valid(form)

     def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
        return super().form_invalid(form)	   
     

class UpdateLocationView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
      login_url = '/accounts/login/'
      redirect_field_name = 'redirect_to' 
      model=Location
      template_name = 'location/update-location.html'
      form_class = CreateLocationForm   
      success_url = reverse_lazy("location-list")
      permission_required = 'cctv.change_location'
      success_message = "The Branch was Added successfully."
      
      def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location
           
         except UserProfile.DoesNotExist:
               
                return self.form_invalid(form)          
       
         form.instance.location = userprofile
       
         return super().form_valid(form)


      def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
        return super().form_invalid(form)
   

class DeleteLocationView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
       login_url = '/accounts/login/'
       redirect_field_name = 'redirect_to' 
       model=Location
       context_object_name = 'location'
       template_name='location/confirm_delete.html'   
       success_url = reverse_lazy("location-list")
       permission_required = 'cctv.delete_location'
          
       success_message = "The Branch was Deleted successfully."
       error_message = (
            "Cannot delete the Branch '{name}' because it is related to other records: {details}."
              )
       

       def post(self, request, *args, **kwargs):
                self.object = self.get_object()  # Obtener el objeto a eliminar
              
                try:
                    # Intentar eliminar el objeto
                    self.object.delete()
                    messages.success(request, self.success_message)
                    return redirect(self.success_url)
                except ProtectedError as e:
                 
                    related_objects = ', '.join(str(obj) for obj in e.protected_objects)
                    
                    error_message = self.error_message.format(name=str(self.object), details=related_objects)
                    messages.error(request, error_message)
                    return redirect(self.success_url)
       
class  DetailLocationView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,DetailView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to' 
    model = Location
    context_object_name = 'location'
    template_name='location/detail-location.html'   
    success_url = reverse_lazy("location-list")
    permission_required = 'cctv.view_location' 




   #Location------End
#Sex----Begin
class ListSexView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
   login_url = '/accounts/login/'
   redirect_field_name = 'redirect_to' 
   template_name='sex/list-sex.html'
   model=Sex
   permission_required = 'cctv.view_sex'

   def dispatch(self, request, *args, **kwargs):
            if not hasattr(request.user, 'userprofile') and not self.request.user.is_superuser:
                messages.error(self.request, "No profile associated with the user was found")
                return redirect(self.login_url)
                
            return super().dispatch(request, *args, **kwargs)

   def get_queryset(self):
        qs=Sex.objects.all()
        return qs
     
class CreateSexView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,CreateView):
     login_url = '/accounts/login/'
     redirect_field_name = 'redirect_to' 
     model=Sex
     template_name = 'sex/create-sex.html'
     form_class = CreateSexForm    
     success_url = reverse_lazy("sex-list")
     permission_required = 'cctv.add_sex'
     success_message = "The Sex was Added successfully."
      
     def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location
           
         except UserProfile.DoesNotExist:
               
                return self.form_invalid(form)          
       
         form.instance.location = userprofile
       
         return super().form_valid(form)


     def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
        return super().form_invalid(form)	   

class UpdateSexView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
      login_url = '/accounts/login/'
      redirect_field_name = 'redirect_to' 
      model=Sex
      template_name = 'sex/update-sex.html'
      form_class = CreateSexForm   
      success_url = reverse_lazy("sex-list")
      permission_required = 'cctv.change_sex'
      success_message = "The Sex was Added successfully."
      
      def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location
           
         except UserProfile.DoesNotExist:
             
                return self.form_invalid(form)          
       
         form.instance.location = userprofile
       
         return super().form_valid(form)


      def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
        return super().form_invalid(form)	   
    
class DeleteSexView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
       login_url = '/accounts/login/'
       redirect_field_name = 'redirect_to' 
       model=Sex
       context_object_name = 'sex'
       template_name='sex/confirm_delete.html'   
       success_url = reverse_lazy("sex-list")
       permission_required = 'cctv.delete_sex'    
  
      
       success_message = "The Sex was Deleted successfully."
       error_message = (
            "Cannot delete the Race '{name}' because it is related to other records: {details}."
              )
       

       def post(self, request, *args, **kwargs):
                self.object = self.get_object()  # Obtener el objeto a eliminar
              
                try:
                    # Intentar eliminar el objeto
                    self.object.delete()
                    messages.success(request, self.success_message)
                    return redirect(self.success_url)
                except ProtectedError as e:
                 
                    related_objects = ', '.join(str(obj) for obj in e.protected_objects)
                    
                    error_message = self.error_message.format(name=str(self.object), details=related_objects)
                    messages.error(request, error_message)
                    return redirect(self.success_url)


class DetailSexView(LoginRequiredMixin,PermissionRequiredMixin,DetailView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to' 
    model = Sex
    context_object_name = 'sex'
    template_name='sex/detail-sex.html'   
    success_url = reverse_lazy("sex-list")
    permission_required = 'cctv.view_sex'
          
#Sex----End
#Race----Begin 
class ListRaceView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
   login_url = '/accounts/login/'
   redirect_field_name = 'redirect_to' 
   template_name='race/list-race.html'
   model=Race
   permission_required = 'cctv.view_race'

   def dispatch(self, request, *args, **kwargs):
            if not hasattr(request.user, 'userprofile') and not self.request.user.is_superuser:
                messages.error(self.request, "No profile associated with the user was found")
                return redirect(self.login_url)
                
            return super().dispatch(request, *args, **kwargs)

   def get_queryset(self):
        qs=Race.objects.all()
        return qs
     
class CreateRaceView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,CreateView):
     login_url = '/accounts/login/'
     redirect_field_name = 'redirect_to' 
     model=Race
     template_name = 'race/create-race.html'
     form_class = CreateRaceForm    
     success_url = reverse_lazy("race-list")
     permission_required = 'cctv.add_race'
     success_message = "The Race was Added successfully."
      
     def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location
           
         except UserProfile.DoesNotExist:              
                return self.form_invalid(form)          
       
         form.instance.location = userprofile       
         return super().form_valid(form)


     def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
        return super().form_invalid(form)	   

class UpdateRaceView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
      login_url = '/accounts/login/'
      redirect_field_name = 'redirect_to' 
      model=Race
      template_name = 'race/update-race.html'
      form_class = CreateRaceForm   
      success_url = reverse_lazy("race-list")
      permission_required = 'cctv.change_race'
      success_message = "The Race was Updated successfully."
      
      def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location
           
         except UserProfile.DoesNotExist:              
                return self.form_invalid(form)          
       
         form.instance.location = userprofile       
         return super().form_valid(form)


      def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
        return super().form_invalid(form)	

class DetailRaceView(LoginRequiredMixin,PermissionRequiredMixin,DetailView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to' 
    model = Race
    context_object_name = 'race'
    template_name='race/detail-race.html'   
    success_url = reverse_lazy("race-list")
    permission_required = 'cctv.view_race'  
     #End Race

class DeleteRaceView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
       login_url = '/accounts/login/'
       redirect_field_name = 'redirect_to' 
       model=Race
       context_object_name = 'race'
       template_name='race/confirm_delete.html'   
       success_url = reverse_lazy("race-list")
       permission_required = 'cctv.delete_race'
       
      
       success_message = "The Race was Deleted successfully."
       error_message = (
            "Cannot delete the Race '{name}' because it is related to other records: {details}."
              )
       

       def post(self, request, *args, **kwargs):
                self.object = self.get_object()  # Obtener el objeto a eliminar
              
                try:
                    # Intentar eliminar el objeto
                    self.object.delete()
                    messages.success(request, self.success_message)
                    return redirect(self.success_url)
                except ProtectedError as e:
                 
                    related_objects = ', '.join(str(obj) for obj in e.protected_objects)
                    
                    error_message = self.error_message.format(name=str(self.object), details=related_objects)
                    messages.error(request, error_message)
                    return redirect(self.success_url)
#MAchine Begin
class ListMachineView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
   login_url = '/accounts/login/'
   redirect_field_name = 'redirect_to' 
   template_name='machine/list-machine.html'
   model=Slot_Machine
   permission_required = 'cctv.view_slot_machine'

   def dispatch(self, request, *args, **kwargs):
            if not hasattr(request.user, 'userprofile') and not self.request.user.is_superuser:
                messages.error(self.request, "No profile associated with the user was found")
                return redirect(self.login_url)
                
            return super().dispatch(request, *args, **kwargs)

   def get_queryset(self):
        qs=Slot_Machine.objects.all()
        return qs
     
class CreateMachineView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,CreateView):
     login_url = '/accounts/login/'
     redirect_field_name = 'redirect_to' 
     model=Slot_Machine
     template_name = 'machine/create-machine.html'
     form_class = CreateSlotMachineForm    
     success_url = reverse_lazy("machine-list")
     permission_required = 'cctv.add_slot_machine'
     success_message = "The Slot Machine was Added successfully."
      
     def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location
           
         except UserProfile.DoesNotExist:              
                return self.form_invalid(form)          
       
         form.instance.location = userprofile       
         return super().form_valid(form)


     def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
        return super().form_invalid(form)	   

class UpdateMachineView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
      login_url = '/accounts/login/'
      redirect_field_name = 'redirect_to' 
      model=Slot_Machine
      template_name = 'machine/update-machine.html'
      form_class = CreateSlotMachineForm   
      success_url = reverse_lazy("machine-list")
      permission_required = 'cctv.change_solot_machine'
      success_message = "The Slot Machine was Updated successfully."
      
      def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location
           
         except UserProfile.DoesNotExist:              
                return self.form_invalid(form)          
       
         form.instance.location = userprofile       
         return super().form_valid(form)


      def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
        return super().form_invalid(form)	

class DetailMachineView(LoginRequiredMixin,PermissionRequiredMixin,DetailView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to' 
    model = Slot_Machine
    context_object_name = 'machine'
    template_name='machine/detail-machine.html'   
    success_url = reverse_lazy("machine-list")
    permission_required = 'cctv.view_slot_machine'  
     #End Machine

class DeleteMachineView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
       login_url = '/accounts/login/'
       redirect_field_name = 'redirect_to' 
       model=Slot_Machine
       context_object_name = 'machine'
       template_name='machine/confirm_delete.html'   
       success_url = reverse_lazy("machine-list")
       permission_required = 'cctv.delete_slot_machine'
       
      
       success_message = "The Slot Machine was Deleted successfully."
       error_message = (
            "Cannot delete the Slot MAchine '{name}' because it is related to other records: {details}."
              )
       

       def post(self, request, *args, **kwargs):
                self.object = self.get_object()  # Obtener el objeto a eliminar
              
                try:
                    # Intentar eliminar el objeto
                    self.object.delete()
                    messages.success(request, self.success_message)
                    return redirect(self.success_url)
                except ProtectedError as e:
                 
                    related_objects = ', '.join(str(obj) for obj in e.protected_objects)
                    
                    error_message = self.error_message.format(name=str(self.object), details=related_objects)
                    messages.error(request, error_message)
                    return redirect(self.success_url)
 
 #Machine----End
#Reason------Begin
class ListReasonView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
   login_url = '/accounts/login/'
   redirect_field_name = 'redirect_to' 
   template_name='reason/list-reason.html'
   model=Reason
   permission_required = 'cctv.view_reason'

   def dispatch(self, request, *args, **kwargs):
            if not hasattr(request.user, 'userprofile') and not self.request.user.is_superuser:
                messages.error(self.request, "No profile associated with the user was found")
                return redirect(self.login_url)
                
            return super().dispatch(request, *args, **kwargs)
   

   def get_queryset(self):
        qs=Reason.objects.all()
        return qs
     
class CreateReasonView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,CreateView):
     login_url = '/accounts/login/'
     redirect_field_name = 'redirect_to' 
     model=Reason
     template_name = 'reason/create-reason.html'
     form_class = CreateReasonForm    
     success_url = reverse_lazy("reason-list")
     permission_required = 'cctv.add_reason'
     success_message = "The Race was Added successfully."
      
     def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location
           
         except UserProfile.DoesNotExist:               
                return self.form_invalid(form)          
       
         form.instance.location = userprofile
       
         return super().form_valid(form)
     def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
        return super().form_invalid(form)	   

class UpdateReasonView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
      login_url = '/accounts/login/'
      redirect_field_name = 'redirect_to' 
      model=Reason
      template_name = 'reason/update-reason.html'
      form_class = CreateReasonForm   
      success_url = reverse_lazy("reason-list")
      permission_required = 'cctv.change_reason'
      success_message = "The Reason was Updated successfully."
      
      def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location           
         except UserProfile.DoesNotExist:
               return self.form_invalid(form)          
       
         form.instance.location = userprofile       
         return super().form_valid(form)


      def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
        return super().form_invalid(form)	   

class DeleteReasonView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
       
       login_url = '/accounts/login/'
       redirect_field_name = 'redirect_to' 
       model=Reason
       context_object_name = 'reason'
       template_name='reason/confirm_delete.html'   
       success_url = reverse_lazy("reason-list")
       permission_required = 'cctv.delete_reason'
       success_message = "The Reason was Updated successfully."
      
       def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location           
         except UserProfile.DoesNotExist:
               return self.form_invalid(form)          
       
         
         return super().form_valid(form)


       def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
        return super().form_invalid(form)	 

class DetailReasonView(LoginRequiredMixin,PermissionRequiredMixin,DetailView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to' 
    model = Reason
    context_object_name = 'reason'
    template_name='reason/detail-reason.html'   
    success_url = reverse_lazy("reason-list")
    permission_required = 'cctv.view_reason'    


#Reason------End
#Duration --Begin
class ListDurationView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
   login_url = '/accounts/login/'
   redirect_field_name = 'redirect_to' 
   template_name='duration/list-duration.html'
   model=Duration
   permission_required = 'cctv.view_duration'

   def dispatch(self, request, *args, **kwargs):
            if not hasattr(request.user, 'userprofile') and not self.request.user.is_superuser:
                messages.error(self.request, "No profile associated with the user was found")
                return redirect(self.login_url)
                
            return super().dispatch(request, *args, **kwargs)

   def get_queryset(self):
        qs=Duration.objects.all()
        return qs
     
class CreateDurationView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,CreateView):
     login_url = '/accounts/login/'
     redirect_field_name = 'redirect_to' 
     model=Duration
     template_name = 'duration/create-duration.html'
     form_class = CreateDurationForm    
     success_url = reverse_lazy("duration-list")
     permission_required = 'cctv.add_duration'
     success_message = "The Duration was Added successfully."
      
     def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location
           
         except UserProfile.DoesNotExist:
               
                return self.form_invalid(form)          
         form.instance.location = userprofile
         return super().form_valid(form)


     def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
        return super().form_invalid(form)	   

class UpdateDurationView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
      login_url = '/accounts/login/'
      redirect_field_name = 'redirect_to' 
      model=Duration
      template_name = 'duration/update-duration.html'
      form_class = CreateDurationForm   
      success_url = reverse_lazy("duration-list")
      permission_required = 'cctv.change_duration'
      success_message = "The Duration was Updated successfully."
      
      def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location           
         except UserProfile.DoesNotExist:
               return self.form_invalid(form)          
       
         form.instance.location = userprofile       
         return super().form_valid(form)


      def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
        return super().form_invalid(form)	   
   
class DeleteDurationView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
       login_url = '/accounts/login/'
       redirect_field_name = 'redirect_to' 
       model=Duration
       context_object_name = 'duration'
       template_name='duration/confirm_delete.html'   
       success_url = reverse_lazy("duration-list")
       permission_required = 'cctv.delete_duration'    
       success_message = "The Duration was Deleted successfully."
      
       def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location           
         except UserProfile.DoesNotExist:
               
                return self.form_invalid(form)              
             
         return super().form_valid(form)


       def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
        return super().form_invalid(form)	

class DetailDurationView(LoginRequiredMixin,PermissionRequiredMixin,DetailView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to' 
    model = Duration
    context_object_name = 'duration'
    template_name='duration/detail-duration.html'   
    success_url = reverse_lazy("duration-list")
    permission_required = 'cctv.view_duration'    
 #Duration --Begin       

#CD Error Type----End
class ListCDErrorTypeView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
   login_url = '/accounts/login/'
   redirect_field_name = 'redirect_to' 
   template_name='cash_desk_error_type/list-cash_desk_error_type.html'
   model=CDErrorType
   permission_required = 'cctv.view_cderrortype'


   def dispatch(self, request, *args, **kwargs):
            if not hasattr(request.user, 'userprofile') and not self.request.user.is_superuser:
                messages.error(self.request, "No profile associated with the user was found")
                return redirect(self.login_url)
                
            return super().dispatch(request, *args, **kwargs)

   def get_queryset(self):
        qs=CDErrorType.objects.all()
        return qs
     
class CreateCDErrorTypeView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,CreateView):
     login_url = '/accounts/login/'
     redirect_field_name = 'redirect_to' 
     model=CDErrorType
     template_name = 'cash_desk_error_type/create-cash_desk_error_type.html'
     form_class = CreateCDErrorTypeForm    
     success_url = reverse_lazy("cash_desk_error_type-list")  
     permission_required = 'cctv.add_cderrortype'  
     success_message = "The Cash Desk Error Type was Added successfully."
      
     def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location
           
         except UserProfile.DoesNotExist:                
                return self.form_invalid(form)          
       
         form.instance.location = userprofile       
         return super().form_valid(form)


     def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
        return super().form_invalid(form)	   
  
class UpdateCDErrorTypeView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
      login_url = '/accounts/login/'
      redirect_field_name = 'redirect_to' 
      model=CDErrorType
      template_name = 'cash_desk_error_type/update-cash_desk_error_type.html'
      form_class = CreateCDErrorTypeForm   
      success_url = reverse_lazy("cash_desk_error_type-list") 
      permission_required = 'cctv.change_cderrortype'
      success_message = "The Cash Desk Error Type was Updated successfully."
      
      def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location
           
         except UserProfile.DoesNotExist:                
                return self.form_invalid(form)  
       
         form.instance.location = userprofile       
         return super().form_valid(form)


      def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
        return super().form_invalid(form)	   
  
class DeleteCDErrorTypeView(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
       login_url = '/accounts/login/'
       redirect_field_name = 'redirect_to' 
       model=CDErrorType
       context_object_name = 'cash_desk_error_type'
       template_name='cash_desk_error_type/confirm_delete.html'   
       success_url = reverse_lazy("cash_desk_error_type-list")
       permission_required = 'cctv.delete_cderrortype'
       success_message = "The Cash Desk Error Type was Deleted successfully."
      
       def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location
           
         except UserProfile.DoesNotExist:                
                return self.form_invalid(form)  
       
         form.instance.location = userprofile
       
         return super().form_valid(form)


       def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
        return super().form_invalid(form)	

class DetailCDErrorTypeView(LoginRequiredMixin,PermissionRequiredMixin,DetailView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to' 
    model = CDErrorType
    context_object_name = 'cash_desk_error_type'
    template_name='cash_desk_error_type/detail-cash_desk_error_type.html'   
    success_url = reverse_lazy("cash_desk_error_type-list")
    permission_required = 'cctv.view_cderrortype'    
         
 #CD Error Type----End 

#CD Exeption Type-----Begin
class ListCDExeptionTypeView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
   login_url = '/accounts/login/'
   redirect_field_name = 'redirect_to' 
   template_name='exeption_type/list-cash_desk_exeption_type.html'
   model=ExceptionType
   permission_required = 'cctv.view_exceptiontype'

   def dispatch(self, request, *args, **kwargs):
            if not hasattr(request.user, 'userprofile') and not self.request.user.is_superuser:
                messages.error(self.request, "No profile associated with the user was found")
                return redirect(self.login_url)                
            return super().dispatch(request, *args, **kwargs)
   

   def get_queryset(self):
        qs=ExceptionType.objects.all()
        return qs
     
class CreateCDExeptionTypeView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,CreateView):
     login_url = '/accounts/login/'
     redirect_field_name = 'redirect_to' 
     model=ExceptionType
     template_name = 'exeption_type/create-cash_desk_exeption_type.html'
     form_class = CreateCDExeptionTypeForm    
     success_url = reverse_lazy("cash_desk_exeption_type-list") 
     permission_required = 'cctv.add_exceptiontype'    
     success_message = "The Cash Desk Exeption Type was Added successfully."
      
     def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location
           
         except UserProfile.DoesNotExist:              
                return self.form_invalid(form)          
       
         form.instance.location = userprofile       
         return super().form_valid(form)


     def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
        return super().form_invalid(form)	   

class UpdateCDExeptionTypeView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
      login_url = '/accounts/login/'
      redirect_field_name = 'redirect_to' 
      model=ExceptionType
      template_name = 'exeption_type/update-cash_desk_exeption_type.html'
      form_class = CreateCDExeptionTypeForm   
      success_url = reverse_lazy("cash_desk_exeption_type-list")    
      permission_required = 'cctv.change_exceptiontype'
      success_message = "The Cash Desk Exeption Type was Updated successfully."

      def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location           
         except UserProfile.DoesNotExist:              
                return self.form_invalid(form)          
       
         form.instance.location = userprofile       
         return super().form_valid(form)


      def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
        return super().form_invalid(form)	   

class DeleteCDExeptionTypeView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
       login_url = '/accounts/login/'
       redirect_field_name = 'redirect_to' 
       model=ExceptionType
       context_object_name = 'exeption_type'
       template_name='exeption_type/confirm_delete.html'   
       success_url = reverse_lazy("cash_desk_exeption_type-list")
       permission_required = 'cctv.delete_exceptiontype'   
       success_message = "The Cash Desk Exeption Type was Deleted successfully."

       
       error_message = (
            "Cannot delete the Cash Desk Exeption Type '{name}' because it is related to other records: {details}."
              )
       

       def post(self, request, *args, **kwargs):
                self.object = self.get_object()  # Obtener el objeto a eliminar
              
                try:
                    # Intentar eliminar el objeto
                    self.object.delete()
                    messages.success(request, self.success_message)
                    return redirect(self.success_url)
                except ProtectedError as e:
                 
                    related_objects = ', '.join(str(obj) for obj in e.protected_objects)
                    
                    error_message = self.error_message.format(name=str(self.object), details=related_objects)
                    messages.error(request, error_message)
                    return redirect(self.success_url)
       
class DetailCDExeptionTypeView(LoginRequiredMixin,PermissionRequiredMixin,DetailView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to' 
    model = ExceptionType
    context_object_name = 'exeption_type'
    template_name='exeption_type/detail-exeption_type.html'   
    success_url = reverse_lazy("exeption_type-list")
    permission_required = 'cctv.view_exceptiontype'    
         
#CD Exeption Type-----End   
# ****************************************************************************************************************    
#Poker Combination -- Begin
class ListPokerCombinationView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
   template_name='poker_combination/list-poker_combination.html'
   model=PokerCombination
   permission_required = 'cctv.view_pokercombination'

   def dispatch(self, request, *args, **kwargs):
            if not hasattr(request.user, 'userprofile') and not self.request.user.is_superuser:
                messages.error(self.request, "No profile associated with the user was found")
                return redirect(self.login_url)
                
            return super().dispatch(request, *args, **kwargs)

   def get_queryset(self):
        qs=PokerCombination.objects.all()
        return qs
     
class CreatePokerCombinationView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,CreateView):
     login_url = '/accounts/login/'
     redirect_field_name = 'redirect_to' 
     model=PokerCombination
     template_name = 'poker_combination/create-poker_combination.html'
     form_class = CreatePokerCombinationForm    
     success_url = reverse_lazy("poker_combination-list") 
     permission_required = 'cctv.add_pokercombination' 
     success_message = "The Poker Combination was Added successfully."
      
     def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location           
         except UserProfile.DoesNotExist:
                messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
                return self.form_invalid(form)     
       
         form.instance.location = userprofile       
         return super().form_valid(form)


     def form_invalid(self, form):
        messages.error(self.request, "There was an error submitting the form.")
        return super().form_invalid(form)	   

class UpdatePokerCombinationView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
      login_url = '/accounts/login/'
      redirect_field_name = 'redirect_to' 
      model=PokerCombination
      template_name = 'poker_combination/update-poker_combination.html'
      form_class = CreatePokerCombinationForm   
      success_url = reverse_lazy("poker_combination-list")  
      permission_required = 'cctv.add_pokercombination'
      success_message = "The Poker Combination was Updated successfully."  

      def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location           
         except UserProfile.DoesNotExist:              
                return self.form_invalid(form)        
         form.instance.location = userprofile      
         return super().form_valid(form)


      def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
        return super().form_invalid(form)	 

class DeletePokerCombinationView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
       login_url = '/accounts/login/'
       redirect_field_name = 'redirect_to' 
       model=PokerCombination
       context_object_name = 'poker_combination'
       template_name='poker_combination/confirm_delete.html'   
       success_url = reverse_lazy("poker_combination-list")
       permission_required = 'cctv.delete_pokercombination'
       
    
       success_message = "The Poker Combination was Deleted successfully." 
       error_message = (
            "Cannot delete the Poker Table'{name}' because it is related to other records: {details}."
              )
       

       def post(self, request, *args, **kwargs):
                self.object = self.get_object()  # Obtener el objeto a eliminar
              
                try:
                    # Intentar eliminar el objeto
                    self.object.delete()
                    messages.success(request, self.success_message)
                    return redirect(self.success_url)
                except ProtectedError as e:
                 
                    related_objects = ', '.join(str(obj) for obj in e.protected_objects)
                    
                    error_message = self.error_message.format(name=str(self.object), details=related_objects)
                    messages.error(request, error_message)
                    return redirect(self.success_url)
class DetailPoker_CombinationView(LoginRequiredMixin,PermissionRequiredMixin,DetailView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to' 
    model = PokerCombination
    context_object_name = 'poker_combination'
    template_name='poker_combination/detail-poker_combination.html'   
    success_url = reverse_lazy("poker_combination-list")
    permission_required = 'cctv.view_pokercombination'    
         
 #CD Error Type----End 
#Poker Combination -- End

#Poker Table ------Begin
class ListPokerTableView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
   login_url = '/accounts/login/'
   redirect_field_name = 'redirect_to' 
   template_name='poker_table/list-poker_table.html'
   model=PokerTable
   permission_required = 'cctv.view_pokertable'


   def dispatch(self, request, *args, **kwargs):
            if not hasattr(request.user, 'userprofile') and not self.request.user.is_superuser:
                messages.error(self.request, "No profile associated with the user was found")
                return redirect(self.login_url)
                
            return super().dispatch(request, *args, **kwargs)

   def get_queryset(self):
        qs=PokerTable.objects.all()
        return qs
     
class CreatePokerTableView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,CreateView):
     login_url = '/accounts/login/'
     redirect_field_name = 'redirect_to' 
     model=PokerTable
     template_name = 'poker_table/create-poker_table.html'
     form_class = CreatePokerTableForm    
     success_url = reverse_lazy("poker_table-list")  
     permission_required = 'cctv.add_pokertable'  
     success_message = "The Poker Table was Added successfully."
      
     def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location
           
         except UserProfile.DoesNotExist:               
                return self.form_invalid(form)          
       
         form.instance.location = userprofile
         messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
         return super().form_valid(form)


     def form_invalid(self, form):
        messages.error(self.request, "There was an error submitting the form.")
        return super().form_invalid(form)	   
  
class UpdatePokerTableView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
      login_url = '/accounts/login/'
      redirect_field_name = 'redirect_to' 
      model=PokerTable
      template_name = 'poker_table/update-poker_table.html'
      form_class = CreatePokerTableForm   
      success_url = reverse_lazy("poker_table-list") 
      permission_required = 'cctv.change_pokertable'
      success_message = "The Poker Table was Updated successfully."   

      def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location           
         except UserProfile.DoesNotExist:                
                return self.form_invalid(form)          
       
         form.instance.location = userprofile       
         return super().form_valid(form)


      def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
        return super().form_invalid(form)	    

class DeletePokerTableView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
       login_url = '/accounts/login/'
       redirect_field_name = 'redirect_to' 
       model=PokerTable
       context_object_name = 'poker_table'
       template_name='poker_table/confirm_delete.html'   
       success_url = reverse_lazy("poker_table-list")
       permission_required = 'cctv.delete_pokertable'

       success_message = "The Poker Table was Deleted successfully."     
       error_message = (
            "Cannot delete the Poker Table'{name}' because it is related to other records: {details}."
              )
       

       def post(self, request, *args, **kwargs):
                self.object = self.get_object()  # Obtener el objeto a eliminar
              
                try:
                    # Intentar eliminar el objeto
                    self.object.delete()
                    messages.success(request, self.success_message)
                    return redirect(self.success_url)
                except ProtectedError as e:
                 
                    related_objects = ', '.join(str(obj) for obj in e.protected_objects)
                    
                    error_message = self.error_message.format(name=str(self.object), details=related_objects)
                    messages.error(request, error_message)
                    return redirect(self.success_url)
       
class DetailPokerTableView(LoginRequiredMixin,PermissionRequiredMixin,DetailView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to' 
    model = PokerTable
    context_object_name = 'poker_table'
    template_name='poker_table/detail-poker_table.html'   
    success_url = reverse_lazy("poker_table-list")
    permission_required = 'cctv.view_pokertable'    
#Poker Table ------End    

#DailyReport-----Begin

class ListReportView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
     login_url = '/accounts/login/'
     redirect_field_name = 'redirect_to' 
     template_name='report_main/list-report_main.html'
     model=Report
     permission_required = 'cctv.view_report'
     

     def dispatch(self, request, *args, **kwargs):
            if not hasattr(request.user, 'userprofile') and not self.request.user.is_superuser:
                messages.error(self.request, "No profile associated with the user was found")
                return redirect(self.login_url)
                
            return super().dispatch(request, *args, **kwargs)
     
     #def get_queryset(self):
      #  if self.request.user.is_superuser:
       #     qs=Report.objects.all()                
       # else:
        #    qs=Report.objects.filter(location=self.request.user.userprofile.location).order_by('-report')     
        
       # return qs
    
     def get_queryset(self):        
        if self.request.user.is_superuser:
            queryset=self.model.objects.all()                
        else:
            queryset=self.model.objects.filter(location=self.request.user.userprofile.location).order_by('-report')   

        search_value=self.request.GET.get('search[value]','').strip()
        if search_value:
           
            queryset=queryset.annotate(
                duty_manager_fullname=Trim(
                    Concat(
                        Coalesce(F('duty_manager__name'),Value('')),
                                                  Value(' '),
                                                  Coalesce(F('duty_manager__surname'), Value('')),
                                                  output_field=CharField()
                                                  )
                                          )
                                        )
          
            queryset=queryset.annotate(
                        pittboss_fullname=Trim(
                            Concat(
                                Coalesce(F('pittboss__name'),Value('')),
                                Value(' '),
                                Coalesce(F('pittboss__surname'), Value('')),
                                output_field=CharField()
                            )
                            
                        )   

                        )
            queryset=queryset.annotate(
                inspector_fullname=Trim(
                    Concat(
                        Coalesce(F('inspector__name'), Value('')),
                        Value(' '),
                        Coalesce(F('inspector__surname'), Value('')),
                        output_field=CharField()

                    )

                )
            )
            
            queryset=queryset.filter(
                Q(report_nro__icontains=search_value) |                  
                Q(date__icontains=search_value)|
                Q(time__icontains=search_value)|
                Q(report_type__report_type__icontains=search_value)|
                Q(report_title__title__icontains=search_value)|
                Q(area__area__icontains=search_value)|
                Q(origination__origination__icontains=search_value)|
                Q(duty_manager_fullname__icontains=search_value)|
                Q(pittboss_fullname__icontains=search_value)|
                Q(inspector_fullname__icontains=search_value)|
                Q(location__location__icontains=search_value)  
            ) 

        order_column_index = self.request.GET.get('order[0][column]', '0')
        order_dir = self.request.GET.get('order[0][dir]', 'asc')        

        column_map = {
            '0': 'report_nro',
            '1':'date',
            '2': 'time',  
            '3': 'report_type__report_type',  
            '4': 'report_title__title',  
            '5': 'area__area',  
            '6': 'origination__origination',
            '7': 'duty_manager__name',
            '8': 'pittboss__name',
            '9': 'inspector__name',           
            '10':'location__location'
        }


        order_field = column_map.get(order_column_index, 'report')
        if order_dir == 'desc':
            order_field = f"-{order_field}"

        queryset = queryset.order_by(order_field)     
       
        return queryset
    
     def render_to_response(self, context, **response_kwargs):
      
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            draw = int(self.request.GET.get('draw', 1))
            start = int(self.request.GET.get('start', 0))
         
           
            length = int(self.request.GET.get('length', 10))
          
            queryset = self.get_queryset()
            
           
            total_records = Report.objects.count()
            
            filtered_records = queryset.count()
            

            report = queryset[start:start+length]

            data = [{
                "report_nro": report.report_nro,            
                "date": report.date,
                "time": str(report.time),
                "report_type": str(report.report_type.report_type) if report.report_type else "",
                "report_title": str(report.report_title.title) if report.report_title else "",
                "area": str(report.area.area) if report.area else "",
                "origination": str(report.origination.origination) if report.origination else "",
                "duty_manager":str( report.duty_manager) if report.duty_manager else "",
                "pittboss": str(report.pittboss) if report.pittboss else "",
                "inspector": str(report.inspector) if report.inspector else "",                            
                "location": str(report.location) if report.location else "",
                "dubbed_to":report.dubbed_to,
                "detail_url": report.get_absolute_url(),
                "edit_url": report.get_edit_url(),
                "delete_url":report.get_delete_url(),
                "view_video":report.get_report_video(),
            } for report in report]

            return JsonResponse({
                "draw": draw,
                "recordsTotal": total_records,
                "recordsFiltered": filtered_records,
                "data": data,
            })
       

        return super().render_to_response(context, **response_kwargs)
     
   
      
class CreateReportView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,CreateView):
     login_url = '/accounts/login/'
     redirect_field_name = 'redirect_to' 
     model=Report
     template_name = 'report_main/create-report_main.html'
     form_class = CreateReportForm    
     success_url = reverse_lazy("report-list") 
     permission_required = 'cctv.add_report'
     success_message = "The Daily Report was Added successfully."

     def get_initial(self):      
        initial = super().get_initial()
        initial['date'] = datetime.datetime.now()
        initial['time'] = datetime.datetime.now()
        initial['usd_rate'] = 7.50  
        initial['euro_rate'] = 7.75  
        initial['gbp_rate'] = 8.50
      
        if self.request.user.is_superuser:
            initial['location_id']=None
        else:
            initial['location_id'] = self.request.user.userprofile.location_id   
        
        return initial
      
     def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location  
                   
         except UserProfile.DoesNotExist:               
                return self.form_invalid(form)          
             
         if 'save_and_continue' in self.request.POST:
             form.instance.location = userprofile or self.get_initial().get('location_id')
            
             form.save()
             messages.success(self.request, "The Report  was Added successfully.You can continue adding!")
             return redirect('report-create')  
        
         form.instance.location = userprofile
         return super().form_valid(form)


     def form_invalid(self, form):
       
        messages.error(self.request, "An error has occurred.Contact the administrator.")
        return super().form_invalid(form)	  
      
class UpdateReportView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
      login_url = '/accounts/login/'
      redirect_field_name = 'redirect_to' 
      model=Report
      template_name = 'report_main/update-report_main.html'
      form_class = CreateReportForm   
      success_url = reverse_lazy("report-list") 
      permission_required = 'cctv.change_report'
      success_message = "The Daily Report was Updated successfully."
      
      def get_initial(self):      
        initial = super().get_initial()        
        if self.request.user.is_superuser:
            initial['location_id']=None
        else:
            initial['location_id'] = self.request.user.userprofile.location_id         
       
       
        return initial
      def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location
           
         except UserProfile.DoesNotExist:               
                return self.form_invalid(form)          
       
         form.instance.location = userprofile       
         return super().form_valid(form)


      def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
        return super().form_invalid(form)	    

class DeleteReportView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
       login_url = '/accounts/login/'
       redirect_field_name = 'redirect_to' 
       model=Report
       context_object_name = 'report'
       template_name='report_main/confirm_delete.html'   
       success_url = reverse_lazy("report-list")
       permission_required = 'cctv.delete_report'    
       success_message = "The Daily Report was Deleted successfully."

       def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location
           
         except UserProfile.DoesNotExist:
               
                return self.form_invalid(form)          
       
    
       
         return super().form_valid(form)


       def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
        return super().form_invalid(form)	   
       
class DetailReportView(LoginRequiredMixin,PermissionRequiredMixin,DetailView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to' 
    model = Report
    context_object_name = 'report'
    template_name='report_main/detail-report_main.html'   
    success_url = reverse_lazy("report-list")
    permission_required = 'cctv.view_report'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        report = self.get_object()  # Obtener el objeto Report actual
        context['videos'] = ReportVideo.objects.filter(report_id=report)
        return context

@login_required
def FilterReportView(request):
    if request.user.is_superuser:
         report=Report.objects.all()
         user_location=''
    else:
        report=Report.objects.filter(location=request.user.userprofile.location)
        user_location=request.user.userprofile.location 
            
    form=FilterReport(request.GET or None,  initial={'location': user_location})
    if form.is_valid():             
             date_begin = form.cleaned_data.get('date_begin')      
             date_end = form.cleaned_data.get('date_end')        
             if date_begin and date_end :        
                 report=report.filter(date__range=(date_begin, date_end))    
    return render(request, 'report_main/filter_report_select.html', {'form': form, 'report': report})

@login_required
def FilterReportByIdView(request):
    
    if request.user.is_superuser:
         report=Report.objects.all()
      
    else:       
        report=Report.objects.filter(location=request.user.userprofile.location)

    form=FilterReportById(request.GET)
    if form.is_valid():
             report_id = form.cleaned_data.get('report_id')
             
             if report_id :
                 report=report.filter(report_nro__iexact=report_id)   
    return render(request, 'report_main/filter_by_id.html', {'form': form, 'report': report})
    
@login_required
def FilterReportByTypeView(request):
     if request.user.is_superuser:
         report=Report.objects.all()
     else:
        report=Report.objects.filter(location=request.user.userprofile.location)       
       
     form=FilterReportByType(request.GET)

     if form.is_valid():
        report_type = form.cleaned_data.get('report_type')
        
        if report_type :        
          report=report.filter(report_type__exact=report_type)
    
     return render(request, 'report_main/filter_by_type.html', {'form': form, 'report': report})
 
#DailyReport-----End
#ReportVideo----Begin

class ReportVideoListView(ListView):
    model = ReportVideo
    template_name = "video/reportvideo_list.html"
    context_object_name = "videos"

    def get_queryset(self):
        report_id = self.kwargs.get("report_id")
        return ReportVideo.objects.filter(report_id__pk=report_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['report_id'] = self.kwargs.get("report_id")
       
        return context

class ReportVideoCreateView(CreateView):
    model = ReportVideo
    form_class = ReportVideoForm
    template_name = "video/reportvideo_form.html"

    def get_form_kwargs(self):
       
        kwargs = super().get_form_kwargs()
        report_id = self.kwargs.get('report_id') 
       
        kwargs['initial'] = {'report': report_id} 
        kwargs['report_id'] = report_id 
        return kwargs

    def get_success_url(self):
        if 'save_and_continue' in self.request.POST:
            # Redirige a la misma página para continuar editando
            return reverse_lazy('reportvideo_add', kwargs={'report_id': self.object.report.pk})
        # Redirige a la lista de videos del reporte
        return reverse_lazy('reportvideo_list', kwargs={'report_id': self.object.report.pk})
   
    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['report_id'] = self.kwargs.get('report_id')  # Obtiene el report_id de la URL
       return context
   
class MultiVideoUploadView(View):
    template_name = "video/multivideo_upload.html"

    def get(self, request, *args, **kwargs):
        form = MultiVideoUploadForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = MultiVideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.cleaned_data['report']
            video_files = request.FILES.getlist('video_files')
            for video in video_files:
                ReportVideo.objects.create(report=report, video_file=video)
            return redirect('reportvideo_list', report_id=report.pk)
        return render(request, self.template_name, {'form': form})
class ReportVideoUpdateView(UpdateView):
    model = ReportVideo
    form_class = ReportVideoForm
    template_name = "video/reportvideo_update.html"

  

    def get_success_url(self):
        return reverse_lazy('reportvideo_list', kwargs={'report_id': self.object.report.pk}) 
    
class ReportVideoDeleteView(DeleteView):
    model = ReportVideo
    template_name = "video/video_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy('reportvideo_list', kwargs={'report_id': self.object.report.pk}) 

@login_required 
def download_video(request, video_id):
    video = get_object_or_404(ReportVideo, id=video_id)

    # Obtener el archivo de video
    if video.video_file:
        try:
            response = FileResponse(video.video_file.open('rb'), as_attachment=True)
            response['Content-Disposition'] = f'attachment; filename="{video.video_file.name}"'
            return response
        except FileNotFoundError:
            raise Http404("File not found.")
    else:
        raise Http404("No file to download.")
   

#ReportVideo-----End
#DailyShift Report-----Begin

class ListDailyShiftView(LoginRequiredMixin,PermissionRequiredMixin,ListView):  
     login_url = '/accounts/login/'
     redirect_field_name = 'redirect_to' 
     template_name='daily_shift/list-daily_shift.html'
     model=DailyShift   
     permission_required = 'cctv.view_dailyshift'

     def dispatch(self, request, *args, **kwargs):
            if not hasattr(request.user, 'userprofile') and not self.request.user.is_superuser:
                messages.error(self.request, "No profile associated with the user was found")
                return redirect(self.login_url)
                
            return super().dispatch(request, *args, **kwargs)

   
    # def get_queryset(self):        
     #   if self.request.user.is_superuser:
       #     qs=DailyShift.objects.all()                
      #  else:
        
      #      qs=DailyShift.objects.filter(location=self.request.user.userprofile.location)
         
       # return qs
     def get_queryset(self):        
        if self.request.user.is_superuser:
            queryset=self.model.objects.all()  
                       
        else:        
            queryset=self.model.objects.filter(location=self.request.user.userprofile.location)
        
           

        search_value=self.request.GET.get('search[value]', '').strip()

        if search_value:
            queryset = queryset.annotate(
                supervisor_fullname=Trim(Concat(
                    Coalesce(F('supervisor__name'), Value('')), 
                    Value(' '), 
                    Coalesce(F('supervisor__surname'), Value('')),
                    output_field=CharField()
                ))
                )
            queryset = queryset.annotate(
                officer1_fullname=Trim(Concat(
                    Coalesce(F('officer1__name'), Value('')), 
                    Value(' '), 
                    Coalesce(F('officer1__surname'), Value('')),
                    output_field=CharField()
                ))
            )
            queryset = queryset.annotate(
                officer2_fullname=Trim(Concat(
                    Coalesce(F('officer2__name'), Value('')), 
                    Value(' '), 
                    Coalesce(F('officer2__surname'), Value('')),
                    output_field=CharField()
                ))
            )
            queryset = queryset.filter(
                    Q(id__icontains=search_value) |
                    Q(date__icontains=search_value) |
                    Q(location__location__icontains=search_value)|
                    Q(shift__shift__icontains=search_value) |
                    Q(supervisor_fullname__icontains=search_value) |
                    Q(officer1_fullname__icontains=search_value) |
                    Q(officer2_fullname__icontains=search_value) |             
                    Q(usd_rate__icontains=search_value) |
                    Q(euro_rate__icontains=search_value) |
                    Q(gbp_rate__icontains=search_value) |
                    Q(casino_open__icontains=search_value) |
                    Q(casino_close__icontains=search_value) 
                    
                )
       

        order_column_index = self.request.GET.get('order[0][column]', '0')
        order_dir = self.request.GET.get('order[0][dir]', 'asc')

        column_map = {
            '0': 'id',
            '1': 'date', 
            '2': 'shift__shift',  
            '3': 'supervisor',  
            '4': 'officer1', 
            '5':'officer2',
            '6':'casino_open',
            '7':'casino_close',
            '8':'usd_rate',
            '9':'euro_rate',
            '10':'gbp_rate',
            '11': 'location__location',  

        }

        order_field = column_map.get(order_column_index, 'id')
    
        if order_dir == 'desc':
    
            order_field = f"-{order_field}"

        queryset = queryset.order_by(order_field)
        

        return queryset


     def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            draw = int(self.request.GET.get('draw', 1))
            start = int(self.request.GET.get('start', 0))
            length = int(self.request.GET.get('length', 10))

            queryset = self.get_queryset()
           
            total_records = DailyShift.objects.count()
            filtered_records = queryset.count()

            dailyshift = queryset[start:start+length]

            data = [{
                "id": dailyshift.id,            
                "date": dailyshift.date,
                "shift": str(dailyshift.shift),
                "supervisor": str(dailyshift.supervisor) if dailyshift.supervisor else "",
                "officer1": str(dailyshift.officer1) if dailyshift.officer1 else "",
                "officer2": str(dailyshift.officer2) if dailyshift.officer2 else "",
                "usd_rate": dailyshift.usd_rate if dailyshift.usd_rate else "0.0",
                "euro_rate": dailyshift.euro_rate if dailyshift.euro_rate else "0.0",
                "gbp_rate": dailyshift.gbp_rate if dailyshift.gbp_rate else "0.0",
                "casino_open": str(dailyshift.casino_open) if dailyshift.casino_open else "",
                "casino_close":str(dailyshift.casino_close) if dailyshift.casino_close else "",                   
                "location": str(dailyshift.location) if dailyshift.location else "",
                "detail_url": dailyshift.get_absolute_url(),
                "edit_url": dailyshift.get_edit_url(),
                "delete_url":dailyshift.get_delete_url(),
            } for dailyshift in dailyshift]

            return JsonResponse({
                "draw": draw,
                "recordsTotal": total_records,
                "recordsFiltered": filtered_records,
                "data": data,
            })

        return super().render_to_response(context, **response_kwargs)
     
class CreateDailyShiftView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,CreateView):
     login_url = '/accounts/login/'
     redirect_field_name = 'redirect_to' 
     model=DailyShift
     template_name = 'daily_shift/create-daily_shift.html'
     form_class = CreateDailyShiftForm    
     success_url = reverse_lazy("daily_shift-list") 
     permission_required = 'cctv.add_dailyshift' 
     success_message = "The Daily Shift  was Added successfully."
    
     def get_initial(self):      
        initial = super().get_initial()
        initial['date'] = datetime.datetime.now()
        initial['usd_rate'] = 7.50  
        initial['euro_rate'] = 7.75  
        initial['gbp_rate'] = 8.50  
        initial['casino_open'] =  '10:00' 
        initial['casino_close'] =  '04:00'         
        if self.request.user.is_superuser:
            initial['location_id']=None
        else:
            initial['location_id'] = self.request.user.userprofile.location_id     
        
        return initial
      
     def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location           
         except UserProfile.DoesNotExist:               
                return self.form_invalid(form)   
         
         if 'save_and_continue' in self.request.POST:
             form.instance.location = userprofile or self.get_initial().get('location_id')
             form.save()
             messages.success(self.request, "The Daily Shift  was Added successfully.You can continue adding!")
             return redirect('daily_shift-create')  
 
         form.instance.location = userprofile
         return super().form_valid(form)

     def form_invalid(self, form):
        messages.error(self.request, "There was an error submitting the form.")
        return super().form_invalid(form)	   
 
class UpdateDailyShiftView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
      login_url = '/accounts/login/'
      redirect_field_name = 'redirect_to' 
      model=DailyShift
      template_name = 'daily_shift/update-daily_shift.html'
      form_class = CreateDailyShiftForm   
      success_url = reverse_lazy("daily_shift-list") 
      permission_required = 'cctv.change_dailyshift'
      success_message = "The Daily Shift  was Updated successfully." 
     
      def get_initial(self):      
        initial = super().get_initial()        
        if self.request.user.is_superuser:
            initial['location_id']=None
        else:
            initial['location_id'] = self.request.user.userprofile.location_id        
        return initial
      
      def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location           
         except UserProfile.DoesNotExist:               
                return self.form_invalid(form)            
         form.instance.location = userprofile
       
         return super().form_valid(form)


      def form_invalid(self, form):
           
           messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
           return super().form_invalid(form)	   
     
  
class DeleteDailyShiftView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
       login_url = '/accounts/login/'
       redirect_field_name = 'redirect_to' 
       model=DailyShift
       context_object_name = 'shift'
       template_name='daily_shift/confirm_delete.html'   
       success_url = reverse_lazy("daily_shift-list")
       permission_required = 'cctv.delete_dailyshift'
       success_message = "The Daily Shift  was Delete successfully."  

       def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location
           
         except UserProfile.DoesNotExist:               
                return self.form_invalid(form)         
       
           
         return super().form_valid(form)


       def form_invalid(self, form):           
           messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
           return super().form_invalid(form)	       
   
class DetailDailyShiftView(LoginRequiredMixin,PermissionRequiredMixin,DetailView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to' 
    model = DailyShift
    context_object_name = 'daily_shift'
    template_name='daily_shift/detail-daily_shift.html'   
    success_url = reverse_lazy("daily_shift-list")
    permission_required = 'cctv.view_dailyshift' 

   
 
@login_required
def FilterDailyShiftByDateView(request):
     
     if request.user.is_superuser:
         dailyshift=DailyShift.objects.all()
     else:
        dailyshift=DailyShift.objects.filter(location=request.user.userprofile.location)
        
     
     form=FilterDailyShiftByDate(request.GET)   
     if form.is_valid(): 
        
        date_begin = form.cleaned_data.get('date_begin')      
        date_end = form.cleaned_data.get('date_end')        
        if date_begin and date_end :        
          dailyshift=dailyshift.filter(date__range=(date_begin, date_end))  
     return render(request, 'daily_shift/find_daily_shift_by_date.html', {'form': form, 'dailyshift': dailyshift })  


#DailyShift Report---End

#Cash Desk Transactions--------Begin


#class ListCashDeskTransactionsView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
 #    login_url = '/accounts/login/'
 #    redirect_field_name = 'redirect_to' 
 #    template_name='cash_desk_transactions/list-cash_desk_transactions.html'
 #    model=Cash_Desk_Transaction
 #    permission_required = 'cctv.view_cash_desk_transaction' 
 #    paginate_by = 10 

 #    def get_paginate_by(self, queryset): 
 #       paginate_by = self.request.GET.get('length', self.paginate_by)      
 #       paginate_by = int(paginate_by)           
 #       return paginate_by
     

 #    def get_queryset(self):       
 #       if self.request.user.is_superuser:
 #            queryset = self.model.objects.all()          
 #       else:
 #            queryset = self.model.objects.filter(location=self.request.user.userprofile.location)       
      
  #      search_query = self.request.GET.get('search', '')
      
  #      if search_query:         
  #          queryset = queryset.filter(
  #               Q(transactions__icontains=search_query) |              
  #               Q(area_cashier__area_cashier__icontains=search_query)|                
  #               Q(account_type__account_type__icontains=search_query)| 
  #               Q(token__token__icontains=search_query)| 
  #               Q(autorized_by__name__icontains=search_query)| 
  #               Q(autorized_by__surname__icontains=search_query)| 
  #               Q(customer__customer__icontains=search_query)
   #         )
        
  #      return queryset
     
     
  #   def dispatch(self, request, *args, **kwargs):        
              
   #       if not hasattr(request.user, 'userprofile') and not self.request.user.is_superuser:
   #         messages.error(self.request, "No profile associated with the user was found")
   #         return redirect(self.login_url)
            
    #      return super().dispatch(request, *args, **kwargs)
   #  def get_context_data(self, **kwargs):
  #          context = super().get_context_data(**kwargs)     
    #        queryset = self.get_queryset()      
   #         paginate_by = self.get_paginate_by(queryset)    
    #        paginator = Paginator(queryset, paginate_by)
    #        page = self.request.GET.get('page', 1) 

     #       try:
    #            transactions = paginator.page(page)
     #       except PageNotAnInteger:
      #          transactions = paginator.page(1)
       #     except EmptyPage:
        #        transactions = paginator.page(paginator.num_pages)
    
         #   context['transactions'] = transactions
         #   context['paginator'] = paginator
         #   context['paginate_by'] = paginate_by 
         #   context['total_pages'] = paginator.num_pages        
          #  context['search_query'] = self.request.GET.get('search', '')

          #  return context

class ListCashDeskTransactionsView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to' 
    model = Cash_Desk_Transaction
    permission_required = 'cctv.view_cash_desk_transaction' 
    template_name = 'cash_desk_transactions/list-cash_desk_transactions.html'
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):                 
        if not hasattr(request.user, 'userprofile') and not self.request.user.is_superuser:
            messages.error(self.request, "No profile associated with the user was found")
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = self.model.objects.all()
        else:
            queryset = self.model.objects.filter(location=self.request.user.userprofile.location)
      
       
        search_value = self.request.GET.get('search[value]', '').strip()
        if search_value:
            queryset = queryset.annotate(
                        autorized_by_fullname=Concat(
                            F('autorized_by__name'), 
                            Value(' '), 
                            F('autorized_by__surname'), 
                            output_field=CharField()
                        )
                    )
            queryset = queryset.annotate(
                        employee_fullname=Concat(
                            F('employee__name'), 
                            Value(' '), 
                            F('employee__surname'), 
                            output_field=CharField()
                        )
                    )
            queryset = queryset.filter(
                Q(transactions__icontains=search_value) |
                Q(area_cashier__area_cashier__icontains=search_value) |
                Q(location__location__icontains=search_value)|
                Q(customer__customer__icontains=search_value) |
                Q(date__icontains=search_value) |
                Q(time__icontains=search_value) |
                Q(account_type__account_type__icontains=search_value) |
                Q(token__token__icontains=search_value) |
                Q(tt_dolar__icontains=search_value) |
                Q(usd_dolar__icontains=search_value) |
                Q(euro_dolar__icontains=search_value) |
                Q(gbp_dolar__icontains=search_value) |
                Q(cad_dolar__icontains=search_value) |
                Q(autorized_by_fullname__icontains=search_value) |
                Q(employee_fullname__icontains=search_value)|
                Q(machine_no__name__icontains=search_value)            
            )

    
        order_column_index = self.request.GET.get('order[0][column]', '0')
        order_dir = self.request.GET.get('order[0][dir]', 'asc')

        column_map = {
            '0': 'transactions',
            '1':'area_cashier',
            '2': 'date',  
            '3': 'time',  
            '4': 'account_type__account_type',  
            '5': 'token__token',  
            '6': 'tt_dolar',
            '7': 'usd_dolar',
            '8': 'euro_dolar',
            '9': 'gbp_dolar',
            '10':'cad_dolar',
            '11':'autorized_by__name',
            '12':'machine_no',
            '13':'employee__name',
            '13':'customer__customer',
            '14':'location__location'
        }


        order_field = column_map.get(order_column_index, 'transactions')
        if order_dir == 'desc':
            order_field = f"-{order_field}"

        queryset = queryset.order_by(order_field)
        return queryset

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            draw = int(self.request.GET.get('draw', 1))
            start = int(self.request.GET.get('start', 0))
            length = int(self.request.GET.get('length', 10))

            queryset = self.get_queryset()
            total_records = Cash_Desk_Transaction.objects.count()
            filtered_records = queryset.count()

            transactions = queryset[start:start+length]

            data = [{
                "transactions": transactions.transactions,
                "area_cashier":str(transactions.area_cashier),
                "date": transactions.date,
                "time": transactions.time,
                "account_type": transactions.account_type.account_type if transactions.account_type else "",
                "token": transactions.token.token if transactions.token else "",
                "tt_dolar": transactions.tt_dolar if transactions.tt_dolar else "0.0",
                "usd_dolar": transactions.usd_dolar if transactions.usd_dolar else "0.0",
                "euro_dolar": transactions.euro_dolar if transactions.euro_dolar else "0.0",
                "gbp_dolar": transactions.gbp_dolar if transactions.gbp_dolar else "0.0",
                "cad_dolar": transactions.cad_dolar if transactions.cad_dolar else "0.0",
                "autorized_by": str(transactions.autorized_by) if transactions.autorized_by else "",
                "machine_no":str(transactions.machine_no) if transactions.machine_no else "",
                "employee":str( transactions.employee) if transactions.employee else "",
                "customer":str( transactions.customer) if transactions.customer else "",                
                "location": str(transactions.location) if transactions.location else "",
                "detail_url": f"/cash_desk_transactions/detail/{transactions.transactions}/",
                "edit_url": f"/cash_desk_transactions/update/{transactions.transactions}/",
                "delete_url": f"/cash_desk_transactions/delete/{transactions.transactions}/",
            } for transactions in transactions]
        
            return JsonResponse({
                "draw": draw,
                "recordsTotal": total_records,
                "recordsFiltered": filtered_records,
                "data": data,
            })

        return super().render_to_response(context, **response_kwargs)

   
class CreateCashDeskTransactionsView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,CreateView):
     login_url = '/accounts/login/'
     redirect_field_name = 'redirect_to' 
     model=Cash_Desk_Transaction
     template_name = 'cash_desk_transactions/create-cash_desk_transactions.html'
     form_class = CreateCashDeskTransactionsForm    
     success_url = reverse_lazy("cash_desk_transactions-list") 
     permission_required = 'cctv.add_cash_desk_transaction' 
     success_message = "The Cash Desk Transaction was Added successfully."

     def get_initial(self):
        # Proporciona valores iniciales para el formulario
        initial = super().get_initial()
        initial['date'] = datetime.datetime.now()
        initial['time'] = datetime.datetime.now()
       

        if self.request.user.is_superuser:
            initial['location_id']=None
        else:
            initial['location_id'] = self.request.user.userprofile.location_id         
        return initial
      
     def form_valid(self, form):
         try:
         
            userprofile = self.request.user.userprofile.location
         except UserProfile.DoesNotExist:
                return self.form_invalid(form)          
         
         if 'save_and_continue' in self.request.POST:
             form.instance.location = userprofile or self.get_initial().get('location_id')
             form.save()
             messages.success(self.request, "The Cash Desk Transaction  was Added successfully.You can continue adding!")
             return redirect('cash_desk_transactions-create') 
       
         form.instance.location = userprofile
         return super().form_valid(form)


     def form_invalid(self, form):
        messages.error(self.request, "An error occurred while saving the form.")
        return super().form_invalid(form)	    
 
class UpdateCashDeskTransactionsView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
      login_url = '/accounts/login/'
      redirect_field_name = 'redirect_to' 
      model=Cash_Desk_Transaction
      template_name = 'cash_desk_transactions/update-cash_desk_transactions.html'
      form_class = CreateCashDeskTransactionsForm   
      success_url = reverse_lazy("cash_desk_transactions-list") 
      permission_required = 'cctv.change_cash_desk_transaction' 
      success_message = "The Cash Desk Transaction was Updated successfully."     
      
      def get_initial(self):      
        initial = super().get_initial()        
        if self.request.user.is_superuser:
            initial['location_id']=None
        else:
            initial['location_id'] = self.request.user.userprofile.location_id     
       
        return initial
      

      def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location           
         except UserProfile.DoesNotExist:               
                return self.form_invalid(form)         
       
           
         form.instance.location = userprofile
         return super().form_valid(form)


      def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
        return super().form_invalid(form)	 
      
class DeleteCashDeskTransactionsView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
       login_url = '/accounts/login/'
       redirect_field_name = 'redirect_to' 
       model=Cash_Desk_Transaction
       context_object_name = 'transactions'
       template_name='cash_desk_transactions/confirm_delete.html'   
       success_url = reverse_lazy("cash_desk_transactions-list")
       permission_required = 'cctv.delete_cash_desk_transaction' 
       success_message = "The Cash Desk Transaction was Deleted successfully." 

    
       def form_valid(self, form):            
            try:
                userprofile = self.request.user.userprofile.location            
            except UserProfile.DoesNotExist:                                      
                   
                    return self.form_invalid(form)            
            return super().form_valid(form)
       
       def form_invalid(self, form):            
            messages.error(self.request, "You do not have an associated profile. There was an error submitting the form.")
            return super().form_invalid(form)	
       
class DetailCashDeskTransactionsView(LoginRequiredMixin,PermissionRequiredMixin,DetailView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to' 
    model = Cash_Desk_Transaction
    context_object_name = 'transactions'
    template_name='cash_desk_transactions/detail-cash_desk_transactions.html'   
    success_url = reverse_lazy("cash_desk_transactions-list")
    permission_required = 'cctv.view_cash_desk_transaction' 



@login_required
def FilterTransactionsByDateView(request):   

     if request.user.is_superuser:        
         user_location=None
     else:
        user_location=request.user.userprofile.location    
     
     form=FilterTransactionsByDate(request.GET or None,  initial={'location': user_location})  
 
     if form.is_valid():
        if user_location:
            transactions=Cash_Desk_Transaction.objects.filter(location=request.user.userprofile.location)
        else:
             transactions=Cash_Desk_Transaction.objects.all()

        
        date_begin = form.cleaned_data.get('date_begin')      
        date_end = form.cleaned_data.get('date_end')        
             
        if date_begin and date_end :        
          transactions=transactions.filter(date__range=(date_begin, date_end))  
     else:
         transactions=None
         form=FilterTransactionsByDate(request.GET or None,  initial={'location': user_location})

     return render(request, 'cash_desk_transactions/find_transaction_by_date.html', {'form': form, 'transactions': transactions})

@login_required
def FilterTransactionsByCustomerView(request): 
    if request.user.is_superuser:
         user_location=None 
         location_id=None       
    else:
        user_location=request.user.userprofile.location  
        location_id=request.user.userprofile.location.id
       
       
            

    form=FilterTtransactionsByCustomer(request.GET or None, initial={'location':user_location,'location_id':location_id})

    if form.is_valid():
        if user_location:
              customer=Cash_Desk_Transaction.objects.filter(location=request.user.userprofile.location)
        else:
             customer=Cash_Desk_Transaction.objects.all()


        date_begin = form.cleaned_data.get('date_begin')      
        date_end = form.cleaned_data.get('date_end')  
        customer_id = form.cleaned_data.get('customer')
        
        if customer :        
          customer=customer.filter(customer_id__exact=customer_id)
        if date_begin and date_end:
          customer=customer.filter(date__range=(date_begin, date_end))    
    else:
         form=FilterTtransactionsByCustomer(request.GET or None, initial={'location':user_location,'location_id':location_id})
         customer=None


    
    return render(request, 'cash_desk_transactions/find_transaction_by_customer.html', {'form': form, 'customer': customer})
@login_required
def FilterTransactionsByAccountView(request):
    
    if request.user.is_superuser:
         user_location=None
         
    else:
        user_location=request.user.userprofile.location       
              

    form=FilterTransactionsByType(request.GET or None, initial={'location':user_location})

    if form.is_valid():
        if user_location:
             transactions=Cash_Desk_Transaction.objects.filter(location=request.user.userprofile.location) 
        else:
            transactions=Cash_Desk_Transaction.objects.all()


        date_begin = form.cleaned_data.get('date_begin')      
        date_end = form.cleaned_data.get('date_end')  
        account_type = form.cleaned_data.get('account_type')
        
        if account_type :        
          transactions=transactions.filter(account_type__exact=account_type)
        if date_begin and date_end:
          transactions=transactions.filter(date__range=(date_begin, date_end))

    else:
        transactions=None
        form=FilterTransactionsByType(request.GET or None, initial={'location':user_location})    

    
    return render(request, 'cash_desk_transactions/find_transaction_by_account_type.html', {'form': form, 'transactions': transactions})
@login_required
def FilterCustomerExpense(request):
     
    if request.user.is_superuser:        
         user_location=None
         location_id=None
    else:     
        user_location=request.user.userprofile.location
        location_id=request.user.userprofile.location.id
   
    form=CustomerExpenseForm(request.GET or None, initial={'location':user_location,'location_id':location_id})
   
    if form.is_valid():
         if user_location:
             transactions=Cash_Desk_Transaction.objects.filter(location=request.user.userprofile.location)
         else:
             transactions=Cash_Desk_Transaction.objects.all()

         date_begin = form.cleaned_data.get('date_begin')      
         date_end = form.cleaned_data.get('date_end')  
         customer_id=form.cleaned_data.get('customer')

         transactions=transactions.filter(Q(account_type=37) | Q(account_type=7))
         if  customer_id :
             transactions=transactions.filter(customer_id__exact=customer_id)
         if date_begin and date_end :
             transactions=transactions.filter(date__range=(date_begin, date_end))
    else:
        form=CustomerExpenseForm(request.GET or None, initial={'location':user_location,'location_id':location_id})
        transactions=None

        
        
    return render(request, 'cash_desk_transactions/customer_expense.html', {'form': form, 'transactions': transactions})

@login_required
def FilterCustomerCumplimentary(request):
  
    if request.user.is_superuser:        
         user_location=None
         location_id=None
    else:         
        user_location=request.user.userprofile.location  
        location_id=request.user.userprofile.location.id  
   
 
    form=CustomerComplimentaryForm(request.GET or None, initial={'location':user_location,'location_id':location_id})
    if form.is_valid():
         if user_location:
              transactions=Cash_Desk_Transaction.objects.filter(location=request.user.userprofile.location)
             
         else:
              transactions=Cash_Desk_Transaction.objects.all()
              
             
             
         date_begin = form.cleaned_data.get('date_begin')      
         date_end = form.cleaned_data.get('date_end')  
         customer_id=form.cleaned_data.get('customer')
         
         transactions=transactions.filter(Q(account_type=16) | Q(account_type=17) | Q(account_type=21) | Q(account_type=34) | Q(account_type=52) | Q(account_type=53))
         if  customer_id :
             transactions=transactions.filter(customer_id__exact=customer_id)
         if date_begin and date_end :
             transactions=transactions.filter(date__range=(date_begin, date_end))
    else:
        form=CustomerComplimentaryForm(request.GET or None, initial={'location':user_location,'location_id':location_id})
        transactions=None
        
    return render(request, 'cash_desk_transactions/customer_complimentary.html', {'form': form, 'transactions': transactions})
#Cash Desk Transactions--------End

#CDError****Begin
   
class ListCdErrorView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
     login_url = '/accounts/login/'
     redirect_field_name = 'redirect_to' 
     template_name='cash_desk_error/list-cd_error.html'
     model=Cash_Desk_Error
     permission_required = 'cctv.view_cash_desk_error' 

     def dispatch(self, request, *args, **kwargs):   
          if not hasattr(request.user, 'userprofile') and not self.request.user.is_superuser:
            messages.error(self.request, "No profile associated with the user was found")
            return redirect(self.login_url)
          return super().dispatch(request, *args, **kwargs)
        
    
  
     #def get_queryset(self):
        #  if self.request.user.is_superuser:
        #      qs=Cash_Desk_Error.objects.all()
       #   else:
            
        #     qs=Cash_Desk_Error.objects.filter(location=self.request.user.userprofile.location)
             
       #   return qs
    
     def get_queryset(self):
          if self.request.user.is_superuser:
              queryset=Cash_Desk_Error.objects.all()
          else:            
             queryset=Cash_Desk_Error.objects.filter(location=self.request.user.userprofile.location)

          search_value=self.request.GET.get('search[value]','').strip()
       

          if search_value:
                queryset=queryset.annotate(
                duty_manager_fullname=Trim(
                    Concat(
                        Coalesce(F('duty_manager__name'),Value('')),
                                                  Value(' '),
                                                  Coalesce(F('duty_manager__surname'), Value('')),
                                                  output_field=CharField()
                                                  )
                                          )
                                        )
                queryset=queryset.annotate(
                        cashier_fullname=Trim(
                            Concat(
                                Coalesce(F('cashier__name'),Value('')),
                                Value(' '),
                                Coalesce(F('cashier__surname'), Value('')),
                                output_field=CharField()
                                  )
                            
                                    )   

                                  )
                queryset=queryset.annotate(
                supervisor_fullname=Trim(
                    Concat(
                        Coalesce(F('supervisor__name'), Value('')),
                        Value(' '),
                        Coalesce(F('supervisor__surname'), Value('')),
                        output_field=CharField()

                           )

                           )
                       )
            
                queryset=queryset.filter(
                    Q(id__icontains=search_value)|
                    Q(location__location__icontains=search_value)|
                    Q(date__icontains=search_value)|
                    Q(time__icontains=search_value)|
                    Q(area_cashier__area_cashier=search_value)|
                    Q(error_type__error_type__icontains=search_value)|
                    Q(duty_manager_fullname__icontains=search_value)|
                    Q(cashier_fullname__icontains=search_value)|
                    Q(supervisor_fullname__icontains=search_value)|
                    Q(tt__icontains=search_value)|
                    Q(usd__icontains=search_value)|
                    Q(euro__icontains=search_value)|
                    Q(report__icontains=search_value)


                )
          order_colum_index=self.request.GET.get('order[0][column]','0')
     
          order_dir=self.request.GET.get('order[0][dir]','asc')
          

          column_map={
                '0':'id',
                '1':'date',
                '2':'time',
                '3':'area_cashier__area_cashier',
                '4':'error_type__error_type',
                '5':'duty_manager',
                '6':'tt',
                '7':'usd',
                '8':'euro',
                '9':'report',
                '10':'found',
                '11':'cashier',
                '12':'supervisor',
                '13':'location__location'
            

            }
          order_field=column_map.get(order_colum_index,'id')
            
          if order_dir=='desc':
                order_field=f"-{order_field}"
                queryset=queryset.order_by(order_field)  
          return queryset
     
     def render_to_response(self, context, **response_kwargs):
            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                draw = int(self.request.GET.get('draw', 1))
                start = int(self.request.GET.get('start', 0))
                length = int(self.request.GET.get('length', 10))

                queryset = self.get_queryset()
                total_records = Cash_Desk_Error.objects.count()
                filtered_records = queryset.count()

                cash_desk_error = queryset[start:start+length]

                data = [{
                    "id": cash_desk_error.id,                  
                    "date": cash_desk_error.date,
                    "time": cash_desk_error.time,
                    "area_cashier": str(cash_desk_error.area_cashier.area_cashier) if cash_desk_error.area_cashier else "",
                    "error_type": str(cash_desk_error.error_type.error_type) if cash_desk_error.error_type else "",
                    "duty_manager": str(cash_desk_error.duty_manager) if cash_desk_error.duty_manager else "",
                    "tt": cash_desk_error.tt if cash_desk_error.tt else "0.0",
                    "usd": cash_desk_error.usd if cash_desk_error.usd else "0.0",
                    "euro": cash_desk_error.euro if cash_desk_error.euro else "0.0",
                    "report": cash_desk_error.report if cash_desk_error.report else "",
                    "found": str(cash_desk_error.found) ,
                    "cashier":str(cash_desk_error.cashier) if cash_desk_error.cashier else "",
                    "supervisor":str( cash_desk_error.supervisor) if cash_desk_error.supervisor else "",                         
                    "location": str(cash_desk_error.location) if cash_desk_error.location else "",
                    "detail_url": cash_desk_error.get_absolute_url(),
                    "edit_url": cash_desk_error.get_edit_url(),
                    "delete_url":cash_desk_error.get_delete_url(),
                } for cash_desk_error in cash_desk_error]

                return JsonResponse({
                    "draw": draw,
                    "recordsTotal": total_records,
                    "recordsFiltered": filtered_records,
                    "data": data,
                })

            return super().render_to_response(context, **response_kwargs)

   
class CreateCdErrorView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,CreateView):
     login_url = '/accounts/login/'
     redirect_field_name = 'redirect_to' 
     model=Cash_Desk_Error
     template_name = 'cash_desk_error/create-cd_error.html'
     form_class = CashDeskErrorForm    
     success_url = reverse_lazy("cash_desk_error-list")  
     permission_required = 'cctv.add_cash_desk_error' 
     success_message = "The Cash Desk Error was Added successfully."
      
     def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location           
         except UserProfile.DoesNotExist:
                return self.form_invalid(form)          
         if 'save_and_continue' in self.request.POST:
             form.instance.location = userprofile or self.get_initial().get('location_id')
             form.save()
             messages.success(self.request, "The Cash Desk Error was Added successfully.You can continue adding!")
             return redirect('cash_desk_error-create')  
      
         form.instance.location = userprofile
         return super().form_valid(form)


     def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
        return super().form_invalid(form)	     
     
     def get_initial(self):
        initial = super().get_initial()
        initial['date'] = datetime.datetime.now()
        initial['time'] = datetime.datetime.now()
       
        if self.request.user.is_superuser:
            initial['location_id']=None
        else:
            initial['location_id'] = self.request.user.userprofile.location_id         
        return initial
       
        return initial    
   
 
class UpdateCdErrorView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
      login_url = '/accounts/login/'
      redirect_field_name = 'redirect_to' 
      model=Cash_Desk_Error
      template_name = 'cash_desk_error/update-cd_error.html'
      form_class = CashDeskErrorForm   
      success_url = reverse_lazy("cash_desk_error-list")  
      permission_required = 'cctv.change_cash_desk_error' 
      success_message = "The Cash Desk Error  was Updated successfully."
      
      def get_initial(self):      
        initial = super().get_initial()        
        if self.request.user.is_superuser:
            initial['location_id']=None
        else:
            initial['location_id'] = self.request.user.userprofile.location_id         
       
       
        return initial
      
      def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location
           
         except UserProfile.DoesNotExist:
               
                return self.form_invalid(form)          
       
         form.instance.location = userprofile
       
         return super().form_valid(form)


      def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
        return super().form_invalid(form)	         
  

class DeleteCdErrorView(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
       login_url = '/accounts/login/'
       redirect_field_name = 'redirect_to' 
       model=Cash_Desk_Error
       context_object_name = 'cash_desk_error'
       template_name='cash_desk_error/confirm_delete.html'   
       success_url = reverse_lazy("cash_desk_error-list")
       permission_required = 'cctv.delete_cash_desk_error' 
    
       success_message = "The Cash Desk Error was Deleted successfully."
       error_message = (
            "Cannot delete the Cash Desk Error '{name}' because it is related to other records: {details}."
              )
       

       def post(self, request, *args, **kwargs):
                self.object = self.get_object()  # Obtener el objeto a eliminar
              
                try:
                    # Intentar eliminar el objeto
                    self.object.delete()
                    messages.success(request, self.success_message)
                    return redirect(self.success_url)
                except ProtectedError as e:
                 
                    related_objects = ', '.join(str(obj) for obj in e.protected_objects)
                    
                    error_message = self.error_message.format(name=str(self.object), details=related_objects)
                    messages.error(request, error_message)
                    return redirect(self.success_url)
    
class DetailCdErrorView(LoginRequiredMixin,PermissionRequiredMixin,DetailView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to' 
    model = Cash_Desk_Error
    context_object_name = 'cash_desk_error'
    template_name='cash_desk_error/detail-cd_error.html'   
    success_url = reverse_lazy("cash_desk_error-list")
    permission_required = 'cctv.view_cash_desk_error' 

   

@login_required
def FilterCdErrorByDateView(request):    
    if request.user.is_superuser:
         cash_error=Cash_Desk_Error.objects.all()
         user_location=''
    else:       
        cash_error=Cash_Desk_Error.objects.filter(location=request.user.userprofile.location)
        user_location=request.user.userprofile.location
        
    form=FilterCdErrorByDate(request.GET or None,  initial={'location': user_location})

    if form.is_valid(): 
        
        date_begin = form.cleaned_data.get('date_begin')      
        date_end = form.cleaned_data.get('date_end')        
        if date_begin and date_end :        
          cash_error=cash_error.filter(date__range=(date_begin, date_end))    
    return render(request, 'cash_desk_error/find_cd_error_by_date.html', {'form': form, 'cash_error': cash_error})  


@login_required
def FilterSynopsisCashierView(request):
    if request.user.is_superuser:
         cashier=Cash_Desk_Error.objects.all()
         location=None
    else:
       cashier=Cash_Desk_Error.objects.filter(location=request.user.userprofile.location)
       location=request.user.userprofile.location


    form=FilterCashierSynopsis(request.GET or None,initial={'location':location})

    if form.is_valid():
        date_begin = form.cleaned_data.get('date_begin')      
        date_end = form.cleaned_data.get('date_end')  
        if date_begin and date_end :        
          cashier=cashier.filter(date__range=(date_begin, date_end))       
    
        cashier_id = form.cleaned_data.get('cashier')
        
        if cashier_id :        
          cashier=cashier.filter(cashier_id__exact=cashier_id)
    
    return render(request, 'cash_desk_error/find_synopsis_cashier.html', {'form': form, 'cashier': cashier})

def get_report_id(request, report_value,location):
    try: 
        location_obj = Location.objects.get(location=location)
        location_id = location_obj.id        
        report = Report.objects.get(report_nro=report_value, location_id=location_id)         
    
        return JsonResponse({
            'id': report.report  
        
        })
    except Report.DoesNotExist:
        return JsonResponse({'error': 'Report not found'}, status=404)

#Poker Payouts****** BEGIN

class ListPokerPayoutsView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
     login_url = '/accounts/login/'
     redirect_field_name = 'redirect_to' 
     template_name='poker_payouts/list-poker_payouts.html'
     model=Poker_Payout
     permission_required = 'cctv.view_poker_payout'

     def dispatch(self, request, *args, **kwargs):               
          if not hasattr(request.user, 'userprofile') and not self.request.user.is_superuser:
            messages.error(self.request, "No profile associated with the user was found")
            return redirect(self.login_url) 
                     
          return super().dispatch(request, *args, **kwargs)
     


  #   def get_queryset(self):
  #       if self.request.user.is_superuser:
  #             qs=Poker_Payout.objects.all()
  #       else:
 #             qs=Poker_Payout.objects.filter(location=self.request.user.userprofile.location)
            
 #        return qs
     def get_queryset(self):
         if self.request.user.is_superuser:
              queryset=Poker_Payout.objects.all()
         else:
              queryset=Poker_Payout.objects.filter(location=self.request.user.userprofile.location)        
         search_value=self.request.GET.get('search[value]','').strip()      
         """ Este search_value es para buscar en el datatable"""
         if search_value:
                queryset=queryset.annotate(
                dealer_fullname=Trim(
                    Concat(
                        Coalesce(F('dealer__name'),Value('')),
                        Value(' '),
                        Coalesce(F('dealer__surname'), Value('')),
                         output_field=CharField()
                          )
                          )
                          )
                queryset=queryset.annotate(
                        inspector_fullname=Trim(
                            Concat(
                                Coalesce(F('inspector__name'),Value('')),
                                Value(' '),
                                Coalesce(F('inspector__surname'), Value('')),
                                output_field=CharField()
                                  )
                            
                                    )   

                                  )
                queryset=queryset.annotate(
                pitboss_fullname=Trim(
                    Concat(
                        Coalesce(F('pitboss__name'), Value('')),
                        Value(' '),
                        Coalesce(F('pitboss__surname'), Value('')),
                        output_field=CharField()

                           )

                           )
                       )
            
                queryset=queryset.filter(
                    Q(id__icontains=search_value)|
                    Q(location__location__icontains=search_value)|
                    Q(date__icontains=search_value)|
                    Q(time__icontains=search_value)|
                    Q(table__poker_table__icontains=search_value)|
                    Q(combination__poker_combination__icontains=search_value)|
                    Q(dealer_fullname__icontains=search_value)|
                    Q(inspector_fullname__icontains=search_value)|
                    Q(pitboss_fullname__icontains=search_value)|
                    Q(bet__icontains=search_value)|
                    Q(payout__icontains=search_value)|
                    Q(customer__customer__icontains=search_value)   
                    )
            
         order_column_index = self.request.GET.get('order[0][column]', '0')
         order_dir = self.request.GET.get('order[0][dir]', 'asc')        

         column_map = {
                '0': 'id',
                '1':'date',
                '2': 'time',  
                '3': 'table__poker_table',  
                '4': 'combination__poker_combination',  
                '5': 'bet',  
                '6': 'payout',
                '7': 'customer__customer',
                '8': 'dealer__name',
                '9': 'inspector__name',
                '10': 'pitboss__name',           
                '11':'location__location'
            }


         order_field = column_map.get(order_column_index, 'report')
         if order_dir == 'desc':
            order_field = f"-{order_field}"

         queryset = queryset.order_by(order_field)     
            
         return queryset
     
     def render_to_response(self, context, **response_kwargs):
            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                draw = int(self.request.GET.get('draw', 1))
                start = int(self.request.GET.get('start', 0))
                length = int(self.request.GET.get('length', 10))

                queryset = self.get_queryset()
                total_records = Poker_Payout.objects.count()
                filtered_records = queryset.count()

                poker_payout = queryset[start:start+length]

                data = [{
                    "id": poker_payout.id,                  
                    "date": poker_payout.date,
                    "time": poker_payout.time,
                    "table": str(poker_payout.table.poker_table) if poker_payout.table else "",
                    "combination": str(poker_payout.combination.poker_combination) if poker_payout.combination else "",
                    "bet": poker_payout.bet if poker_payout.bet else "0.0",
                    "payout": poker_payout.payout if poker_payout.payout else "0.0",
                    "customer": str(poker_payout.customer) if poker_payout.customer else "",
                    "dealer": str(poker_payout.dealer) if poker_payout.dealer else "",
                    "inspector": str(poker_payout.inspector) if poker_payout.inspector else "",
                    "pitboss": str(poker_payout.pitboss) ,                                        
                    "location": str(poker_payout.location.location) if poker_payout.location else "",
                    "detail_url": poker_payout.get_absolute_url() if poker_payout and self.request.user.has_perm("cctv.view_poker_payout") else None,
                    "edit_url": poker_payout.get_edit_url() if poker_payout and self.request.user.has_perm("cctv.change_poker_payout") else None,
                    "delete_url":poker_payout.get_delete_url() if poker_payout and self.request.user.has_perm("cctv.delete_poker_payout") else None,
                } for poker_payout in poker_payout]

                return JsonResponse({
                    "draw": draw,
                    "recordsTotal": total_records,
                    "recordsFiltered": filtered_records,
                    "data": data,
                })

            return super().render_to_response(context, **response_kwargs)
   
  
class CreatePokerPayoutsView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,CreateView):
     login_url = '/accounts/login/'
     redirect_field_name = 'redirect_to' 
     model=Poker_Payout
     template_name = 'poker_payouts/create-poker_payouts.html'
     form_class = PokerPayoutForm  
     success_url = reverse_lazy("poker_payouts-list")   
     permission_required = 'cctv.add_poker_payout' 
     success_message = "The Poker Payouts was Added successfully."
      
     def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location
           
         except UserProfile.DoesNotExist:               
                return self.form_invalid(form)          
        
         if 'save_and_continue' in self.request.POST:
             form.instance.location = userprofile or self.get_initial().get('location_id')
             form.save()
             messages.success(self.request, "The Poker Payouts was Added successfully.You can continue adding!")
             return redirect('poker_payouts-create') 
        
         form.instance.location = userprofile
         return super().form_valid(form)


     def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile or some validation failed.")
        return super().form_invalid(form)	    

     def get_initial(self):
        initial = super().get_initial()
        initial['date'] = datetime.datetime.now()
        initial['time'] = datetime.datetime.now()

        if self.request.user.is_superuser:
            initial['location_id']=None
        else:
            initial['location_id'] = self.request.user.userprofile.location_id         
       
        return initial    
          

class UpdatePokerPayoutsView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
      login_url = '/accounts/login/'
      redirect_field_name = 'redirect_to' 
      model=Poker_Payout
      template_name = 'poker_payouts/update-poker_payouts.html'
      form_class = PokerPayoutForm   
      success_url = reverse_lazy("poker_payouts-list")  
      permission_required = 'cctv.change_poker_payout'  
      success_message = "The Poker Payouts was Updated successfully."
      
      def get_initial(self):      
        initial = super().get_initial()        
        if self.request.user.is_superuser:
            initial['location_id']=None
        else:
            initial['location_id'] = self.request.user.userprofile.location_id         
       
       
        return initial
      def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location
           
         except UserProfile.DoesNotExist:
               
                return self.form_invalid(form)          
       
         form.instance.location = userprofile
       
         return super().form_valid(form)


      def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile or some validation failed.")
        return super().form_invalid(form)	               
  

class DeletePokerPayoutsView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
       login_url = '/accounts/login/'
       redirect_field_name = 'redirect_to' 
       model=Poker_Payout
       context_object_name = 'poker_payouts'
       template_name='poker_payouts/confirm_delete.html'   
       success_url = reverse_lazy("poker_payouts-list")
       permission_required = 'cctv.delete_poker_payout'
       success_message = "The Poker Payouts was Delete successfully."
      
       def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location
           
         except UserProfile.DoesNotExist:
               
                return self.form_invalid(form)          
       
       
       
         return super().form_valid(form)


       def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile or some validation failed.")
        return super().form_invalid(form)	          
       
class DetailPokerPayoutsView(LoginRequiredMixin,PermissionRequiredMixin,DetailView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'  
    model = Poker_Payout
    context_object_name = 'poker_payouts'
    template_name='poker_payouts/detail-poker_payouts.html'   
    success_url = reverse_lazy("poker_payouts-list")
    permission_required = 'cctv.view_poker_payout'
#Poker Payouts****** END
 
  

@login_required
def FilterPokerPayoutsByDateView(request):
     
     if request.user.is_superuser:
          poker_payouts=Poker_Payout.objects.all()
          user_location=''
     else:
          poker_payouts=Poker_Payout.objects.filter(location=request.user.userprofile.location)
          user_location=request.user.userprofile.location
      
     form=FilterPokerPayoutsDate(request.GET or None,  initial={'location': user_location})

     if form.is_valid(): 
        
        date_begin = form.cleaned_data.get('date_begin')      
        date_end = form.cleaned_data.get('date_end')        
        if date_begin and date_end :        
          poker_payouts=poker_payouts.filter(date__range=(date_begin, date_end))    
     return render(request, 'poker_payouts/find_poker_payouts.html', {'form': form, 'poker_payouts': poker_payouts})  

@login_required
def FilterSynopsisStaffView(request):
   if request.user.is_superuser:
        user_location=''
        staff_synopsis=Poker_Payout.objects.all()
   else:
        user_location=request.user.userprofile.location 
        staff_synopsis=Poker_Payout.objects.filter(location=user_location)  
         
       
  
   
   form=FilterSynopsisStaffForm(request.GET or None,initial={'location':user_location})

   if form.is_valid():
       pitboss=form.cleaned_data.get('pitboss')  
       dealer=form.cleaned_data.get('dealer')  
       inspector=form.cleaned_data.get('inspector')
       date_begin = form.cleaned_data.get('date_begin')      
       date_end = form.cleaned_data.get('date_end')        
       if date_begin and date_end :        
          staff_synopsis=staff_synopsis.filter(date__range=(date_begin, date_end))
             
       if pitboss:
            staff_synopsis=staff_synopsis.filter( pitboss_id__exact=pitboss)
           
       if dealer :
           
           staff_synopsis=staff_synopsis.filter(  dealer_id__exact=dealer)

       if  inspector:
           staff_synopsis=staff_synopsis.filter( inspector_id__exact=inspector)

   return render(request,'poker_payouts/find_synopsis_staff.html',{'form':form, 'staff_synopsis':staff_synopsis})

@login_required
def FilterPokerPayoutCombinationView(request):
    if request.user.is_superuser:
        user_location=''
        poker_payout_combination=Poker_Payout.objects.all()
    else:
        user_location=request.user.userprofile.location 
        poker_payout_combination=Poker_Payout.objects.filter(location=  request.user.userprofile.location)
  
    form=FilterPokerPayoutCombinationForm(request.GET or None,initial={'location':user_location}) 
 
    if form.is_valid():
      date_begin = form.cleaned_data.get('date_begin')      
      date_end = form.cleaned_data.get('date_end')        
      combination=form.cleaned_data.get('combination')
      if date_begin and date_end :        
          poker_payout_combination=poker_payout_combination.filter(date__range=(date_begin, date_end))
      if combination:
          poker_payout_combination=poker_payout_combination.filter(combination_id__exact=combination)     
    return  render(request,'poker_payouts/find_poker_payout_combination.html',{'form':form, 'poker_payout_combination':poker_payout_combination})

@login_required
def FilterPokerPayoutCustomerView (request):
   if request.user.is_superuser:
        location_id=None
        user_location=''
        poker_payout_customer=Poker_Payout.objects.all()
   else:
       user_location=request.user.userprofile.location 
       location_id= request.user.userprofile.location.id
       poker_payout_customer=Poker_Payout.objects.filter(location=request.user.userprofile.location)

   form=FilterPokerPayoutCustomerForm(request.GET or None ,initial={'location':user_location,'location_id':location_id}) 
 
   if form.is_valid():
     
     customer=form.cleaned_data.get('customer')
     date_begin = form.cleaned_data.get('date_begin')      
     date_end = form.cleaned_data.get('date_end')
     if date_begin and date_end :        
         poker_payout_customer=poker_payout_customer.filter(date__range=(date_begin, date_end))
     if customer:
         poker_payout_customer=poker_payout_customer.filter(customer_id__exact=customer)     
   return  render(request,'poker_payouts/find_poker_payout_customer.html',{'form':form, 'poker_payout_customer':poker_payout_customer})
      


###***** POKER PAYOUTS*****END
#Report Synopsis

class ListReportSynopsisView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
   login_url = '/accounts/login/'
   redirect_field_name = 'redirect_to' 
   template_name='report_synopsis/list-report_synopsis.html'
   model=Report
   permission_required = 'cctv.view_report'

   def dispatch(self, request, *args, **kwargs): 
          if not hasattr(request.user, 'userprofile') and not self.request.user.is_superuser:
            messages.error(self.request, "No profile associated with the user was found")
            return redirect(self.login_url)            
          return super().dispatch(request, *args, **kwargs)    
   
   def get_queryset(self):
        if self.request.user.is_superuser:
             qs=Report.objects.all().order_by('date','report_nro')
        else:           
            qs=Report.objects.filter(location=self.request.user.userprofile.location).order_by('date','report_nro') 
       
        return qs

        
@login_required
def ReportSynopsisCCTV(request):
    if request.user.is_superuser:
        synopsis_cctv=Report.objects.filter(cctv_id__isnull=False).order_by('date','report_nro','cctv_id')
        user_location=None
    else:
        synopsis_cctv=Report.objects.filter(location=request.user.userprofile.location,cctv_id__isnull=False).order_by('date','report_nro','cctv_id')
        user_location=request.user.userprofile.location    

    form=Synopsis_CCTV(request.GET or None,  initial={'location': user_location})

    if form.is_valid():
        employee_id = form.cleaned_data.get('employee')
        date_begin = form.cleaned_data.get('date_begin')      
        date_end = form.cleaned_data.get('date_end')  
       
        if date_begin and date_end :        
          synopsis_cctv=synopsis_cctv.filter(date__range=(date_begin, date_end))   
        if employee_id :        
          synopsis_cctv=synopsis_cctv.filter( cctv_id__exact=employee_id)
    
    return render(request, 'report_synopsis/list-report_synopsis_cctv.html', {'form': form, 'synopsis_cctv': synopsis_cctv})


        
@login_required
def ReportSynopsisDEALER(request):
    if request.user.is_superuser:
        synopsis_dealer=Report.objects.filter(dealer__isnull=False).order_by('date','dealer')
        user_location=None
    else:
        synopsis_dealer=Report.objects.filter(location=request.user.userprofile.location,dealer__isnull=False).order_by('date','dealer')
        user_location=request.user.userprofile.location    

    form=Synopsis_DEALER(request.GET or None,  initial={'location': user_location})

    if form.is_valid():
        employee_id = form.cleaned_data.get('employee')
        date_begin = form.cleaned_data.get('date_begin')      
        date_end = form.cleaned_data.get('date_end')  
       
        if date_begin and date_end :        
          synopsis_dealer=synopsis_dealer.filter(date__range=(date_begin, date_end))   
        if employee_id :        
          synopsis_dealer=synopsis_dealer.filter( dealer__exact=employee_id)    
    return render(request, 'report_synopsis/list-report_synopsis_dealer.html', {'form': form, 'synopsis_dealer': synopsis_dealer})

@login_required
def ReportSynopsisINSPECTOR(request):
    if request.user.is_superuser:
        synopsis_inspector=Report.objects.filter(inspector__isnull=False).order_by('date','inspector')
        user_location=None
    else:
        synopsis_inspector=Report.objects.filter(location=request.user.userprofile.location,inspector__isnull=False).order_by('date','inspector')
        user_location=request.user.userprofile.location    

    form=Synopsis_INSPECTOR(request.GET or None,  initial={'location': user_location})

    if form.is_valid():
        employee_id = form.cleaned_data.get('employee')
        date_begin = form.cleaned_data.get('date_begin')      
        date_end = form.cleaned_data.get('date_end')  
       
        if date_begin and date_end :        
          synopsis_inspector=synopsis_inspector.filter(date__range=(date_begin, date_end))   
        if employee_id :        
          synopsis_inspector=synopsis_inspector.filter( inspector__exact=employee_id)
    

    
    return render(request, 'report_synopsis/list-report_synopsis_inspector.html', {'form': form, 'synopsis_inspector': synopsis_inspector})


@login_required
def ReportSynopsisPITBOSS(request):
    if request.user.is_superuser:
        synopsis_pitboss=Report.objects.filter(pittboss__isnull=False).order_by('date','pittboss')
        user_location=None
    else:
        synopsis_pitboss=Report.objects.filter(location=request.user.userprofile.location,pittboss__isnull=False).order_by('date','pittboss')
        user_location=request.user.userprofile.location    

    form=Synopsis_PITBOSS(request.GET or None,  initial={'location': user_location})

    if form.is_valid():
        employee_id = form.cleaned_data.get('employee')
        date_begin = form.cleaned_data.get('date_begin')      
        date_end = form.cleaned_data.get('date_end')  
       
        if date_begin and date_end :        
          synopsis_pitboss=synopsis_pitboss.filter(date__range=(date_begin, date_end))   
        if employee_id :        
          synopsis_pitboss=synopsis_pitboss.filter( pittboss__exact=employee_id)
    

    
    return render(request, 'report_synopsis/list-report_synopsis_pitboss.html', {'form': form, 'synopsis_pitboss': synopsis_pitboss})

@login_required
def ReportSynopsisSUMMARY(request):
    if request.user.is_superuser:
        synopsis_summary=Report.objects.all().order_by('date','pittboss')
        user_location=None
    else:
        synopsis_summary=Report.objects.filter(location=request.user.userprofile.location).order_by('date','pittboss')
        user_location=request.user.userprofile.location    

    form=Synopsis_SUMMARY(request.GET or None,  initial={'location': user_location})

    if form.is_valid():
     
        date_begin = form.cleaned_data.get('date_begin')      
        date_end = form.cleaned_data.get('date_end')  
       
        if date_begin and date_end :        
          synopsis_summary=synopsis_summary.filter(date__range=(date_begin, date_end))    
    

    
    return render(request, 'report_synopsis/list-report_synopsis_summary.html', {'form': form, 'synopsis_summary': synopsis_summary})


@login_required
def ReportSynopsisTITLE(request):
    if request.user.is_superuser:
        synopsis_title=Report.objects.filter(report_title__isnull=False).order_by('date','report_title')
        user_location=None
    else:
      
        synopsis_title=Report.objects.filter(report_title__isnull=False,location=request.user.userprofile.location).order_by('date','report_title')
        user_location=request.user.userprofile.location    

    form=Synopsis_TITTLE(request.GET or None,  initial={'location': user_location})

    if form.is_valid():
       
        tittle_id = form.cleaned_data.get('tittle')
       
        date_begin = form.cleaned_data.get('date_begin')      
        date_end = form.cleaned_data.get('date_end')  
       
        if date_begin and date_end :        
          synopsis_title=synopsis_title.filter(date__range=(date_begin, date_end))   
        if tittle_id :        
          synopsis_title=synopsis_title.filter( report_title__exact=tittle_id)
    

    
    return render(request, 'report_synopsis/list-report_synopsis_tittle.html', {'form': form, 'synopsis_title': synopsis_title})

    
@login_required
def ReportSynopsisUNDERPAYMENT(request):
    if request.user.is_superuser:
        synopsis_underpayment=Report.objects.filter(report_title__id=20).order_by('date','report_title')
        user_location=None
    else:
      
        synopsis_underpayment=Report.objects.filter(report_title__id=20,location=request.user.userprofile.location).order_by('date','report_title')
        user_location=request.user.userprofile.location    

    form=Synopsis_UNDERPAYMENT(request.GET or None,  initial={'location': user_location})

    if form.is_valid():
        date_begin = form.cleaned_data.get('date_begin')      
        date_end = form.cleaned_data.get('date_end')  
       
        if date_begin and date_end :        
          synopsis_underpayment=synopsis_underpayment.filter(date__range=(date_begin, date_end))   
       
    

    
    return render(request, 'report_synopsis/list-report_synopsis_underpayment.html', {'form': form, 'synopsis_underpayment': synopsis_underpayment})

  
@login_required
def ReportSynopsisOVERPAYMENT(request):
    if request.user.is_superuser:
        synopsis_overpayment=Report.objects.filter(report_title__id=16).order_by('date','report_title')
        user_location=None
    else:
      
        synopsis_overpayment=Report.objects.filter(report_title__id=16,location=request.user.userprofile.location).order_by('date','report_title')
        user_location=request.user.userprofile.location    

    form=Synopsis_OVERPAYMENT(request.GET or None,  initial={'location': user_location})

    if form.is_valid():
        date_begin = form.cleaned_data.get('date_begin')      
        date_end = form.cleaned_data.get('date_end')  
       
        if date_begin and date_end :        
          synopsis_overpayment=synopsis_overpayment.filter(date__range=(date_begin, date_end))   
       
    

    
    return render(request, 'report_synopsis/list-report_synopsis_overpayment.html', {'form': form, 'synopsis_underpayment': synopsis_overpayment})


#Counterfait Money****Begin

class ListCounterfaitView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
     login_url = '/accounts/login/'
     redirect_field_name = 'redirect_to' 
     template_name='counterfeit/list-counterfeit.html'
     model=Counterfait
     permission_required = 'cctv.view_counterfait'

     def dispatch(self, request, *args, **kwargs): 
          if not hasattr(request.user, 'userprofile') and not self.request.user.is_superuser:
            messages.error(self.request, "You do not have an associated profile or some validation failed.")
            return redirect(self.login_url)
            
          return super().dispatch(request, *args, **kwargs)
     
    
   #  def get_queryset(self):
   #     if self.request.user.is_superuser:
   #         qs=Counterfait.objects.all()
   #     else:
   #         qs=Counterfait.objects.filter(location=self.request.user.userprofile.location)
   #     return qs

     def get_queryset(self):
         if self.request.user.is_superuser:
            queryset=Counterfait.objects.all()
         else:
            queryset=Counterfait.objects.filter(location=self.request.user.userprofile.location)

         search_value=self.request.GET.get('search[value]','').strip()      
         """ Este search_value es para buscar en el datatable"""
         if search_value:
                queryset=queryset.annotate(
                employee_fullname=Trim(
                    Concat(
                        Coalesce(F('employee__name'),Value('')),
                        Value(' '),
                        Coalesce(F('employee__surname'), Value('')),
                         output_field=CharField()
                          )
                          )
                          )
             
            
                queryset=queryset.filter(
                    Q(id__icontains=search_value)|                  
                    Q(date__icontains=search_value)|
                    Q(location__location__icontains=search_value)| 
                    Q(area_cashier__area_cashier__icontains=search_value)|
                    Q(report_nro__icontains=search_value)|
                    Q(serial_number__icontains=search_value)|
                    Q(employee_fullname__icontains=search_value)|
                    Q(gbp_dolar__icontains=search_value)|
                    Q(euro_dolar__icontains=search_value)|
                    Q(tt_dolar__icontains=search_value)|
                    Q(usd_dolar__icontains=search_value)|
                    Q(notes__contains=search_value)|
                    Q(customer__customer__icontains=search_value) 
                   
                      
                    )
            
         order_column_index = self.request.GET.get('order[0][column]', '0')
         order_dir = self.request.GET.get('order[0][dir]', 'asc')        

         column_map = {
                '0': 'id',
                '1':'date',
                '2': 'area_cashier__area_cashier',  
                '3': 'tt_dolar',  
                '4': 'usd_dolar',  
                '5': 'euro_dolar',  
                '6': 'gbp_dolar',
                '7': 'serial_number',
                '8': 'report_nro',
                '9': 'employee__name', 
                '10':'customer__customer',
                '11': 'notes',
                '12':'location___location'
            }


         order_field = column_map.get(order_column_index, 'report')
         if order_dir == 'desc':
            order_field = f"-{order_field}"

         queryset = queryset.order_by(order_field)     
            
         return queryset
     
     def render_to_response(self, context, **response_kwargs):
            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                draw = int(self.request.GET.get('draw', 1))
                start = int(self.request.GET.get('start', 0))
                length = int(self.request.GET.get('length', 10))

                queryset = self.get_queryset()
                total_records = Counterfait.objects.count()
                filtered_records = queryset.count()

                counterfait_money = queryset[start:start+length]

                data = [{
                    "id": counterfait_money.id,                  
                    "date": counterfait_money.date,
                    "area_cashier":str( counterfait_money.area_cashier),
                    "tt_dolar": str(counterfait_money.tt_dolar) if counterfait_money.tt_dolar else "0",
                    "usd_dolar": str(counterfait_money.usd_dolar) if counterfait_money.usd_dolar else "0",
                    "euro_dolar": counterfait_money.euro_dolar if counterfait_money.euro_dolar else "0",
                    "gbp_dolar": counterfait_money.gbp_dolar if counterfait_money.gbp_dolar else "0",
                    "serial_number": str(counterfait_money.serial_number) if counterfait_money.serial_number else "No Serial",
                    "report_nro": str(counterfait_money.report_nro) if counterfait_money.report_nro else "" ,                    
                    "employee": str(counterfait_money.employee) if counterfait_money.employee else "" ,   
                    "customer": str(counterfait_money.customer) if counterfait_money.customer else "" ,
                    "notes": str(counterfait_money.notes) if counterfait_money.notes else "",   
                    "location": str(counterfait_money.location) ,                    
                    "detail_url": counterfait_money.get_absolute_url() if counterfait_money and self.request.user.has_perm("cctv.view_counterfait") else None,
                    "edit_url": counterfait_money.get_edit_url() if counterfait_money and self.request.user.has_perm("cctv.change_counterfait") else None,
                    "delete_url":counterfait_money.get_delete_url() if counterfait_money and self.request.user.has_perm("cctv.delete_counterfait") else None,
                } for counterfait_money in counterfait_money]

                return JsonResponse({
                    "draw": draw,
                    "recordsTotal": total_records,
                    "recordsFiltered": filtered_records,
                    "data": data,
                })

            return super().render_to_response(context, **response_kwargs)
   
class CreateCounterfaitView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,CreateView):
     login_url = '/accounts/login/'
     redirect_field_name = 'redirect_to' 
     model=Counterfait
     template_name = 'counterfeit/create-counterfeit.html'
     form_class = CounterfaitForm  
     success_url = reverse_lazy("counterfeit-list") 
     permission_required = 'cctv.add_counterfait'
     success_message = "The Counterfeit was Added successfully."
      
     def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location           
         except UserProfile.DoesNotExist:
                return self.form_invalid(form)  
         if 'save_and_continue' in self.request.POST:
             form.instance.location = userprofile or self.get_initial().get('location_id')
             form.save()
             messages.success(self.request, "The Daily Shift  was Added successfully.You can continue adding!")
             return redirect('counterfeit-create')          
       
         form.instance.location = userprofile
         return super().form_valid(form)


     def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile or some validation failed.")
        return super().form_invalid(form)	   
     
     def get_initial(self):
        initial = super().get_initial()
        initial['date'] = datetime.datetime.now()
        initial['time'] = datetime.datetime.now()
        if self.request.user.is_superuser:
            initial['location_id']=None
        else:
            initial['location_id'] = self.request.user.userprofile.location_id       
        return initial
     
   

class UpdateCounterfaitView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
      login_url = '/accounts/login/'
      redirect_field_name = 'redirect_to' 
      model=Counterfait
      template_name = 'counterfeit/update-counterfeit.html'
      form_class =CounterfaitForm   
      success_url = reverse_lazy("counterfeit-list")  
      permission_required = 'cctv.change_counterfait'
      success_message = "The Counterfeit was Updated successfully."


      def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location
           
         except UserProfile.DoesNotExist:
              
                return self.form_invalid(form)          
       
         form.instance.location = userprofile
       
         return super().form_valid(form)


      def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile or some validation failed.")
        return super().form_invalid(form)
      
      def get_initial(self):      
        initial = super().get_initial()        
        if self.request.user.is_superuser:
            initial['location_id']=None
        else:
            initial['location_id'] = self.request.user.userprofile.location_id         
       
       
        return initial	    
      
class DeleteCounterfaitView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
       login_url = '/accounts/login/'
       redirect_field_name = 'redirect_to' 
       model=Counterfait
       context_object_name = 'counterfeit'
       template_name='counterfeit/confirm_delete.html'   
       success_url = reverse_lazy("counterfeit-list")
       permission_required = 'cctv.delete_counterfait'
    
       success_message = "The Counterfeit was Added successfully."
      
       def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location
           
         except UserProfile.DoesNotExist:
                
                return self.form_invalid(form)          
       
       
       
         return super().form_valid(form)


       def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile or some validation failed.")
        return super().form_invalid(form)	   

       
class DetailCounterfaitView(LoginRequiredMixin,PermissionRequiredMixin,DetailView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to' 
    model = Counterfait
    context_object_name = 'counterfeit'
    template_name='counterfeit/detail-counterfeit.html'   
    success_url = reverse_lazy("counterfeit-list")
    permission_required = 'cctv.view_counterfait'

@login_required
def FilterCounterfaitByDateView(request):
     if request.user.is_superuser:
         counterfeit=Counterfait.objects.all()
         user_location=''
     else:
         counterfeit=Counterfait.objects.filter(location=request.user.userprofile.location)
         user_location=request.user.userprofile.location

     form=FilterCounterfaitDate(request.GET or None,  initial={'location': user_location})

     if form.is_valid(): 
        
        date_begin = form.cleaned_data.get('date_begin')      
        date_end = form.cleaned_data.get('date_end')        
        if date_begin and date_end :        
          counterfeit=counterfeit.filter(date__range=(date_begin, date_end))    
     return render(request, 'counterfeit/filter_counterfeit_day.html', {'form': form, 'counterfeit': counterfeit})  


#Daily Exeption****Begin
 
class ListDailyExeptionView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
     login_url = '/accounts/login/'
     redirect_field_name = 'redirect_to' 
     template_name='daily_exeption/list-daily_exeption.html'
     model=DailyExeption
     permission_required = 'cctv.view_dailyexeption'
  
     def dispatch(self, request, *args, **kwargs): 
          if not hasattr(request.user, 'userprofile') and not self.request.user.is_superuser:
            messages.error(self.request, "No profile associated with the user was found")
            return redirect(self.login_url)
            
          return super().dispatch(request, *args, **kwargs)


   #  def get_queryset(self):
        

     #   if self.request.user.is_superuser:
    #         qs=DailyExeption.objects.all()
   #     else:           
   #         qs=DailyExeption.objects.filter(location=self.request.user.userprofile.location) 
            
        
   #     return qs
     def get_queryset(self):    
        if self.request.user.is_superuser:
             queryset=DailyExeption.objects.all()
        else:           
            queryset=DailyExeption.objects.filter(location=self.request.user.userprofile.location) 
         
        search_value=self.request.GET.get('search[value]','').strip()      
        """ Este search_value es para buscar en el datatable"""
   
        if search_value:
            queryset=queryset.annotate(
                employee_fullname=Trim(
                    Concat(
                        Coalesce(F('employee__name'),Value('')),
                        Value(' '),
                        Coalesce(F('employee__surname'), Value('')),
                         output_field=CharField()
                          )
                          )
                          )
             
            
            queryset=queryset.filter(
                    Q(id__icontains=search_value)|                  
                    Q(date__icontains=search_value)|
                    Q(location__location__icontains=search_value)| 
                    Q(employee_fullname__icontains=search_value)|
                    Q(exception_type__exeption_type__icontains=search_value)|
                    Q(daily_from__icontains=search_value)|
                    Q(daily_to__icontains=search_value)|
                    Q(detail__icontains=search_value)
                      
                    )
            
        order_column_index = self.request.GET.get('order[0][column]', '0')
        order_dir = self.request.GET.get('order[0][dir]', 'asc')        

        column_map = {
                '0': 'id',
                '1':'date',
                '2': 'employee__name',  
                '3': 'exception_type__exception_type',  
                '4': 'daily_from',  
                '5': 'daily_to',  
                '6': 'detail',         
                '7':'location__location'
            }


        order_field = column_map.get(order_column_index, 'id')
        if order_dir == 'desc':
            order_field = f"-{order_field}"
        queryset = queryset.order_by(order_field)                 
        return queryset

     def render_to_response(self, context, **response_kwargs):
            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                draw = int(self.request.GET.get('draw', 1))
                start = int(self.request.GET.get('start', 0))
                length = int(self.request.GET.get('length', 10))

                queryset = self.get_queryset()
               
                total_records = DailyExeption.objects.count()
                filtered_records = queryset.count()

                daily_exception = queryset[start:start+length]

                data = [{
                    "id": daily_exception.id,                  
                    "date": daily_exception.date,
                    "employee":str( daily_exception.employee),
                    "exception_type": str(daily_exception.exception_type) if daily_exception.exception_type else "",
                    "daily_from": str(daily_exception.daily_from) if daily_exception.daily_from else "",
                    "daily_to": daily_exception.daily_to if daily_exception.daily_to else "",
                    "detail": daily_exception.detail if daily_exception.detail else "",                  
                    "location": str(daily_exception.location) ,                    
                    "detail_url": daily_exception.get_absolute_url() if daily_exception and self.request.user.has_perm("cctv.view_dailyexeption") else None,
                    "edit_url": daily_exception.get_edit_url() if daily_exception and self.request.user.has_perm("cctv.change_dailyexeption") else None,
                    "delete_url":daily_exception.get_delete_url() if daily_exception and self.request.user.has_perm("cctv.delete_dailyexeption") else None,
                } for daily_exception in daily_exception]
               
                return JsonResponse({
                    "draw": draw,
                    "recordsTotal": total_records,
                    "recordsFiltered": filtered_records,
                    "data": data,
                })

            return super().render_to_response(context, **response_kwargs)
  
class CreateDailyExeptionView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,CreateView):
     login_url = '/accounts/login/'
     redirect_field_name = 'redirect_to' 
     model=DailyExeption
     template_name = 'daily_exeption/create-daily_exeption.html'
     form_class = CreateDailyExeptionForm    
     success_url = reverse_lazy("daily_exeption-list") 
     permission_required = 'cctv.add_dailyexeption'
     success_message = "The Daily Exeption was Added successfully."
      
     def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location           
         except UserProfile.DoesNotExist:               
                return self.form_invalid(form)          
             
         if 'save_and_continue' in self.request.POST:
             form.instance.location = userprofile or self.get_initial().get('location_id')
             form.save()
             messages.success(self.request, "The Daily Exeption  was Added successfully.You can continue adding!")
             return redirect('daily_exeption-create')  
        
         form.instance.location = userprofile
         return super().form_valid(form)


     def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
        return super().form_invalid(form)	 

     def get_initial(self):
        initial = super().get_initial()
        initial['date'] = datetime.datetime.now()
        
        if self.request.user.is_superuser:
            initial['location_id']=None
        else:
            initial['location_id'] = self.request.user.userprofile.location_id         
       
        return initial  

class UpdateDailyExeptionView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
      login_url = '/accounts/login/'
      redirect_field_name = 'redirect_to' 
      model=DailyExeption
      template_name = 'daily_exeption/update-daily_exeption.html'
      form_class = CreateDailyExeptionForm   
      success_url = reverse_lazy("daily_exeption-list")
      permission_required = 'cctv.change_dailyexeption'
      success_message = "The Daily Exeption was Updated successfully."

      def get_initial(self):      
        initial = super().get_initial()        
        if self.request.user.is_superuser:
            initial['location_id']=None
        else:
            initial['location_id'] = self.request.user.userprofile.location_id           
        return initial
      
      def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location
           
         except UserProfile.DoesNotExist:
               
                return self.form_invalid(form)          
       
         form.instance.location = userprofile
       
         return super().form_valid(form)


      def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
        return super().form_invalid(form)	   
      
class DeleteDailyExeptionView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
       login_url = '/accounts/login/'
       redirect_field_name = 'redirect_to' 
       model=DailyExeption
       context_object_name = 'daily_exeption'
       template_name='daily_exeption/confirm_delete.html'   
       success_url = reverse_lazy("daily_exeption-list")
       permission_required = 'cctv.delete_dailyexeption'
    
       success_message = "The Daily Exeption was Deleted successfully."
      
       def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location
           
         except UserProfile.DoesNotExist:
               
                return self.form_invalid(form)          
       
  
       
         return super().form_valid(form)


       def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
        return super().form_invalid(form)	   
       
class DetailDailyExeptionView(LoginRequiredMixin,PermissionRequiredMixin,DetailView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to' 
    model = DailyExeption
    context_object_name = 'daily_exeption'
    template_name='daily_exeption/detail-daily_exeption.html'   
    success_url = reverse_lazy("daily_exeption-list")
    permission_required = 'cctv.view_dailyexeption'

@login_required
def FilterDailyExeptionByDateView(request):
    if request.user.is_superuser:
        daily_exeption=DailyExeption.objects.all()
        user_location=''
    else:
        daily_exeption=DailyExeption.objects.filter(location=request.user.userprofile.location)
        user_location=request.user.userprofile.location
   
    form=FilterDailyExeptionByDate(request.GET or None,  initial={'location': user_location})

    if form.is_valid(): 
        
        date_begin = form.cleaned_data.get('date_begin')      
        date_end = form.cleaned_data.get('date_end')   
        exclude=form.cleaned_data.get('exclude')  
             
        if date_begin and date_end :
          daily_exeption=daily_exeption.filter(date__range=(date_begin, date_end))  

        if exclude:
            excluded_departments = [11] 
            daily_exeption=daily_exeption.exclude(employee__department_id__in=excluded_departments)        

    
    return render(request, 'daily_exeption/find_daily_exeption_by_date.html', {'form': form, 'daily_exeption': daily_exeption})

@login_required
def FilterDailyExeptionByEmployeeView(request):
    if request.user.is_superuser:
        daily_exeption=DailyExeption.objects.all()
        user_location=''
    else:
        daily_exeption=DailyExeption.objects.filter(location=request.user.userprofile.location)
        user_location=request.user.userprofile.location    

    form=FilterDailyExeptionByEmployee(request.GET or None,  initial={'location': user_location})

    if form.is_valid():
        employee_id = form.cleaned_data.get('employee')
        date_begin = form.cleaned_data.get('date_begin')      
        date_end = form.cleaned_data.get('date_end')  
       
        if date_begin and date_end :        
          daily_exeption=daily_exeption.filter(date__range=(date_begin, date_end))   
        if daily_exeption :        
          daily_exeption=daily_exeption.filter(employee_id__exact=employee_id)
    
    return render(request, 'daily_exeption/find_daily_exeption_by_employee.html', {'form': form, 'daily_exeption': daily_exeption})

@login_required
def FilterDailyExeptionByTypeView(request):
    if request.user.is_superuser:
        daily_exeption=DailyExeption.objects.all()
        user_location=''
    else:
        daily_exeption=DailyExeption.objects.filter(location=request.user.userprofile.location)
        user_location=request.user.userprofile.location    
    
    form=FilterDailyExeptionByType(request.GET or None,initial={'location':user_location })
    if form.is_valid():
        exeption_type = form.cleaned_data.get('type')
        date_begin = form.cleaned_data.get('date_begin')      
        date_end = form.cleaned_data.get('date_end')  
        if date_begin and date_end :        
          daily_exeption=daily_exeption.filter(date__range=(date_begin, date_end))       
        
        if exeption_type :        
          daily_exeption=daily_exeption.filter(exception_type__exact=exeption_type)    
    return render(request, 'daily_exeption/find_by_exeption_type.html', {'form': form, 'daily_exeption': daily_exeption})
#Daily Exeption****End

#Department

class ListDepartmentView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
   login_url = '/accounts/login/'
   redirect_field_name = 'redirect_to' 
   template_name='department/list-department.html'
   model=Department
   permission_required = 'cctv.view_department'

   def dispatch(self, request, *args, **kwargs): 
          if not hasattr(request.user, 'userprofile') and not self.request.user.is_superuser:
            messages.error(self.request, "No profile associated with the user was found")
            return redirect(self.login_url)            
          return super().dispatch(request, *args, **kwargs)    
   
   def get_queryset(self):
        qs=Department.objects.all()
        return qs

class CreateDepartmentView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,CreateView):
     login_url = '/accounts/login/'
     redirect_field_name = 'redirect_to' 
     model=Department
     template_name = 'department/create-department.html'
     form_class = CreateDepartmentForm    
     success_url = reverse_lazy("department-list") 
     permission_required = 'cctv.add_department'

     success_message = "The Department was Added successfully."
      
     def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location
           
         except UserProfile.DoesNotExist:
                messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
                return self.form_invalid(form)          
       
         form.instance.location = userprofile
       
         return super().form_valid(form)


     def form_invalid(self, form):
        messages.error(self.request, "There was an error submitting the form.")
        return super().form_invalid(form)	   
   
class UpdateDepartmentView(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
      login_url = '/accounts/login/'
      redirect_field_name = 'redirect_to' 
      model=Department
      template_name = 'department/update-department.html'
      form_class = CreateDepartmentForm   
      success_url = reverse_lazy("department-list") 
      permission_required = 'cctv.change_department'
      success_message = "The Department was Updated successfully."
    

      def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location
           
         except UserProfile.DoesNotExist:
                messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
                return self.form_invalid(form)          
       
         form.instance.location = userprofile
       
         return super().form_valid(form)


      def form_invalid(self, form):
        messages.error(self.request, "There was an error submitting the form.")
        return super().form_invalid(form)	   
class DeleteDepartmentView(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
       login_url = '/accounts/login/'
       redirect_field_name = 'redirect_to' 
       model=Department
       context_object_name = 'department'
       template_name='department/confirm_delete.html'   
       success_url = reverse_lazy("department-list")
       permission_required = 'cctv.delete_department'
    
       success_message = "The Department was Deleted successfully."
       error_message = (
            "Cannot delete the Department '{name}' because it is related to other records: {details}."
              )
       

       def post(self, request, *args, **kwargs):
                self.object = self.get_object()  # Obtener el objeto a eliminar
              
                try:
                    # Intentar eliminar el objeto
                    self.object.delete()
                    messages.success(request, self.success_message)
                    return redirect(self.success_url)
                except ProtectedError as e:
                 
                    related_objects = ', '.join(str(obj) for obj in e.protected_objects)
                    
                    error_message = self.error_message.format(name=str(self.object), details=related_objects)
                    messages.error(request, error_message)
                    return redirect(self.success_url)

class DetailDepartmentView(LoginRequiredMixin,PermissionRequiredMixin,DetailView):
        login_url = '/accounts/login/'
        redirect_field_name = 'redirect_to' 
        model = Department
        context_object_name = 'department'
        template_name='department/detail-department.html'   
        success_url = reverse_lazy("department-list")
        permission_required = 'cctv.view_department'

#Position******Begin
class ListPositionView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
   
   login_url = '/accounts/login/'
   redirect_field_name = 'redirect_to'
   template_name='position/list-position.html'
   model=Position
   permission_required = 'cctv.view_position'


   def dispatch(self, request, *args, **kwargs): 
          if not hasattr(request.user, 'userprofile') and not self.request.user.is_superuser:
            messages.error(self.request, "No profile associated with the user was found")
            return redirect(self.login_url)
          return super().dispatch(request, *args, **kwargs)

   def get_queryset(self):
        qs=Position.objects.all()
        return qs
     
class CreatePositionView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,CreateView):
     login_url = '/accounts/login/'
     redirect_field_name = 'redirect_to'
     model=Position
     template_name = 'position/create-position.html'
     form_class = CreatePositionForm    
     success_url = reverse_lazy("position-list") 
     permission_required = 'cctv.add_position'
     success_message = "The Position was Added successfully."
      
     def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location
           
         except UserProfile.DoesNotExist:
                
                return self.form_invalid(form)          
       
         form.instance.location = userprofile
       
         return super().form_valid(form)


     def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
        return super().form_invalid(form)	   

class UpdatePositionView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
      login_url = '/accounts/login/'
      redirect_field_name = 'redirect_to'
      model=Position
      template_name = 'position/update-position.html'
      form_class = CreatePositionForm   
      success_url = reverse_lazy("position-list") 
      permission_required = 'cctv.change_position'
      success_message = "The Position was Updated successfully."
      
      def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location
           
         except UserProfile.DoesNotExist:
               
                return self.form_invalid(form)          
       
         form.instance.location = userprofile
       
         return super().form_valid(form)


      def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
        return super().form_invalid(form)	   

class DeletePositionView(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
       login_url = '/accounts/login/'
       redirect_field_name = 'redirect_to'     
       model=Position
       context_object_name = 'position'
       template_name='position/confirm_delete.html'   
       success_url = reverse_lazy("position-list")
       permission_required = 'cctv.delete_position'
    
       success_message = "The Position was Deleted successfully."
      
      
       error_message = (
            "Cannot delete the Position'{name}' because it is related to other records: {details}."
              )
       

       def post(self, request, *args, **kwargs):
                self.object = self.get_object()  # Obtener el objeto a eliminar
              
                try:
                    # Intentar eliminar el objeto
                    self.object.delete()
                    messages.success(request, self.success_message)
                    return redirect(self.success_url)
                except ProtectedError as e:
                 
                    related_objects = ', '.join(str(obj) for obj in e.protected_objects)
                    
                    error_message = self.error_message.format(name=str(self.object), details=related_objects)
                    messages.error(request, error_message)
                    return redirect(self.success_url)
       

class DetailPositionView(LoginRequiredMixin,PermissionRequiredMixin,DetailView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to' 
    model = Position
    context_object_name = 'position'
    template_name='position/detail-position.html'   
    success_url = reverse_lazy("position-list")
    permission_required = 'cctv.view_position'
       
@login_required   
def LoadPosition(request):   
     id = request.GET.get('id')  
     name = Position.objects.filter(department_id=id).values('id', 'name')
   
     return JsonResponse(list(name), safe=False)
#Position******



#Supplies

class SuppliesListView(ListView,LoginRequiredMixin,PermissionRequiredMixin):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to' 
    model = Supplies
    template_name = 'supplies/supplies_list.html'  # Plantilla para mostrar la lista
    context_object_name = 'supplies'  # Nombre del contexto en la plantilla
    success_url = reverse_lazy("supplies_list")
    permission_required = 'cctv.view_supplies'

    def get_queryset(self):
        if self.request.user.is_superuser:
            qs=Supplies.objects.all()
        else:
            qs=Supplies.objects.filter(branch=self.request.user.userprofile.location)
        return qs

class SuppliesDetailView(DetailView,LoginRequiredMixin,PermissionRequiredMixin):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to' 
    model = Supplies
    template_name = 'supplies/supplies_detail.html'  # Plantilla para mostrar los detalles
    context_object_name = 'supply'
    success_url = reverse_lazy("supplies_list")
    permission_required = 'cctv.view_supplies'
    

class SuppliesCreateView(CreateView,LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    model = Supplies
    template_name = 'supplies/supplies_form.html'  # Plantilla del formulario
    form_class = CreateSuppliesForm      
    success_url = reverse_lazy('supplies_list')  # Redirigir después de crear
    permission_required = 'cctv.add_supplies'
    success_message = "The Supplies was Added successfully."

    def form_valid(self, form):
         try:
            userprofile = self.request.user.userprofile.location           
         except UserProfile.DoesNotExist:               
                return self.form_invalid(form)          
             
         if 'save_and_continue' in self.request.POST:
             form.instance.branch = userprofile or self.get_initial().get('location_id')
             form.save()
             messages.success(self.request, "The Supplies was Added successfully.You can continue adding!")
             return redirect('supplies_create')  
        
         form.instance.branch = userprofile
         return super().form_valid(form)


    def form_invalid(self, form):
        messages.error(self.request, "You do not have an associated profile. Please create a profile first.")
        return super().form_invalid(form)	 

    def get_initial(self):
        initial = super().get_initial()
      #  initial['date'] = datetime.datetime.now()
        
        if self.request.user.is_superuser:
            initial['branch_id']=None
        else:
            initial['branch_id'] = self.request.user.userprofile.location_id         
       
        return initial  
  
class SuppliesUpdateView(UpdateView,LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin):
    model = Supplies
    template_name = 'supplies/supplies_form.html'  # Usamos el mismo formulario
    form_class = CreateSuppliesForm  
    success_url = reverse_lazy('supplies_list')
    permission_required = 'cctv.change_supplies'
    success_message = "The Supplies was Updated successfully."


class SuppliesDeleteView(DeleteView,LoginRequiredMixin,PermissionRequiredMixin):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'    
    model = Supplies
    template_name = 'supplies/supplies_confirm_delete.html'  # Confirmación antes de eliminar
    success_url = reverse_lazy('supplies_list')
    permission_required = 'cctv.delete_supplies'
    success_message = "The Supplies was Deleted successfully."
    context_object_name = 'supplies'

@login_required
def SynopsisSupplies(request):
    if request.user.is_superuser:
        supplies=Supplies.objects.all().order_by('-id')
        branch=None
    else:
        supplies=Supplies.objects.filter(branch=request.user.userprofile.location).order_by('-id')
        branch=request.user.userprofile.location    

    form=Synopsis_Supplies(request.GET or None,  initial={'branch': branch})
  
    if form.is_valid():
        department = form.cleaned_data.get('department')
        date_begin = form.cleaned_data.get('date_begin')      
        date_end = form.cleaned_data.get('date_end') 
        prepared_by = form.cleaned_data.get('prepared_by')
        approved_by = form.cleaned_data.get('approved_by')
        request_for= form.cleaned_data.get('request_for')
        
       
        if date_begin and date_end :        
          supplies=supplies.filter(date__range=(date_begin, date_end))   
        if department :        
          supplies=supplies.filter( department_id__exact=department)
        if prepared_by :        
          supplies=supplies.filter( prepared_by_id__exact=prepared_by)
        if approved_by :        
          supplies=supplies.filter( approved_by_id__exact=approved_by)
        if request_for :
             
          supplies=supplies.filter( request_for__exact=request_for)

    return render(request, 'supplies/synopsis_supplies.html', {'form': form, 'supplies': supplies})
    