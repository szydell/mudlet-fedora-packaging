Name:           mudlet  
Version:        4.19.1
Release:        5%{?dist}
Summary:        Crossplatform mud client  

License:        GPL-2.0-or-later  
URL:            https://www.mudlet.org  
Patch0:         https://github.com/szydell/mudlet-fedora-packaging/raw/refs/heads/main/regparse.patch



BuildRequires:  cmake
BuildRequires:  gcc  
BuildRequires:  gcc-c++  
BuildRequires:  libasan
# Qt6 requirements  
BuildRequires:  qt6-qtbase-devel  
BuildRequires:  qt6-qtdeclarative-devel  
BuildRequires:  qt6-qtmultimedia-devel  
BuildRequires:  qt6-qttools-devel  
BuildRequires:  qt6-qt5compat-devel  
BuildRequires:  qt6-qtwebsockets-devel  
BuildRequires:  qt6-qtsvg-devel  
BuildRequires:  qt6-qtnetworkauth-devel  
# Lua requirements  
BuildRequires:  compat-lua  
BuildRequires:  compat-lua-devel  
BuildRequires:  luarocks  
BuildRequires:  sqlite-devel  
BuildRequires:  zziplib-devel  
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
Requires:       hunspell  
Requires:       yajl  
Requires:       lua  
Requires:       pcre  
Requires:       pugixml  
Requires:       libzip  
Requires:       openssl  
Requires:       compat-lua  
Requires:       sqlite-libs  
Requires:       zziplib  
Requires:       mesa-libGL  
Requires:       mesa-libGLU  

%description  
Mudlet is a quality MUD client, designed to take mudding to a new level.

It's a new breed of a client on the MUD scene – with an intuitive user interface,
a specially designed scripting framework, and a very fast text display.
Add to that cross-platform capability, an open-source development model,
and you'll get a very likable MUD client.

%prep  
  
# repo fetch
git init  
git remote add origin https://github.com/Mudlet/Mudlet.git  
git fetch --depth 1 origin Mudlet-%{version}  
git checkout FETCH_HEAD

# get submodules
git submodule update --init --recursive --depth 1  

# Patch
%patch 0 -p1

# Create git info file for build system  
#echo "#define APP_BUILD \"$(cd ../mudlet-git && git rev-parse HEAD)\"" > src/app-git-sha.h  

alias lua='/usr/bin/lua-5.1'  

lua -v

# Configure luarocks to use Lua 5.1  
luarocks config --local lua_interpreter lua5.1  
luarocks config --local lua_version 5.1
# Add debug symbols
export CFLAGS="%{optflags} -g"  
export CXXFLAGS="%{optflags} -g"  
export LDFLAGS="%{optflags}"  
# Install required Lua packages  
luarocks --lua-version 5.1 --tree=%{_builddir}/.luarocks install luazip ZZIP_DIR=/usr || echo "Failed to install luazip"
luarocks --lua-version 5.1 --tree=%{_builddir}/.luarocks install luasql-sqlite3 || echo "Failed to install luasql-sqlite3"
luarocks --lua-version 5.1 --tree=%{_builddir}/.luarocks install lcf || echo "Failed to install lcf"
luarocks --lua-version 5.1 --tree=%{_builddir}/.luarocks install luautf8 || echo "Failed to install luautf8"
luarocks --lua-version 5.1 --tree=%{_builddir}/.luarocks install lua-yajl || echo "Failed to install lua-yajl"
luarocks --lua-version 5.1 --tree=%{_builddir}/.luarocks install lrexlib-pcre || echo "Failed to install lrexlib-pcre"
luarocks --lua-version 5.1 --tree=%{_builddir}/.luarocks install luafilesystem || echo "Failed to install luafilesystem"

export LUA_PATH="%{_builddir}/.luarocks/share/lua/5.1/?.lua;%{_builddir}/.luarocks/share/lua/5.1/?/init.lua;;"  
export LUA_CPATH="%{_builddir}/.luarocks/lib64/lua/5.1/?.so;;"

# Ensure the lib64 directory for lua exists  
mkdir -p %{_builddir}/usr/lib64/lua

# Symlink the lua/5.1 directory into /usr/lib64/lua
if [ -d %{_builddir}/.luarocks/lib64/lua/5.1 ]; then
  ln -s %{_builddir}/.luarocks/lib64/lua/5.1 %{_builddir}/usr/lib64/lua/5.1
else
  echo "Directory %{_builddir}/.luarocks/lib64/lua/5.1 does not exist"
fi

# Verify Lua module loading  
echo "Testing Lua module loading:"  
lua -e "local yajl = require('yajl'); print('YAJL module loaded successfully')"  

find .

%build  
export LUA_CPATH="%{_builddir}/.luarocks/lib64/lua/5.1/?.so;;"  
export LUA_EXECUTABLE=/usr/bin/lua-5.1  
export LUA_INCLUDE_DIR=/usr/include/lua5.1  

%cmake \
    -DCMAKE_BUILD_TYPE=Release \
    -DWITH_FONTS=ON \
    -DUSE_UPDATER="" \
    -DWITH_OWN_QTKEYCHAIN=ON \
    -DFORCE_USE_QT6=ON \
    -DWITH_3DMAPPER=ON \
    -DUSE_BUILTIN_LUA=ON \
    -DOpenGL_GL_PREFERENCE=GLVND \
    -DUSE_SANITIZER=""

%cmake_build


%install  
%cmake_install  

mkdir -p %{buildroot}/usr/lib64/lua/5.1  

if [ -d %{_builddir}/.luarocks/lib64/lua/5.1 ]; then  
    cp -r %{_builddir}/.luarocks/lib64/lua/5.1/* %{buildroot}/usr/lib64/lua/5.1/  
else  
    echo "Directory %{_builddir}/.luarocks/lib64/lua/5.1 does not exist"  
    exit 1  
fi  

find %{buildroot}/usr/lib64/lua/5.1 -name "*.so" -exec chrpath --delete {} \; || :

mkdir -p %{buildroot}/%{_datadir}/lua/5.1  

if [ -d %{_builddir}/.luarocks/share/lua/5.1 ]; then
    cp -r %{_builddir}/.luarocks/share/lua/5.1/* %{buildroot}/%{_datadir}/lua/5.1/
else
    echo "No Lua scripts found in %{_builddir}/.luarocks/share/lua/5.1"
fi

rm -f %{buildroot}/usr/lib64/libqt6keychain.so*  
rm -f %{buildroot}/usr/lib/debug/usr/lib64/libqt6keychain.so*

find %{buildroot}

%check  
desktop-file-validate %{buildroot}/%{_datadir}/applications/mudlet.desktop  

%files  
%license COPYING  
%doc README.md  
%{_bindir}/mudlet  
%{_datadir}/applications/mudlet.desktop  
%{_datadir}/icons/hicolor/*/apps/mudlet.png  
%{_datadir}/icons/hicolor/scalable/apps/mudlet.svg  
%{_libdir}/lua/5.1/*  
%{_datadir}/lua/5.1/*  
%{_datadir}/mudlet/lua/*  
%{_datadir}/mudlet/tests/*  
%{_includedir}/QsLog/*  
%{_includedir}/qt6keychain/*
%{_libdir}/cmake/Qt6Keychain/*  
%{_libdir}/qt6/mkspecs/modules/qt_Qt6Keychain.pri  
%{_datadir}/qt6keychain/translations/*  
/usr/lib/libQsLog.so

#package debug  
#Summary: Debug information for mudlet  
#Group: Development/Debug  

#description debug  
#This package contains debug information for Mudlet.  
#files debug  
#*.debug


%changelog  
* Wed Feb 05 2025 Package Maintainer <your@email.com> - 4.19.1-5
- Update to version 4.19.0  
- Switched to Qt6  
- Improved Lua module handling  
- Fixed OpenGL configuration

