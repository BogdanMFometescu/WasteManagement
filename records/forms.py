from django.forms import ModelForm
from .models import Record


class RecordForm(ModelForm):
    class Meta:
        model = Record
        fields = '__all__'
        exclude = ['owner', 'tags', 'waste_name']
        labels = {'picture': 'Waste photo (if available).',
                  'waste_description': 'Additional details about this record:', 'waste_code': 'Waste code and name',
                  'evidence': 'Transport documents evidence (mandatory field)'}

    def __init__(self, *args, **kwargs):
        super(RecordForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

        self.fields['type_of_waste'].widget.attrs.update(
            {'class': 'content-box'})

        self.fields['waste_code'].widget.attrs.update(
            {'class': 'content-box'})

        self.fields['recycling_method'].widget.attrs.update(
            {'class': 'content-box'})

        self.fields['disposal_method'].widget.attrs.update(
            {'class': 'content-box'})

    def clean(self):
        cleaned_data = super().clean()
        generated_quantity = cleaned_data.get('generated_quantity')
        recycled_quantity = cleaned_data.get('recycled_quantity')
        disposed_quantity = cleaned_data.get('disposed_quantity')
        evidence_file = cleaned_data.get('evidence')

        if generated_quantity is not None and recycled_quantity is not None and disposed_quantity is not None:
            if generated_quantity < recycled_quantity:
                self.add_error('recycled_quantity', 'Recycled quantity must be lower or equal to generated quantity')

            elif generated_quantity < disposed_quantity:
                self.add_error('disposed_quantity', 'Disposed quantity must be lower or equal to generated quantity')

            elif generated_quantity < 0:
                self.add_error('generated_quantity', 'Generated quantity must be greater than zero.')
            elif recycled_quantity < 0:
                self.add_error('recycled_quantity', 'Recycled quantity must be greater than zero.')

            elif disposed_quantity < 0:
                self.add_error('disposed_quantity', 'Disposed quantity must be greater than zero.')

            elif evidence_file is None:
                self.add_error('evidence', 'Please upload a file for waste transport documents')
