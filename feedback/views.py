from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from tracking.models import WorkoutSession, SessionSummary

class AIFeedbackView(APIView):
    def get(self, request):
        return Response({"message": "man.."})
    
    def post(self, request):
        session_id = request.data.get('session_id')
        performance_metrics = request.data.get('metrics', {})

        try:
            session = WorkoutSession.objects.get(id=session_id)
            accuracy = performance_metrics.get('avg_accuracy', 0)
            
            if accuracy >= 85:
                ai_comment = "die trying"
            elif accuracy >= 60:
                ai_comment = "keep up"
            else:
                ai_comment = "try dying"

            summary_data = {
                "ai_summary": ai_comment,
                "raw_metrics": performance_metrics
            }
            
            SessionSummary.objects.update_or_create(
                session=session,
                defaults={'summary_json': summary_data}
            )

            return Response({
                "session_id": session_id,
                "ai_comment": ai_comment,
                "status": "Summary generated and saved"
            }, status=status.HTTP_200_OK)

        except WorkoutSession.DoesNotExist:
            return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)