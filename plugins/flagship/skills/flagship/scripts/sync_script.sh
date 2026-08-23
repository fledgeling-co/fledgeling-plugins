#!/bin/zsh
# Sync a flagship script to the repo copy ATOMICALLY.
#
# `cp` writes THROUGH the inode a running process may be mid-read of, so a live
# watcher resumes into the middle of the new bytes and dies on a parse error --
# measured tonight, and it produced a task marked failed over a mechanism that
# had already succeeded. `mv` swaps the directory entry instead: the running
# process keeps reading the old inode to completion, and the next start gets the
# new file.
set -u
src="${1:?src}"; dst="${2:?dst}"
tmp="${dst}.new.$$"
cat "$src" > "$tmp" && chmod --reference="$src" "$tmp" 2>/dev/null || chmod +x "$tmp"
mv -f "$tmp" "$dst"
print -r -- "synced atomically: $dst"
