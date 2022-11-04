from django import forms
from .models import Store, Review, Comment


class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = [
            "store_name",
            "address",
            "phone_num",
            "menu",
            "image",
            "price",
            "parking",
            "week_time",
            "weekend",
            "last_order",
            "website",
        ]
        labels = {
            "store_name": "가게명",
            "address": "주소",
            "phone_num": "전화번호",
            "menu": "대표메뉴",
            "image": "사진",
            "price": "가격대",
            "parking": "주차",
            "week_time": "영업시간",
            "weekend": "휴일",
            "last_order": "마지막주문가능시간",
            "website": "홈페이지",
        }


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
