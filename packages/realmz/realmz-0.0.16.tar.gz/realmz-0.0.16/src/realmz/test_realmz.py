from .factory                                import GetInput


def test_birthday_wishes():

    resp = GetInput('1', crontab='Y').get_input_redirect()
    assert resp == '1'

    return resp


def test_anniversary_wishes():

    resp = GetInput('2', crontab='Y').get_input_redirect()
    assert resp == '2'

    return resp
