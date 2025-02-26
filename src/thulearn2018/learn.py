"""
This script provides a command-line interface (CLI) for interacting with the THU learning platform.
It includes commands for downloading course files, resetting configurations, showing configurations,
clearing records of downloaded files, submitting homework, and showing homework deadlines.

The CLI is implemented using the `click` library. 

### Methods

    **download** (_exclude, include, semester, path, download_submission_) -> _None_
    Download all course files for specified courses and semester.
    **reset** (_void_) -> _None_
    Reset configurations.
    **config** (_void_) -> _None_
    Show configurations.
    **clear** (_semester_) -> _None_
    Clear records of all downloaded files for a specified semester. The files themselves will not be deleted.
    **submit** (_name, m_) -> _None_
    Submit homework with a specified name (path) and message.
"""
# -*- coding: UTF-8 -*-

import os
import click
from . import browser

learn = browser.Learn()


@click.command(help='Download all course files')
@click.option('-e', '--exclude', default='', help='excluded courses(override)')
@click.option('-i', '--include', default='', help='included courses')
@click.option('-s', '--semester', default='',
              help='Semester id, e.g. 2023-2024-1')
@click.option('-o', '--path', default='', help='Path to save files')
@click.option('--download-submission', is_flag=True, default=False,
              help='Download submissions, used when not locally stored')
def download(exclude, include, semester, path, download_submission):
    """ Download all course files for specified courses and semester. 
    
    This method will first log in and check the specified semester, then download all course files for the specified courses.

    Args:
        exclude (str):              `exclude` parameter for `Learn.init_lessons()` method. List of lesson names to exclude with `,` as separator. If not specified, all lessons will be included.
        include (str):              `include` parameter for `Learn.init_lessons()` method. List of lesson names to include with `,` as separator. If not specified, all lessons will be included.
        semester (str):             Semester id, e.g. `2023-2024-1`.
        path (str):                 Path to save files. If not specified, the default path will be used.
        download_submission (bool): Whether to download submissions. If set, submissions will be downloaded when not locally stored.
    """
    learn.login()
    learn.set_semester(semester)
    if (path != ''):
        learn.path = path
    lessons = learn.init_lessons(exclude=exclude.split(',') if exclude else [],
                                 include=include.split(',') if include else [])
    for lesson in lessons:
        click.echo("Check " + lesson[4])
        groups = learn.get_files_id(lesson[0])
        for group in groups:
            learn.download_files(lesson[0], lesson[4], group)
        learn.download_homework(lesson[0], lesson[4], download_submission)


@click.command(help='Reset configurations.')
def reset():
    """ Reset configurations such as user and path. """
    learn.set_user()
    learn.set_path()


@click.command(help='Show configurations.')
def config():
    """ Show current configurations including username and path. """
    username, _ = learn.get_user()
    path = learn.get_path()
    print('Username: %s' % username)
    print('Path: %s' % path)


@click.command(help='Clear records of all downloaded files.')
@click.option('-s', '--semester', default='',
              help='Semester id to clear, e.g. 2023-2024-1')
def clear(semester):
    """ Clear records of all downloaded files for a specified semester.

    This method will first log in and set the specified semester, then clear all records of downloaded files. It will **not** delete the files themselves.
    
    Args:
        semester (str): Semester id to clear, e.g. `2023-2024-1`.
    """
    learn.login()
    learn.set_semester(semester)
    learn.set_local()


@click.command(help='Submit homework.')
@click.argument('name', default='')
@click.option('-m', default='', help='The message to submit')
def submit(name, m):
    """ Submit homework with a specified name and message.

    This method will first log in and set the specified semester, then submit the homework with the specified name and message.

    Args:
        name (str):     The path of the homework file to submit.
        m (str):        The message to submit.
    """
    learn.login()
    learn.set_semester()
    id_path = ".xszyid"
    if (not os.path.exists(id_path)):
        print("Homwork Id Not Found!")
        return
    if (name != '' and not os.path.exists(name)):
        print("Upload File Not Found!")
        return
    with open(id_path, 'r') as f:
        xszyid = f.read().strip()
    f.close()
    learn.upload(xszyid, name, m)


@click.command(help='Show homework deadlines.')
@click.option('-e', '--exclude', default='', help='excluded courses(override)')
@click.option('-i', '--include', default='', help='included courses')
@click.option('-s', '--semester', default='',
              help='Semester to show ddl, e.g. 2023-2024-1')
@click.option('-o', '--path', default='', help='Path to save homework files')
@click.option('--download-submission', is_flag=True, default=False,
              help='Download submissions, used when not locally stored')
def ddl(exclude, include, semester, path, download_submission):
    """ Show homework deadlines for specified courses and semester.

    This method will first log in and set the specified semester, then show the homework deadlines for the specified courses.

    Args:
        exclude (str):              `exclude` parameter for `Learn.init_lessons()` method. List of lesson names to exclude with `,` as separator. If not specified, all lessons will be included.
        include (str):              `include` parameter for `Learn.init_lessons()` method. List of lesson names to include with `,` as separator. If not specified, all lessons will be included.
        semester (str):             Semester id to show ddl, e.g. `2023-2024-1`.
        path (str):                 Path to save homework files. If not specified, the default path will be used.
        download_submission (bool): Whether to download submissions. If set, submissions will be downloaded when not locally stored.
    """
    def align(string, length=0):
        len_en = len(string)
        len_utf8 = len(string.encode('utf-8'))
        lent = len_en + (len_utf8 - len_en) // 2
        return string + ' ' * (length - lent)
    learn.login()
    learn.set_semester(semester)
    if (path != ''):
        learn.path = path
    ddls = learn.get_ddl(learn.init_lessons(
        exclude=exclude.split(',') if exclude else [],
        include=include.split(',') if include else []), download_submission)
    print('Total %d ddl(s)' % (len(ddls)))
    for ddl in ddls:
        print(align(ddl[0][0:8], 25), align(
            ddl[1][0:20], 30) + align(ddl[3][0:20], 30), ddl[4])


@click.group()
def main():
    pass


main.add_command(download)
main.add_command(reset)
main.add_command(clear)
main.add_command(submit)
main.add_command(ddl)
main.add_command(config)


if __name__ == "__main__":
    main()
