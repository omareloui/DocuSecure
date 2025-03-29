from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from docs.models import Doc
from docs.views import save_file


@csrf_exempt
@require_POST
def create_document(request):
    file = request.FILES.get("file")
    doc = save_file(file, request.user)
    data = {"document_id": doc.id}
    return JsonResponse(data)


@require_GET
def metadata(request, document_id):
    try:
        doc = Doc.objects.get(id=document_id)
        doc.get_metadata()
        return JsonResponse(doc.get_metadata())
    except ObjectDoesNotExist:
        return JsonResponse(
            {
                "message": f"Can't find the document with id {document_id}",
            },
            status=404,
        )


@csrf_exempt
@require_POST
def extract_metadata(request):
    url = request.POST.get("file_url")
    try:
        doc = Doc.objects.get(url=url)
        return JsonResponse(
            {
                "status": doc.status,
                "message": "Not sure message for what exactly",
                "extracted_metadata": doc.get_metadata(),
            }
        )
    except ObjectDoesNotExist:
        return JsonResponse(
            {
                "message": f"Can't find the document with url {url}",
            },
            status=404,
        )


@csrf_exempt
@require_POST
def classify(request):
    url = request.POST.get("file_url")
    try:
        doc = Doc.objects.get(url=url)
        return JsonResponse(
            {
                "status": doc.status,
                "classification": "news",
                "confidence": 0.542,
            }
        )
    except ObjectDoesNotExist:
        return JsonResponse(
            {
                "message": f"Can't find the document with url {url}",
            },
            status=404,
        )


@require_GET
def status(request, document_id):
    try:
        doc = Doc.objects.get(id=document_id)
        return JsonResponse(
            {
                "document_id": document_id,
                "status": doc.status,
                "last_updated": doc.updated_at,
            }
        )
    except ObjectDoesNotExist:
        return JsonResponse(
            {
                "message": f"Can't find the document with id {document_id}",
            },
            status=404,
        )
