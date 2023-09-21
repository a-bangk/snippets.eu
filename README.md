# Hosting

## Infrastruture
Currently running on raspberrypi codename hal.
With python libraries installed on hal and running from virtual environments. See details in tech-guides/hosting-flask.md

## Access to Snippets
### Public
Public facing running snippets
#### Test (snippets-a)
* snippets-a.akjems.com (Running latest build on main)
    * ~/websites/snippets-a/snippets/

#### Production (snippets-l)
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

Source

https://www.digitalocean.com/community/tutorials/how-to-use-python-markdown-with-flask-and-sqlite?utm_source=pocket_saves

relevant libraries
* flask
* markdown

SQL schema goes in 'schema.sql'
DB is created and started with 'init_db.py'

