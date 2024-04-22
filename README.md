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

* main : Code branch all works starts from and returns to always pushed to origin
* snip-### : A specific feature reflecting the user story, task, bug ,or epic in Jira. If Jira item is an epic, other branches come out of here, to keep main in a runnable state
* build-YYMMDD : Builds that are run on production, always pushed to origin. 

# Hosting Setup

nginx
gunicorn
mariadb

## Production 
Branch production is run on coolermaster as a service. Configuration is in 

```
/etc/systemd/system/snippets-website.service
```

Environment variables in snippets/env and snippets/.secrets.toml both outside of version control.

Private key password in Bitwarden under "Private Key service-user-snippets"

To update production
```
sudo su service-user-snippets
cd ~/websites/snippets
git branch
git fetch origin/build-YYMMDD 
git checkout build-YYMMDD
```

It case it doesn't work go back to working build

```
git checkout build-YYMMDD
```

To update need to be a sudo user and run:
```sudo systemctl restart snippets-website```

## Flask Server
Snippets runs on Coolermaster under the service-user-snippets account. Passwords and logins are kept in Bitwarden. 

To follow logs

```
sudo journalctl -u snippets-website.service -f
```

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

Based on date of build. 

## Releases

2024-04-22: build-240422
2024-04-05: alpha-0.6