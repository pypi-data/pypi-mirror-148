#!/usr/bin/python
import argparse
import logging
from pprint import pformat

from gitlab import Gitlab
from .__version__ import __version__


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')


def create_branch(project, args):
    logging.info(
        f'create branch[{args.branch}] for {project.web_url} from {args.ref}')
    project.branches.create({'branch': args.branch, 'ref': args.ref})


def delete_branch(project, args):
    logging.info(f'delete branch[{args.branch}] from {project.web_url}')
    project.branches.delete(args.branch)


def list_branch(project, args):
    logging.info(f'list branches of {project.web_url}')
    logging.info('\n' + pformat({b.name: b.commit['id']
                                 for b in project.branches.list()}))


def protect_branch(project, args):
    logging.info(f'protect branch[{args.branch}] of {project.web_url}')
    project.branches.get(args.branch).protect()


def unprotect_branch(project, args):
    logging.info(f'unprotect branch[{args.branch}] of {project.web_url}')
    project.branches.get(args.branch).unprotect()


def main():
    com_opts = argparse.ArgumentParser(add_help=False)
    com_opts.add_argument(
        "-u", "--url", required=True, help="url of gitlab")
    com_opts.add_argument("-t", '--token', help='token of gitlab account')
    com_opts.add_argument(
        '-g', '--group', action='append', dest='groups',
        metavar='GROUP', type=int, help='group id')
    com_opts.add_argument(
        '-p', '--project', action='append', dest='projects',
        metavar='PROJECT', default=[], type=int, help='project id')
    branch_opts = argparse.ArgumentParser(add_help=False)
    branch_opts.add_argument(
        '-b', '--branch', required=True, help='branch name')

    parser = argparse.ArgumentParser(
        description='manage branch for gitlab project')
    parser.add_argument(
        '-V', '--version', action='version', version=__version__)

    sub_parser = parser.add_subparsers(
        required=True, dest='sub-command', description="the following commands are supported")
    create_parser = sub_parser.add_parser(
        "create", parents=[com_opts, branch_opts], help='create branch')
    create_parser.add_argument(
        '-r', '--ref', help='ref of branch, default: %(default)s',
        default='master')
    create_parser.set_defaults(func=create_branch)

    delete_parser = sub_parser.add_parser(
        "delete", parents=[com_opts, branch_opts], help='delete branch')
    delete_parser.set_defaults(func=delete_branch)

    list_parser = sub_parser.add_parser(
        "list", parents=[com_opts], help='list branch')
    list_parser.set_defaults(func=list_branch)

    protect_parser = sub_parser.add_parser(
        "protect", parents=[com_opts, branch_opts], help='protect branch')
    protect_parser.set_defaults(func=protect_branch)

    unprotect_parser = sub_parser.add_parser(
        "unprotect", parents=[com_opts, branch_opts], help='unprotect branch')
    unprotect_parser.set_defaults(func=unprotect_branch)
    args = parser.parse_args()

    gl = Gitlab(args.url, args.token)

    if args.groups:
        for group in args.groups:
            group = gl.groups.get(group)
            args.projects.extend(p.id for p in group.projects.list(
                all=True) if p.id not in args.projects)
    for project in args.projects:
        try:
            args.func(gl.projects.get(project), args)
        except Exception as e:
            logging.warning(e)


if __name__ == '__main__':
    main()
