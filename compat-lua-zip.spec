Name:           compat-lua-zip  
Version:        1.2.7  
Release:        1%{?dist}  
Summary:        A ZIP support module for Lua 5.1  

License:        MIT  
URL:            https://github.com/mpeterv/luazip  
Source0:        https://github.com/mpeterv/luazip/archive/refs/tags/%{version}.tar.gz  

%global debug_package %{nil}  

BuildRequires:  compat-lua-devel >= 5.1.5  
BuildRequires:  compat-lua-devel < 5.2  
BuildRequires:  gcc  
BuildRequires:  make  
BuildRequires:  zziplib-devel

Requires:       compat-lua-libs >= 5.1.5  
Requires:       compat-lua-libs < 5.2  

%description  
ZIP support module for Lua 5.1.  

%prep  
%autosetup -n luazip-%{version}  

%build  
gcc -fPIC -I/usr/include/lua-5.1 -c -o src/luazip.o src/luazip.c  
gcc -shared -o src/zip.so src/luazip.o -lzzip  

%install  
mkdir -p %{buildroot}%{_libdir}/lua/5.1
install -p -m 755 src/zip.so %{buildroot}%{_libdir}/lua/5.1/

%files
%license LICENSE
%{_libdir}/lua/5.1/zip.so  


%changelog  
* Mon Feb 24 2025 Marcin Szydelski <marcin@szydelscy.pl> - 1.2.7-1  
- Initial package for Lua 5.1

