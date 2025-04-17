from rest_framework.views import APIView
from .models import Transaction, Category
import pandas as pd
from rest_framework.response import Response
from .serializers import CategorySerializer


class SpendingAnalyticsView(APIView):
    def get(self, request):
        transactions = Transaction.objects.filter(user=request.user)
        df = pd.DataFrame.from_records(
            transactions.values("date", "amount", "category__name")
        )

        # Generate monthly insights
        monthly_data = df.resample("M", on="date").agg(
            {"amount": ["sum", "mean", "max"]}
        )

        # Category distribution
        category_data = df.groupby("category__name").agg({"amount": "sum"}).to_dict()

        return Response(
            {
                "monthly_insights": monthly_data.to_dict(),
                "category_distribution": category_data,
            }
        )

class CategoriesView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)