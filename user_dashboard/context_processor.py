from django.conf import settings
#from django.utils import timezone
#from datetime import  timedelta
from .models import Notification



def user_notification_processor(request):
    user = request.user
    if user.is_authenticated:
        user_notify = Notification.objects.filter(user=request.user).order_by('-date')[:3]
        user_notify_count = Notification.objects.filter(user=request.user,read=False).count()
        return {"user_notify": user_notify,"user_notify_count":user_notify_count}
    else:
        return {"user_notify": "user_notify"}
