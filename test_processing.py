from processing import LabeledSection, identify_blastbeat_intervals


def test_identify_blasts_1():
    input: list[LabeledSection] = [
        LabeledSection(1,2, False, True),
        LabeledSection(2,3, True, True),
        LabeledSection(3,4, True, True),
        LabeledSection(4,5, True, True),
        LabeledSection(5,6, True, True),
        LabeledSection(6,7, True, False),
        LabeledSection(7,8, True, False)
    ]

    expected = [(2,6)]

    actual = identify_blastbeat_intervals(input)

    assert actual == expected


def test_identify_blasts_2():
    input: list[LabeledSection] = [
        LabeledSection(1,2, False, True),
        LabeledSection(2,3, True, True),
        LabeledSection(3,4, True, True),
        LabeledSection(4,5, True, False),
        LabeledSection(5,6, True, True),
        LabeledSection(6,7, True, True),
        LabeledSection(7,8, True, True),
        LabeledSection(8,9, True, False),
    ]

    expected = []

    actual = identify_blastbeat_intervals(input)

    assert actual == expected