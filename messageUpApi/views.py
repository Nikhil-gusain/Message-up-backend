# api/views.py
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response

from .controllers.businessController.businessController import business_controller, getBusinessData
from .controllers.statusController.statusController import status_controller
from .controllers.cartController.cartController import cart_controller
from .controllers.orderController.orderController import (
    user_order_controller,
    business_order_controller,
)
from .controllers.productController.productController import (
    product_controller,
    business_product_controller,
    product_by_category_controller,
    business_by_category_controller,
)

from .controllers.metaController.metaController import (
    business_category_controller,
    product_category_controller,
    user_type_controller,
)

from .controllers.authController.authController import google_auth_controller

class BusinessAPI(APIView):
    def get(self, request, slug=None):
        user = None
        if request.user.is_authenticated:
            user = request.user
        ok, data, code = business_controller("GET", request, slug,user)
        return Response(data, status=code)

    def post(self, request):
        ok, data, code = business_controller("POST", request, None)
        return Response(data, status=code)

    def put(self, request):
        ok, data, code = business_controller("PUT", request, None)
        return Response(data, status=code)

    def delete(self, request):
        ok, data, code = business_controller("DELETE", request, None)
        return Response(data, status=code)



class StatusAPI(APIView):
    
    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request, slug):
        
        ok, data, code = status_controller("GET", request, slug)
        return Response(data, status=code)

    def post(self, request):
        ok, data, code = status_controller("POST", request, None)
        return Response(data, status=code)

    def delete(self, request):
        ok, data, code = status_controller("DELETE", request, None)
        return Response(data, status=code)


class CartAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ok, data, code = cart_controller("GET", request, None)
        return Response(data, status=code)

    def put(self, request):
        ok, data, code = cart_controller("PUT", request, None)
        return Response(data, status=code)

    def delete(self, request, item_id=None):
        ok, data, code = cart_controller("DELETE", request, item_id)
        return Response(data, status=code)


class UserOrderAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ok, data, code = user_order_controller("GET", request)
        return Response(data, status=code)

    def post(self, request):
        ok, data, code = user_order_controller("POST", request)
        return Response(data, status=code)


class BusinessOrderAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ok, data, code = business_order_controller("GET", request)
        return Response(data, status=code)

    def put(self, request):
        ok, data, code = business_order_controller("PUT", request)
        return Response(data, status=code)


class ProductAPI(APIView):

    def get(self, request, slug=None):
        ok, data, code = product_controller("GET", request, slug)
        return Response(data, status=code)


class BusinessProductAPI(APIView):

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request, slug=None):
        user = None
        if request.user.is_authenticated:
            user = request.user
        ok, data, code = business_product_controller("GET", request, slug,user)
        return Response(data, status=code)

    def post(self, request):
        ok, data, code = business_product_controller("POST", request, None)
        return Response(data, status=code)

    def put(self, request, slug):
        ok, data, code = business_product_controller("PUT", request, slug)
        return Response(data, status=code)

    def delete(self, request, slug):
        ok, data, code = business_product_controller("DELETE", request, slug)
        return Response(data, status=code)


class ProductByCategoryAPI(APIView):
    def get(self, request, category_id):
        ok, data, code = product_by_category_controller(category_id, request)
        return Response(data, status=code)


class BusinessByCategoryAPI(APIView):
    def get(self, request, category_id):
        ok, data, code = business_by_category_controller(category_id, request)
        return Response(data, status=code)



class GoogleAuthAPI(APIView):
    def post(self, request):
        ok, data, code = google_auth_controller(request.data)
        return Response(data, status=code)

class BusinessCategoryAPI(APIView):
    def get(self, request):
        ok, data, code = business_category_controller(request)
        return Response(data, status=code)


class ProductCategoryAPI(APIView):
    def get(self, request):
        ok, data, code = product_category_controller(request)
        return Response(data, status=code)


class UserTypeAPI(APIView):
    def get(self, request):
        ok, data, code = user_type_controller(request)
        return Response(data, status=code)
    

@api_view(['GET'])
def getBusiness(request):
    data=[]
    user = None
    if request.user.is_authenticated:
        user = request.user
    ok, data, code = getBusinessData(user)
    return Response(data, status=code)