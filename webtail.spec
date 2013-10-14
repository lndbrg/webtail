Name:           webtail
Version:        0.3.1
Release:        1%{?dist}
Summary:        Tail your filesystem from the web

Group:          Applications/Text
License:        MIT
URL:            https://bitbucket.org/olle/webtail 
Source0:        https://bitbucket.org/olle/webtail/get/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python-devel
Requires:       python-gevent
Requires:       python-flask

%description
Tail your filesystem from the web.

%prep
%setup -q

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE
%{_bindir}/%{name}

%changelog
* Mon Oct 14 2013 Olle Lundberg <geek@nerd.sh> - 0.3.0
- First release.
