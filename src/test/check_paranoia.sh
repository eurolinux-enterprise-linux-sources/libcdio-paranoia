#!/bin/sh
# Compare our cd-paranoia with known good results.

if test ! -d "$abs_top_builddir" ; then
  abs_top_builddir=/src/external-vcs/libcdio-paranoia
fi

if test ! -d "$abs_top_srcdir" ; then
  abs_top_srcdir=/src/external-vcs/libcdio-paranoia
fi

cue_file=$abs_top_srcdir/test/data/cdda.cue

if test "/usr/bin/cmp" != no ; then
  cd_paranoia=$abs_top_builddir/src/cd-paranoia 
  $cd_paranoia -d $cue_file -v -r -- "1-"
  if test $? -ne 0 ; then
    exit 6
  fi
  cdda1_file=$abs_top_builddir/test/cdda-1.raw
  cdda2_file=$abs_top_builddir/test/cdda-2.raw
  dd bs=16 if=$abs_top_builddir/test/cdda.raw of=$cdda1_file
  dd bs=16 if=$abs_top_srcdir/test/data/cdda.bin of=$cdda2_file
  if /usr/bin/cmp $cdda1_file $cdda2_file ; then
    echo "** Raw cdda.bin extraction okay"
  else
    echo "** Raw cdda.bin extraction differ"
    exit 3
  fi
  mv cdda.raw cdda-good.raw
  $cd_paranoia -d $cue_file -x 64 -v -r -- "1-"
  mv cdda.raw cdda-underrun.raw
  $cd_paranoia -d $cue_file -r -- "1-"
  if test $? -ne 0 ; then
    exit 6
  fi
  if /usr/bin/cmp cdda-underrun.raw cdda-good.raw ; then
    echo "** Under-run correction okay"
  else
    echo "** Under-run correction problem"
    exit 3
  fi
  # Start out with small jitter
  $cd_paranoia -l ./cd-paranoia.log -d $cue_file -x 5 -v -r -- "1-"
  if test $? -ne 0 ; then
    exit 6
  fi
  mv cdda.raw cdda-jitter.raw
  if /usr/bin/cmp cdda-jitter.raw cdda-good.raw ; then
    echo "** Small jitter correction okay"
  else
    echo "** Small jitter correction problem"
    exit 3
  fi
  tail -3 ./cd-paranoia.log | sed -e's/\[.*\]/\[\]/' > ./cd-paranoia-filtered.log
  if /usr/bin/cmp $abs_top_srcdir/test/cd-paranoia-log.right ./cd-paranoia-filtered.log ; then
    echo "** --log option okay"
    rm ./cd-paranoia.log ./cd-paranoia-filtered.log
  else
    echo "** --log option problem"
    exit 4
  fi
  # A more massive set of failures: underrun + small jitter
  $cd_paranoia -d $cue_file -x 69 -v -r -- "1-"
  if test $? -ne 0 ; then
    exit 6
  fi
  mv cdda.raw cdda-jitter.raw
  if /usr/bin/cmp cdda-jitter.raw cdda-good.raw ; then
    echo "** under-run + jitter correction okay"
  else
    echo "** under-run + jitter correction problem"
    exit 3
  fi
  ### FIXME: medium jitter is known to fail. Investigate.
  ### FIXME: large jitter is known to fail. Investigate.
  exit 0
else 
  if test "/usr/bin/cmp" != no ; then
    echo "Don't see 'cmp' program. Test skipped."
  else  
    echo "Don't see libcdio 'cd-paranoia' program. Test skipped."
  fi
  exit 77
fi
fi
#;;; Local Variables: ***
#;;; mode:shell-script ***
#;;; eval: (sh-set-shell "bash") ***
#;;; End: ***

