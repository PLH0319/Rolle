from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from .models import ModelActivity

class OperationView(LoginRequiredMixin, TemplateView):
    template_name = '1_operation.html'
    Activities = ModelActivity.objects.none()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Activities'] = self.Activities
        # additional context data if needed
        return context

def delete_data(request):
    if request.method == 'POST':
        # process delete request here
        # Example: Delete data based on ID
        data_id = request.POST.get('data_id')
        # Your delete logic here
        return JsonResponse({'message': 'Data deleted successfully.'})
    return JsonResponse({'error': 'Method not allowed.'}, status=405)

def query_data(request):
    # Example query API, accessible to logged-in and non-logged-in users
    if request.method == 'GET':
        # Your query logic here
        Activities = ModelActivity.objects.all()
        Activities = list(Activities.values('UID','title','startDate','endDate'))
        print(Activities)
        # data = {'result': 'This is the queried data.'}
        return JsonResponse(Activities, safe=False)
    return JsonResponse({'error': 'Method not allowed.'}, status=405)

def modify_data(request):
    if request.method == 'POST':
        # process modify request here
        # Example: Update data based on ID
        data_id = request.POST.get('data_id')
        new_data = request.POST.get('new_data')
        # Your modify logic here
        return JsonResponse({'message': 'Data modified successfully.'})
    return JsonResponse({'error': 'Method not allowed.'}, status=405) 