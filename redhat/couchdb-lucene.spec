# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
%define is_snapshot YES
Summary:        lucene interface for couchdb
Name:           couchdb-lucene
Version:	0.8.0
Release:        1%{?dist}
Epoch:          0
License:        Apache License 2.0
URL:            http://wiki.apache.org/couchdb/Full_text_search
Group:          Java
Source0:	https://github.com/rnewson/couchdb-lucene/tarball/master/couchdb-lucene-0b94022.tar.gz
Source1:	couchdb-lucene.sh
Source2:	couchdb-lucene.init
Source3:	/etc/couchdb/default.d/couchdb-lucene.ini
BuildRequires:	maven
BuildRequires:  java-devel >= 1:1.6.0
Requires:	python
Requires:	java
Requires:	couchdb
Provides:       couchdb-lucene = %{epoch}:%{version}-%{release}
BuildArch:      noarch
%define snapshot 0b94022
%define user lucouch
%description 
Apache Lucene is a high-performance, full-featured text search
engine library written entirely in Java. It is a technology suitable
for nearly any application that requires full-text search, especially
cross-platform. This application creates an interface for couchdb to
utilise this functionality. lucene, and all other required java components
are compiled into this package using the sources provided by maven.

%prep
%setup -q -n rnewson-%{name}-%{snapshot}
# changing version
mv pom.xml pom.old
cat pom.old | sed "s/-SNAPSHOT/.%{release}/g" > pom.xml

%build
mvn compile

%install
mvn assembly:assembly
tar -xzvf target/%{name}-%{version}.%{release}-dist.tar.gz

%define _sharedir /usr/share/%{name}
install -d -m 0755 $RPM_BUILD_ROOT%{_sharedir}
install -d -m 0755 $RPM_BUILD_ROOT%{_sharedir}/jars
install -m 644 %{name}-%{version}.%{release}/lib/*.jar $RPM_BUILD_ROOT%{_sharedir}/jars
install -d -m 0755 $RPM_BUILD_ROOT/var/log/%{name}
ln -sf /var/log/%{name} $RPM_BUILD_ROOT%{_sharedir}/logs 
install -d -m 0755 $RPM_BUILD_ROOT/%{_bindir}
install -m 0755 %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/%{name}
install -d -m 0755 $RPM_BUILD_ROOT/etc/init.d
install -m 0755 %{SOURCE2} $RPM_BUILD_ROOT/etc/init.d/%{name}
install -d -m 0755 $RPM_BUILD_ROOT%{_sharedir}/hook
install -m 0755 couchdb-external-hook.py $RPM_BUILD_ROOT/%{_sharedir}/hook/
install -d -m 0755 $RPM_BUILD_ROOT/etc/couchdb/default.d/
install -m 0644 %{SOURCE3} $RPM_BUILD_ROOT/etc/couchdb/default.d/couchdb-lucene.ini

%pre
#add user
useradd -s /sbin/nologin -r -d /usr/share/couchdb-lucene %{user} || :

%files
#%doc %attr(0444,root,root) /usr/share/man/man1/curl.1.gz
%dir %attr(755,%{user},%{user}) %{_sharedir}
%dir %{_sharedir}/jars
%{_sharedir}/jars/*.jar
%dir %attr(755,%{user},%{user}) /var/log/%{name}
%{_sharedir}/logs
%{_bindir}/%{name}
/etc/init.d/%{name}
%{_sharedir}/hook/couchdb-external-hook.py
%{_sharedir}/hook/couchdb-external-hook.pyc
%{_sharedir}/hook/couchdb-external-hook.pyo
/etc/couchdb/default.d/couchdb-lucene.ini


%changelog
* Sun Oct 23 2011 Nido Media <nido@foxserver.be> 1:0.8.0-%{snapshot}
- Made all-in "static" build with maven

* Fri Oct 21 2011 Nido Media <nido@foxserver.be> 0:0.8.0-%{snapshot}
- Copied to turn into couchdb-lucene specfile

* Mon Sep 12 2011 Alexander Kurtakov <akurtako@redhat.com> 0:2.9.4-7
- Fix duplicate Manifes-version warnings.

* Mon Jun 27 2011 Alexander Kurtakov <akurtako@redhat.com> 0:2.9.4-6
- BR zip - fixes FTBFS.

* Tue May 3 2011 Alexander Kurtakov <akurtako@redhat.com> 0:2.9.4-5
- Update OSGi manifests.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.9.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb  8 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.9.4-3
- Fix empty lucene-analyzers (rhbz#675950)

* Wed Feb  2 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.9.4-2
- Add maven metadata (rhbz#566775)

* Mon Jan 31 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.9.4-1
- Update to latest 2.x version (3.x is not API compatible)
- Add new modules
- Enable tests again
- Versionless jars & javadocs

* Wed Oct 13 2010 Alexander Kurtakov <akurtako@redhat.com> 0:2.4.1-7
- BR java 1.6.0.

* Wed Oct 13 2010 Alexander Kurtakov <akurtako@redhat.com> 0:2.4.1-6
- Fix merge review comments (rhbz#226110).

* Fri Oct 01 2010 CaolÃ¡n McNamara <caolanm@redhat.com> 0:2.4.1-5
- remove empty lines from MANIFEST.MF

* Fri Oct 01 2010 CaolÃ¡n McNamara <caolanm@redhat.com> 0:2.4.1-4
- Resolves: rhbz#615609 custom MANIFEST.MF in lucene drops
  "Specification-Version"

* Mon Jun 7 2010 Alexander Kurtakov <akurtako@redhat.com> 0:2.4.1-3
- Fix build.
- FIx various rpmlint warnings.

* Fri Mar 5 2010 Alexander Kurtakov <akurtako@redhat.com> 0:2.4.1-2
- Drop gcj_support.

* Tue Dec  1 2009 Orion Poplawski <orion@cora.nwra.com> - 0:2.4.1-1
- Update to 2.4.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.3.1-5.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Apr 30 2009 Deepak Bhole <dbhole@redhat.com> - 0:2.3.1-4.5
- rhbz #465344: Fix Implementation-Version and remove Class-Path from manifest

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.3.1-4.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jul 14 2008 Andrew Overholt <overholt@redhat.com> 0:2.3.1-3.4
- Update OSGi manifest data for Eclipse SDK 3.4

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:2.3.1-3.2
- drop repotag

* Thu May 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:2.3.1-3jpp.1
- fix license tag

* Mon May 19 2008 Lubomir Rintel <lkundrak@v3.sk> - 0:2.3.1-3jpp.0
- Correct gcj-compat dependencies, so that this builds on RHEL
- Use --without gcj to disable gcj aot compilation

* Mon May 5 2008 Lubomir Rintel <lkundrak@v3.sk> - 0:2.3.1-2jpp.0
- Unbreak build by repacing the version patch with and -Dversion

* Mon May 5 2008 Lubomir Rintel <lkundrak@v3.sk> - 0:2.3.1-1jpp.0
- 2.3.1, bugfixes only

* Tue Feb 19 2008 Lubomir Kundrak <lkundrak@redhat.com> - 0:2.3.0-1jpp.0
- 2.3.0 (#228141)

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:1.9.1-2jpp.5
- Autorebuild for GCC 4.3

* Fri Sep 21 2007 Deepak Bhole <dbhole@redhat.com> 1.9.1-1jpp.5
- Disable tests due to random hangs (see FIXME comment above ant call)

* Thu Sep 20 2007 Deepak Bhole <dbhole@redhat.com> 0:1.9.1-1jpp.4
- Rebuild for ppc32 execmem issue and new build-id

* Thu Aug 02 2007 Ben Konrath <bkonrath@redhat.com> 0:1.9.1-1jpp.3
- Cleanup packaging of OSGi manifests.

* Tue Jul 31 2007 Ben Konrath <bkonrath@redhat.com> 0:1.9.1-1jpp.2
- Use OSGi manifests from eclipse 3.3.0 instead of merged manifests.
- Resolves: #250221.

* Tue Jul 17 2007 Ben Konrath <bkonrath@redhat.com> 0:1.9.1-1jpp.1
- Disable db sub-package.
- Disable generating test report.
- Add OSGi manifest.
- Obsolete lucene-devel.

* Wed Mar 29 2006 Ralph Apel <r.apel@r-apel.de> 0:1.9.1-1jpp
- Upgrade to 1.9.1

* Tue Apr 26 2005 Ville SkyttÃ¤ <scop at jpackage.org> - 0:1.4.3-2jpp
- Add unversioned javadoc dir symlink.
- Crosslink with local JDK javadocs.
- Convert specfile to UTF-8.
- Fix URLs.

* Mon Jan 10 2005 Kaj J. Niemi <kajtzu@fi.basen.net> 0:1.4.3
- 1.4.3

* Mon Aug 23 2004 Fernando Nasser <fnasser at redhat.com> - 0:1.3-3jpp
- Rebuild with Ant 1.6.2

* Tue Jun 01 2004 Randy Watler <rwatler at finali.com> - 0:1.3-2jpp
- Upgrade to Ant 1.6.X

* Wed Jan 21 2004 David Walluck <david@anti-microsoft.org> 0:1.3-1jpp
- 1.3

* Wed Mar 26 2003 Ville SkyttÃ¤ <scop at jpackage.org> - 0:1.2-2jpp
- Rebuilt for JPackage 1.5.

* Thu Mar  6 2003 Ville SkyttÃ¤ <scop at jpackage.org> - 1.2-1jpp
- First JPackage release.
