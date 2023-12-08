# Hosting

## Development

Environment is set the environmental variable ENV_FOR_DYNACONF, see settings.toml for possible environments

## Infrastructure
Currently running on raspberrypi codename hal.
With python libraries installed on hal and running from virtual environments. See details in tech-guides/hosting-flask.md

## User Access to Snippets
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
