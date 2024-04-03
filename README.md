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

End of sprint aim is to update live branch

## Branches

* Live: the live version running. Tested and works
* Main : Code branch all works starts from and returns to
* snip-### : A specific feature reflecting the user story, task, bug ,or epic in Jira. If Jira item is an epic, other branches come out of here, to keep main in a runnable.

# Hosting

nginx
gunicorn
mariadb

## Production 
Branch live is run on coolermaster as a service. Configuration is in /etc/systemd/system/snippets-website.service
Environment variables in snippets/env and snippets/.secrets.toml both outside of version control.

Private key password in Bitwarden under "Private Key service-user-snippets"

To update live
```
sudo su service-user-snippets
cd ~/websites/snippets
git fetch origin main:main
git merge main
```

It case it doesn't work

```
git reset --hard origin/live
```

To update need to run ```systemctl restart snippets-website```

## Flask Server
Snippets runs on Coolermaster under the service-user-snippets account. Passwords and logins are kept in Bitwarden. 

## Database Server

raspberrypi
password saved as "raspberry pi mariadb root user" in Bitwarden


```
mysql -u root -p
```

### Testing

VSCode uses pytest and relies on a local test database


## Infrastructure
Currently running on coolermaster codename hal2.
With python libraries installed on hal2 and running from virtual environments. See details in tech-guides/hosting-flask.md

# Versioning

Builds are named as Major.Minor.Fix

Versions running on server:
* alpha - main branch running alpha/snippets. Pulled from live after a release
* beta - release candidates beta/snippets. Get own named branches on github
* live - running on main URL websites/snippets. Merged from beta branch on github

Numbering
* Major for changes that break backwards compatibly or major new release
* Minor Changing new features and usability
* Fix, cosmetic and bug fixes
