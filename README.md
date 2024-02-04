# Use

Test user
username: Adam
password: savage23.3

To reset the password for username Adam

```
>>> u=db.session.scalar(sa.select(User).where(User.username == "Adam"))
>>> u.set_password("new password)
>>> db.session.add(u)
>>> db.session.commit()
```

## Development
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
### Public
Public facing running snippets
#### Test (snippets-a) 2024-01-10 Down
* snippets-a.akjems.com (Running latest build on main)
    * ~/websites/snippets-a/snippets/

#### Production (snippets-l) -> move to mysnippets.eu
* snippets.akjems.com (live branch) Significant versions are tagged, merged from main
    * ~/websites/snippets-l/snippets

### Private (snippets-p)
Access to my private database is labeled *snippets-p* only accessible from the home network.
It is run on the rasberrypi
* 192.168.0.42:5042
    * ~/websites/snippets-p/snippets

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
