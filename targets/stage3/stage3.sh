# Copyright 1999-2003 Gentoo Technologies, Inc.
# Distributed under the terms of the GNU General Public License v2
# $Header: /var/cvsroot/gentoo/src/catalyst/targets/stage3/Attic/stage3.sh,v 1.3 2003/10/29 06:52:15 drobbins Exp $

case $1 in
enter)
	$clst_CHROOT $clst_chroot_path
	;;
run)
	$clst_CHROOT $clst_chroot_path /bin/bash << EOF
	env-update
	source /etc/profile
	if [ -n "${clst_CCACHE}" ]
	then
		export FEATURES="ccache"
		emerge --oneshot --nodeps --usepkg --buildpkg ccache || exit 1
	fi
	if [ ${clst_rel_type} = "hardened" ]
	then
		emerge --oneshot --nodeps hardened-gcc || exit 1
	fi
	export CONFIG_PROTECT="-*"
	
	#portage needs to be merged manually with USE="build" set to avoid frying our
	#make.conf. emerge system could merge it otherwise.
	USE="build" emerge portage
	
	if [ -n "${clst_PKGCACHE}" ]
	then
		emerge system --usepkg --buildpkg || exit 1
	else
		emerge system || exit 1
	fi
EOF
	[ $? -ne 0 ] && exit 1
	;;
clean)
	$clst_CHROOT $clst_chroot_path /bin/bash << EOF
	env-update
	source /etc/profile
	if [ -n "${clst_CCACHE}" ]
	then
		emerge -C ccache || exit 1
	fi
EOF
	[ $? -ne 0 ] && exit 1
	;;
*)
	exit 1
	;;
esac
