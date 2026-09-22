from django import forms
from .models import Application, Job



class JobForm(forms.ModelForm):

    class Meta:
        model = Job
        fields = [
            'title',
            'description',
            'location',
            'salary',
            'is_active',
        ]

    def clean_title(self):
        title = self.cleaned_data['title'].strip()

        if len(title) < 3:
            raise forms.ValidationError(
                "Job title must be at least 3 characters."
            )

        return title

    def clean_description(self):
        description = self.cleaned_data['description'].strip()

        if len(description) < 20:
            raise forms.ValidationError(
                "Description must be at least 20 characters."
            )

        return description

    def clean_location(self):
        location = self.cleaned_data['location'].strip()

        if len(location) < 2:
            raise forms.ValidationError(
                "Location must be at least 2 characters."
            )

        return location

    def clean_salary(self):
        salary = self.cleaned_data['salary']

        if salary <= 0:
            raise forms.ValidationError(
                "Salary must be greater than zero."
            )

        return salary

class ApplicationForm(forms.ModelForm):

    class Meta:
        model = Application
        fields = ['resume']

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')

        if not resume:
            raise forms.ValidationError("Please upload your resume.")

        if resume.size > 5 * 1024 * 1024:
            raise forms.ValidationError(
                "Resume file size must not exceed 5 MB."
            )

        if not resume.name.lower().endswith('.pdf'):
            raise forms.ValidationError(
                "Only PDF resume files are allowed."
            )

        # Check that the file actually has a PDF signature
        resume.seek(0)
        file_header = resume.read(4)
        resume.seek(0)

        if file_header != b'%PDF':
            raise forms.ValidationError(
                "Uploaded file is not a valid PDF."
            )

        return resume