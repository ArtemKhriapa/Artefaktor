from rest_framework.decorators import api_view

@api_view(['POST'])
def reg_try_request(request):
    if request.method == 'POST':
        return Response('Please check your mail box')
    return Response('Invalid data')