Name:           v4l-utils
Version:        1.1.0
Release:        1%{?dist}
Summary:        Utilities for video4linux and DVB devices
Group:          Applications/System
# ir-keytable and v4l2-sysfs-path are GPLv2 only
License:        GPLv2+ and GPLv2
URL:            http://www.linuxtv.org/downloads/v4l-utils/
Source0:        http://linuxtv.org/downloads/v4l-utils/v4l-utils-%{version}.tar.bz2
Source1:        qv4l2.desktop
Source2:        qv4l2.svg
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  qt4-devel libsysfs-devel kernel-headers desktop-file-utils
# For /etc/udev/rules.d ownership
Requires:       udev
Requires:       libv4l = %{version}-%{release}

%description
v4l-utils is a collection of various video4linux (V4L) and DVB utilities. The
main v4l-utils package contains cx18-ctl, ir-keytable, ivtv-ctl, v4l2-ctl and
v4l2-sysfs-path.


%package        devel-tools
Summary:        Utilities for v4l2 / DVB driver development and debugging
# decode_tm6000 is GPLv2 only
License:        GPLv2+ and GPLv2
Requires:       libv4l = %{version}-%{release}

%description    devel-tools
Utilities for v4l2 / DVB driver authors: decode_tm6000, v4l2-compliance and
v4l2-dbg.


%package -n     qv4l2
Summary:        QT v4l2 test control and streaming test application
License:        GPLv2+
Requires:       libv4l = %{version}-%{release}

%description -n qv4l2
QT v4l2 test control and streaming test application.


%package -n     libv4l
Summary:        Collection of video4linux support libraries
Group:          System Environment/Libraries
# Some of the decompression helpers are GPLv2, the rest is LGPLv2+
License:        LGPLv2+ and GPLv2
URL:            http://hansdegoede.livejournal.com/3636.html

%description -n libv4l
libv4l is a collection of libraries which adds a thin abstraction layer on
top of video4linux2 devices. The purpose of this (thin) layer is to make it
easy for application writers to support a wide variety of devices without
having to write separate code for different devices in the same class. libv4l
consists of 3 different libraries: libv4lconvert, libv4l1 and libv4l2.

libv4lconvert offers functions to convert from any (known) pixel-format
to V4l2_PIX_FMT_BGR24 or V4l2_PIX_FMT_YUV420.

libv4l1 offers the (deprecated) v4l1 API on top of v4l2 devices, independent
of the drivers for those devices supporting v4l1 compatibility (which many
v4l2 drivers do not).

libv4l2 offers the v4l2 API on top of v4l2 devices, while adding for the
application transparent libv4lconvert conversion where necessary.


%package -n     libv4l-devel
Summary:        Development files for libv4l
Group:          Development/Libraries
License:        LGPLv2+
URL:            http://hansdegoede.livejournal.com/3636.html
Requires:       libv4l = %{version}-%{release}

%description -n libv4l-devel
The libv4l-devel package contains libraries and header files for
developing applications that use libv4l.


%prep
%setup -q


%build
make %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" \
  PREFIX=%{_prefix} LIBDIR=%{_libdir}


%install
rm -rf $RPM_BUILD_ROOT
make install PREFIX=%{_prefix} LIBDIR=%{_libdir} DESTDIR=$RPM_BUILD_ROOT
# below is the desktop file and icon stuff.
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
desktop-file-install --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  %{SOURCE1}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps
install -p -m 644 %{SOURCE2} \
  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps


%clean
rm -rf $RPM_BUILD_ROOT


%post -n libv4l -p /sbin/ldconfig

%postun -n libv4l -p /sbin/ldconfig

%post -n qv4l2
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun -n qv4l2
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans -n qv4l2
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%defattr(-,root,root,-)
%doc README
%dir %{_sysconfdir}/rc_keymaps
%config(noreplace) %{_sysconfdir}/rc_keymaps/*
%config(noreplace) %{_sysconfdir}/rc_maps.cfg
%config(noreplace) %{_sysconfdir}/udev/rules.d/70-infrared.rules
%{_bindir}/cx18-ctl
%{_bindir}/ir-keytable
%{_bindir}/ivtv-ctl
%{_bindir}/v4l2-ctl
%{_bindir}/v4l2-sysfs-path
%{_mandir}/man1/ir-keytable.1*

%files devel-tools
%defattr(-,root,root,-)
%doc README
%{_bindir}/decode_tm6000
%{_bindir}/v4l2-compliance
%{_sbindir}/v4l2-dbg

%files -n qv4l2
%defattr(-,root,root,-)
%doc README
%{_bindir}/qv4l2
%{_datadir}/applications/qv4l2.desktop
%{_datadir}/icons/hicolor/scalable/apps/qv4l2.svg

%files -n libv4l
%defattr(-,root,root,-)
%doc COPYING.LIB COPYING ChangeLog README.libv4l TODO
%{_libdir}/libv4l*.so.*
%{_libdir}/libv4l

%files -n libv4l-devel
%defattr(-,root,root,-)
%doc README.lib-multi-threading
%{_includedir}/libv4l*.h
%{_libdir}/libv4l*.so
%{_libdir}/pkgconfig/libv4l*.pc


%changelog
* Thr Oct 06 2011 Mauro Carvalho Chehab <mchehab@redhat.com> 0.9.0-test
- Initial v4l-utils.spec file
