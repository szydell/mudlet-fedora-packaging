Name:           compat-lua-utf8  
Version:        0.1.6
Release:        1%{?dist}  
Summary:        A UTF-8 support module for Lua 5.1  

License:        MIT  
URL:            https://github.com/starwing/luautf8  
Source0:        https://github.com/starwing/luautf8/archive/0.1.5/luautf8-%{version}.tar.gz  

BuildRequires:  compat-lua-devel >= 5.1.5  
BuildRequires:  compat-lua-devel < 5.2  
BuildRequires:  gcc  

Requires:       compat-lua-libs >= 5.1.5  
Requires:       compat-lua-libs < 5.2  

%description  
UTF-8 support module for Lua 5.1  

%prep  
%autosetup -n luautf8-%{version}  

%build  
%{__cc} %{optflags} -fPIC -I/usr/include/lua-5.1 -shared lutf8lib.c -o utf8.so  

%install  
mkdir -p %{buildroot}%{_libdir}/lua/5.1  
install -p -m 755 utf8.so %{buildroot}%{_libdir}/lua/5.1/  

%files  
%license LICENSE  
%{_libdir}/lua/5.1/utf8.so  

%changelog
* Mon Feb 24 2025 Marcin Szydelski <marcin@szydelscy.pl> - 0.1.6-1
- Initial package for Lua 5.1

