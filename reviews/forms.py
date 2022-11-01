from django import forms
from .models import Store, Review, Comment


class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = "__all__"


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            "content",
            "grade",
            "image",
        ]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            "content",
        ]
        widgets = {
            "content": forms.Textarea(attrs={"class": "from-control", "rows": 1})
        }
        labels = {
            "content": "댓글",
        }
