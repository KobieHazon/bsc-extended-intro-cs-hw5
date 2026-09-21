from extended_intro_hw5_cli import main


def test_det_command(capsys):
    assert main(["det", "1,2;3,4"]) == 0
    assert capsys.readouterr().out == "-2\n"


def test_intersects_command(capsys):
    assert main(["intersects", "byebyebaboonboy", "babyboy", "3"]) == 0
    assert capsys.readouterr().out == "bab\n"
