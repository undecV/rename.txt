def yes(string):
    # https://blog.oxforddictionaries.com/2015/10/23/ways-to-say-yes/
    yes_list = "y", "yes", "yea", "yup", "yep", "yuppers", "yeppers", "ok",\
                "affirmative", "roger", "sure", "yessir", "true", "t"
    if string.lower() in yes_list:
        return True
    else:
        return False
