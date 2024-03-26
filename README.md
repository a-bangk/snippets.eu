# Use

Test user
username: susan
email/login : susan@example.com
password: see Bitwarden

To reset the password for username Adam

```
>>> u = User(username='New user', email='Their Email.com')

>>> u=db.session.scalar(sa.select(User).where(User.username == "Martin"))
>>> u.set_password("new password)
>>> db.session.add(u)
>>> db.session.commit()
```

# Source Control

Epics get own branch

End of sprint aim is to update live branch

## Branches

* Live: the live version running. Tested and works
* Main : Code branch all works starts from and returns to
* snip-### : A specific feature reflecting the user story, task, bug ,or epic in Jira. If Jira item is an epic, other branches come out of here, to keep main in a runnable.

# Hosting

nginx
gunicorn

## Production 
branch live is run on coolermaster. 
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
Currently running on coolermaster codename hal2.
With python libraries installed on hal2 and running from virtual environments. See details in tech-guides/hosting-flask.md

# Versioning <not being used>

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
