def write_fimi(context, path):
    output_file = open(path, "w")

    for o in context.objects:
        intent = context.get_object_intent(o)
        for a in intent:
            output_file.write('%s ' % a)
        output_file.write('\n')

    output_file.close()
