#!/bin/bash

source debian/vars.sh

set -x

export php_version=`echo "$scl" | perl -pe '$_ =~ s/^ea-php(\d)(\d)$/$1.$2/'`

# The module itself
install -d -m 755 $DEB_INSTALL_ROOT$php_extdir
install -m 755 ixed.$php_version.lin $DEB_INSTALL_ROOT$php_extdir
# The ini snippet
install -d -m 755 $DEB_INSTALL_ROOT$php_inidir

file=$DEB_INSTALL_ROOT$php_inidir/sourceguardian.ini

cat > $file <<EOF
; Enable SourceGuardian Loader extension module
extension=ixed.$php_version.lin
EOF

cat -n $file

mkdir -p $DEB_INSTALL_ROOT/opt/cpanel/$scl/root/usr/share/doc/$name
cp README $DEB_INSTALL_ROOT/opt/cpanel/$scl/root/usr/share/doc/$name
cp SourceGuardian_Loader_License.pdf $DEB_INSTALL_ROOT/opt/cpanel/$scl/root/usr/share/doc/$name

echo "FILELIST"

echo `pwd`
find . -type f -print | sort

echo "DONE"

