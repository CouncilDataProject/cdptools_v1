def body_name_shortener(bodies):
    names = []
    for body in bodies:
        n_one = body["BodyName"].lower()
        n = body["BodyDescription"].split('/')

        try:
            n_two = n[n.index("committees") + 1]
            n_two = n_two.replace("-", " ").lower()
        except ValueError:
            n_two = n_one

        name = n_one if len(n_one) <= len(n_two) else n_two
        names.append(name)

    return names
