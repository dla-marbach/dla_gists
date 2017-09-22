## SLES: OpenLDAP memberOf-Overlay

The memberOf- and refint-overlay are statically linked in SLES OpenLDAP. This can be verified with

```bash
/usr/lib/openldap/slapd -VVV

# Included static overlays:
# ...
#    memberof
#    ppolicy
#    pcache
#    refint
# ...
``` 

### 1. Configuration

At DLA we currently use the configuration via `slapd.conf`.

#### 1.1 Dynamic

```bash
# Clone this repo
cd ~
git clone https://github.com/dla-marbach/dla_gists
cd dla_gists/OpenLDAP_overlay_memberof

# Add memberof overlay
sudo ldapadd -Q -Y EXTERNAL -H ldapi:/// -f memberof_add.ldif

# Configure memberof overlay
sudo ldapadd -Q -Y EXTERNAL -H ldapi:/// -f memberof_config.ldif

# Setup reference integrity
sudo ldapmodify -Q -Y EXTERNAL -H ldapi:/// -f refint1.ldif
sudo ldapadd -Q -Y EXTERNAL -H ldapi:/// -f refint2.ldif

# Restart OpenLDAP
/etc/init.d/ldap restart
```

#### 1.2 slapd.conf

```bash
# /etc/openldap/slapd.conf
...
overlay refint
refint_attributes memberof member manager owner

overlay memberof
memberof-refint TRUE
...

# Always test your config
slaptest -f /etc/openldap/slapd.conf

# Restart OpenLDAP
/etc/init.d/ldap restart
```

### 2. Update group membership

The virtual memberOf attribute is not applied retroactively. We need to remove all users from groups and readd them. The `posixGroup`-attribute does not work with the memberOf-overlay so we cannot use `ou=group,dc=dla-marbach,dc=de` but have to revert to `ou=group4beehive,dc=dla-marbach,dc=de`.

Execute the python script supplied:

```bash
# Install python-ldap
zypper in python-ldap
cd ~
git clone https://github.com/dla-marbach/dla_gists
cd dla_gists/OpenLDAP_overlay_memberof
# refer to 'python memberof_update.py --help' if needed
python memberof_update.py -p <password>
```