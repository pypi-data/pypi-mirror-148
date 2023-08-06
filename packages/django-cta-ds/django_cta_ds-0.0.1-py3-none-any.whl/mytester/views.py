from django.shortcuts import render


def home(request):
    context = {
        "theme": "medilab_ds",
        "cta": {
            "title" : "카카오톡 상담",
            "desc" : "카카오톡을 통해 상담 및 예약 가능합니다.",
            "link" : "http://pf.kakao.com/_xexhxgxlV"
        }
    }
    return render(request, f"home.html", context)
