from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import ModelActivity, ModelShowInfo

def ajax_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse(status=401)
    return wrapper

class OperationView(TemplateView):
    template_name = '1_operation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        Activities = ModelActivity.objects.all()
        Activities = list(Activities.values('id','UID','title','startDate','endDate'))
        context['Activities'] = Activities
        # additional context data if needed
        return context
    
@ajax_login_required
def delete_data(request):
    if request.method == 'POST':
        # process delete request here
        # Example: Delete data based on ID
        show_id = request.POST.get('show_id')
        show = ModelShowInfo.objects.get(id = show_id)
        show.delete()
        # Your delete logic here
        return JsonResponse({'message': 'Data deleted successfully.'})
    return JsonResponse({'error': 'Method not allowed.'}, status=405)

def query_data(request):
    # Example query API, accessible to logged-in and non-logged-in users
    if request.method == 'GET':
        # Your query logic here
        id = int(request.GET.get('id'))
        ShowInfo = ModelShowInfo.objects.filter(activity_id=id)
        ShowInfo = list(ShowInfo.values())

        for item in ShowInfo:
            endtime = item['endTime']
            item['endTime'] = '' if endtime is None else endtime
        return JsonResponse(ShowInfo, safe=False)
    return JsonResponse({'error': 'Method not allowed.'}, status=405)

@ajax_login_required
def modify_data(request):
    if request.method == 'POST':
        # process modify request here
        # Example: Update data based on ID
        show_id = request.POST.get('show_id')
        price = request.POST.get('price')
        # Your modify logic here
        show = ModelShowInfo.objects.get(id = show_id)
        show.price = int(price)
        show.save()
        return JsonResponse({'message': 'Data modified successfully.'})
    return JsonResponse({'error': 'Method not allowed.'}, status=405) 
