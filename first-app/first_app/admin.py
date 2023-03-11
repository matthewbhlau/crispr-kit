from django.contrib import admin
from django.utils.html import format_html

from .models import DataModel, ExpressionPlot

class ExpressionPlotInline(admin.TabularInline):
    model = ExpressionPlot
    extra = 0

class DataModelAdmin(admin.ModelAdmin):
    inlines = [ExpressionPlotInline]
    list_display = ('id', 'name', "organization", "color")

    def image_tag(self, obj):
        print(obj.image.url)
        return format_html('<img src="{}" style="max-width:50%"/>'.format(obj.image.url))

    image_tag.short_description = 'Image Preview'

    def referenced_expression_plots(self, obj):
        expression_plot = ExpressionPlot.objects.filter(related_data=obj.id)
        return [test for test in expression_plot]

    referenced_expression_plots.short_description = 'Referenced Expression Plots'
    readonly_fields = ('image_tag',)
    exclude = ('image',)

admin.site.register(DataModel, DataModelAdmin)