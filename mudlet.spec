Name:           mudlet  
Version:        4.19.1
Release:        9%{?dist}
Summary:        Crossplatform mud client  

License:        GPL-2.0-or-later  
URL:            https://www.mudlet.org  
Patch0:         https://github.com/szydell/mudlet-fedora-packaging/raw/refs/heads/main/regparse.patch



BuildRequires:  cmake
BuildRequires:  gcc  
BuildRequires:  gcc-c++  
BuildRequires:  libasan
BuildRequires:  qt6-rpm-macros
# Qt6 requirements  
BuildRequires:  qt6-qtbase-devel  
BuildRequires:  qt6-qtdeclarative-devel  
BuildRequires:  qt6-qtmultimedia-devel  
BuildRequires:  qt6-qttools-devel
BuildRequires:  qt6-qttools
BuildRequires:  qt6-qttools-static
BuildRequires:  qt6-qt5compat-devel  
BuildRequires:  qt6-qtwebsockets-devel  
BuildRequires:  qt6-qtsvg-devel  
BuildRequires:  qt6-qtnetworkauth-devel
BuildRequires:  qtkeychain-qt6-devel
# Lua requirements  
BuildRequires:  compat-lua
BuildRequires:  compat-lua-devel
BuildRequires:  compat-lua-libs
BuildRequires:  luarocks  
BuildRequires:  sqlite-devel  
BuildRequires:  zziplib-devel
BuildRequires:  lua5.1-filesystem
# Other dependencies  
BuildRequires:  hunspell-devel  
BuildRequires:  yajl-devel  
BuildRequires:  pcre-devel  
BuildRequires:  zlib-devel  
BuildRequires:  pugixml-devel  
BuildRequires:  boost-devel  
BuildRequires:  libzip-devel  
BuildRequires:  openssl-devel  
BuildRequires:  desktop-file-utils  
BuildRequires:  git
BuildRequires:  libsecret-devel  
BuildRequires:  mesa-libGL-devel  
BuildRequires:  mesa-libGLU-devel
BuildRequires:  libxkbcommon-devel
BuildRequires:  chrpath

# Runtime requirements  
Requires:       qt6-qtbase
Requires:       qt6-qtmultimedia
Requires:       qtkeychain-qt6
Requires:       qt6-qttools
Requires:       qt6-qttools-static
Requires:       hunspell
Requires:       yajl
Requires:       pcre
Requires:       pugixml
Requires:       libzip
Requires:       openssl
Requires:       compat-lua
Requires:       compat-lua-libs
Requires:       sqlite-libs
Requires:       zziplib
Requires:       mesa-libGL
Requires:       mesa-libGLU
Requires:       lua5.1-filesystem 
Requires:       bitstream-vera-fonts-all

%description  
Mudlet is a quality MUD client, designed to take mudding to a new level.

It's a new breed of a client on the MUD scene – with an intuitive user interface,
a specially designed scripting framework, and a very fast text display.
Add to that cross-platform capability, an open-source development model,
and you'll get a very likable MUD client.

%global luarocks_tree %{_builddir}/luarocks  

%prep  

#lua5.1 rocks packages
mkdir -p %{luarocks_tree}
export LUA_PATH="%{luarocks_tree}/share/lua/5.1/?.lua;;"
export LUA_CPATH="%{luarocks_tree}/lib/lua/5.1/?.so;;"
luarocks --lua-version 5.1 --tree=%{luarocks_tree} install luazip --no-rpath
luarocks --lua-version 5.1 --tree=%{luarocks_tree} install luasql-sqlite3 --no-rpath
luarocks --lua-version 5.1 --tree=%{luarocks_tree} install lcf --no-rpath
luarocks --lua-version 5.1 --tree=%{luarocks_tree} install luautf8 --no-rpath
luarocks --lua-version 5.1 --tree=%{luarocks_tree} install lua-yajl --no-rpath
luarocks --lua-version 5.1 --tree=%{luarocks_tree} install lrexlib-pcre --no-rpath

# source code
git clone --recursive --branch=Mudlet-%{version} https://github.com/Mudlet/Mudlet.git

cd Mudlet
mkdir build

#fix mudlet.pro for Fedora
sed -i '/linux {/,/}/ {  
    s/-llua5\.1/-llua-5.1/  
    s/-lhunspell/-lhunspell-1.7/  
    s|/usr/include/lua5\.1|/usr/include/lua-5.1|  
}' src/mudlet.pro


%build
#lua5.1 rocks packages
export LUA_PATH="%{luarocks_tree}/share/lua/5.1/?.lua;;"
export LUA_CPATH="%{luarocks_tree}/lib/lua/5.1/?.so;;"

cd Mudlet/build
WITH_FONTS=NO WITH_OWN_QTKEYCHAIN=NO WITH_UPDATER=NO WITH_VARIABLE_SPLASH_SCREEN=NO XDG_DATA_DIRS=/usr/share %qmake_qt6 PREFIX=%{_qt6_prefix} INCLUDEPATH+=/usr/include/lua-5.1 LUA_SEARCH_OUT=lua-5.1 ../src/mudlet.pro
make %{?_smp_mflags}  


%install
cd Mudlet/build
%make_install INSTALL_ROOT=%{buildroot}

#install lua5.1 rocks packages
if [ -d %{luarocks_tree}/share/lua/5.1 ]; then
  mkdir -p %{buildroot}%{_datadir}/lua/5.1
  cp -r %{luarocks_tree}/share/lua/5.1/* %{buildroot}%{_datadir}/lua/5.1/
fi

if [ -d %{luarocks_tree}/lib64/lua/5.1 ]; then
  mkdir -p %{buildroot}%{_libdir}/lua/5.1  
  cp -r %{luarocks_tree}/lib64/lua/5.1/* %{buildroot}%{_libdir}/lua/5.1/
fi

# Usuń RPATH z bibliotek Lua  
if [ -d %{buildroot}%{_libdir}/lua/5.1 ]; then  
  for lib in %{buildroot}%{_libdir}/lua/5.1/*.so; do  
    chrpath --delete "$lib" || :  
  done  
fi

# Install the icon file  
install -Dm644 ../mudlet.png %{buildroot}%{_datadir}/pixmaps/mudlet.png  
# Install the desktop entry file  
install -Dm644 ../mudlet.desktop %{buildroot}%{_datadir}/applications/mudlet.desktop  


%check  
desktop-file-validate %{buildroot}/%{_datadir}/applications/mudlet.desktop  



%files  
%{_bindir}/mudlet  

%dir %{_datadir}/mudlet  
%{_datadir}/mudlet/*  

%dir %{_datadir}/lua  
%{_datadir}/lua/*  

%dir %{_datadir}/pixmaps  
%{_datadir}/pixmaps/*  

%dir %{_datadir}/applications  
%{_datadir}/applications/*  


%changelog  
* Sat Feb 15 2025 Package Maintainer <your@email.com> - 4.19.1-9
- Update to version 4.19.0  
- Switched to Qt6  
- Improved Lua module handling  
- Fixed OpenGL configuration

