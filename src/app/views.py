from pprint import pprint

from flask import flash, g, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from app import db, flaskapp
from app.forms import LoginForm, SearchExpenseForm
from app.models import User
from app.redirect import get_local_redirect

###
# Part 1.
# The function below returns a login page to the user when it is not connected to the
# system yet. This is where part 1 will take place. For part 2, see below.
###

@flaskapp.route('/login', methods=['GET', 'POST'])
def login():
    """
    The login view of this application. Return a login page or login a user if authentication
    is successful.
    """

    # Redirect if the current user is logged in
    if g.user and g.user.is_authenticated:
        next = get_local_redirect()
        return redirect(next or url_for('index'))

    # Prepare the login form
    form = LoginForm()

    # If the form is filled
    if form.validate_on_submit():
        # Part 1
        # A terrible way to implement login
        # The administrator of Great Bank is very confident in his application and has published the
        # source code on the internet. That is what you are reading right now. You can thus see how
        # the code is implemented and try to find a vulnerability.
        # The code below execute a request to the database where it tries to match a username and
        # the password provided by the user in the form.
        # Unfortunately, he did not escape the values from the user in any way and you can thus
        # control the query by inserting the right values.

        # Try to input some code  in the login page and see how the code changes in the console.
        # Can you bypass the password check?

        # See below for the answer.

        query = "SELECT * FROM user WHERE username = '" + form.username.data + "' AND password = '" +form.password.data+"'";

        # Print the current query into the console for you to see
        print(query)

        result = list(db.engine.execute(query))
        if result:
            for row in result:
                login_user(User.get_by_username(row['username']), remember=form.remember_me.data)
                flash('Logged in!', 'success')
                return form.redirect('index')
        else:
            flash('Wrong username or password.', 'error')

        # By exploiting the fact that none of the code is escaped properly, we can control the SQL
        # statement and basically, make it always true. By using for instance:
        # Example of SQL injection: 1' OR '1'='1
        # we can make the database say: "Give me 'admin' where password is '1' OR 1=1"
        # As 1=1 is always true, the second part of the predicament is always true and we bypass the
        # authentication entirely. You successfully logged in as an admin!
        # This is one of the simplest form of SQL injection and it is unfortunately still too
        # common today.

        # Part 2 #
        # The admin is pissed as you managed to login as him and take some money from the bank. He
        # discovered the flaw and patched it. (Please comment the whole code above and uncomment the
        # code below.)
        # You can no longer login using the magic password as he now verifies the user exist first
        # and then check the password.
        # See below for the next part.

        ### Patched version of the login:

        # print("Username: {username}".format(username=form.username.data))
        # print("Password: {password}".format(password=form.password.data))
        #
        # user = User.get_by_username(form.username.data)
        # if user and user.check_password(form.password.data):
        #     login_user(user, remember=form.remember_me.data)
        #     flash('Logged in!', 'success')
        #     return form.redirect('index')
        # else:
        #     flash('Wrong username or password.', 'error')

    return render_template('login.html', form=form)


@flaskapp.route('/logout', methods=['GET', 'POST'])
def logout():
    """
    The logout view of this application.
    """
    logout_user()
    flash('Logged out!', 'success')
    return redirect(url_for('login'))


###
# Part 2.
# Please make sure you have un/commented the code above in the login function as instructed.
#
# It has been a while and the bank made more money that you can now steal again. Unfortunately, you
# can no longer login as you did last time. You have to find another way. The page below contains a
# search form that is once again, controlled entirely by the user. Is there a way to exploit this
# to steal the password of the admin?
###

@flaskapp.route('/', methods=['GET'])
@flaskapp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    """
    The index view of this application.
    """

    # Part 2
    # A terrible way to search from the database
    # SQL is a complete language that is very powerful and can actually become quite complex.
    # For large applications, a query can be several pages long and touch 100's of tables. In our
    # scenario, we can exploit the language itself and use one of its feature to steal the password
    # of the admin. The `UNION` keyword in SQL allows you to return in one dataset the data from 2
    # or more tables. We can see that in the query below, we query the `record` table to find
    # all the transactions of the user. We can probably exploit that to also include in the result
    # the information contained in the `user` table that we have seen above.

    # Can you find out how? See below for the answer.

    form = SearchExpenseForm()
    if form.validate_on_submit():
        query = "SELECT * FROM record WHERE user_id = '" + str(g.user.id) + "' AND description LIKE '%" + form.search_string.data + "%'";
    else:
        query = "SELECT * FROM record WHERE user_id = '" + str(g.user.id) + "' ORDER BY date DESC";

    # Print the current query into the console for you to see
    print(query)

    # If you need a hint, here is one: `%' UNION SELECT username FROM user WHERE '%`
    # Try to see if you can use the error message to your advantage

    # By using the `UNION` keyword, we can actually include in the result the data from the `user`
    # table but it has a caviat: We need the same number of columns in the first table and in the
    # second. For that, we can actually just repeat the columns we would like from the `user` table
    # until it matches the number we have in the `record` one.
    # Our SQL injection becomes: `%' UNION SELECT username, username, password, password, password FROM user '`
    # as there is 5 columns in the record table (see `model.py`).
    # With a matching number of columns, the query execute properly and is return as a `record`
    # which is then displayed on screen.
    # You just stole the admin password and can now login with it.
    # Congrats!

    balance_list = []
    try:
        balance_list = list(db.engine.execute(query))
    except Exception as e:
        flash(str(e), "error")

    pprint(balance_list)

    return render_template(
        'index.html',
        balance_list=balance_list,
        search_expense=form
    )
