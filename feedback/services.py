import logging
logger = logging.getLogger(__name__)

class AIFeedbackEngine:
    @staticmethod
    def generate_post_workout_analysis(session_summary_data):
        avg_accuracy = session_summary_data.get("avg_form_accuracy", 0)
        common_errors = session_summary_data.get("common_errors", [])
        duration = session_summary_data.get("duration_minutes", 0)
        # TODO: OpenAI veya Gemini API entegrasyonu
        
        error_text = ", ".join(set(common_errors)) if common_errors else "Belirgin bir form hatası gözlemlenmedi."
        if avg_accuracy >= 85:
            analysis = f"{duration} dakikalık harika bir performans! Formun oldukça stabil. Özellikle {error_text} konusundaki başarını korumalısın."
        elif avg_accuracy >= 65:
            analysis = f"Antrenmanı tamamladın. Genel formun iyi ancak şu hatalara dikkat etmelisin: {error_text}. Bir sonraki seans için odağını buraya ver."
        else:
            analysis = f"Zorlayıcı bir antrenman oldu. {error_text} gibi hatalar performansını düşürüyor. Formunu düzeltmek için ayna karşısında çalışmanı öneririm."

        return analysis