from django import forms
from ckeditor.widgets import CKEditorWidget
from app.models import Course
from .models import Module, Page

class SyllabusForm(forms.ModelForm):
	syllabus = forms.CharField(widget=CKEditorWidget())

	class Meta:
		model = Course
		fields = ['syllabus']


class ModuleForm(forms.ModelForm):
	class Meta:
		model = Module
		fields = ['title']


class PageForm(forms.ModelForm):
	title = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate'}), required=True)
	content = forms.CharField(widget=CKEditorWidget())
	files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

	class Meta:
		model = Page
		fields = ['title', 'content', 'files']