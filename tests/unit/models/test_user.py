# -*- coding: utf-8 -*-

"""
tests.models.test_user
~~~~~~~~~~~~~~~~~~~~~~

Unit tests for the user model.
"""

import pytest

from sqlalchemy.exc import IntegrityError, OperationalError

from app.models import (
    DuplicateEmailError,
    Email,
    IntegrityConstraintViolation,
    User
)
from tests.utilities.decorators import requires_mysql
from tests.utilities.fixtures import app, db, session
from tests.utilities.helpers import create_user


def test_user_has_expected_attributes(session):
    """A user should have a first_name and last_name."""
    # Given a user
    user = User(first_name='Jane', last_name='Doe', email='jane@example.com')

    # Then you should see expected attributes
    assert user.first_name == 'Jane'
    assert user.last_name == 'Doe'

def test_user_can_be_saved_to_database(session):
    """A user can be saved to the database."""
    # Given a user
    user = User(first_name='Jane', last_name='Doe', password='password123',
                email='jane@example.com')

    # When a user is saved to the database
    user.save()

    # Then a query should find it and it should be active
    user = session.query(User).filter_by(first_name='Jane').first()
    assert user.first_name == 'Jane'
    assert user.active
    assert user.is_active  # Proxied from active property

def test_user_can_be_compared_to_another_user(session):
    """A user can be be compared to another user."""
    # Given 2 users and a mock copy of the first
    user_1 = User(first_name='Jane', last_name='Doe', password='password123',
                  email='_jane@example.com')
    user_1_copy = User(first_name='Jane', last_name='Doe',
                       password='password123', email='_jane@example.com')
    user_2 = User(first_name='John', last_name='Smith', password='password123',
                  email='john@example.com')
    user_1.save()
    user_1_copy.id = user_1.id

    # Then comparisons should be correct
    assert user_1 == user_1_copy
    assert not user_1 == user_2

def test_user_has_a_dynamic_name_property(session):
    """A user has a dynaimc name property that is the first and last names
    combined."""
    # Given a user
    user = User(first_name='John', last_name='Smith', email='john@example.com')

    # Then you should have dynamic name property
    assert user.name == 'John Smith'

def test_user_saves_password_as_hash(session):
    """A user stores its password as a one-way hash that it checks against."""
    # Given a user
    user = User(email='example@example.com')

    # When a password is set
    user.password = 'my_password'

    # Then the password is stored encrypted
    assert user.password != 'my_password'
    assert user.check_password('my_password')

def test_user_must_be_created_with_at_least_one_email(session):
    """A user must be created with at least one email."""
    # When a user is created without an email
    # Then a value error is thrown
    with pytest.raises(ValueError):
        User(first_name='John', last_name='Smith')

def test_user_can_have_more_than_one_email(session):
    """A user can be created with more than one email."""
    # Given a user with more than one email
    user = create_user(session, email=None, emails=['jane1@example.com',
                                                    'jane2@example.com',
                                                    'jane3@example.com'])

    # Then those emails should all be accessible
    assert user.emails[0].email == 'jane1@example.com'
    assert user.emails[1].email == 'jane2@example.com'
    assert user.emails[2].email == 'jane3@example.com'

def test_user_can_add_emails(session):
    """A user can add emails to their existing account."""
    # Given a user
    user = create_user(session, email='jane1@example.com')

    # When an email is added using `add_email` method
    user.add_email('jane2@example.com')
    # Then that email should be accessible
    assert user.emails[1].email == 'jane2@example.com'

    # When an email is added using `add_email` method using keyword
    user.add_email(email='jane3@example.com')
    # Then that email should be accessible
    assert user.emails[2].email == 'jane3@example.com'

    # When a list of  emails is added using `add_email` method
    user.add_email(emails=['jane4@example.com', 'jane5@example.com'])
    # Then that email should be accessible
    assert user.emails[3].email == 'jane4@example.com'
    assert user.emails[4].email == 'jane5@example.com'

    # When an email is added using SQLAlchemy's `append` method
    user.emails.append(Email(email='jane6@example.com'))
    # Then that email should be accessible
    assert user.emails[5].email == 'jane6@example.com'

def test_user_can_use_the_email_property_to_add_emails(session):
    """A user can use the email property to add emails to their existing
    account."""
    user = create_user(session, email='jane1@example.com')

    # When an email is added using `add_email` method
    user.email = 'jane2@example.com'

    # Then that email should be accessible
    assert user.emails[1].email == 'jane2@example.com'

def test_user_can_remove_emails(session):
    """A user can remove emails from their account."""
    # Given a user with multiple emails
    user = create_user(session, email='jane1@example.com')

    # When an email is removed
    user.remove_email('jane1@example.com')
    session.commit()

    # Then that email should no longer be accessible
    assert len(user.emails) == 0

def test_user_cannot_add_another_users_verified_email(session):
    """A user cannot add another users verified email address."""
    # Given a user with a verified email and another user
    user_1 = create_user(session, email='jane@example.com')
    user_1.emails[0].verify()

    user_2 = create_user(session, email='john@example.com')

    # When trying to add the first user's email on the second user
    # Then expect a DuplicateEmailError
    with pytest.raises(DuplicateEmailError):
        user_2.add_email(email='jane@example.com')

def test_user_can_add_another_users_unverified_email(session):
    """A user *can* add another user's unverified email address. If they
    haven't verified it, it's still up for grabs. This keeps someone from
    'holding' an email hostage.

    Note that in the database, the old row is removed and a new row is
    created."""
    # Given a user with an unverified email and another user
    user_1 = create_user(session, email='jane@example.com')
    user_2 = create_user(session, email='john@example.com')

    # When second user tries to take the unverified email
    user_2.add_email(email='jane@example.com')
    session.commit()

    # Then the second user should now be the new owner
    assert 'jane@example.com' in user_2.emails
    assert 'jane@example.com' not in user_1.emails

def test_primary_email_property_returns_first_verified_email_if_not_set(session):
    """A user's primary email propery returns the first verified email if the
    primary email is not yet set."""
    # Given a user with multiple emails, some verified
    user = create_user(session, emails=['jane1@example.com',
                                        'jane2@example.com',
                                        'jane3@example.com',
                                        'jane4@example.com'])
    user.emails[2].verify()
    user.emails[3].verify()
    session.commit()

    # When accessing the primary_email property
    # Then expect it to be the first verified email
    assert user.primary_email == 'jane3@example.com'

def test_primary_email_property_returns_first_email_if_not_set_and_no_verified(session):
    """A user's primary email propery returns the first email if the primary
    email is not yet set and none of the emails are verified."""
    # Given a user with no verified emails
    user = create_user(session, emails=['jane1@example.com',
                                        'jane2@example.com',
                                        'jane3@example.com',
                                        'jane4@example.com'])

    # When accessing the primary_email property
    # Then expect it to be the first verified email
    assert user.primary_email == 'jane1@example.com'

def test_user_can_set_a_primary_email_from_their_emails(session):
    """A user has set a primary email from their emails. This attribute is also
    accessible via the email dynamic property."""
    # Given a user with verified emails
    user = create_user(session, emails=['jane1@example.com',
                                        'jane2@example.com',
                                        'jane3@example.com'])
    for email in user.emails:
        email.verify()

    # When setting the primary email
    user.primary_email = 'jane1@example.com'
    session.commit()

    # Then the primary email is accessible
    assert user.primary_email == 'jane1@example.com'
    assert user.email == 'jane1@example.com'

    # When setting the primary email via the `email` property to a verified email
    user.email = 'jane2@example.com'
    session.commit()

    # Then the primary email is accessible
    assert user.email == 'jane2@example.com'
    assert user.primary_email == 'jane2@example.com'

def test_users_primary_email_must_be_verified__when_using_orm(session):
    """A users primary email must be verified. The ORM will enforce this."""
    # Given a user with an unverified email
    user = create_user(session, email='jane@example.com')

    # When the user attempts to change the primary_email_fk attribute
    # Then expect an error
    with pytest.raises(IntegrityConstraintViolation):
        user.primary_email_fk = 'jane@example.com'
        user.save()

@requires_mysql
def test_users_primary_email_must_be_verified__when_using_sql(session):
    """A users primary email must be verified. The Database will also enforce
    this."""
    # Given a user with an unverified email saved to the database
    user = create_user(session, email='jane@example.com')
    session.commit()

    # When the user attempts to update the primary_email_fk column
    query = User.__table__.update().where(User.id==user.id).\
                values(primary_email_fk='jane@example.com')

    # Then expect an error
    with pytest.raises(OperationalError):
        session.connection().execute(query)

def test_user_can_update_attributes_other_than_unverified_primary_email__when_using_sql(session):
    """A users can update other attributes besides the email when using SQL. In
    other words, the primary email can remain 'NULL' in an update as long as it
    isn't being changed."""
    # Given a user with an unverified email saved to the database
    user = create_user(session, email='jane@example.com')
    session.commit()

    # When the user attempts to update first_name column
    session.connection().execute(
        User.__table__.update().where(User.id==user.id).\
                values(first_name='Janett')
    )

    # Then expect no errors and the first_name to be changed
    user = user.fresh()
    assert user.first_name == 'Janett'

def test_user_can_update_attributes_other_than_unverified_primary_email__when_using_orm(session):
    """A users can update other attributes besides the email when using ORM. In
    other words, the primary email can remain 'NULL' in an update as long as it
    isn't being changed."""
    # Given a user with an unverified email saved to the database
    user = create_user(session, email='jane@example.com')
    session.commit()

    # When the user attempts to update first_name
    user.first_name = 'Janett'
    user.save()

    # Then expect no errors and the first_name to be changed
    assert user.first_name == 'Janett'

@requires_mysql
def test_users_primary_email_must_exist_in_email_table(session):
    """A user's primary email must exist as one of the emails in the email
    table."""
    # Given a user
    user = create_user(session, email='jane@example.com')

    # When trying to set the primary email to a non-existing email
    # Then an IntegrityError should be thrown
    with pytest.raises(OperationalError):
        user.primary_email = 'new_email@example.com'
        user.save()

@requires_mysql
def test_user_cannot_set_primary_email_to_another_users_email(session):
    """A User cannot set a primary email to another user's email."""
    # Given 2 users and user_1 has an verified email
    user_1 = create_user(session, email='jane@example.com')
    user_1.emails[0].verify()
    user_2 = create_user(session, email='john@example.com')

    # When user_2 tries to set user_1's verified email as a primary email
    # Then an IntegrityError should be thrown
    with pytest.raises(IntegrityError):
        user_2.primary_email = 'jane@example.com'
        user_2.save()

def test_users_primary_email_defaults_to_their_first_verified_email(session):
    """When a user doesn't have a primary_email, their first verified email is
    set to the primary email.

    NOTE: This means that, from the ORM's perspective, a primary_email might be
    unverified."""
    # Given a user with several emails
    user = create_user(session, email=None, emails=['jane1@example.com',
                                                    'jane2@example.com',
                                                    'jane3@example.com'])

    # When a user's primary email is not set
    # Then the first email in the list is the default
    assert user.primary_email == 'jane1@example.com'
    assert user.email == 'jane1@example.com'

    # When committing the database after retrieving the email
    # Then the database does not try to save this unverified email
    session.commit()  # (this would throw a database error)
    assert user.primary_email_fk == None

def test_users_primary_email_returns_first_email_when_no_verified_emails_exist(session):
    """Whan a user doesn't have a verified email, the primary_email property
    will return the first email. However, it will not save this as the primary
    email in the database."""
    # Given a user with several emails
    user = create_user(session, emails=['jane1@example.com',
                                        'jane2@example.com',
                                        'jane3@example.com'])
    session.commit()

    # When a user's primary email is not set
    # Then the first email in the list is the default
    assert user.primary_email == 'jane1@example.com'
    assert user.primary_email_fk == None

@requires_mysql
def test_user_cannot_delete_their_primary_email__using_sql(session):
    """A User cannot delete their primary email."""
    # Given a user with an email set as primary.
    user = create_user(session, emails=['jane1@example.com',
                                        'jane2@example.com',
                                        'jane3@example.com'])
    user.emails[0].verify()
    user.primary_email = 'jane1@example.com'
    user.save()

    # When attempting to delete this email
    # Then expect an IntegrityError
    with pytest.raises(IntegrityError):
        user.emails[0].delete()

@requires_mysql
def test_a_user_cannot_set_their_primary_email_to_null__using_sql(session):
    """A user cannot set their primary email to null."""
    # Given a user with an email set as primary.
    user = create_user(session, emails=['jane1@example.com',
                                        'jane2@example.com',
                                        'jane3@example.com'])
    user.emails[0].verify()
    user.primary_email = 'jane1@example.com'
    user.save()

    # When attempting to delete this email
    # Then expect an OperationalError
    with pytest.raises(OperationalError):
        user.primary_email = None
        user.save()

def test_a_user_can_be_deleted(session):
    """When a user is deleted, the user's emails are also deleted."""
    # Given a user with its corresponding id
    user = create_user(session, email='jane@example.com')

    user.save()
    user_id = user.id

    assert session.query(User).filter_by(id=user_id).count() == 1

    # When the user is deleted
    user.delete()

    # Expect not to find the user.
    assert session.query(User).filter_by(id=user_id).count() == 0

def test_when_a_user_is_deleted_their_emails_are_also_deleted(session):
    """When a user is deleted, the user's emails are also deleted."""
    # Given a user with multiple emails (none set as primary)
    user = create_user(session, emails=['jane1@example.com',
                                        'jane2@example.com',
                                        'jane3@example.com'])

    assert session.query(Email).filter_by(email='jane1@example.com').count() == 1
    assert session.query(Email).filter_by(email='jane2@example.com').count() == 1
    assert session.query(Email).filter_by(email='jane3@example.com').count() == 1

    # When the user is deleted
    user.delete()

    # Expect not to find the emails.
    assert session.query(Email).filter_by(email='jane1@example.com').count() == 0
    assert session.query(Email).filter_by(email='jane2@example.com').count() == 0
    assert session.query(Email).filter_by(email='jane3@example.com').count() == 0

def test_when_an_email_is_deleted_the_user_remains_untouched(session):
    """When a user is deleted, the user's emails are also deleted."""
    # Given a user with multiple email addresses
    user = create_user(session, emails=['jane1@example.com',
                                        'jane2@example.com',
                                        'jane3@example.com'])
    user.save()
    user_id = user.id

    # When one of those emails is deleted
    session.query(Email).filter_by(email='jane1@example.com').delete()
    assert session.query(Email).filter_by(email='jane1@example.com').count() == 0

    # Expect the user to still be there
    assert session.query(User).filter_by(id=user_id).count() == 1

@requires_mysql
def test_a_primary_email_cannot_be_deleted_using__the_sql(session):
    """A primary email cannot be deleted. This is enforced in the SQL."""
    # Given a user with a primary email set
    user = create_user(session, emails=['jane1@example.com',
                                        'jane2@example.com',
                                        'jane3@example.com'])
    user.emails[0].verify()
    user.primary_email = 'jane1@example.com'
    user.save()

    # When attempting to delete this primary email
    # Then expect an IntegrityError
    with pytest.raises(IntegrityError):
        session.query(Email).filter_by(email='jane1@example.com').delete()

def test_a_user_with_a_primary_email_can_be_deleted(session):
    """A user with a primary email can be deleted. This also deletes the
    primary email."""
    # Given a user with a primary email set
    user = create_user(session, emails=['jane1@example.com',
                                        'jane2@example.com',
                                        'jane3@example.com'])
    user.emails[0].verify()
    user.primary_email = 'jane1@example.com'
    user.save()
    user_id = user.id

    # When deletin the user
    user.delete()

    # Then expect both the user and the email to be gone from the database
    assert session.query(Email).filter_by(email='jane1@example.com').count() == 0
    assert session.query(User).filter_by(id=user_id).count() == 0

def test_an_email_is_initially_created_unverified(session):
    """An email is initially created unverified."""
    # Given a user with an email
    user = create_user(session, email='jane1@example.com')

    # When the email has been initially created
    # Then it should not yet be verified
    assert not user.emails[0].verified
    assert not user.emails[0].is_verified

def test_an_email_models_string_is_the_email(session):
    """An email model's string is the email itself."""
    # Given an email
    email = Email(email='example@example.com')

    # Then it's email is its string representation
    assert str(email) == 'example@example.com'

def test_an_email_cannot_be_changed_after_its_created__when_using_orm(session):
    """An email cannot be changed once created. The ORM enforces this. It must
    be deleted and a new email should then be added. Note that in order to be
    saved in the database, the email must be created off a user since it
    requires a user_id.

    NOTE: It may be a good idea to make this transparent to the user from a UX
    standpoint."""
    # Given a user with an email
    user = create_user(session, email='jane@example.com')

    # When the user attempts to change the email
    # Then expect an error
    with pytest.raises(IntegrityConstraintViolation):
        user.emails[0].email = 'john@example.com'
        user.emails[0].save()

@requires_mysql
def test_an_email_cannot_be_changed_after_its_created__when_using_sql(session):
    """An email cannot be changed once created. The database enforces this. It
    must be deleted and a new email should then be added. Note that in order to
    be saved in the database, the email must be created off a user since it
    requires a user_id."""
    # Given a user with an email
    user = create_user(session, email='jane@example.com')
    session.commit()

    # When the user attempts to change the email
    query = Email.__table__.update().where(Email.email=='jane@example.com').\
                values(email='jane_new@example.com')

    # Then expect an error
    with pytest.raises(OperationalError):
        session.connection().execute(query)

def test_user_has_is_confirmed_property_set_to_false_initially(session):
    """An email model's string is the email itself."""
    # Given a user with an email
    user = create_user(session, email='jane@example.com')
    session.commit()

    # When initially checking its is_confirmed property
    # Then it should be false
    assert user.is_confirmed == False

def test_user_is_confirmed_property_set_to_true_after_verifying_email(session):
    """An email model's string is the email itself."""
    # Given a user with an email
    user = create_user(session, email='jane@example.com')

    # When the user verifies its email and sets it as primary
    user.emails[0].verify()
    user.primary_email = user.emails[0]
    user.save()

    # Then it should be confirmed
    assert user.is_confirmed == True

def test_an_email_can_generate_verification_token(app, session):
    """An email can generate a verification token."""
    # Given an email (on a user) and that email's verification token
    user = create_user(session, email='jane@example.com')
    email_verification_token = user.email.verification_token

    # When the token is used to retrieve the email
    email_to_verify = Email.get_email_by_token(email_verification_token)

    # Then it returns the email to verify
    assert email_to_verify == 'jane@example.com'

    # When the token is decoded
    from jwt import decode as jwt_decode
    decoded_token = jwt_decode(email_verification_token,
                               app.config['SECRET_KEY'],
                               algorithms=['HS256'])

    # Then the email and user id should be accessible.
    assert decoded_token['email'] == 'jane@example.com'
    assert decoded_token['user_id'] == user.id

def test_user_can_generate_password_reset_token(app, session):
    """A user can generate a password reset token."""
    # Given a user and the user's password reset token
    user = create_user(session, password='password123', email='jane@example.com')
    password_reset_token = user.password_reset_token

    # When the user is retrieved by password reset token
    verified_user = User.verify_password_reset_token(password_reset_token)

    # Then it returns the user to change the password
    assert verified_user.id == user.id

    # When the token is decoded
    from jwt import decode as jwt_decode
    decoded_token = jwt_decode(password_reset_token,
                               app.config['SECRET_KEY'],
                               algorithms=['HS256'])

    # Then the user's email should be accessible.
    assert decoded_token['password_reset_for_email'] == 'jane@example.com'
