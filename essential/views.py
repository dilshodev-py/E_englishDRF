
import random
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Book, Unit, Word
from .serializers import QuizRequestSerializer

@extend_schema(tags=["Quiz"], request=QuizRequestSerializer)
class QuizView(APIView):
    def post(self, request):
        serializer = QuizRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        book_id = serializer.validated_data["book_id"]
        unit_ids = serializer.validated_data["unit_ids"]
        question_count = serializer.validated_data["question_count"]

        if not Book.objects.filter(id=book_id).exists():
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

        units = Unit.objects.filter(id__in=unit_ids, book_id=book_id)
        if not units.exists():
            return Response({"error": "No matching units found"}, status=status.HTTP_404_NOT_FOUND)

        words = list(Word.objects.filter(unit__in=units))
        if not words:
            return Response({"error": "No words found for the given units"}, status=status.HTTP_404_NOT_FOUND)

        word_samples = random.sample(words, min(len(words), question_count))
        quiz = []

        question_types = {
            "uz_to_en": lambda w: {
                "type": "uz_to_en",
                "question": f"'{w.uz}' so‘zining inglizcha tarjimasini toping:",
                "correct_answer": w.en,
                "options": self.get_options(w.en, True),
            },
            "en_to_uz": lambda w: {
                "type": "en_to_uz",
                "question": f"'{w.en}' so‘zining o‘zbekcha tarjimasini toping:",
                "correct_answer": w.uz,
                "options": self.get_options(w.uz, False),
            },
            "definition": lambda w: {
                "type": "definition",
                "question": f"Quyidagi ta’rifga mos keladigan so‘zni tanlang: '{w.definition}'",
                "correct_answer": w.en,
                "options": self.get_options(w.en, True),
            },
            "sentence": lambda w: self.generate_sentence_question(w),
        }

        for word in word_samples:
            q_type = random.choice(list(question_types.keys()))
            question = question_types[q_type](word)
            quiz.append(question)

        return Response({"quiz": quiz}, status=status.HTTP_200_OK)

    def get_options(self, correct_answer, is_english):
        """To‘g‘ri javobga mos variantlarni tanlaydi"""
        all_words = list(Word.objects.values_list("en" if is_english else "uz", flat=True))
        wrong_answers = random.sample([w for w in all_words if w != correct_answer], min(len(all_words) - 1, 3))
        return random.sample([correct_answer] + wrong_answers, len(wrong_answers) + 1)

    def generate_sentence_question(self, word):
        """Bo‘sh joy qo‘yilgan gapni generatsiya qiladi"""
        word_capitalized = word.en.capitalize()
        sentence = word.sentence.replace(word.en, "______").replace(word_capitalized, "______")
        return {
            "type": "sentence",
            "question": f"Bo‘sh joyni to‘ldiring: {sentence}",
            "correct_answer": word.en,
            "options": self.get_options(word.en, True),
        }