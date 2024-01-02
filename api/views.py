from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from api.serializers import RecordSerializer
from records.models import Record


@api_view(['GET'])
def get_response(request):
    routes = [
        {'GET': '/api/records'},
        {'GET': '/api/records/id'},
        {'POST': '/api/users/token'},
        {'POST': 'api/users/token/refresh'},
    ]

    return Response(routes)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_records(request):
    records = Record.objects.all()
    serializer = RecordSerializer(records, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_record(request, pk):
    record = get_object_or_404(Record, id=pk)
    serializer = RecordSerializer(record, many=False)
    return Response(serializer.data)
