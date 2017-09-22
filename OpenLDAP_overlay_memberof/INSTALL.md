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

### 1. Dynamic Configuration

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
```

### 2. Configuration using slapd.conf

```bash
# /etc/openldap/slapd.conf
...
overlay memberof
memberof-refint TRUE

overlay refint
refint_attributes memberof member manager owner
```