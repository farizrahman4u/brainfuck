def syntax_check(code):
    br_count = 0
    br = None
    for i, x in enumerate(code):
        if x == '[':
            br = i
            br_count += 1
        elif x == ']':
            if br_count:
                br_count -= 1
            else:
                raise Exception("Unbalanced ] at position " + str(i) + " (0 based index).")
    if br_count:
        raise Exception("Unbalanced [ at position " + str(br) + " (0 based index).")
