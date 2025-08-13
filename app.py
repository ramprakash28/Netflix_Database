from flask import Flask, render_template, request, redirect, url_for, abort, flash
import mysql.connector
from mysql.connector import IntegrityError
from forms import UserForm, ProfileForm, SubscriptionForm, ContentForm, EpisodeForm, UserActivityForm, PaymentForm, PaymentHistoryForm, CastForm

# Connect to MySQL and specify the Netflix database
try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="rpdatabase",
        database="Netflix"
    )
    mycursor = mydb.cursor()
    print(f"Successfully connected to the database: {mydb.database}")
except Exception as e:
    print(f"An error occurred: {e}")

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'secret_key_group_17'

import logging
from logging.handlers import RotatingFileHandler

# Configure logging
if not app.debug:  # Only enable logging when not in debug mode
    handler = RotatingFileHandler('error.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.ERROR)
    app.logger.addHandler(handler)


@app.route('/')
def splash():
    return render_template('splash.html')


@app.route('/home')
def home():
    mycursor.execute("SHOW TABLES")
    tables = mycursor.fetchall()
    tables = tables[:-1]  
    return render_template('index.html', tables=tables)

# Routes for CRUD Operations

# 1. User Routes
@app.route('/users')
def users():
    mycursor.execute("SELECT * FROM user")
    data = mycursor.fetchall()
    return render_template('users.html', data=data)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        sql = """
            INSERT INTO user (user_id, username, first_name, last_name, email, password, phone_number, date_of_birth, signup_date, age) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            form.user_id.data, form.username.data, form.first_name.data, form.last_name.data,
            form.email.data, form.password.data, form.phone_number.data, form.date_of_birth.data,
            form.signup_date.data, form.age.data
        )
        mycursor.execute(sql, values)
        mydb.commit()
        return redirect(url_for('users'))
    return render_template('add_user.html', form=form, action='Add')

@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    sql = "DELETE FROM user WHERE user_id = %s"
    mycursor.execute(sql, (user_id,))
    mydb.commit()
    return redirect(url_for('users'))

@app.route('/update_user/<int:user_id>', methods=['GET', 'POST'])
def update_user(user_id):
    mycursor.execute("SELECT * FROM user WHERE user_id = %s", (user_id,))
    user = mycursor.fetchone()
    if user is None:
        abort(404)
    form = UserForm(request.form, is_update=True)
    if not form.is_submitted():
        form.user_id.data, form.username.data, form.first_name.data, form.last_name.data = user[:4]
        form.email.data, form.password.data, form.phone_number.data = user[4:7]
        form.date_of_birth.data, form.signup_date.data, form.age.data = user[7:10]
    if form.is_submitted():
        sql = """
            UPDATE user SET username = %s, first_name = %s, last_name = %s, email = %s, password = %s,
            phone_number = %s, date_of_birth = %s, signup_date = %s, age = %s WHERE user_id = %s
        """
        values = (
            form.username.data, form.first_name.data, form.last_name.data, form.email.data,
            form.password.data, form.phone_number.data, form.date_of_birth.data, form.signup_date.data,
            form.age.data, user_id
        )
        mycursor.execute(sql, values)
        mydb.commit()
        return redirect(url_for('users'))
    return render_template('add_user.html', form=form, action='Update')

# 2. Profile Routes
@app.route('/profiles')
def profiles():
    mycursor.execute("SELECT * FROM profile")
    data = mycursor.fetchall()
    return render_template('profiles.html', data=data)

@app.route('/add_profile', methods=['GET', 'POST'])
def add_profile():
    form = ProfileForm()
    if form.validate_on_submit():
        sql = """
            INSERT INTO profile (profile_id, user_id, profile_name, profile_type) 
            VALUES (%s, %s, %s, %s)
        """
        values = (form.profile_id.data, form.user_id.data, form.profile_name.data, form.profile_type.data)
        try:
            mycursor.execute(sql, values)
            mydb.commit()
            flash('Profile added successfully!', 'success')
            return redirect(url_for('profiles'))
        except IntegrityError:
            flash('Failed to add profile: user_id does not exist or violates foreign key constraints.', 'danger')
            return redirect(url_for('add_profile'))
        mycursor.execute(sql, values)
        mydb.commit()
        return redirect(url_for('profiles'))
    return render_template('add_profile.html', form=form, action='Add')

@app.route('/delete_profile/<int:profile_id>')
def delete_profile(profile_id):
    sql = "DELETE FROM profile WHERE profile_id = %s"
    mycursor.execute(sql, (profile_id,))
    mydb.commit()
    return redirect(url_for('profiles'))

@app.route('/update_profile/<int:profile_id>', methods=['GET', 'POST'])
def update_profile(profile_id):
    mycursor.execute("SELECT * FROM profile WHERE profile_id = %s", (profile_id,))
    profile = mycursor.fetchone()
    if profile is None:
        abort(404)
    form = ProfileForm(request.form, is_update=True)
    if not form.is_submitted():
        form.profile_id.data, form.user_id.data, form.profile_name.data, form.profile_type.data = profile
    if form.is_submitted():
        sql = """
            UPDATE profile SET user_id = %s, profile_name = %s, profile_type = %s WHERE profile_id = %s
        """
        values = (form.user_id.data, form.profile_name.data, form.profile_type.data, profile_id)
        mycursor.execute(sql, values)
        mydb.commit()
        return redirect(url_for('profiles'))
    return render_template('add_profile.html', form=form, action='Update')

# 3. Subscription Routes
@app.route('/subscriptions')
def subscriptions():
    mycursor.execute("SELECT * FROM subscription")
    data = mycursor.fetchall()
    return render_template('subscriptions.html', data=data)

@app.route('/add_subscription', methods=['GET', 'POST'])
def add_subscription():
    form = SubscriptionForm()
    if form.validate_on_submit():
        sql = """
            INSERT INTO subscription (subscription_id, user_id, subscription_type, start_date, end_date) 
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (
            form.subscription_id.data, form.user_id.data, form.subscription_type.data,
            form.start_date.data, form.end_date.data
        )
        mycursor.execute(sql, values)
        mydb.commit()
        return redirect(url_for('subscriptions'))
    return render_template('add_subscription.html', form=form, action='Add')

@app.route('/delete_subscription/<int:subscription_id>')
def delete_subscription(subscription_id):
    sql = "DELETE FROM subscription WHERE subscription_id = %s"
    mycursor.execute(sql, (subscription_id,))
    mydb.commit()
    return redirect(url_for('subscriptions'))

@app.route('/update_subscription/<int:subscription_id>', methods=['GET', 'POST'])
def update_subscription(subscription_id):
    mycursor.execute("SELECT * FROM subscription WHERE subscription_id = %s", (subscription_id,))
    subscription = mycursor.fetchone()
    if subscription is None:
        abort(404)
    form = SubscriptionForm(request.form, is_update=True)
    if not form.is_submitted():
        form.subscription_id.data, form.user_id.data, form.subscription_type.data = subscription[:3]
        form.start_date.data, form.end_date.data = subscription[3:5]
    if form.is_submitted():
        sql = """
            UPDATE subscription SET user_id = %s, subscription_type = %s, start_date = %s, end_date = %s 
            WHERE subscription_id = %s
        """
        values = (
            form.user_id.data, form.subscription_type.data, form.start_date.data,
            form.end_date.data, subscription_id
        )
        mycursor.execute(sql, values)
        mydb.commit()
        return redirect(url_for('subscriptions'))
    return render_template('add_subscription.html', form=form, action='Update')

# 4. Content Routes
@app.route('/content')
def content():
    mycursor.execute("SELECT * FROM content")
    data = mycursor.fetchall()
    return render_template('content.html', data=data)

@app.route('/add_content', methods=['GET', 'POST'])
def add_content():
    form = ContentForm()
    if form.validate_on_submit():
        sql = """
            INSERT INTO content (content_id, title, description, release_date, duration, content_type, rating, genre, user_id, movies_tvshows_id) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            form.content_id.data, form.title.data, form.description.data, form.release_date.data,
            form.duration.data, form.content_type.data, form.rating.data, form.genre.data,
            form.user_id.data, form.movies_tvshows_id.data
        )
        mycursor.execute(sql, values)
        mydb.commit()
        return redirect(url_for('content'))
    return render_template('add_content.html', form=form, action='Add')

@app.route('/delete_content/<int:content_id>')
def delete_content(content_id):
    sql = "DELETE FROM content WHERE content_id = %s"
    mycursor.execute(sql, (content_id,))
    mydb.commit()
    return redirect(url_for('content'))

@app.route('/update_content/<int:content_id>', methods=['GET', 'POST'])
def update_content(content_id):
    mycursor.execute("SELECT * FROM content WHERE content_id = %s", (content_id,))
    content = mycursor.fetchone()
    if content is None:
        abort(404)
    form = ContentForm(request.form, is_update=True)
    if not form.is_submitted():
        form.content_id.data, form.title.data, form.description.data, form.release_date.data = content[:4]
        form.duration.data, form.content_type.data, form.rating.data, form.genre.data = content[4:8]
        form.user_id.data, form.movies_tvshows_id.data = content[8:10]
    if form.is_submitted():
        sql = """
            UPDATE content SET title = %s, description = %s, release_date = %s, duration = %s,
            content_type = %s, rating = %s, genre = %s, user_id = %s, movies_tvshows_id = %s
            WHERE content_id = %s
        """
        values = (
            form.title.data, form.description.data, form.release_date.data, form.duration.data,
            form.content_type.data, form.rating.data, form.genre.data, form.user_id.data,
            form.movies_tvshows_id.data, content_id
        )
        mycursor.execute(sql, values)
        mydb.commit()
        return redirect(url_for('content'))
    return render_template('add_content.html', form=form, action='Update')

# 5. Episode Routes
@app.route('/episode')
def episode():
    mycursor.execute("SELECT * FROM episode")
    data = mycursor.fetchall()
    return render_template('episode.html', data=data)

@app.route('/add_episode', methods=['GET', 'POST'])
def add_episode():
    form = EpisodeForm()
    if form.validate_on_submit():
        sql = """
            INSERT INTO episode (episode_id, episode_number, season_number, episode_title, episode_duration, movies_tvshows_id) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (
            form.episode_id.data, form.episode_number.data, form.season_number.data,
            form.episode_title.data, form.episode_duration.data, form.movies_tvshows_id.data
        )
        mycursor.execute(sql, values)
        mydb.commit()
        return redirect(url_for('episode'))
    return render_template('add_episode.html', form=form, action='Add')

@app.route('/delete_episode/<int:episode_id>')
def delete_episode(episode_id):
    sql = "DELETE FROM episode WHERE episode_id = %s"
    mycursor.execute(sql, (episode_id,))
    mydb.commit()
    return redirect(url_for('episode'))

@app.route('/update_episode/<int:episode_id>', methods=['GET', 'POST'])
def update_episode(episode_id):
    mycursor.execute("SELECT * FROM episode WHERE episode_id = %s", (episode_id,))
    episode = mycursor.fetchone()
    if episode is None:
        abort(404)
    form = EpisodeForm(request.form, is_update=True)
    if not form.is_submitted():
        form.episode_id.data, form.episode_number.data, form.season_number.data = episode[:3]
        form.episode_title.data, form.episode_duration.data, form.movies_tvshows_id.data = episode[3:6]
    if form.is_submitted():
        sql = """
            UPDATE episode SET episode_number = %s, season_number = %s, episode_title = %s,
            episode_duration = %s, movies_tvshows_id = %s WHERE episode_id = %s
        """
        values = (
            form.episode_number.data, form.season_number.data, form.episode_title.data,
            form.episode_duration.data, form.movies_tvshows_id.data, episode_id
        )
        mycursor.execute(sql, values)
        mydb.commit()
        return redirect(url_for('episode'))
    return render_template('add_episode.html', form=form, action='Update')

# 6. User Activity Routes
@app.route('/user_activity')
def user_activity():
    mycursor.execute("SELECT * FROM user_activity")
    data = mycursor.fetchall()
    return render_template('user_activity.html', data=data)

@app.route('/add_user_activity', methods=['GET', 'POST'])
def add_user_activity():
    form = UserActivityForm()
    if form.validate_on_submit():
        sql = """
            INSERT INTO user_activity (activity_id, user_id, activity_type, watch_status) 
            VALUES (%s, %s, %s, %s)
        """
        values = (form.activity_id.data, form.user_id.data, form.activity_type.data, form.watch_status.data)
        mycursor.execute(sql, values)
        mydb.commit()
        return redirect(url_for('user_activity'))
    return render_template('add_user_activity.html', form=form, action='Add')

@app.route('/delete_user_activity/<int:activity_id>')
def delete_user_activity(activity_id):
    sql = "DELETE FROM user_activity WHERE activity_id = %s"
    mycursor.execute(sql, (activity_id,))
    mydb.commit()
    return redirect(url_for('user_activity'))

@app.route('/update_user_activity/<int:activity_id>', methods=['GET', 'POST'])
def update_user_activity(activity_id):
    mycursor.execute("SELECT * FROM user_activity WHERE activity_id = %s", (activity_id,))
    user_activity = mycursor.fetchone()
    if user_activity is None:
        abort(404)
    form = UserActivityForm(request.form, is_update=True)
    if not form.is_submitted():
        form.activity_id.data, form.user_id.data, form.activity_type.data, form.watch_status.data = user_activity
    if form.is_submitted():
        sql = """
            UPDATE user_activity SET user_id = %s, activity_type = %s, watch_status = %s WHERE activity_id = %s
        """
        values = (form.user_id.data, form.activity_type.data, form.watch_status.data, activity_id)
        mycursor.execute(sql, values)
        mydb.commit()
        return redirect(url_for('user_activity'))
    return render_template('add_user_activity.html', form=form, action='Update')

# 7. Payment Routes
@app.route('/payment')
def payment():
    mycursor.execute("SELECT * FROM payment")
    data = mycursor.fetchall()
    return render_template('payment.html', data=data)

@app.route('/add_payment', methods=['GET', 'POST'])
def add_payment():
    form = PaymentForm()
    if form.validate_on_submit():
        sql = """
            INSERT INTO payment (payment_id, user_id, payment_date, due_date, discount_code, payment_method, amount_paid) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            form.payment_id.data, form.user_id.data, form.payment_date.data,
            form.due_date.data, form.discount_code.data, form.payment_method.data, form.amount_paid.data
        )
        mycursor.execute(sql, values)
        mydb.commit()
        return redirect(url_for('payment'))
    return render_template('add_payment.html', form=form, action='Add')

@app.route('/update_payment/<int:payment_id>', methods=['GET', 'POST'])
def update_payment(payment_id):
    mycursor.execute("SELECT * FROM payment WHERE payment_id = %s", (payment_id,))
    payment = mycursor.fetchone()
    if payment is None:
        abort(404)
    form = PaymentForm(request.form, is_update=True)
    if not form.is_submitted():
        form.payment_id.data, form.user_id.data, form.payment_date.data = payment[:3]
        form.due_date.data, form.discount_code.data, form.payment_method.data, form.amount_paid.data = payment[3:]
    if form.is_submitted():
        sql = """
            UPDATE payment SET user_id = %s, payment_date = %s, due_date = %s, discount_code = %s, 
            payment_method = %s, amount_paid = %s WHERE payment_id = %s
        """
        values = (
            form.user_id.data, form.payment_date.data, form.due_date.data,
            form.discount_code.data, form.payment_method.data, form.amount_paid.data, payment_id
        )
        mycursor.execute(sql, values)
        mydb.commit()
        return redirect(url_for('payment'))
    return render_template('add_payment.html', form=form, action='Update')

@app.route('/delete_payment/<int:payment_id>')
def delete_payment(payment_id):
    sql = "DELETE FROM payment WHERE payment_id = %s"
    mycursor.execute(sql, (payment_id,))
    mydb.commit()
    return redirect(url_for('payment'))

# 8. Payment History Routes
@app.route('/payment_history')
def payment_history():
    mycursor.execute("SELECT * FROM payment_history")
    data = mycursor.fetchall()
    return render_template('payment_history.html', data=data)

@app.route('/add_payment_history', methods=['GET', 'POST'])
def add_payment_history():
    form = PaymentHistoryForm()
    if form.validate_on_submit():
        sql = """
            INSERT INTO payment_history (history_id, start_date, end_date, payment_id) 
            VALUES (%s, %s, %s, %s)
        """
        values = (
            form.history_id.data, form.start_date.data, form.end_date.data, form.payment_id.data
        )
        mycursor.execute(sql, values)
        mydb.commit()
        return redirect(url_for('payment_history'))
    return render_template('add_payment_history.html', form=form, action='Add')

@app.route('/delete_payment_history/<int:history_id>')
def delete_payment_history(history_id):
    sql = "DELETE FROM payment_history WHERE history_id = %s"
    mycursor.execute(sql, (history_id,))
    mydb.commit()
    return redirect(url_for('payment_history'))

@app.route('/update_payment_history/<int:history_id>', methods=['GET', 'POST'])
def update_payment_history(history_id):
    mycursor.execute("SELECT * FROM payment_history WHERE history_id = %s", (history_id,))
    history = mycursor.fetchone()
    if history is None:
        abort(404)
    form = PaymentHistoryForm(request.form, is_update=True)
    if not form.is_submitted():
        form.history_id.data, form.start_date.data, form.end_date.data, form.payment_id.data = history
    if form.is_submitted():
        sql = """
            UPDATE payment_history SET start_date = %s, end_date = %s, payment_id = %s 
            WHERE history_id = %s
        """
        values = (
            form.start_date.data, form.end_date.data, form.payment_id.data, history_id
        )
        mycursor.execute(sql, values)
        mydb.commit()
        return redirect(url_for('payment_history'))
    return render_template('add_payment_history.html', form=form, action='Update')

# 9. Cast Routes
@app.route('/cast')
def cast():
    mycursor.execute("SELECT * FROM cast")
    data = mycursor.fetchall()
    return render_template('cast.html', data=data)

@app.route('/add_cast', methods=['GET', 'POST'])
def add_cast():
    form = CastForm()
    if form.validate_on_submit():
        sql = """
            INSERT INTO cast (cast_id, director_name, actor_name, actress_name) 
            VALUES (%s, %s, %s, %s)
        """
        values = (
            form.cast_id.data, form.director_name.data, form.actor_name.data, form.actress_name.data
        )
        mycursor.execute(sql, values)
        mydb.commit()
        return redirect(url_for('cast'))
    return render_template('add_cast.html', form=form, action='Add')

@app.route('/delete_cast/<int:cast_id>')
def delete_cast(cast_id):
    sql = "DELETE FROM cast WHERE cast_id = %s"
    mycursor.execute(sql, (cast_id,))
    mydb.commit()
    return redirect(url_for('cast'))

@app.route('/update_cast/<int:cast_id>', methods=['GET', 'POST'])
def update_cast(cast_id):
    mycursor.execute("SELECT * FROM cast WHERE cast_id = %s", (cast_id,))
    cast_record = mycursor.fetchone()
    if cast_record is None:
        abort(404)
    form = CastForm(request.form, is_update=True)
    if not form.is_submitted():
        form.cast_id.data, form.director_name.data, form.actor_name.data, form.actress_name.data = cast_record
    if form.is_submitted():
        sql = """
            UPDATE cast SET director_name = %s, actor_name = %s, actress_name = %s 
            WHERE cast_id = %s
        """
        values = (
            form.director_name.data, form.actor_name.data, form.actress_name.data, cast_id
        )
        mycursor.execute(sql, values)
        mydb.commit()
        return redirect(url_for('cast'))
    return render_template('add_cast.html', form=form, action='Update')

@app.route('/query/total_users')
def total_users():
    mycursor.execute("SELECT COUNT(*) AS total_users FROM user;")
    result = mycursor.fetchone()
    return render_template('total_users.html', result=result)

@app.route('/query/average_rating')
def average_rating():
    mycursor.execute("""
        SELECT content_type, AVG(rating) AS average_rating
        FROM content
        GROUP BY content_type;
    """)
    result = mycursor.fetchall()  # Fetch the results as a list of tuples
    return render_template('average_rating.html', result=result)


@app.route('/query/rank_content')
def rank_content():
    mycursor.execute("""
        SELECT title, rating,
               RANK() OVER (ORDER BY rating DESC) AS content_rank
        FROM content;
    """)
    result = mycursor.fetchall()
    return render_template('rank_content.html', result=result)

@app.route('/query/subscription_percentage')
def subscription_percentage():
    mycursor.execute("""
        SELECT subscription_type,
               COUNT(*) AS total_subscriptions,
               (COUNT(*) * 100.0 / SUM(COUNT(*)) OVER ()) AS percentage
        FROM subscription
        GROUP BY subscription_type;
    """)
    result = mycursor.fetchall()
    return render_template('subscription_percentage.html', result=result)

@app.route('/window_functions')
def window_functions():
    queries = [
        # Set Operations
        {"title": "Same Signup Date", "url": "/query/set_operations"},
        
        # Set Membership
        {"title": "Unpaid Users", "url": "/query/set_membership"},
        {"title": "Inactive Subscriptions", "url": "/query/subscriptions_never_watched"},
        
        # Set Comparison
        {"title": "Watched All Horror", "url": "/query/profiles_watched_all_genre/horror"},
        {"title": "Movies Only", "url": "/query/users_movies_no_tv"},
        
        # Subqueries Using the WITH Clause
        {"title": "Top Watched", "url": "/query/top_watched_content"},
        
        # Advanced Aggregate Functions
        {"title": "Avg Rating by Type", "url": "/query/average_rating"},
        {"title": "Genre Performance", "url": "/query/content_performance"},
        
        # OLAP Queries
        {"title": "Cumulative Content", "url": "/query/cumulative_content"},
        {"title": "Sub. Percentage", "url": "/query/subscription_percentage"},
        {"title": "Payment Dates", "url": "/query/payment_dates"}
    ]
    return render_template('window_functions.html', queries=queries)


@app.route('/query/set_operations')
def set_operations():
    mycursor.execute("""
        SELECT u1.username AS user1, u2.username AS user2, u1.signup_date
        FROM user u1
        JOIN user u2 ON u1.signup_date = u2.signup_date AND u1.user_id != u2.user_id
        EXCEPT
        SELECT u1.username, u2.username, u1.signup_date
        FROM user u1
        JOIN user u2 ON u1.signup_date = u2.signup_date AND u1.username LIKE '%test%';
    """)
    result = mycursor.fetchall()
    return render_template('set_operations.html', result=result)

@app.route('/query/set_membership')
def set_membership():
    mycursor.execute("""
        SELECT username
        FROM user
        WHERE user_id NOT IN (SELECT user_id FROM payment);
    """)
    result = mycursor.fetchall()
    return render_template('set_membership.html', result=result)

@app.route('/query/top_watched_content')
def top_watched_content():
    try:
        mycursor.execute("""
            WITH watch_counts AS (
                SELECT c.title, COUNT(cb.profile_id) AS total_watches
                FROM content c
                JOIN content_bridge_profile cb ON c.content_id = cb.content_id
                GROUP BY c.title
            )
            SELECT title, total_watches
            FROM watch_counts
            ORDER BY total_watches DESC
            LIMIT 5;
        """)
        result = mycursor.fetchall()  # Fetch the results
        return render_template('top_watched_content.html', result=result)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return f"An error occurred: {err}"
    
@app.route('/query/content_performance')
def content_performance():
    try:
        mycursor.execute("""
            SELECT c.genre, 
                   AVG(c.rating) AS avg_rating, 
                   COUNT(cb.profile_id) AS watch_count
            FROM content c
            LEFT JOIN content_bridge_profile cb ON c.content_id = cb.content_id
            GROUP BY c.genre
            ORDER BY watch_count DESC, avg_rating DESC;
        """)
        result = mycursor.fetchall()  # Fetch the results
        return render_template('content_performance.html', result=result)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return f"An error occurred: {err}"
    
@app.route('/query/cumulative_content')
def cumulative_content():
    try:
        mycursor.execute("""
            SELECT release_date, 
                   COUNT(*) AS content_count,
                   SUM(COUNT(*)) OVER (ORDER BY release_date) AS cumulative_content
            FROM content
            GROUP BY release_date;
        """)
        result = mycursor.fetchall()  # Fetch the results
        return render_template('cumulative_content.html', result=result)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return f"An error occurred: {err}"
    
@app.route('/query/payment_dates')
def payment_dates():
    try:
        mycursor.execute("""
            SELECT u.username,
                   MIN(p.payment_date) OVER (PARTITION BY u.user_id) AS first_payment,
                   MAX(p.payment_date) OVER (PARTITION BY u.user_id) AS last_payment
            FROM payment p
            JOIN user u ON p.user_id = u.user_id;
        """)
        result = mycursor.fetchall()  # Fetch the results
        return render_template('payment_dates.html', result=result)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return f"An error occurred: {err}"

@app.route('/query/users_movies_no_tv')
def users_movies_no_tv():
    try:
        query = """
            WITH user_movies AS (
                SELECT ua.user_id
                FROM user_activity ua
                JOIN content c ON ua.activity_id = c.content_id
                WHERE c.content_type = 'Movie'
                  AND ua.activity_type = 'Watched'
            ),
            user_tv_shows AS (
                SELECT ua.user_id
                FROM user_activity ua
                JOIN content c ON ua.activity_id = c.content_id
                WHERE c.content_type = 'TV Show'
                  AND ua.activity_type = 'Watched'
            )
            SELECT DISTINCT um.user_id
            FROM user_movies um
            WHERE um.user_id NOT IN (SELECT user_id FROM user_tv_shows);
        """
        mycursor.execute(query)
        result = mycursor.fetchall()
        return render_template('users_movies_no_tv.html', result=result)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return f"An error occurred: {err}"
    
@app.route('/query/subscriptions_never_watched')
def subscriptions_never_watched():
    try:
        query = """
            WITH watched_users AS (
                SELECT DISTINCT ua.user_id
                FROM user_activity ua
                WHERE ua.activity_type = 'Watched'
            )
            SELECT s.subscription_id, s.user_id
            FROM subscription s
            WHERE s.user_id NOT IN (SELECT user_id FROM watched_users);
        """
        mycursor.execute(query)
        result = mycursor.fetchall()
        return render_template('subscriptions_never_watched.html', result=result)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return f"An error occurred: {err}"
    
@app.route('/query/profiles_watched_all_genre/horror')
def profiles_watched_all_horror():
    try:
        query = f"""
            WITH genre_content AS (
                SELECT content_id
                FROM content
                WHERE genre = %s
            ),
            profile_watched_content AS (
                SELECT profile_id, content_id
                FROM content_bridge_profile
            )
            SELECT pwc.profile_id
            FROM profile_watched_content pwc
            WHERE pwc.content_id IN (SELECT content_id FROM genre_content)
            GROUP BY pwc.profile_id
            HAVING COUNT(DISTINCT pwc.content_id) = (SELECT COUNT(*) FROM genre_content);
        """
        mycursor.execute(query, ('Horror',))
        result = mycursor.fetchall()
        return render_template('profiles_watched_all_genre.html', genre='Horror', result=result)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return f"An error occurred: {err}"

# Custom 404 Error Handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', error="Oops! The page you are looking for doesn't exist."), 404

# Custom 500 Error Handler
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', error="Sorry! Something went wrong on our side. Please try again later."), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)

