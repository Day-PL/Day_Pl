from django.contrib import admin
from .models import *

class MyModelAdmin(admin.ModelAdmin):
    list_display = ('name', )
    
    def delete_selected(self, request, queryset):
        for obj in queryset:
            obj.delete()
        self.message_user(request, f"선택한 {len(queryset)} 항목이 삭제되었습니다.")

    actions = [delete_selected]

admin.site.register(PlaceTypeCategory)
admin.site.register(PlaceType)
admin.site.register(Place, MyModelAdmin)
admin.site.register(Plan)
admin.site.register(UserPlanView)
admin.site.register(Preference)
admin.site.register(PlanPlace)
admin.site.register(PlaceComment)
admin.site.register(PlanComment)