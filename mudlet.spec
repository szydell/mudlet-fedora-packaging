Name:           mudlet  
Version:        4.19.0  
Release:        1%{?dist}  
Summary:        Crossplatform mud client  

License:        GPL-2.0-or-later  
URL:            https://www.mudlet.org  
Source0:        https://github.com/Mudlet/Mudlet/archive/refs/tags/Mudlet-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  qt6-qtmultimedia-devel
BuildRequires:  qt6-qttools-devel
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
BuildRequires:  git

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
%autosetup -n Mudlet-Mudlet-%{version}  

# Initialize git repo and submodules with specific versions  
git init  
git remote add origin https://github.com/Mudlet/Mudlet.git  
git fetch --depth 1 origin Mudlet-%{version}  # Używamy prawidłowego formatu tagu  
git checkout FETCH_HEAD  

# Konfiguracja i pobranie submodułów  
git submodule init  
git config submodule.3rdparty/edbee-lib.url https://github.com/Mudlet/edbee-lib.git  
git config submodule.3rdparty/lcf.url https://github.com/Mudlet/lcf.git  
git config submodule.3rdparty/lua-code-formatter.url https://github.com/Mudlet/lua-code-formatter.git  
git config submodule.3rdparty/qtkeychain.url https://github.com/frankosterfeld/qtkeychain.git  

git submodule update --init --recursive --depth 1

%build  
%cmake -DFORCE_USE_QT6=ON  
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
* Tue Feb 04 2025 Package Maintainer <your@email.com> - Mudlet-4.19.0-1
- Update to Mudlet-4.19.0

