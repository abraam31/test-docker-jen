from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Login_User)

# admin.site.register(Question)
# admin.site.register(Answer)
# admin.site.register(Hint)


admin.site.register(Password_Reset)
admin.site.register(Folder)
admin.site.register(SetTable)
admin.site.register(Category)
admin.site.register(CardContent)
admin.site.register(UserVoiceInput)
admin.site.register(ReportResult)
