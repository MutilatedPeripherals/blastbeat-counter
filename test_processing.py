from processing import LabeledSection, identify_hammer_blast, identify_traditional_blast


def test_identify_blasts_1():
    input: list[LabeledSection] = [
        LabeledSection(1, 2, False, True),
        LabeledSection(2, 3, True, True),
        LabeledSection(3, 4, True, True),
        LabeledSection(4, 5, True, True),
        LabeledSection(5, 6, True, True),
        LabeledSection(6, 7, True, True),
        LabeledSection(7, 8, True, True),
        LabeledSection(8, 9, True, True),
        LabeledSection(9, 10, True, True),
        LabeledSection(10, 11, False, False),
    ]
    expected = [(2, 10)]
    actual = identify_hammer_blast(input)

    assert actual == expected


def test_identify_blasts_2():
    input: list[LabeledSection] = [
        LabeledSection(1, 2, True, True),
        LabeledSection(2, 3, True, True),
        LabeledSection(3, 4, True, True),
        LabeledSection(4, 5, True, True),
        LabeledSection(5, 6, True, False),
        LabeledSection(6, 7, True, True),
        LabeledSection(7, 8, True, True),
        LabeledSection(8, 9, True, True),
    ]
    expected = []
    actual = identify_hammer_blast(input)

    assert actual == expected


def test_traditional_blast():
    input: list[LabeledSection] = [
        LabeledSection(1, 2, bass_drum_present=False, snare_present=False),
        LabeledSection(2, 3, bass_drum_present=True, snare_present=False),
        LabeledSection(3, 4, bass_drum_present=False, snare_present=True),
        LabeledSection(4, 5, bass_drum_present=True, snare_present=False),
        LabeledSection(5, 6, bass_drum_present=False, snare_present=True),
        LabeledSection(6, 7, bass_drum_present=False, snare_present=False),
        LabeledSection(7, 8, bass_drum_present=False, snare_present=False),
        LabeledSection(8, 9, bass_drum_present=False, snare_present=False),
    ]

    expected = [(2, 6)]

    actual = identify_traditional_blast(input)

    assert actual == expected
