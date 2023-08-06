from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.utils.translation import gettext as _

from material import Layout, Row, Span2

from .models import Item, Order, ProcessingOption


class OrderFormForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["full_name", "email"]


class OrderItemForm(forms.ModelForm):
    count = forms.IntegerField(label=_("Count"), initial=0, validators=[MinValueValidator(0)])

    def clean_count(self):
        count = self.cleaned_data["count"]

        if count > self.instance.max_count:
            raise ValidationError(
                _(f"You can only order {self.instance.max_count} pieces of this item.")
            )

        return count

    class Meta:
        model = Item
        fields = ["count"]


OrderItemFormSet = forms.modelformset_factory(Item, form=OrderItemForm, max_num=0, extra=0)


class ProcessingOptionForm(forms.Form):
    processing_option = forms.ModelChoiceField(ProcessingOption.objects.all())


class ShippingAddressForm(forms.Form):
    layout = Layout(
        Row("full_name"),
        Row("second_address_row"),
        Row(Span2("street"), "housenumber"),
        Row("plz", Span2("place")),
    )
    full_name = forms.CharField(label=_("First and last name"))
    second_address_row = forms.CharField(label=_("Second address row"), required=False)
    street = forms.CharField(label=_("Street"))
    housenumber = forms.CharField(label=_("Housenumber"))
    plz = forms.CharField(label=_("PLZ"), max_length=5)
    place = forms.CharField(label=_("Place"))


class NotesForm(forms.Form):
    notes = forms.CharField(widget=forms.Textarea, label=_("Notes to your order"), required=False)


class AccessForm(forms.Form):
    access_code = forms.CharField(
        label=_("Access code"), widget=forms.TextInput(attrs={"autofocus": "autofocus"})
    )

    def clean_access_code(self):
        return self.cleaned_data.get("access_code", "").lower().strip()
