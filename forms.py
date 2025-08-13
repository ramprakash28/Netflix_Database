from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, DateField, SelectField, SubmitField, DecimalField
from wtforms.validators import DataRequired, Email

class UserForm(FlaskForm):
    user_id = IntegerField('User ID', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d', validators=[DataRequired()])
    signup_date = DateField('Signup Date', format='%Y-%m-%d', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        if 'is_update' in kwargs:
            self.submit.label.text = 'Update User'
        else:
            self.submit.label.text = 'Add User'
    
    submit = SubmitField()

class ProfileForm(FlaskForm):
    profile_id = IntegerField('Profile ID', validators=[DataRequired()])
    user_id = IntegerField('User ID', validators=[DataRequired()])
    profile_name = StringField('Profile Name', validators=[DataRequired()])
    profile_type = SelectField(
        'Profile Type',
        choices=[('Standard', 'Standard'), ('Premium', 'Premium')],
        validators=[DataRequired()]
    )
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        if 'is_update' in kwargs:
            self.submit.label.text = 'Update Profile'
        else:
            self.submit.label.text = 'Add Profile'
    
    submit = SubmitField()

class SubscriptionForm(FlaskForm):
    subscription_id = IntegerField('Subscription ID', validators=[DataRequired()])
    user_id = IntegerField('User ID', validators=[DataRequired()])
    subscription_type = SelectField(
        'Subscription Type',
        choices=[('Yearly', 'Yearly'), ('Monthly', 'Monthly')],
        validators=[DataRequired()]
    )
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(SubscriptionForm, self).__init__(*args, **kwargs)
        if 'is_update' in kwargs:
            self.submit.label.text = 'Update Subscription'
        else:
            self.submit.label.text = 'Add Subscription'
    
    submit = SubmitField()

class ContentForm(FlaskForm):
    content_id = IntegerField('Content ID', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    release_date = DateField('Release Date', format='%Y-%m-%d', validators=[DataRequired()])
    duration = IntegerField('Duration', validators=[DataRequired()])
    content_type = SelectField(
        'Content Type',
        choices=[('Movie', 'Movie'), ('TV Show', 'TV Show')],
        validators=[DataRequired()]
    )
    rating = DecimalField('Rating', validators=[DataRequired()])
    genre = StringField('Genre', validators=[DataRequired()])
    user_id = IntegerField('User ID', validators=[DataRequired()])
    movies_tvshows_id = IntegerField('Movies/TV Shows ID', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(ContentForm, self).__init__(*args, **kwargs)
        if 'is_update' in kwargs:
            self.submit.label.text = 'Update Content'
        else:
            self.submit.label.text = 'Add Content'
    
    submit = SubmitField()

class EpisodeForm(FlaskForm):
    episode_id = IntegerField('Episode ID', validators=[DataRequired()])
    episode_number = IntegerField('Episode Number', validators=[DataRequired()])
    season_number = IntegerField('Season Number', validators=[DataRequired()])
    episode_title = StringField('Episode Title', validators=[DataRequired()])
    episode_duration = IntegerField('Episode Duration', validators=[DataRequired()])
    movies_tvshows_id = IntegerField('Movies/TV Shows ID', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(EpisodeForm, self).__init__(*args, **kwargs)
        if 'is_update' in kwargs:
            self.submit.label.text = 'Update Episode'
        else:
            self.submit.label.text = 'Add Episode'
    
    submit = SubmitField()

class UserActivityForm(FlaskForm):
    activity_id = IntegerField('Activity ID', validators=[DataRequired()])
    user_id = IntegerField('User ID', validators=[DataRequired()])
    activity_type = SelectField(
        'Activity Type',
        choices=[('Like', 'Like'), ('Dislike', 'Dislike')],
        validators=[DataRequired()]
    )
    watch_status = SelectField(
        'Watch Status',
        choices=[('Watched', 'Watched'), ('Not watched', 'Not Watched')],
        validators=[DataRequired()]
    )

    def __init__(self, *args, **kwargs):
        super(UserActivityForm, self).__init__(*args, **kwargs)
        if 'is_update' in kwargs:
            self.submit.label.text = 'Update Activity'
        else:
            self.submit.label.text = 'Add Activity'
    
    submit = SubmitField()

class PaymentForm(FlaskForm):
    payment_id = IntegerField('Payment ID', validators=[DataRequired()])
    user_id = IntegerField('User ID', validators=[DataRequired()])
    payment_date = DateField('Payment Date', format='%Y-%m-%d', validators=[DataRequired()])
    due_date = DateField('Due Date', format='%Y-%m-%d', validators=[DataRequired()])
    discount_code = StringField('Discount Code')
    payment_method = SelectField(
        'Payment Method',
        choices=[('Credit Card', 'Credit Card'), ('Debit Card', 'Debit Card'), ('PayPal', 'PayPal')],
        validators=[DataRequired()]
    )
    amount_paid = DecimalField('Amount Paid', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        if 'is_update' in kwargs:
            self.submit.label.text = 'Update Payment'
        else:
            self.submit.label.text = 'Add Payment'
    
    submit = SubmitField()

class PaymentHistoryForm(FlaskForm):
    history_id = IntegerField('History ID', validators=[DataRequired()])
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
    payment_id = IntegerField('Payment ID', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(PaymentHistoryForm, self).__init__(*args, **kwargs)
        if 'is_update' in kwargs:
            self.submit.label.text = 'Update Payment History'
        else:
            self.submit.label.text = 'Add Payment History'
    
    submit = SubmitField()

class CastForm(FlaskForm):
    cast_id = IntegerField('Cast ID', validators=[DataRequired()])
    director_name = StringField('Director Name', validators=[DataRequired()])
    actor_name = StringField('Actor Name', validators=[DataRequired()])
    actress_name = StringField('Actress Name', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(CastForm, self).__init__(*args, **kwargs)
        if 'is_update' in kwargs:
            self.submit.label.text = 'Update Cast'
        else:
            self.submit.label.text = 'Add Cast'
    
    submit = SubmitField()



