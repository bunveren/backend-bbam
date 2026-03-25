import logging
from google import genai
from django.conf import settings
logger = logging.getLogger(__name__)

class AIFeedbackEngine:
    @staticmethod
    def generate_post_workout_analysis(session_summary_data):
        avg_accuracy = session_summary_data.get("avg_form_accuracy", 0)
        common_errors = session_summary_data.get("common_errors", [])
        duration = session_summary_data.get("duration_minutes", 0)

        error_text = ", ".join(set(common_errors)) if common_errors else "No major form errors detected"

        prompt = f"""
        You are an expert AI fitness coach.
        Your task is to write a detailed, professional, motivating, and educational post-workout feedback message based on the user's workout summary data.
        Workout data:
        - Workout duragetion: {duration} minutes
        - Average form accuracy: {avg_accuracy}%
        - Common form errors: {error_text}

        Follow these rules:
        1. The response must be in English.
        2. Start with a short motivational sentence.
        3. Evaluate the user's overall performance.
        4. Comment on the average form accuracy and explain what that performance level means.
        5. Analyze the detected form mistakes and explain why they matter.
        6. Give specific and practical suggestions for the next workout.
        7. Avoid overly short, generic, or shallow comments.
        8. Sound natural, professional, and coach-like.
        9. Do not provide medical advice.
        10. The response should be around 5 to 8 sentences.
        11. Use only the information provided and do not invent missing details.

        Structure:
        - First part: overall performance and motivation
        - Second part: form analysis
        - Third part: improvement suggestions and closing encouragement
        
        Return only one plain paragraph.
        """.strip()
        
        try:
            client = genai.Client(api_key=settings.GEMINI_API_KEY)
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )

            text = (response.text or "").strip()
            if text:
                return text

            logger.warning("Gemini returned empty text, using fallback.")

        except Exception as e:
            logger.exception("Gemini feedback generation failed: %s", e)

        # fallback
        if avg_accuracy >= 85:
            return f"Great job completing your {duration}-minute workout. Your form was quite stable, and you should maintain this level, especially regarding {error_text}."
        elif avg_accuracy >= 65:
            return f"You completed the workout well. Your overall form is decent, but you should pay closer attention to {error_text} in your next session."
        else:
            return f"This was a challenging workout. Mistakes such as {error_text} are reducing your performance. Focus on slower, more controlled repetitions to improve your form."