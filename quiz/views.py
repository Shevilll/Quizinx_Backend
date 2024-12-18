from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Quiz, Question
from .serializers import QuizSerializer, QuestionSerializer
from rest_framework.views import APIView
from django.http import Http404


class ListCreateQuiz(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class RetriveUpdateDestroyQuiz(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    lookup_url_kwarg = "quiz_id"


class QuizQuestion(APIView):
    """
    List all questions for a quiz or create multiple questions for a quiz.
    """

    def get(self, request, quiz_id, format=None):
        """
        List all questions for the specified quiz.
        """
        try:
            quiz = Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            raise Http404

        questions = Question.objects.filter(quiz=quiz)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request, quiz_id, format=None):
        """
        Create multiple questions for the specified quiz.
        """
        try:
            quiz = Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            raise Http404

        # Assume the request contains a list of questions
        questions_data = request.data.get("questions", [])
        if not questions_data:
            return Response(
                {"message": "No questions provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        created_questions = []
        for question_data in questions_data:
            # Here we assume each question has a list of 'answers'
            answers_data = question_data.pop("answers", [])
            serializer = QuestionSerializer(data=question_data)
            if serializer.is_valid():
                question = serializer.save(quiz=quiz)
                # Handle answers creation
                for answer_data in answers_data:
                    # Assuming you have an AnswerSerializer to handle this
                    answer_serializer = AnswerSerializer(data=answer_data)
                    if answer_serializer.is_valid():
                        answer_serializer.save(question=question)
                created_questions.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"message": "Questions created successfully.", "data": created_questions},
            status=status.HTTP_201_CREATED,
        )


class QuizQuestionDetail(APIView):
    """
    Retrieve, update or delete a specific question.
    """

    def get_object(self, pk):
        try:
            return Question.objects.get(id=pk)
        except Question.DoesNotExist:
            raise Http404("Question not found.")

    def get(self, request, pk, format=None):
        question = self.get_object(pk)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        question = self.get_object(pk)
        serializer = QuestionSerializer(question, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        question = self.get_object(pk)
        question.delete()
        return Response(
            {"message": "Question deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
