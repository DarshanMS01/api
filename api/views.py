from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from students.models import Student

from .serializers import StudentSerializer


# @api_view takes a LIST of methods: ['GET', 'POST']
@api_view(['GET', 'POST'])
def studentsview(request):
    if request.method == 'GET':
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Give the browsable page a real HTML form (Student id / Name / Branch + POST).
# Function-based views don't expose one unless the view class has a serializer.
studentsview.cls.serializer_class = StudentSerializer

# Keep the browsable API page titled "Students" instead of "studentsview".
studentsview.cls.name = 'Students'


@api_view(['GET', 'PUT', 'DELETE'])
def student_detail(request, pk):
    try:
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        return Response(
            {'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        serializer = StudentSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


student_detail.cls.serializer_class = StudentSerializer
student_detail.cls.name = 'Student'
