from django import forms

class GradeCalculatorForm(forms.Form):
    current_gpa = forms.FloatField(label='Current GPA', min_value=0, max_value=4, required=True)
    target_gpa = forms.FloatField(label='Target GPA', min_value=0, max_value=4, required=True)
    credits_completed = forms.IntegerField(label='Credits Completed', min_value=0, required=True)
    one_credit_courses = forms.IntegerField(label='1-Credit Courses Remaining', min_value=0, required=True)
    two_credit_courses = forms.IntegerField(label='2-Credit Courses Remaining', min_value=0, required=True)
    three_credit_courses = forms.IntegerField(label='3-Credit Courses Remaining', min_value=0, required=True)