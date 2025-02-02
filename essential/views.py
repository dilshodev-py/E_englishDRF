
import random

from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Book, Unit, Word
from .serializers import QuizRequestSerializer

@extend_schema(tags=["Quiz"],request=QuizRequestSerializer)
class QuizView(APIView):
    def post(self, request):
        # So‘rovni tekshirish
        serializer = QuizRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # So‘rovdan ma’lumotlarni olish
        book_id = serializer.validated_data['book_id']
        unit_ids = serializer.validated_data['unit_ids']
        question_count = serializer.validated_data['question_count']

        # Kitob mavjudligini tekshirish
        if not Book.objects.filter(id=book_id).exists():
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

        # Unitlarni olish
        units = Unit.objects.filter(id__in=unit_ids, book_id=book_id)
        if not units.exists():
            return Response({"error": "No matching units found"}, status=status.HTTP_404_NOT_FOUND)

        # Shu unitlarga tegishli barcha so‘zlarni olish
        words = list(Word.objects.filter(unit__in=units))
        if not words:
            return Response({"error": "No words found for the given units"}, status=status.HTTP_404_NOT_FOUND)

        # Tasodifiy so‘zlarni tanlash
        word_samples = random.sample(words, min(len(words), question_count))

        # Quiz formatini yaratish
        quiz = []
        for word in word_samples:
            question_type = random.choice(["uz_to_en", "en_to_uz", "definition", "sentence"])

            # Noto‘g‘ri javoblar
            wrong_answers = list(Word.objects.exclude(id=word.id).values_list('en', flat=True))
            random.shuffle(wrong_answers)
            wrong_answers = wrong_answers[:3] if len(wrong_answers) >= 3 else wrong_answers

            if question_type == "uz_to_en":
                question = {
                    "type": "uz_to_en",
                    "question": f"'{word.uz}' so‘zining inglizcha tarjimasini toping:",
                    "correct_answer": word.en,
                    "options": random.sample([word.en] + wrong_answers, len(wrong_answers) + 1)
                }
            elif question_type == "en_to_uz":
                question = {
                    "type": "en_to_uz",
                    "question": f"'{word.en}' so‘zining o‘zbekcha tarjimasini toping:",
                    "correct_answer": word.uz,
                    "options": random.sample([word.uz] + wrong_answers, len(wrong_answers) + 1)
                }
            elif question_type == "definition":
                question = {
                    "type": "definition",
                    "question": f"Quyidagi ta’rifga mos keladigan so‘zni tanlang: '{word.definition}'",
                    "correct_answer": word.en,
                    "options": random.sample([word.en] + wrong_answers, len(wrong_answers) + 1)
                }
            else:  # "sentence"
                question = {
                    "type": "sentence",
                    "question": f"Bo‘sh joyni to‘ldiring: {word.sentence.replace(word.en, '______')}",
                    "correct_answer": word.en,
                    "options": random.sample([word.en] + wrong_answers, len(wrong_answers) + 1)
                }

            quiz.append(question)

        return Response({"quiz": quiz}, status=status.HTTP_200_OK)
