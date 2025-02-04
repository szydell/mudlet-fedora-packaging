Name:           mudlet  
Version:        4.19.1  
Release:        1%{?dist}  
Summary:        Crossplatform mud client  

License:        GPL-2.0-or-later  
URL:            https://www.mudlet.org  
Source0:        https://github.com/Mudlet/Mudlet/archive/Mudlet-%{version}.tar.gz  

BuildRequires:  cmake  
BuildRequires:  gcc-c++  
BuildRequires:  qt5-qtbase-devel  
BuildRequires:  qt5-qttools-devel  
BuildRequires:  qt5-qtmultimedia-devel  
BuildRequires:  qt5-qtdeclarative-devel  
BuildRequires:  hunspell-devel  
BuildRequires:  yajl-devel  
BuildRequires:  lua-devel  
BuildRequires:  pcre-devel  
BuildRequires:  zlib-devel  
BuildRequires:  pugixml-devel  
BuildRequires:  boost-devel  
BuildRequires:  libzip-devel  
BuildRequires:  openssl-devel  
BuildRequires:  desktop-file-utils  

Requires:       qt5-qtbase  
Requires:       qt5-qtmultimedia  
Requires:       hunspell  
Requires:       yajl  
Requires:       lua  
Requires:       pcre  
Requires:       pugixml  
Requires:       libzip  
Requires:       openssl  

%description  
Mudlet is a quality MUD client, designed to take mudding to a new level.  

It's a new breed of a client on the MUD scene – with an intuitive user interface,   
a specially designed scripting framework, and a very fast text display.   
Add to that cross-platform capability, an open-source development model,   
and you'll get a very likable MUD client.  

%prep  
%autosetup -n Mudlet-%{version}  

%build  
%cmake  
%cmake_build  

%install  
%cmake_install  

%check  
desktop-file-validate %{buildroot}/%{_datadir}/applications/mudlet.desktop  

%files  
%license COPYING  
%doc README.md  
%{_bindir}/mudlet  
%{_datadir}/applications/mudlet.desktop  
%{_datadir}/icons/hicolor/*/apps/mudlet.png  
%{_datadir}/metainfo/mudlet.appdata.xml  

%changelog  
* Tue Feb 04 2025 Package Maintainer <marcin@szydelscy.pl> - 4.19.1-1  
- Initial package

