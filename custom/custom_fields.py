import re
from wtforms import StringField
from wtforms.validators import ValidationError


class EgyptPhone:
    """
    Validator للرقم المصري:
    - لازم يكون 11 رقم
    - لازم يكون كله أرقام
    - لازم يبدأ بـ 010 / 011 / 012 / 015
    """

    def __call__(self, form, field):
        number = field.data.strip()


        if not number.isdigit():
            raise ValidationError("رقم الموبايل يجب أن يحتوي على أرقام فقط.")


        if len(number) != 11:
            raise ValidationError("رقم الموبايل يجب أن يكون 11 رقم بالضبط.")


        if not re.match(r"^(010|011|012|015)", number):
            raise ValidationError("رقم الموبايل يجب أن يبدأ بـ 010 أو 011 أو 012 أو 015.")


class EgyptPhoneField(StringField):
    """حقل جديد مثل StringField لكن مخصص لأرقام مصر"""

    def __init__(self, label=None, **kwargs):
        super().__init__(label, **kwargs)

    def process_formdata(self, valuelist):

        if valuelist:
            self.data = valuelist[0].replace(" ", "")
        else:
            self.data = ""
