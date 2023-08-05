from git_release.git_release import SemVer

def test_int():
    assert int(SemVer(1,1,1)) == 7  # binary 111
    assert int(SemVer(123,123,123)) == 2031099  # binary 1111011 1111011 1111011

def test_equalities(semver):
    assert SemVer(semver.major,semver.minor,semver.patch-1) < semver
    assert SemVer(semver.major,semver.minor-1,semver.patch) < semver
    assert SemVer(semver.major-1,semver.minor,semver.patch) < semver
    assert semver > SemVer(semver.major-1,semver.minor,semver.patch)
    assert semver > SemVer(semver.major,semver.minor-1,semver.patch)
    assert semver > SemVer(semver.major,semver.minor,semver.patch-1)
    assert semver <= SemVer(semver.major,semver.minor,semver.patch)
    assert semver >= SemVer(semver.major,semver.minor,semver.patch)
    assert semver == SemVer(semver.major,semver.minor,semver.patch)
    assert semver != SemVer(semver.major,semver.minor,semver.patch+1)

    assert semver != "string"
    assert semver != tuple()
    assert semver != dict()
