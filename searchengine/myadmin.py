from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
       
	def reset_password(self, request, user_id):
        	if not self.has_change_permission(request):
                	raise PermissionDenied
            	user = get_object_or_404(self.model, pk=user_id)

            	#form = PasswordResetForm(data={'email': user.email})
            	#form.is_valid()
		print 'bang'
           	#form.save(email_template_name='my_template.html')
            	return HttpResponseRedirect('/login')

        def get_urls(self):
            	urls = super(UserAdmin, self).get_urls()
	
            	my_urls = patterns('',
                (r'^(\d+)/reset-password/$',
                   self.admin_site.admin_view(self.reset_password)
                	),
            	)
            	return my_urls + urls
