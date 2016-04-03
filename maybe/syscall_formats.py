# maybe - see what a program does before deciding whether you really want it to happen
#
# Copyright (c) 2016 Philipp Emanuel Weidmann <pew@worldwidemann.com>
#
# Nemo vir est qui mundum non reddat meliorem.
#
# Released under the terms of the GNU General Public License, version 3
# (https://gnu.org/licenses/gpl.html)


from pwd import getpwuid
from grp import getgrgid
from os.path import abspath, dirname, basename, exists
from os import O_WRONLY, O_RDWR, O_APPEND, O_CREAT, O_TRUNC
from stat import S_IFCHR, S_IFBLK, S_IFIFO, S_IFSOCK

from .utilities import T, format_permissions


def format_delete(path):
    return "%s %s" % (T.red(_("delete")), T.underline(abspath(path)))


def format_move(path_old, path_new):
    path_old = abspath(path_old)
    path_new = abspath(path_new)
    if dirname(path_old) == dirname(path_new):
        label = _("rename")
        path_new = basename(path_new)
    else:
        label = _("move")
    return _("%s %s to %s") % (T.green(label), T.underline(path_old), T.underline(path_new))


def format_change_permissions(path, permissions):
    return _("%s of %s to %s") % (T.yellow(_("change permissions")), T.underline(abspath(path)),
                               T.bold(format_permissions(permissions)))


def format_change_owner(path, owner, group):
    if owner == -1:
        label = _("change group")
        owner = getgrgid(group)[0]
    elif group == -1:
        label = _("change owner")
        owner = getpwuid(owner)[0]
    else:
        label = _("change owner")
        owner = getpwuid(owner)[0] + ":" + getgrgid(group)[0]
    return _("%s of %s to %s") % (T.yellow(label), T.underline(abspath(path)), T.bold(owner))


def format_create_directory(path):
    return "%s %s" % (T.cyan(_("create directory")), T.underline(abspath(path)))


def format_create_link(path_source, path_target, symbolic):
    label = _("create symbolic link") if symbolic else _("create hard link")
    return _("%s from %s to %s") % (T.cyan(label), T.underline(abspath(path_source)), T.underline(abspath(path_target)))


# Start with a large number to avoid collisions with other FDs
# TODO: This approach is extremely brittle!
next_file_descriptor = 1000
file_descriptors = {}


def get_next_file_descriptor():
    global next_file_descriptor
    file_descriptor = next_file_descriptor
    next_file_descriptor += 1
    return file_descriptor


def get_file_descriptor_path(file_descriptor):
    return file_descriptors.get(file_descriptor, "/dev/fd/%d" % file_descriptor)


allowed_files = set(["/dev/null", "/dev/zero", "/dev/tty"])


def format_open(path, flags):
    path = abspath(path)
    if path in allowed_files:
        return None
    elif (flags & O_CREAT) and not exists(path):
        return "%s %s" % (T.cyan(_("create file")), T.underline(path))
    elif (flags & O_TRUNC) and exists(path):
        return "%s %s" % (T.red(_("truncate file")), T.underline(path))
    else:
        return None


def substitute_open(path, flags):
    path = abspath(path)
    if path in allowed_files:
        return None
    elif (flags & O_WRONLY) or (flags & O_RDWR) or (flags & O_APPEND) or (format_open(path, flags) is not None):
        # File might be written to later, so we need to track the file descriptor
        file_descriptor = get_next_file_descriptor()
        file_descriptors[file_descriptor] = path
        return file_descriptor
    else:
        return None


def format_mknod(path, type):
    path = abspath(path)
    if exists(path):
        return None
    elif (type & S_IFCHR):
        label = _("create character special file")
    elif (type & S_IFBLK):
        label = _("create block special file")
    elif (type & S_IFIFO):
        label = _("create named pipe")
    elif (type & S_IFSOCK):
        label = _("create socket")
    else:
        # mknod(2): "Zero file type is equivalent to type S_IFREG"
        label = _("create file")
    return "%s %s" % (T.cyan(label), T.underline(path))


def substitute_mknod(path, type):
    return None if (format_mknod(path, type) is None) else 0


def format_write(file_descriptor, byte_count):
    if file_descriptor in file_descriptors:
        path = file_descriptors[file_descriptor]
        return _("%s %s to %s") % (T.red(_("write")), T.bold(_("%d bytes") % byte_count), T.underline(path))
    else:
        return None


def substitute_write(file_descriptor, byte_count):
    return None if (format_write(file_descriptor, byte_count) is None) else byte_count


def substitute_dup(file_descriptor_old, file_descriptor_new=None):
    if file_descriptor_old in file_descriptors:
        if file_descriptor_new is None:
            file_descriptor_new = get_next_file_descriptor()
        # Copy tracked file descriptor
        file_descriptors[file_descriptor_new] = file_descriptors[file_descriptor_old]
        return file_descriptor_new
    else:
        return None


