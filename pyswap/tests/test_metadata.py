from pyswap.core.metadata import Metadata


def test_metadata():
    metadata = Metadata(
        author="Author",
        institution="Institution",
        email="email@box.com",
        project_name="Project",
        swap_ver='1.0',
        comment="Comment",
    )

    assert metadata.author == "Author"
    assert metadata.institution == "Institution"
    assert metadata.email == "email@box.com"
    assert metadata.project_name == "Project"
    assert metadata.swap_ver == '1.0'
    assert metadata.comment == "Comment"
