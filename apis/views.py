import requests
from datetime import datetime, timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response

GENDERIZE_URL = "https://api.genderize.io"


def error_response(message, status_code):
    return Response(
        {"status": "error", "message": message},
        status=status_code,
        headers={"Access-Control-Allow-Origin": "*"}
    )


@api_view(['GET'])
def classify(request):
    name = request.query_params.get("name")

    # CLEAN VALIDATION (like FastAPI)
    clean_name = name.strip() if name else None

    if not clean_name:
        return error_response("Missing or empty name parameter", 400)

    try:
        response = requests.get(
            GENDERIZE_URL,
            params={"name": clean_name},
            timeout=5
        )

        # Equivalent of raise_for_status()
        if response.status_code != 200:
            return error_response("Error fetching gender prediction", 502)

        data = response.json()

        # SAFE EXTRACTION (FastAPI style)
        probability = float(data.get("probability") or 0)
        sample_size = int(data.get("count") or 0)
        gender = data.get("gender")

        # EDGE CASE (same as FastAPI)
        if gender is None or sample_size == 0:
            return error_response(
                "No prediction available for the provided name",
                422
            )

    except requests.Timeout:
        return error_response("External API timed out", 502)

    except requests.RequestException:
        return error_response("External API failure", 502)

    # SUCCESS RESPONSE
    return Response(
        {
            "status": "success",
            "data": {
                "name": data.get("name"),
                "gender": gender,
                "probability": probability,
                "sample_size": sample_size,
                "is_confident": probability >= 0.7 and sample_size >= 100,
                "processed_at": datetime.now(timezone.utc)
                .isoformat(timespec="seconds")
                .replace("+00:00", "Z"),
            },
        },
        status=200,
        headers={"Access-Control-Allow-Origin": "*"}
    )