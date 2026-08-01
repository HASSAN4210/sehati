from django import forms


class FoodPhotoAnalysisForm(forms.Form):
    photo = forms.ImageField(
        label="صورة الوجبة",
        help_text="استخدم صورة واضحة من الأعلى ويُفضّل إظهار حجم الطبق.",
        widget=forms.ClearableFileInput(
            attrs={
                "accept": "image/jpeg,image/png,image/webp",
                "capture": "environment",
                "class": "photo-input",
            }
        ),
    )
    meal_context = forms.CharField(
        label="معلومات تساعد على دقة التقدير (اختياري)",
        required=False,
        max_length=200,
        widget=forms.TextInput(
            attrs={
                "placeholder": "مثال: الطبق قطره 25 سم، الدجاج 150 غرامًا",
                "autocomplete": "off",
            }
        ),
    )
    accept_ai_processing = forms.BooleanField(
        label="أوافق على إرسال الصورة إلى خدمة OpenAI لتحليلها",
        required=True,
    )

    def clean_photo(self):
        photo = self.cleaned_data["photo"]
        allowed_types = {"image/jpeg", "image/png", "image/webp"}

        if photo.size > 8 * 1024 * 1024:
            raise forms.ValidationError(
                "حجم الصورة كبير. الحد الأقصى المسموح به هو 8 ميجابايت."
            )

        if photo.content_type not in allowed_types:
            raise forms.ValidationError(
                "صيغة الصورة غير مدعومة. استخدم JPG أو PNG أو WebP."
            )

        width = getattr(photo.image, "width", 0)
        height = getattr(photo.image, "height", 0)
        if width < 320 or height < 320:
            raise forms.ValidationError(
                "الصورة صغيرة جدًا. استخدم صورة لا تقل عن 320×320 بكسل."
            )
        if width > 8000 or height > 8000:
            raise forms.ValidationError(
                "أبعاد الصورة كبيرة جدًا. الحد الأقصى هو 8000 بكسل لكل جانب."
            )

        photo.seek(0)
        return photo
