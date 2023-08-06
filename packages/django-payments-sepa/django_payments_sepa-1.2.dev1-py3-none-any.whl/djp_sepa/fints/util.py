from fints.hhd.flicker import parse, swap_bytes
from svgwrite import Drawing


# FIXME import from fints after #141 in python-fints gets merged
def code_to_bitstream(code):
    """Convert a flicker code into a bitstream in strings."""
    # Inspired by Andreas Schiermeier
    # https://git.ccc-ffm.de/?p=smartkram.git;a=blob_plain;f=chiptan/flicker/flicker.sh;h
    # =7066293b4e790c2c4c1f6cbdab703ed9976ffe1f;hb=refs/heads/master
    code = parse(code).render()
    data = swap_bytes(code)
    stream = ["10000", "00000", "11111", "01111", "11111", "01111", "11111"]
    for c in data:
        v = int(c, 16)
        stream.append("1" + str(v & 1) + str((v & 2) >> 1) + str((v & 4) >> 2) + str((v & 8) >> 3))
        stream.append("0" + str(v & 1) + str((v & 2) >> 1) + str((v & 4) >> 2) + str((v & 8) >> 3))
    return stream


def flicker_svg(code, frame_duration=0.1, bar_width=3, space_width=1, bar_height=9):
    """Render an HHD (optical chipTAN) flicke rcode as SVG."""
    css = """
        .background { fill: black }
        .bar { fill: white }
    """
    stream = code_to_bitstream(code)

    svg = Drawing(filename="flickercode.svg")

    # The viewbox defines the user unit; we choose it in multiple of
    # our space width and bar width
    vb_width = 6 * space_width + 5 * bar_width
    vb_height = 2 * space_width + bar_height
    svg.viewbox(0, 0, vb_width, vb_height)

    # Add CSS for styling (colours)
    svg.defs.add(svg.style(css))

    # Draw full-size background
    svg.add(svg.rect(size=("100%", "100%"), class_="background"))

    # Generate rects for flicker bars
    bars = []
    for i in range(5):
        x = (i + 1) * space_width + i * bar_width
        y = space_width
        bars.append(svg.rect(insert=(x, y), size=(bar_width, bar_height), class_="bar"))

    # Generate animations for bars
    n_frames = len(stream)
    for f, frame in enumerate(stream):
        for i, bit in enumerate(frame):
            bars[i].add(
                svg.set(
                    id_=f"anim_{i}_{f}",
                    begin=f"0s;anim_{i}_{n_frames-1}.end" if f == 0 else f"anim_{i}_{f-1}.end",
                    dur=str(frame_duration),
                    attributeName="display",
                    to="inline" if bit == "1" else "none",
                )
            )

    # Add bars to drawing
    for bar in bars:
        svg.add(bar)

    return svg.tostring()
