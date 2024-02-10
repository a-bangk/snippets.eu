# Use

Test user
username: Adam
password: savage23.3

To reset the password for username Adam

```
>>> u = User(username='New user', email='Their Email.com')

>>> u=db.session.scalar(sa.select(User).where(User.username == "Martin"))
>>> u.set_password("new password)
>>> db.session.add(u)
>>> db.session.commit()
```


# Hosting

nginx
gunicorn

## Production 
branch production is run on coolermaster. 
To update need to run ```systemctl restart snippets-website```

## Server
Snippets runs on Coolermaster under the service-user-snippets account. Passwords and logins are kept in Bitwarden. 

### Environments
Dynaconf sets database by FLASK_ENV, see settings.toml for possible environments

```
export FLASK_ENV=""
```
### Testing

VSCode uses pytest and relies on a local test database


## Infrastructure
Currently running on raspberrypi codename hal.
With python libraries installed on hal and running from virtual environments. See details in tech-guides/hosting-flask.md

## User Access to Snippets



# Versioning

Builds are named as Build-Major.Minor.Fix
Builds numbers are incremented in sync with sprint stories

Build:
* alpha
* beta
* release

Numbering
* Major for changes that break backwards compatibly or major new release
* Minor Changing new features and usability
* Fix, cosmetic and bug fixes
