Name:       aide
Version:    0.17.4
Release:    1
Summary:    Advanced Intrusion Detection Environment
License:    GPLv2+
URL:        http://sourceforge.net/projects/aide
Source0:    http://github.com/aide/aide/releases/download/v%{version}/%{name}-%{version}.tar.gz
Source1:    aide.conf
Source2:    aide.logrotate

BuildRequires:  gcc make bison flex pcre2-devel libgpg-error-devel libgcrypt-devel zlib-devel libcurl-devel
BuildRequires:  libacl-devel libselinux-devel libattr-devel e2fsprogs-devel audit-libs-devel
# command autoreconf needs autoconf and automake
BuildRequires:  autoconf automake

%ifnarch riscv64
Patch0:    Add-sm3-algorithm-for-aide.patch 
%endif
Patch2:    backport-Handle-malformed-database-lines.patch
Patch4:    backport-Switch-from-PCRE-to-PCRE2-closes-116.patch

%description
AIDE (Advanced Intrusion Detection Environment, [eyd]) is a file and directory integrity checker.
It creates a database from the regular expression rules that it finds from the config file(s).
Once this database is initialized it can be used to verify the integrity of the files.

%package_help

%prep
%autosetup -n %{name}-%{version} -p1

%build
# add command autoreconf to regenerate configure file
# because, the patch Switch-from-PCRE-to-PCRE2 changed configure.ac file
autoreconf -ivf
%configure  --disable-static --with-config_file=%{_sysconfdir}/aide.conf --with-gcrypt --with-zlib \
            --with-curl --with-posix-acl --with-selinux  --with-xattr --with-e2fsattrs --with-audit
make %{?_smp_mflags}

%install
%make_install bindir=%{_sbindir}
install -Dpm0644 -t %{buildroot}%{_sysconfdir} %{S:1}
install -Dpm0644 %{S:2} %{buildroot}%{_sysconfdir}/logrotate.d/aide 
mkdir -p %{buildroot}%{_localstatedir}/log/aide
mkdir -p -m0700 %{buildroot}%{_localstatedir}/lib/aide

%pre

%preun

%post

%postun

%files
%defattr(-,root,root)
%license COPYING AUTHORS
%doc ChangeLog contrib/
%{_sbindir}/*
%config(noreplace) %attr(0600,root,root) %{_sysconfdir}/aide.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/aide
%dir %attr(0700,root,root) %{_localstatedir}/lib/aide
%dir %attr(0700,root,root) %{_localstatedir}/log/aide

%files help
%defattr(-,root,root)
%doc NEWS README
%{_mandir}/*/*

%changelog
* Wed Apr 13 2022 YukariChiba <i@0x7f.cc> - 0.17.4-1
- Upgrade version to 0.17.4
- Temporary disable SM3 patch for RISC-V
- Merged patches: 175d1f2 and 1067d1e from upstream

* Thu Mar 31 2022 yixiangzhike <yixiangzhike007@163.com> - 0.17.3-6
- Type:bugfix
- ID:NA
- SUG:NA
- DESC: switch from PCRE to PCRE2

* Tue Feb 22 2022 yixiangzhike <yixiangzhike007@163.com> - 0.17.3-5
- Type:bugfix
- ID:NA
- SUG:NA
- DESC: handle malformed path and duplicate database entries

* Tue Feb 8 2022 yixiangzhike <yixiangzhike007@163.com> - 0.17.3-4
- Type:CVE
- ID:CVE-2021-45417
- SUG:NA
- DESC: fix CVE-2021-45417

* Fri Dec 31 2021 wangcheng <wangcheng156@huawei.com> - 0.17.3-3
- Type:enhancement
- ID:NA
- SUG:NA
- DESC: add the sm3 crypt support

* Thu Aug 19 2021 yixiangzhike <zhangxingliang3@huawei.com> - 0.17.3-2
- Type:bugfix
- ID:NA
- SUG:NA
- DESC: fix wrong config options in aide.conf

* Sat Jul 31 2021 zoulin <zoulin13@huawei.com> - 0.17.3-1
- Type:enhancement
- ID:NA
- SUG:NA
- DESC: update to 0.17.3;
        delete -Sgit from %autosetup, and delete BuildRequires git

* Wed Jul 29 2020 wangchen <wangchen137@huawei.com> - 0.16.2-1
- Type:enhancement
- ID:NA
- SUG:NA
- DESC: update to 0.16.2

* Tue Mar 17 2020 openEuler Buildteam <buildteam@openeuler.org> - 0.16-16
- Type:bugfix
- ID:NA
- SUG:NA
- DESC: change file from /etc/logrotate.d/aide/aide.logrotate to /etc/logrotate.d/aide

* Fri Jan 10 2020 openEuler Buildteam <buildteam@openeuler.org> - 0.16-15
- Type:enhancement
- ID:NA
- SUG:NA
- DESC: clean code

* Wed Oct 9 2019 openEuler Buildteam <buildteam@openeuler.org> - 0.16-14
- Type:enhancement
- ID:NA
- SUG:NA
- DESC: change the directory of AUTHORS

* Sat Sep 21 2019 openEuler Buildteam <buildteam@openeuler.org> - 0.16-13
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:revise description

* Fri Aug 23 2019 openEuler Buildteam <buildteam@openeuler.org> - 0.16-12
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:strengthen spec

* Tue Aug 20 2019 guoxiaoqi<guoxiaoqi2@huawei.com> - 0.16-11
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:rename patches

* Tue Apr 9 2019 wangxiao<wangxiao65@huawei.com> - 0.16-10
- Type:bugfix
- ID:NA
- SUG:restart
- DESC:Fix short form of --limit parameter
       Fix root_prefix option
       Add missing include in src/db.c
       Fix memory leak in is_prelinked
       Skip reading section data if the section doesn't contain any table.

* Sun Apr 7 2019 zoujing<zoujing13@huawei.com> - 0.16-9
- Type:enhancement
- ID:NA
- SUG:restart
- DESC: backport patch for fixing "DBG: md_enable: algorithm 7 not available"

* Tue Jul 31 2018 openEuler Buildteam <buildteam@openeuler.org> - 0.16-8
- Package init
