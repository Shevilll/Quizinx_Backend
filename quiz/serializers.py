from rest_framework import serializers
from .models import Quiz, Question, Answer


class QuizSerializer(serializers.ModelSerializer):
    # Dynamically calculate the question count from related Question objects
    question_count = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = ["id", "title", "created_at", "question_count"]

    def get_question_count(self, obj):
        return obj.questions.count()  # Use related objects to count questions


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ["id", "answer_text", "is_right"]


class QuestionSerializer(serializers.ModelSerializer):
    quiz = QuizSerializer(read_only=True)
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ["id", "quiz", "title", "answers"]

    def create(self, validated_data):
        # Create the question instance
        answers_data = validated_data.pop("answers", [])
        question = Question.objects.create(**validated_data)

        # Create associated answers for the question
        for answer_data in answers_data:
            Answer.objects.create(question=question, **answer_data)

        return question

    def update(self, instance, validated_data):
        # Update the question title
        instance.title = validated_data.get("title", instance.title)

        # Handle answers: Remove existing answers and add new ones
        answers_data = validated_data.pop("answers", [])

        # Only delete the answers if new ones are provided
        if answers_data:
            instance.answers.all().delete()
            for answer_data in answers_data:
                Answer.objects.create(question=instance, **answer_data)

        instance.save()
        return instance
