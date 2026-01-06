# api/controllers/metaController/metaTasks/metaTasks.py
from messageUpApi.models import (
    BusinessCategory,
    ProductCategory,
    UserType,
)

# -------------------------
# Business Category
# -------------------------
def get_business_categories_task(params):
    qs = BusinessCategory.objects.all()
    print("QS: ", qs)
    if "value" in params:
        qs = qs.filter(value=params["value"])

    data = [{"id": c.id, "label": c.label, "value": c.value} for c in qs]
    print(data)
    return True, data, 200


# -------------------------
# Product Category
# -------------------------
def get_product_categories_task(params):
    qs = ProductCategory.objects.all()

    if "value" in params:
        qs = qs.filter(value=params["value"])

    data = [{"id": c.id, "label": c.label, "value": c.value} for c in qs]
    return True, data, 200


# -------------------------
# User Type
# -------------------------
def get_user_types_task(params):
    qs = UserType.objects.all()

    if "label" in params:
        qs = qs.filter(label=params["label"])

    data = [{"id": u.id, "name": u.name, "label": u.label} for u in qs]
    return True, data, 200
