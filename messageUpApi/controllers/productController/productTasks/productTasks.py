# api/controllers/productController/productTasks/productTasks.py
from messageUpApi.models import (
    Product,
    ProductCategory,
    ProductImage,
    Business,
)
from django.core.paginator import Paginator
from django.utils.text import slugify

def serialize_product(product):
    return {
        "name": product.name,
        "slug": product.slug,
        "image": product.image.url if product.image else None,
        "category": product.category.label,
        "price": product.price,
        "description": product.description,
        "business_name": product.business.name,
        "productimages": [
            img.image.url for img in product.images.all()
        ],
    }


def get_product_task(slug, params):
    try:
        product = Product.objects.get(slug=slug, available=True)
        return True, serialize_product(product), 200
    except Product.DoesNotExist:
        return False, {"error": "product_not_found"}, 404


def get_business_products_task(user=None, slug=None):
    business = None
    try:
        business = Business.objects.get(user=user)
    except Business.DoesNotExist:
        pass
    qs = None

    if business:
        qs = Product.objects.filter(business=business)
    qs = Product.objects.filter(available=True)
    if slug:
        try:
            product = qs.get(slug=slug)
            return True, serialize_product(product), 200
        except Product.DoesNotExist:
            return False, {"error": "product_not_found"}, 404

    return True, [serialize_product(p) for p in qs], 200


def create_product_task(user, data):
    try:
        business = Business.objects.get(user=user)
        category = ProductCategory.objects.get(id=data["category"])

        product = Product.objects.create(
            name=data["name"],
            slug=slugify(data["name"]),
            image=data.get("image"),
            category=category,
            price=data["price"],
            available=data.get("available", True),
            description=data.get("description", ""),
            business=business,
        )

        for img in data.get("images", []):
            ProductImage.objects.create(product=product, image=img)

        return True, serialize_product(product), 201
    except Exception:
        return False, {"error": "invalid_data"}, 400


def update_product_task(user, slug, data):
    try:
        product = Product.objects.get(
            slug=slug,
            business__user=user,
        )
        for k, v in data.items():
            if k == "name":
                setattr(product, "slug", slugify(v))
            setattr(product, k, v)
        product.save()
        return True, serialize_product(product), 200
    except Product.DoesNotExist:
        return False, {"error": "product_not_found"}, 404


def delete_product_task(user, slug):
    try:
        Product.objects.get(
            slug=slug,
            business__user=user,
        ).delete()
        return True, None, 204
    except Product.DoesNotExist:
        return False, {"error": "product_not_found"}, 404


def get_products_by_category_task(category_id, params):
    qs = Product.objects.filter(
        category_id=category_id,
        available=True,
    ).order_by("-created_at")

    page = int(params.get("page", 1))
    size = int(params.get("size", 10))

    paginator = Paginator(qs, size)
    page_obj = paginator.get_page(page)

    return True, {
        "count": paginator.count,
        "page": page,
        "results": [serialize_product(p) for p in page_obj],
    }, 200


def get_business_by_category_task(category_id, params):
    qs = Business.objects.filter(
        category_id=category_id,
    ).order_by("-created_at")

    page = int(params.get("page", 1))
    size = int(params.get("size", 10))

    paginator = Paginator(qs, size)
    page_obj = paginator.get_page(page)

    data = []
    for b in page_obj:
        data.append({
            "name": b.name,
            "slug": b.slug,
            "address": b.address,
            "profile": b.profile.url if b.profile else None,
        })

    return True, {
        "count": paginator.count,
        "page": page,
        "results": data,
    }, 200
