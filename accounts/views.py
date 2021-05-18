from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .serializers import UserSerializer

# Create your views here.


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    # 클라이언트로부터 데이터 받아서
    password = request.data.get('password')
    password_confirmation = request.data.get('passwordConfirmation')
    # 패스워드 일치 여부 체크
    if password != password_confirmation:
        return Response({'error': '비밀번호가 일치하지 않습니다.'}, status=status.status.HTTP_400_BAD_REQUEST)

    # 데이터 직렬화
    serializer = UserSerializer(data=request.data)

    # validation
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        # 비밀번호 해싱 후 저장
        user.set_password(password)
        user.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
