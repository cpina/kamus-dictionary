from django.urls import reverse

def _link(current_path, url, text):
    if current_path == url:
        return {"text": text}
    else:
        return {"url": url, "text": text}

def footer_links(request):
    result = []

    result.append(_link(request.path, reverse("homepage"), "Main page"))
    result.append(_link(request.path, reverse("about"), "About"))
    result.append(_link(request.path, reverse("shortcuts"), "Shortcuts"))
    result.append(_link(request.path, reverse("imports"), "Imports"))

    return {"footer_links": result}
