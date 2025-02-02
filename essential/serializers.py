from rest_framework import serializers

class QuizRequestSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()
    unit_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False
    )
    question_count = serializers.IntegerField(default=10, min_value=1, max_value=20)
