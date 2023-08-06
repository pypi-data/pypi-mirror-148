from django.shortcuts import render


def home(request):
    context = {
        "theme": "mentor_ds",
        "counts": [
            ["학생", 17],
            ["클래스", 4],
            ["이벤트", 3],
            ["교사", 1]
        ]
    }
    return render(request, f"home.html", context)