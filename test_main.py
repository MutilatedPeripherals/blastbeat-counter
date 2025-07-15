from main import identify_blasts


def test_identify_blasts_1():
    input: list[tuple[tuple[int, int], bool, bool]] = [
        ((1,2), False,True),
        ((2,3), True,True),
        ((3,4), True,True),
        ((4,5), True,True),
        ((5,6), True,True),
        ((6,7), True,False),
        ((7,8), True,False),
    ]

    expected = [(2,6)]

    actual = identify_blasts(input)

    assert actual==expected



def test_identify_blasts_2():
    input: list[tuple[tuple[int, int], bool, bool]] = [
        ((1,2), False,True),
        ((2,3), True,True),
        ((3,4), True,True),
        ((4,5), True,False),
        ((5,6), True,True),
        ((6,7), True,True),
        ((7,8), True,True),
        ((8,9), True,False),
    ]

    expected = []

    actual = identify_blasts(input)

    assert actual==expected
