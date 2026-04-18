# Name Classifier API

A Django REST API that classifies a given name using the Genderize API and returns a structured, processed response.

---

## 🚀 Project Overview

This API accepts a `name` as a query parameter, sends it to the external Genderize API, processes the response, and returns a cleaned and structured JSON output.

It includes:
- Input validation
- External API integration
- Data transformation
- Confidence logic
- Error handling
- Timestamp generation (UTC)

---

## 📌 Base URL
http://127.0.0.1:8000

If deployed:
https://your-domain.com

---

## 📡 API Endpoint

### GET `/api/classify`

### Example Request
/api/classify?name=John

---

## 📥 Query Parameters

| Parameter | Type | Required | Description |
|----------|------|----------|-------------|
| name | string | Yes | Name to classify |

---

## 📤 Successful Response

```json
{
  "status": "success",
  "data": {
    "name": "John",
    "gender": "male",
    "probability": 0.99,
    "sample_size": 1234,
    "is_confident": true,
    "processed_at": "2026-04-01T12:00:00Z"
  }
}
