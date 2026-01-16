# messageUp API Documentation

This document provides a comprehensive guide to all API endpoints available in the messageUp platform.

## Table of Contents
1. [Authentication](#1-authentication)
2. [Business Management](#2-business-management)
3. [Product Management](#3-product-management)
4. [Category & Metadata](#4-category--metadata)
5. [Status (Stories)](#5-status-stories)
6. [Cart Management](#6-cart-management)
7. [Order Management](#7-order-management)
8. [Notifications & Chat (SSE)](#8-notifications--chat-sse)

---

## 1. Authentication

### Google Authentication
- **Endpoint**: `POST /api/auth/google/`
- **Auth Required**: No
- **Input (Required)**:
  - `id_token` (string): The Google ID token obtained from the frontend.
- **Example Request**:
  ```json
  {
    "id_token": "YOUR_GOOGLE_ID_TOKEN"
  }
  ```
- **Example Response**:
  ```json
  {
    "message": "Login successful",
    "user": {
      "id": 1,
      "email": "user@example.com",
      "name": "John Doe",
      "picture": "http://...",
      "is_new_user": false
    },
    "tokens": {
      "access": "...",
      "refresh": "..."
    }
  }
  ```
- **Notes**: Sets an `access_token` cookie (HttpOnly, Secure, Lax).

---

## 2. Business Management

### Get Business Profile (Self)
- **Endpoint**: `GET /api/business/profile/`
- **Auth Required**: Yes
- **Example Response**:
  ```json
  {
      "id": 1,
      "name": "My Cafe",
      "slug": "my-cafe",
      "description": "Best coffee in town",
      "address": "123 Coffee St",
      "phone": 1234567890,
      "category": { "id": 1, "label": "Cafe", "value": "cafe" },
      "profile": "/media/business/profile/img.jpg",
      "user": { "id": 1, "username": "user@example.com" }
  }
  ```

### Create Business
- **Endpoint**: `POST /api/business/`
- **Auth Required**: Yes
- **Input (Required)**:
  - `name` (string)
  - `description` (string)
  - `address` (string)
  - `phone` (number)
  - `category` (integer): ID of the BusinessCategory
  - `profile` (file): Image file
- **Notes**: Multipart/form-data required.

### Update Business
- **Endpoint**: `PUT /api/business/`
- **Auth Required**: Yes
- **Input (Optional)**:
  - `name`, `description`, `address`, `phone`, `category`, `profile`
- **Notes**: Only fields provided will be updated.

### Get Business by Slug
- **Endpoint**: `GET /api/business/<slug:slug>/`
- **Auth Required**: No (Optional for tracking)
- **Example Response**: Same as Business Profile.

---

## 3. Product Management

### Get Product Detail
- **Endpoint**: `GET /api/product/<slug:slug>/`
- **Auth Required**: No
- **Example Response**:
  ```json
  {
      "name": "Espresso",
      "slug": "espresso",
      "image": "/media/products/main/esp.jpg",
      "category": "Drinks",
      "price": 5,
      "description": "Pure caffeine",
      "business_name": "My Cafe",
      "productimages": ["/media/products/extra/1.jpg"]
  }
  ```

### List Products by Category
- **Endpoint**: `GET /api/product/category/<int:category_id>/`
- **Query Params**:
  - `page` (int, default: 1)
  - `size` (int, default: 10)

### Business: Manage Products
- **Endpoint**: `GET/POST/PUT/DELETE /api/business/product/` (or with `/<slug:slug>/`)
- **Auth Required**: Yes (Business Owner)
- **POST Input**: `name`, `price`, `category` (ID), `image` (file), `available` (bool, optional), `description` (optional), `images` (list of files, optional).

---

## 4. Category & Metadata

### List Business Categories
- **Endpoint**: `GET /api/categories/business/`
- **Query Params**: `value` (optional filter)

### List Product Categories
- **Endpoint**: `GET /api/categories/product/`
- **Query Params**: `value` (optional filter)

### List User Types
- **Endpoint**: `GET /api/user-types/`
- **Query Params**: `label` (optional filter)

---

## 5. Status (Stories)

### Get Business Statuses
- **Endpoint**: `GET /api/status/<slug:slug>/` (By slug for public) or `GET /api/status/` (For self)
- **Response**: List of images and IDs.

### Create Status
- **Endpoint**: `POST /api/status/`
- **Input**: `image` (file)

### Delete Status
- **Endpoint**: `DELETE /api/status/`
- **Input**: `{ "id": 123 }`

---

## 6. Cart Management

### Get Cart
- **Endpoint**: `GET /api/cart/`
- **Auth Required**: Yes

### Add/Update Cart Item
- **Endpoint**: `PUT /api/cart/`
- **Input**: `{ "product": "product-slug", "quantity": 2 }`

### Remove from Cart
- **Endpoint**: `DELETE /api/cart/` (Clear all) or `DELETE /api/cart/<int:item_id>/` (Remove specific)

---

## 7. Order Management

### User: List My Orders
- **Endpoint**: `GET /api/user/orders/`

### User: Create Order from Cart
- **Endpoint**: `POST /api/user/orders/`
- **Auth Required**: Yes (Requires non-empty cart)

### Business: List My Orders
- **Endpoint**: `GET /api/business/orders/`

### Business: Update Order Status
- **Endpoint**: `PUT /api/business/orders/`
- **Input**: `{ "order_id": 1, "status": "completed" }`

---

## 8. Notifications & Chat (SSE)

### SSE Endpoint (Real-time)
- **Endpoint**: `GET /sse/sse/`
- **Auth Required**: Yes (via `access_token` cookie)
- **Response**: Stream of `data: { ... }`

### List Chats
- **Endpoint**: `GET /sse/chats/`

### Send Message
- **Endpoint**: `POST /sse/chat/send/`
- **Input**: 
  - `message` (required)
  - `recipient_id` (OR `chat_id`)

### Get Messages
- **Endpoint**: `GET /sse/chat/<int:chat_id>/messages/`
- **Query Params**: `pageNo` (default: 1), `pageSize` (default: 20)
