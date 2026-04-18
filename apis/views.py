import requests
from datetime import datetime, timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

GENDERIZE_URL = "https://api.genderize.io"

class ClassifyView(APIView):
    def get(self, request):
        name = request.query_params.get('name', '').strip()

        # 400: Missing or empty name
        if not name:
            return Response(
                {"status": "error", "message": "Missing or empty name parameter"},
                status=status.HTTP_400_BAD_REQUEST,
                headers={"Access-Control-Allow-Origin": "*"}
            )

        # 422: Name is not a string (defensive check)
        if not isinstance(name, str):
            return Response(
                {"status": "error", "message": "name is not a string"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                headers={"Access-Control-Allow-Origin": "*"}
            )

        # Call Genderize API
        try:
            resp = requests.get(GENDERIZE_URL, params={'name': name}, timeout=5)
            resp.raise_for_status()
            data = resp.json()
        except requests.exceptions.RequestException:
            return Response(
                {"status": "error", "message": "Upstream or server failure"},
                status=status.HTTP_502_BAD_GATEWAY,
                headers={"Access-Control-Allow-Origin": "*"}
            )

        # 422: No prediction (gender null or count 0)
        if data.get('gender') is None or data.get('count', 0) == 0:
            return Response(
                {"status": "error", "message": "No prediction available for the provided name"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                headers={"Access-Control-Allow-Origin": "*"}
            )

        # Process data
        gender = data['gender']
        probability = data['probability']
        sample_size = data['count']
        is_confident = (probability >= 0.7) and (sample_size >= 100)

        response_data = {
            "status": "success",
            "data": {
                "name": name.lower(),
                "gender": gender,
                "probability": probability,
                "sample_size": sample_size,
                "is_confident": is_confident,
                "processed_at": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
            }
        }

        # 200 Success with CORS header
        return Response(
            response_data,
            status=status.HTTP_200_OK,
            headers={"Access-Control-Allow-Origin": "*"}
        )