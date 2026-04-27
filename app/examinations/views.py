from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, CreateView, UpdateView, ListView
from django.views import View
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse, HttpResponseRedirect
from django.db.models import Q

from core.mixins import create_audit_log
from patients.models import Patient
from appointments.models import Appointment, AppointmentStatus
from .models import Examination, VitalSigns, ExaminationTemplate
from .forms import ExaminationForm, VitalSignsForm, ExaminationTemplateForm


class ExaminationCreateView(LoginRequiredMixin, CreateView):
    model = Examination
    form_class = ExaminationForm
    template_name = 'examinations/form.html'

    def dispatch(self, request, *args, **kwargs):
        self.patient = get_object_or_404(Patient, pk=kwargs['patient_pk'])
        self.appointment = None
        apt_pk = kwargs.get('appointment_pk')
        if apt_pk:
            self.appointment = get_object_or_404(Appointment, pk=apt_pk)
            # Randevunun zaten bir muayenesi varsa mevcut muayeneye yönlendir
            try:
                existing_exam = self.appointment.examination
                messages.info(request, 'Bu randevu için zaten bir muayene kaydı mevcut.')
                return HttpResponseRedirect(reverse('examinations:detail', kwargs={'pk': existing_exam.pk}))
            except Examination.DoesNotExist:
                pass
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        self.vitals_form = VitalSignsForm(
            self.request.POST or None,
            prefix='vitals'
        )
        return form

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['patient'] = self.patient
        ctx['appointment'] = self.appointment
        ctx['vitals_form'] = self.vitals_form
        ctx['past_examinations'] = self.patient.examinations.select_related('doctor__user').order_by('-created_at')[:5]
        user = self.request.user
        ctx['exam_templates'] = (
            ExaminationTemplate.objects.filter(created_by=user) |
            ExaminationTemplate.objects.filter(is_shared=True)
        ).order_by('category', 'name')
        return ctx

    def form_valid(self, form):
        if not self.vitals_form.is_valid():
            return self.form_invalid(form)

        form.instance.patient = self.patient

        # Doktor profiline sahip kullanıcı otomatik atanır, değilse form seçiminden alınır
        if hasattr(self.request.user, 'doctor_profile'):
            form.instance.doctor = self.request.user.doctor_profile
        else:
            selected_doctor = form.cleaned_data.get('doctor')
            if not selected_doctor:
                messages.error(self.request, 'Lütfen muayeneyi yapan doktoru seçin.')
                return self.form_invalid(form)
            form.instance.doctor = selected_doctor

        if self.appointment:
            form.instance.appointment = self.appointment

        response = super().form_valid(form)

        vitals = self.vitals_form.save(commit=False)
        vitals.examination = self.object
        vitals.save()

        if self.appointment:
            self.appointment.status = AppointmentStatus.COMPLETED
            self.appointment.save(update_fields=['status', 'updated_at'])

        create_audit_log(
            self.request, 'CREATE', 'Examination', self.object.pk,
            f'Muayene kaydı: {self.patient.full_name}'
        )
        messages.success(self.request, 'Muayene kaydı oluşturuldu.')
        return response

    def get_success_url(self):
        return reverse_lazy('examinations:detail', kwargs={'pk': self.object.pk})


class ExaminationDetailView(LoginRequiredMixin, DetailView):
    model = Examination
    template_name = 'examinations/detail.html'
    context_object_name = 'examination'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        create_audit_log(
            self.request, 'VIEW', 'Examination', obj.pk,
            f'Muayene görüntülendi: {obj.patient.full_name}'
        )
        return obj

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        try:
            ctx['vitals'] = self.object.vitals
        except VitalSigns.DoesNotExist:
            ctx['vitals'] = None
        ctx['prescriptions'] = self.object.prescriptions.prefetch_related('items').all()
        ctx['documents'] = self.object.documents.all()
        from payments.models import Service
        from django.db.models import Sum
        ctx['services'] = Service.objects.filter(status=True).order_by('name')
        ctx['examination_services'] = self.object.services.select_related('service').order_by('created_at')
        ctx['examination_total'] = (
            ctx['examination_services'].aggregate(total=Sum('amount'))['total'] or 0
        )
        return ctx


class ExaminationUpdateView(LoginRequiredMixin, UpdateView):
    model = Examination
    form_class = ExaminationForm
    template_name = 'examinations/form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy('examinations:detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['patient'] = self.object.patient
        ctx['vitals_form'] = VitalSignsForm(
            self.request.POST or None,
            instance=getattr(self.object, 'vitals', None),
            prefix='vitals'
        )
        user = self.request.user
        ctx['exam_templates'] = (
            ExaminationTemplate.objects.filter(created_by=user) |
            ExaminationTemplate.objects.filter(is_shared=True)
        ).order_by('category', 'name')
        return ctx

    def form_valid(self, form):
        ctx = self.get_context_data()
        vitals_form = ctx['vitals_form']
        if vitals_form.is_valid():
            vitals = vitals_form.save(commit=False)
            vitals.examination = self.object
            vitals.save()
        messages.success(self.request, 'Muayene güncellendi.')
        return super().form_valid(form)


class ExaminationListView(LoginRequiredMixin, ListView):
    model = Examination
    template_name = 'examinations/list.html'
    context_object_name = 'examinations'
    paginate_by = 30

    def get_queryset(self):
        qs = Examination.objects.select_related('patient', 'doctor__user').order_by('-created_at')
        user = self.request.user
        if user.is_doctor:
            try:
                qs = qs.filter(doctor=user.doctor_profile)
            except Exception:
                pass

        # Arama filtresi
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(patient__name__icontains=q) |
                Q(patient__surname__icontains=q) |
                Q(diagnosis__icontains=q) |
                Q(icd10_code__icontains=q)
            )
        doctor_id = self.request.GET.get('doctor')
        if doctor_id:
            qs = qs.filter(doctor_id=doctor_id)
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        if date_from:
            qs = qs.filter(created_at__date__gte=date_from)
        if date_to:
            qs = qs.filter(created_at__date__lte=date_to)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        from appointments.models import Doctor
        from datetime import date
        ctx['doctors'] = Doctor.objects.filter(status=True).select_related('user')
        ctx['q'] = self.request.GET.get('q', '')
        ctx['selected_doctor'] = self.request.GET.get('doctor', '')
        ctx['date_from'] = self.request.GET.get('date_from', '')
        ctx['date_to'] = self.request.GET.get('date_to', '')
        ctx['today'] = date.today()
        return ctx


# ── Şablon CRUD ──────────────────────────────────────────────────────────────

class ExaminationTemplateListView(LoginRequiredMixin, ListView):
    model = ExaminationTemplate
    template_name = 'examinations/template_list.html'
    context_object_name = 'templates'

    def get_queryset(self):
        user = self.request.user
        qs = ExaminationTemplate.objects.all() if user.is_admin else (
            ExaminationTemplate.objects.filter(created_by=user) |
            ExaminationTemplate.objects.filter(is_shared=True)
        )
        category = self.request.GET.get('category', '')
        if category:
            qs = qs.filter(category=category)
        return qs.order_by('category', 'name')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = ExaminationTemplate.Category.choices
        ctx['selected_category'] = self.request.GET.get('category', '')
        return ctx


class ExaminationTemplateCreateView(LoginRequiredMixin, CreateView):
    model = ExaminationTemplate
    form_class = ExaminationTemplateForm
    template_name = 'examinations/template_form.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Şablon oluşturuldu.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('examinations:template_list')


class ExaminationTemplateUpdateView(LoginRequiredMixin, UpdateView):
    model = ExaminationTemplate
    form_class = ExaminationTemplateForm
    template_name = 'examinations/template_form.html'

    def get_success_url(self):
        messages.success(self.request, 'Şablon güncellendi.')
        return reverse_lazy('examinations:template_list')


class ExaminationTemplateDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        tpl = get_object_or_404(ExaminationTemplate, pk=pk)
        if tpl.created_by == request.user or request.user.is_admin:
            tpl.delete()
            messages.success(request, 'Şablon silindi.')
        else:
            messages.error(request, 'Bu şablonu silme yetkiniz yok.')
        return redirect('examinations:template_list')


class ExaminationTemplateApiView(LoginRequiredMixin, View):
    """AJAX: Şablon verilerini JSON döndür (muayene formuna otomatik doldurma için)."""
    def get(self, request, pk):
        tpl = get_object_or_404(ExaminationTemplate, pk=pk)
        return JsonResponse({
            'complaint': tpl.complaint,
            'findings': tpl.findings,
            'diagnosis': tpl.diagnosis,
            'icd10_code': tpl.icd10_code,
            'treatment_plan': tpl.treatment_plan,
            'doctor_note': tpl.doctor_note,
        })


# Sık kullanılan ICD-10 kodları (statik liste — genişletilebilir)
ICD10_CODES = [
    ("J00", "Akut nazofarenjit (nezle)"),
    ("J06.9", "Akut üst solunum yolu enfeksiyonu"),
    ("J18.9", "Pnömoni"),
    ("J20.9", "Akut bronşit"),
    ("J45.9", "Astım"),
    ("J30.1", "Alerjik rinit"),
    ("J03.9", "Akut tonsillit"),
    ("J02.9", "Akut farenjit"),
    ("J01.9", "Akut sinüzit"),
    ("H66.9", "Otitis media"),
    ("A09", "Gastroenterit"),
    ("K21.0", "Gastroözofageal reflü"),
    ("K29.7", "Gastrit"),
    ("K57.3", "Divertikül"),
    ("K80.2", "Kolelitiyazis"),
    ("K35.8", "Akut apandisit"),
    ("I10", "Esansiyel hipertansiyon"),
    ("I25.9", "Kronik iskemik kalp hastalığı"),
    ("I48", "Atriyal fibrilasyon"),
    ("I50.9", "Kalp yetmezliği"),
    ("I63.9", "Serebral infarktüs"),
    ("E11.9", "Tip 2 diyabetes mellitus"),
    ("E10.9", "Tip 1 diyabetes mellitus"),
    ("E78.5", "Hiperlipidemi"),
    ("E03.9", "Hipotiroidizm"),
    ("E05.9", "Hipertiroidizm"),
    ("E66.9", "Obezite"),
    ("M54.5", "Bel ağrısı"),
    ("M54.4", "Siyatik"),
    ("M51.1", "Lomber disk hernisi"),
    ("M16.9", "Kalça artriti"),
    ("M17.9", "Diz artriti"),
    ("M79.3", "Kas ağrısı / miyalji"),
    ("G43.9", "Migren"),
    ("G40.9", "Epilepsi"),
    ("G47.0", "Uyku bozukluğu"),
    ("F32.9", "Depresif dönem"),
    ("F41.1", "Yaygın anksiyete bozukluğu"),
    ("F10.2", "Alkol bağımlılığı"),
    ("N39.0", "İdrar yolu enfeksiyonu"),
    ("N20.0", "Böbrek taşı"),
    ("N40", "Prostat hiperplazisi"),
    ("N92.1", "Düzensiz menstrüasyon"),
    ("L30.9", "Dermatit"),
    ("L40.0", "Psöriyazis"),
    ("L50.9", "Ürtiker"),
    ("B02.9", "Zona (herpes zoster)"),
    ("B34.9", "Viral enfeksiyon"),
    ("A41.9", "Sepsis"),
    ("Z00.0", "Rutin sağlık muayenesi"),
    ("Z13.9", "Tarama muayenesi"),
    ("Z30.0", "Kontrasepsiyon danışmanlığı"),
    ("R05", "Öksürük"),
    ("R07.9", "Göğüs ağrısı"),
    ("R10.4", "Karın ağrısı"),
    ("R51", "Baş ağrısı"),
    ("R50.9", "Ateş"),
    ("R11", "Bulantı ve kusma"),
    ("R42", "Baş dönmesi"),
    ("R55", "Senkop"),
    ("S00-T98", "Travma / Yaralanma"),
]


class ICD10SearchView(LoginRequiredMixin, View):
    """AJAX: ICD-10 kodu araması."""
    def get(self, request):
        q = request.GET.get('q', '').strip().upper()
        if len(q) < 2:
            return JsonResponse({'results': []})
        results = [
            {'code': code, 'label': f'{code} — {desc}'}
            for code, desc in ICD10_CODES
            if q in code.upper() or q in desc.upper()
        ][:20]
        return JsonResponse({'results': results})
