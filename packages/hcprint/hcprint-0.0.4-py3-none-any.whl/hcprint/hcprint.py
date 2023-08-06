import regex as re

def hcprint(text):

    """
    Example Text:

    <red>This somewhat depends on what platform you are on.</>
    The most common way to do this is <blue>by printing ANSI escape sequences.</> For a simple example
    """

    result = text

    search_param = r"<\w+>[^<>]*</\w+>"
    matches = list(re.findall(search_param, text))

    for m in matches:
        result = result.replace(m, get_colored_chunk_from_match(m))

    print(result)

def get_colored_chunk_from_match(match):
    chunk = str(match)

    color_map = {
        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "lightgray": "\033[37m",
        "darkgray": "\033[90m",
        "lightred": "\033[91m",
        "lightgreen": "\033[92m",
        "lightyellow": "\033[93m",
        "lightblue": "\033[94m",
        "lightmagenta": "\033[95m",
        "lightcyan": "\033[96m",
        "white": "\033[97m"
    } # + ;1m

    for color, code in color_map.items():

        code_header = "<{}>".format(color)
        code_end = "</{}>".format(color)

        if code_header in match:
            chunk = chunk.replace(code_header, "")
            chunk = chunk.replace(code_end, "")

            color_code = code

            return color_code + chunk + '\033[0m'

if __name__ == "__main__":
    text = """
    Example Text:

    <red>This somewhat depends on what platform you are on.</red>
    The most <yellow>common</yellow> way to do this is <blue>by printing ANSI escape sequences.</blue> 
    For a simple example, see this color map:

    <black>black</black>
    <red>red</red>
    <green>green</green>
    <yellow>yellow</yellow>
    <blue>blue</blue>
    <magenta>magenta</magenta>
    <cyan>cyan</cyan>
    <lightgray>lightgray</lightgray>
    <darkgray>darkgray</darkgray>
    <lightred>lightred</lightred>
    <lightgreen>lightgreen</lightgreen>
    <lightyellow>lightyellow</lightyellow>
    <lightblue>lightblue</lightblue>
    <lightmagenta>lightmagenta</lightmagenta>
    <lightcyan>lightcyan</lightcyan>
    <white>white</white>
    """

    # text = "<green>TASIN IS REALLY COOL</green> Also: <blue>Ethan is cool i guess</blue>"

    hcprint(text)