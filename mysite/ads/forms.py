from django import forms
from ads.models import Ad
from django.core.files.uploadedfile import InMemoryUploadedFile

# Really simple naturalsize that is missing from django humanize :(
def naturalsize(count) :
    fcount = float(count)
    k = 1024
    m = k * k
    g = m * k
    if fcount < k : return str(count) + 'B'
    if fcount >= k and fcount < m :
        return str(int(fcount / (k/10.0) ) / 10.0) + 'KB'
    if fcount >= m and fcount < g :
        return str(int(fcount / (m/10.0) ) / 10.0) + 'MB'
    return str(int(fcount / (g/10.0) ) / 10.0) + 'GB'


# Create the form class.
class CreateForm(forms.ModelForm):
    max_upload_limit = 2 * 1024 * 1024
    max_upload_limit_text = naturalsize(max_upload_limit)

    # Call this 'picture' so it gets copied from the form to the in-memory model
    # It will not be the "bytes", it will be the "InMemoryUploadedFile"
    # because we need to pull out things like content_type
    picture = forms.FileField(required=False, label='File to Upload <= ' + max_upload_limit_text)
    upload_field_name = 'picture'

    # Hint: this will need to be changed for use in the ads application :)
    class Meta:
        model = Ad
        fields = ['title', 'text', 'picture']  # Picture is manual

    # Validate the size of the picture
    def clean(self):
        cleaned_data = super().clean()
        pic = cleaned_data.get('picture')
        if pic is None: return
        if len(pic) > self.max_upload_limit:
            self.add_error('picture', "File must be < " + self.max_upload_limit_text + " bytes")

    # Convert uploaded File object to a picture
    def save(self, commit=True):
        instance = super(CreateForm, self).save(commit=False)

        # We only need to adjust picture if it is a freshly uploaded file
        f = instance.picture  # Make a copy
        if isinstance(f, InMemoryUploadedFile):  # Extract data from the form to the model
            bytearr = f.read()
            instance.content_type = f.content_type
            instance.picture = bytearr  # Overwrite with the actual image data

        if commit:
            instance.save()

        return instance


class CommentForm(forms.Form):
    comment = forms.CharField(required=True, max_length=500, min_length=3, strip=True)

