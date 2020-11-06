

def students_proc(request):
    return {'PORTAL_URL': request.build_absolute_uri('/')[:-1]}


# request.build_absolute_uri(location) - повертає абсолютний URL до location
# [:-1] - повертаємо значення без '/', щоб його не дублювати
