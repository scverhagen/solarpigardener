from flask_wtf import Form
from wtforms import StringField, BooleanField, SubmitField, IntegerField, TimeField
from wtforms.validators import DataRequired


# defaultsettingsdict = {'water_inches_per_week':2, 'water_days_per_week':2 , 'sprinkler_inches_per_minute':0.00418, 'enable_auto_watering':0}


class ConfigForm(Form):
    hardware_water_gpio_pin = IntegerField(label=u'Water GPIO Pin', validators=[DataRequired()])
    water_inches_per_week = StringField(label=u'Desired Inches per Week', validators=[DataRequired()])
    water_days_per_week = StringField(label=u'Water Days per Week', validators=[DataRequired()])
    water_time_hour = IntegerField('Watering Time Hour (0-23)', validators=[DataRequired()])
    sprinkler_inches_per_minute = StringField(validators=[DataRequired()])
    enable_auto_watering = BooleanField('Enable Automatic Watering')
    submit = SubmitField('Save Settings')

    