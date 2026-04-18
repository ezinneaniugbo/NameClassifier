import requests
from datetime import datetime, timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response

GENDERIZE_URL = "https://api.genderize.io"

@api_view(['GET'])
def classify(request):
    name = request.query_params.get('name')

    # 400: Missing or empty
    if name is None or name.strip() == "":
        return Response(
            {"status": "error", "message": "Missing or empty name parameter"},
            status=400,
            headers={"Access-Control-Allow-Origin": "*"}
        )

    # 422: Not string (defensive)
    if not isinstance(name, str):
        return Response(
            {"status": "error", "message": "Name must be a string"},
            status=422,
            headers={"Access-Control-Allow-Origin": "*"}
        )

    name = name.strip()

    # Call external API
    try:
        response = requests.get(GENDERIZE_URL, params={"name": name}, timeout=5)
        data = response.json()
    except requests.RequestException:
        return Response(
            {"status": "error", "message": "External API failure"},
            status=502,
            headers={"Access-Control-Allow-Origin": "*"}
        )

    # Edge case: no prediction
    if data.get("gender") is None or data.get("count", 0) == 0:
        return Response(
            {"status": "error", "message": "No prediction available for the provided name"},
            status=422,
            headers={"Access-Control-Allow-Origin": "*"}
        )

    # Process data
    gender = data.get("gender")
    probability = data.get("probability")
    sample_size = data.get("count")

    is_confident = (probability >= 0.7) and (sample_size >= 100)

    processed_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    return Response(
        {
            "status": "success",
            "data": {
                "name": name,
                "gender": gender,
                "probability": probability,
                "sample_size": sample_size,
                "is_confident": is_confident,
                "processed_at": processed_at
            }
        },
        status=200,
        headers={"Access-Control-Allow-Origin": "*"}
    )
