from django.shortcuts import render


def home(request):
    context = {
        "theme": "mentor_ds",
        "hero": {
            "bg": "bg1",
            "title": "Say Tell Speak Talk",
            "slogan": "Global connection starts with improving your speaking skills<br>Let’s get to talking!",
            "btn": {"title": "Classes", "link": "#classes"}
        }
    }
    return render(request, f"home.html", context)
