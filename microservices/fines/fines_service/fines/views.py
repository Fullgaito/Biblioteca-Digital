from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Fine
from django.utils import timezone

@api_view(['POST'])
def create_fine(request):
    user_id = request.data.get('user_id')
    loan_id = request.data.get('loan_id')
    days_late = request.data.get('days_late')

    if not all([user_id, loan_id, days_late]):
        return Response({'error': 'Missing fields'}, status=400)

    amount = days_late * 580

    fine = Fine.objects.create(
        user_id=user_id,
        loan_id=loan_id,
        days_late=days_late,
        amount=amount
    )

    return Response({'message': 'Fine created', 'id': fine.id}, status=201)


@api_view(['GET'])
def get_user_fines(request, user_id):
    fines = Fine.objects.filter(user_id=user_id)
    data = list(fines.values())
    return Response(data)


@api_view(['PUT'])
def pay_fine(request, id):
    try:
        fine = Fine.objects.get(id=id)

        if fine.status == 'paid':
            return Response({'error': 'Already paid'}, status=400)

        fine.status = 'paid'
        fine.paid_at = timezone.now()
        fine.save()

        return Response({'message': 'Fine paid'})

    except Fine.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)
