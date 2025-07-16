# Snippets: Sourced, Taggable, and Shareable Information

## About

Snippets is a knowledge aggregator where information is always linked to its source, can be tagged to organized, searched and shareable with others.

Development has four progression paths:

1. Refactor and clean up the current Flask and Jinja2 version.
2. Automate deployment and hosting on local and remote servers.
3. Refactor to use an API backend apps or web frontend.
4. Implement new features and use cases.

## Running Locally

Requires a database to run. Currently uses snippets_test_a run locally. 

After setting up the test database and installing python packages needed in the virtual environment. Adjust the settings.toml and run the following commands

```
export ENV_FOR_DYNACONF=test
flask --app snippets run --debug
```


## User Management from Flask Shell

```python
>>> u = User(username='New user', email='Their Email.com')
>>> u = db.session.scalar(sa.select(User).where(User.username == "Martin"))
>>> u.set_password("new password")
>>> db.session.add(u)
>>> db.session.commit()
```

## Branches

- **main**: The main branch where all work starts from and returns to, always pushed to origin.
- **snip-###**: A specific feature branch reflecting the user story, task, bug, or epic in Jira. If the Jira item is an epic, other branches are created from here to keep the main branch in a runnable state.

## Hosting Setup

- nginx
- gunicorn
- mariadb
- flask

### Production

The production branch is run on my local server as a service. Configuration is in:

```
/etc/systemd/system/snippets-website.service
```

Environment variables are in `snippets/env` and `snippets/.secrets.toml`, both outside of version control. The private key password is in password manager under "Private Key service-user-snippets".

To update production:

```bash
sudo su service-user-snippets
cd ~/websites/snippets
git branch
git fetch origin/build-YYMMDD 
git checkout build-YYMMDD
```

If it doesn't work, revert to the previous build:

```bash
git checkout build-previousYYMMDD
```

To update, you need to be a sudo user and run:

```bash
sudo systemctl restart snippets-website
```

### Flask Server

Snippets runs on a local server under the service-user-snippets account. Passwords and logins are kept in password manager. 

To follow logs:

```bash
sudo journalctl -u snippets-website.service -f
```

### Database Server

Runs on a Raspberry Pi. The password is saved as "raspberry pi mariadb root user" in password mananer.

```bash
mysql -u root -p
```

### Testing

VSCode uses pytest and relies on a local test database.

## Infrastructure

Currently running on a hal, with Python libraries installed on hal and running from virtual environments. See details in `tech-guides/hosting-flask.md`.

## Versioning

Versioning is based on the date of the build.

## Releases

- **2024-04-22**: build-240422
- **2024-04-05**: alpha-0.6

