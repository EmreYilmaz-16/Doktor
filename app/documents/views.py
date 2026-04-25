import os
import mimetypes
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView
from django.views import View
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import FileResponse, Http404

from core.mixins import create_audit_log
from patients.models import Patient
from .models import Document
from .forms import DocumentUploadForm


class DocumentListView(LoginRequiredMixin, ListView):
    model = Document
    template_name = 'documents/list.html'
    context_object_name = 'documents'

    def dispatch(self, request, *args, **kwargs):
        self.patient = get_object_or_404(Patient, pk=kwargs['patient_pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Document.objects.filter(patient=self.patient).order_by('-created_at')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['patient'] = self.patient
        ctx['upload_form'] = DocumentUploadForm(patient=self.patient)
        return ctx


class DocumentUploadView(LoginRequiredMixin, CreateView):
    model = Document
    form_class = DocumentUploadForm
    template_name = 'documents/list.html'

    def dispatch(self, request, *args, **kwargs):
        self.patient = get_object_or_404(Patient, pk=kwargs['patient_pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['patient'] = self.patient
        return kwargs

    def form_valid(self, form):
        form.instance.patient = self.patient
        form.instance.uploaded_by = self.request.user
        form.instance.original_filename = self.request.FILES['file'].name
        response = super().form_valid(form)
        create_audit_log(
            self.request, 'UPLOAD', 'Document', self.object.pk,
            f'Belge yüklendi: {self.object.original_filename} - Hasta: {self.patient.full_name}'
        )
        messages.success(self.request, 'Belge başarıyla yüklendi.')
        return response

    def form_invalid(self, form):
        messages.error(self.request, f'Yükleme hatası: {form.errors}')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('documents:list', kwargs={'patient_pk': self.patient.pk})


class DocumentDownloadView(LoginRequiredMixin, View):
    """Belge indirme - erişim denetimli."""
    def get(self, request, pk):
        doc = get_object_or_404(Document, pk=pk)
        if not doc.file:
            raise Http404
        create_audit_log(
            request, 'DOWNLOAD', 'Document', pk,
            f'Belge indirildi: {doc.original_filename} - Hasta: {doc.patient.full_name}'
        )
        file_path = doc.file.path
        content_type, _ = mimetypes.guess_type(file_path)
        response = FileResponse(open(file_path, 'rb'), content_type=content_type or 'application/octet-stream')
        response['Content-Disposition'] = f'inline; filename="{doc.original_filename}"'
        return response


class DocumentDeleteView(LoginRequiredMixin, DeleteView):
    model = Document
    template_name = 'documents/confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('documents:list', kwargs={'patient_pk': self.object.patient.pk})

    def form_valid(self, form):
        create_audit_log(
            self.request, 'DELETE', 'Document', self.object.pk,
            f'Belge silindi: {self.object.original_filename}'
        )
        messages.success(self.request, 'Belge silindi.')
        # Fiziksel dosyayı da sil
        try:
            if self.object.file:
                os.remove(self.object.file.path)
        except Exception:
            pass
        return super().form_valid(form)
