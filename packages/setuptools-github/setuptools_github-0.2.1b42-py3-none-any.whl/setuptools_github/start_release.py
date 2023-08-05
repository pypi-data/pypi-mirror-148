import logging
import re

import pygit2  # type: ignore

from setuptools_github import tools


log = logging.getLogger(__name__)


def newversion(version, mode):
    newver = [int(n) for n in version.split(".")]
    if mode == "major":
        newver[-3] += 1
        newver[-2] = 0
        newver[-1] = 0
    elif mode == "minor":
        newver[-2] += 1
        newver[-1] = 0
    else:
        newver[-1] += 1
    return ".".join(str(v) for v in newver)


def extract_beta_branches(branches, remote=None):
    result = set()
    for branch in branches:
        match = branch.partition("/")[0]
        if remote and remote != match:
            continue
        if re.search(r"beta/\d+([.]\d+)*", branch):
            result.add(branch)
    return result


def repo_checks(repo, remote, error, dryrun, force, curver, mode):

    # check repo has a single remote
    remotes = {remote.name for remote in repo.remotes}
    if len(remotes) > 1 and not remote:
        (log.error if dryrun else error)(
            f"multiple remotes defined: {', '.join(remotes)}"
        )
    if remote and remote not in remotes:
        error(f"requested remote={remote} but found {', '.join(remotes)}")
        (log.error if dryrun else error)(
            f"user select remote={remote} but only found {', '.join(remotes)}"
        )
    remote = remote or (remotes or [None]).pop()
    log.debug("current remote '%s'", remote)

    # check we are on master
    current = repo.head.shorthand
    log.debug("current branch %s", current)
    if current != "master":
        (log.error if dryrun else error)(
            f"current branch is '{current}' but this script runs on the 'master' branch"
        )

    # check we have no uncommitted changes
    def ignore(f):
        return (f & pygit2.GIT_STATUS_WT_NEW) or (f & pygit2.GIT_STATUS_IGNORED)

    modified = {p for p, f in repo.status().items() if not ignore(f)}
    if modified:
        (log.error if (dryrun or force) else error)(
            "local modification staged for commit, use -f|--force to skip check"
        )

    # check the current version has a beta/<curver> branch
    remote_branches = extract_beta_branches(repo.branches.remote, remote=remote)
    local_branches = extract_beta_branches(repo.branches.local)

    if not any(remote_branches | local_branches):
        # no beta/X.Y.Z branches, we start fresh
        return curver

    is_in_local = bool([b for b in local_branches if b.endswith(f"beta/{curver}")])
    is_in_remote = bool([b for b in remote_branches if b.endswith(f"beta/{curver}")])
    if not (is_in_local or is_in_remote):
        (log.error if (dryrun or force) else error)(
            f"cannot find 'beta/{curver}' branch in the local or remote branches"
        )

    newver = newversion(curver, mode)
    is_in_local = bool([b for b in local_branches if b.endswith(f"beta/{newver}")])
    is_in_remote = bool([b for b in remote_branches if b.endswith(f"beta/{newver}")])
    if is_in_local:
        (log.error if (dryrun or force) else error)(
            f"found 'beta/{newver}' branch in the local branches"
        )
    if is_in_remote:
        (log.error if (dryrun or force) else error)(
            f"found 'beta/{newver}' branch in the remote branches"
        )

    return newver


def parse_args(args=None):
    from pathlib import Path
    from argparse import (
        ArgumentParser,
        ArgumentDefaultsHelpFormatter,
        RawDescriptionHelpFormatter,
    )

    class F(ArgumentDefaultsHelpFormatter, RawDescriptionHelpFormatter):
        pass

    parser = ArgumentParser(formatter_class=F, description=__doc__)

    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-f", "--force", action="store_true")
    parser.add_argument("-n", "--dry-run", dest="dryrun", action="store_true")
    parser.add_argument("--remote", help="use remote")
    parser.add_argument("--no-checks", action="store_true")

    parser.add_argument(
        "-w",
        "--workdir",
        help="git working dir",
        default=Path("."),
        type=Path,
    )
    parser.add_argument("mode", choices=["micro", "minor", "major"])
    parser.add_argument("initfile", metavar="__init__.py", type=Path)

    options = parser.parse_args(args)

    options.checks = not options.no_checks
    options.error = parser.error

    logging.basicConfig(
        format="%(levelname)s:%(name)s:(dry-run) %(message)s"
        if options.dryrun
        else "%(levelname)s:%(name)s:%(message)s",
        level=logging.DEBUG if options.verbose else logging.INFO,
    )

    for d in ["verbose", "no_checks"]:
        delattr(options, d)
    return options.__dict__


def run(mode, initfile, workdir, force, dryrun, error, checks, remote):
    workdir = workdir.resolve()
    log.debug("using working dir %s", workdir)

    # get the current version from initfile
    curver = tools.set_module_var(initfile, "__version__", None)[0]
    if not curver:
        error(f"cannot find __version__ in {initfile}")
    log.info("current version '%s'", curver)

    repo = pygit2.Repository(workdir)

    # various checks and generate the new version / branch name
    newver = repo_checks(repo, remote, error, dryrun, force, curver, mode)
    newbranch = f"beta/{newver}"
    if newver == curver:
        log.info(
            "creating first version branch '%s' (v. %s) from 'master'",
            newbranch,
            newver,
        )
    else:
        log.info(
            "creating new version branch '%s' (v. %s) from 'master' (%s)",
            newbranch,
            newver,
            curver,
        )

    # modify the __init__
    log.info("updating init file %s (%s -> %s)", initfile, curver, newver)
    if not dryrun:
        tools.set_module_var(initfile, "__version__", newver)

    # commit the updated __init__.py in the master branch
    msg = f"beta release {newver}"
    log.info("committing '%s'%s", msg, " (skip)" if dryrun else "")
    if not dryrun:
        refname = repo.head.name
        author = repo.default_signature
        commiter = repo.default_signature
        parent = repo.revparse_single(repo.head.shorthand).hex
        relpath = initfile.absolute().relative_to(workdir)
        repo.index.add(str(relpath).replace("\\", "/"))
        repo.index.write()
        tree = repo.index.write_tree()
        oid = repo.create_commit(refname, author, commiter, msg, tree, [parent])
        log.info("created oid %s", oid)

    log.info("switching to new branch '%s'%s", newbranch, " (skip)" if dryrun else "")
    if not dryrun:
        commit = repo.revparse_single(repo.head.shorthand)
        repo.branches.local.create(newbranch, commit)
        ref = repo.lookup_reference(repo.lookup_branch(newbranch).name)
        repo.checkout(ref)

    return newbranch


def main():
    return run(**parse_args())


if __name__ == "__main__":
    main()
