from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from tracking.models import WorkoutSession, SessionSummary

class AIFeedbackView(APIView):
    def get(self, request):
        return Response({"error": "not supposed to do that"}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        return Response({"error": "not supposed to do that"}, status=status.HTTP_400_BAD_REQUEST)
        
"""
class AIFeedbackView(APIView):
    def get(self, request):
        session_id = request.query_params.get("session_id")

        if not session_id:
            return Response(
                {"error": "session_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            session = WorkoutSession.objects.get(id=session_id)
            summary = SessionSummary.objects.get(session=session)

            ai_comment = summary.summary_json.get("ai_comment")
            if not ai_comment:
                return Response(
                    {"error": "AI feedback not generated yet"},
                    status=status.HTTP_404_NOT_FOUND
                )

            return Response(
                {
                    "session_id": session.id,
                    "ai_comment": ai_comment
                },
                status=status.HTTP_200_OK
            )

        except WorkoutSession.DoesNotExist:
            return Response(
                {"error": "Session not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except SessionSummary.DoesNotExist:
            return Response(
                {"error": "Session summary not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    def post(self, request):
        session_id = request.data.get("session_id")

        if not session_id:
            return Response(
                {"error": "session_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            session = WorkoutSession.objects.get(id=session_id)
        except WorkoutSession.DoesNotExist:
            return Response(
                {"error": "Session not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            summary = SessionSummary.objects.get(session=session)
        except SessionSummary.DoesNotExist:
            return Response(
                {"error": "Session summary not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        summary_json = summary.summary_json or {}

        metrics = {
            "avg_form_accuracy": summary_json.get("avg_form_accuracy", 0),
            "common_errors": summary_json.get("common_errors", []),
            "duration_minutes": summary_json.get("duration_minutes", 0),
        }

        ai_comment = AIFeedbackEngine.generate_post_workout_analysis(metrics)

        summary_json["ai_comment"] = ai_comment
        summary.summary_json = summary_json
        summary.save()

        return Response(
            {
                "session_id": session.id,
                "ai_comment": ai_comment,
                "status": "Summary generated and saved"
            },
            status=status.HTTP_200_OK
        )
"""