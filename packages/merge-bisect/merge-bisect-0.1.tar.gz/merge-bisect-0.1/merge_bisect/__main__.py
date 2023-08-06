#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import datetime
import subprocess
import sys
import typing
from collections import OrderedDict
from contextlib import contextmanager


class Call:
    def __init__(self, cmd: typing.List[str]):
        self._p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = self._p.communicate()
        self.stdout, self.stderr = stdout.decode(), stderr.decode()
        self.returncode = self._p.returncode

    def __bool__(self) -> bool:
        return self.returncode == 0


class Commit:
    DELIMITER = "\t"
    LOG_FORMAT = f"%at{DELIMITER}%H{DELIMITER}%an{DELIMITER}%s"

    def __init__(self, date: str, sha1: str, author: str, description: str):
        self.datetime = datetime.datetime.fromtimestamp(int(date))
        self.sha1 = sha1
        self.author = author
        self.description = description

    @classmethod
    def from_log(cls, s: str) -> "Commit":
        return cls(*s.split(cls.DELIMITER))

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} "{self.datetime}" {self.sha1} "{self.author}" "{self.description}">'

    def __hash__(self) -> int:
        return hash(self.sha1)

    def __eq__(self, other) -> bool:
        return self.sha1 == other.sha1


def commits_for_n_days(days: int) -> typing.List[Commit]:
    since = (datetime.datetime.utcnow() - datetime.timedelta(days=days)).strftime(
        "%Y-%m-%d"
    )
    cmd = [
        "git",
        "log",
        "--first-parent",
        f"--pretty=format:{Commit.LOG_FORMAT}",
        f"--since={since}",
    ]
    return [Commit.from_log(i) for i in Call(cmd).stdout.splitlines() if i]


def current_branch() -> str:
    branch = Call(["git", "rev-parse", "--abbrev-ref", "HEAD"]).stdout.strip()
    # already checkout to particular commit
    if branch == "HEAD":
        return Call(["git", "rev-parse", "HEAD"]).stdout.strip()
    return branch


def checkout(sha1: str) -> None:
    Call(["git", "checkout", sha1])


@contextmanager
def stay_on_branch() -> typing.Generator:
    branch = current_branch()
    try:
        yield
    finally:
        checkout(branch)


def call_on_commit(
    cmd: typing.List[str], commit: Commit, verbose: bool = False
) -> Call:
    checkout(commit.sha1)
    c = Call(cmd)

    if verbose:
        print("\n" * 2)

    if c:
        print(f"PASSED: {commit!r}")
    else:
        print(f"FAILED: {commit!r}")

    if verbose:
        print("=" * 150)
        print(c.stdout)
        print(c.stderr)
        print("=" * 150)
        print("\n" * 3)

    return c


parser = argparse.ArgumentParser(description="Like git bisect, but on merge commits.")

parser.add_argument(
    "cmd",
    action="extend",
    nargs=argparse.REMAINDER,
    help="Command to run in order to find whether the commit is good or bad. ",
)
parser.add_argument(
    "--days",
    type=int,
    default=30,
    help="Check merge commits only going this many days "
    "in the past against the given command.",
)
parser.add_argument(
    "-v",
    "--verbose",
    dest="verbose",
    action="store_true",
    default=False,
    help="Print stdout while running each command.",
)


def bisect():
    args = parser.parse_args()

    with stay_on_branch():
        all_commits: OrderedDict[Commit, typing.Optional[bool]] = OrderedDict(
            (i, None) for i in reversed(commits_for_n_days(args.days))
        )
        commits = list(all_commits.keys())

        print(f"Found {len(commits)} commits")
        print("")

        if len(commits) < 2:
            print(
                "At least 2 merge commits must be present in order to bisect on merges",
                file=sys.stderr,
            )
            return 1

        commit = commits[0]
        commits.remove(commit)
        commit_call = call_on_commit(args.cmd, commit, args.verbose)
        all_commits[commit] = bool(commit_call)
        if not commit_call:
            print(
                f"Earliest commit {commit!r} already fails running {' '.join(args.cmd)!r}. "
                "At least one passing commit should be succeeding in the resultset to do bisect."
            )
            return 1

        commit = commits[-1]
        commits.remove(commit)
        commit_call = call_on_commit(args.cmd, commit, args.verbose)
        all_commits[commit] = bool(commit_call)
        if commit_call:
            print(
                f"Latest commit {commit!r} already succeeds running {' '.join(args.cmd)!r}. "
                "At least one passing commit should be failing in the resultset to do bisect."
            )
            return 1

        while commits:
            middle = len(commits) // 2
            commit = commits[middle]
            commit_call = call_on_commit(args.cmd, commit, args.verbose)
            all_commits[commit] = bool(commit_call)

            if commit_call:
                for c in commits[:middle]:
                    all_commits[c] = bool(commit_call)
                commits = commits[middle + 1 :]

            else:
                for c in commits[middle + 1 :]:
                    all_commits[c] = bool(commit_call)
                commits = commits[:middle]

        bad_commit = next(
            commit for commit, is_good in all_commits.items() if not is_good
        )

        print("")
        print("Done")

        print("")
        print("Commit log (last commit first):")
        for commit, is_good in reversed(all_commits.items()):
            t = "SUCCESS" if is_good else "FAILURE"
            print(f"{t}: {commit!r}")

        print()
        print(f"BAD COMMIT: {bad_commit!r}")

    return 0


def main():
    exit(bisect())


if __name__ == "__main__":
    main()
