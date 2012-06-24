
%define		toolkit_date	20060615
%define		elf2flt_date	20060608

Summary:	Cross GNU binary utility development utilities - binutils
Summary(es.UTF-8):	Utilitarios para desarrollo de binarios de la GNU - m68k binutils
Summary(fr.UTF-8):	Utilitaires de développement binaire de GNU - m68k binutils
Summary(pl.UTF-8):	Skrośne narzędzia programistyczne GNU dla m68k - binutils
Summary(pt_BR.UTF-8):	Utilitários para desenvolvimento de binários da GNU - m68k binutils
Summary(tr.UTF-8):	GNU geliţtirme araçlarý - m68k binutils
Name:		crossm68k-binutils
Version:	2.17.50.0.14
Release:	1
License:	GPL
Group:		Development/Tools
Source0:	http://www.kernel.org/pub/linux/devel/binutils/binutils-%{version}.tar.bz2
# Source0-md5:	4ddab973ad9c5169d8f8296bdf67b3f7
Source1:	http://www.uclinux.org/pub/uClinux/m68k-elf-tools/tools-%{toolkit_date}/elf2flt-%{elf2flt_date}.tar.gz
# Source1-md5:	ebfb126a684b43a6cdeb17db2bae09da
URL:		http://sources.redhat.com/binutils/
BuildRequires:	automake
BuildRequires:	bash
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	sed
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		target		m68k-elf
%define		arch		%{_prefix}/%{target}

%description
Binutils is a collection of binary utilities, including:
- ar - create, modify and extract from archives,
- nm - lists symbols from object files,
- objcopy - copy and translate object files,
- objdump - display information from object files,
- ranlib - generate an index for the contents of an archive,
- size - list the section sizes of an object or archive file,
- strings - list printable strings from files,
- strip - discard symbols,
- c++filt - a filter for demangling encoded C++ symbols,
- addr2line - convert addresses to file and line,
- nlmconv - convert object code into an NLM.

This package contains the cross version for m68k.

%description -l pl.UTF-8
Pakiet binutils zawiera zestaw narzędzi umożliwiających kompilację
programów. Znajdują się tutaj między innymi assembler, konsolidator
(linker), a także inne narzędzia do manipulowania binarnymi plikami
programów i bibliotek.

Ten pakiet zawiera wersję skrośną generującą kod dla m68k.

%prep
%setup -q -n binutils-%{version} -a1
sed -i 's/-static//g' elf2flt-%{elf2flt_date}/Makefile.in
sed -i 's@LDSCRIPTPATH="${TOOLDIR}/../lib"@LDSCRIPTPATH="${TOOLDIR}/../lib/ldscripts"@g' \
	elf2flt-%{elf2flt_date}/ld-elf2flt.in

%build
cp /usr/share/automake/config.sub .

# ldscripts won't be generated properly if SHELL is not bash...
CFLAGS="%{rpmcflags} -fno-strict-aliasing" \
LDFLAGS="%{rpmldflags}" \
CONFIG_SHELL="/bin/bash" \
./configure \
	--disable-shared \
	--disable-nls \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--mandir=%{_mandir} \
	--infodir=%{_infodir} \
	--target=%{target}

%{__make} all \
	tooldir=%{_prefix} \
	EXEEXT=""

# Build elf2lft
cd elf2flt-%{elf2flt_date}

CFLAGS="%{rpmcflags} -fno-strict-aliasing" \
LDFLAGS="%{rpmldflags}" \
./configure \
	--with-libbfd=../bfd/libbfd.a \
	--with-libiberty=../libiberty/libiberty.a \
	--with-bfd-include-dir=../bfd \
	--with-binutils-include-dir=../include \
	--target=%{target} \
	--prefix=%{_prefix}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_prefix}

%{__make} install \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	mandir=$RPM_BUILD_ROOT%{_mandir} \
	infodir=$RPM_BUILD_ROOT%{_infodir} \
	libdir=$RPM_BUILD_ROOT%{_libdir}

# remove these man pages unless we cross-build for win*/netware platforms.
# however, this should be done in Makefiles.
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/{*dlltool,*nlmconv,*windres}.1

# Install elf2flt
mv $RPM_BUILD_ROOT%{arch}/bin/ld		\
	$RPM_BUILD_ROOT%{arch}/bin/ld.real

mv $RPM_BUILD_ROOT%{_bindir}/%{target}-ld	\
	$RPM_BUILD_ROOT%{_bindir}/%{target}-ld.real

for prog in flthdr elf2flt; do
	install elf2flt-%{elf2flt_date}/$prog \
		$RPM_BUILD_ROOT%{arch}/bin/$prog
	ln $RPM_BUILD_ROOT%{arch}/bin/$prog \
		$RPM_BUILD_ROOT%{_bindir}/%{target}-$prog
done

install elf2flt-%{elf2flt_date}/ld-elf2flt	\
	$RPM_BUILD_ROOT%{arch}/bin/ld

ln $RPM_BUILD_ROOT%{arch}/bin/ld \
	$RPM_BUILD_ROOT%{_bindir}/%{target}-ld

install elf2flt-%{elf2flt_date}/elf2flt.ld	\
	$RPM_BUILD_ROOT%{arch}/lib/ldscripts/elf2flt.ld

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/%{target}-*
%dir %{arch}
%dir %{arch}/bin
%attr(755,root,root) %{arch}/bin/*
%dir %{arch}/lib
%dir %{arch}/lib/*
%{arch}/lib/ldscripts/*
%{_mandir}/man?/%{target}-*
