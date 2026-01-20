from django.contrib import admin
from django.forms import BaseInlineFormSet, ValidationError
from .models import Article, Scope, Tag


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        main_count = 0
        for form in self.forms:
            data = form.cleaned_data
            if data.get('is_main', False):
                main_count += 1
            if main_count == 0:
                raise ValidationError('Укажите основной раздел')
            if main_count > 1:
                raise ValidationError('Основным может быть только один раздел')
        return super().clean()

class ScopeInline(admin.TabularInline):
    model = Scope
    extra = 1
    formset = ScopeInlineFormset

class ArticleInline(admin.TabularInline):
    model = Article.tags.through
    extra = 0

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]
    
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    inlines = [ArticleInline]