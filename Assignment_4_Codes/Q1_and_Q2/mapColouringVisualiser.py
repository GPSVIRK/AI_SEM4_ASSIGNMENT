import xml.etree.ElementTree as ET
import json


def apply_color(elem, color):
    style = elem.attrib.get("style")

    if style:
        parts = style.split(";")
        new_parts = []
        found = False

        for p in parts:
            p = p.strip()
            if p.startswith("fill:"):
                new_parts.append(f"fill:{color}")
                found = True
            else:
                new_parts.append(p)

        if not found:
            new_parts.append(f"fill:{color}")

        elem.set("style", ";".join(new_parts))
    else:
        elem.set("fill", color)


# ---------------------------
# ---------------------------
def color_australia(svg_path, output_path, data, color_map):
    tree = ET.parse(svg_path)
    root = tree.getroot()

    for elem in root.iter():
        tag = elem.tag.split("}")[-1]

        # CASE 1: direct path (like Western Australia)
        if tag == "path":
            region_id = elem.attrib.get("id")
            if region_id in data:
                apply_color(elem, color_map[data[region_id]])

        # CASE 2: grouped regions (like Northern Territory)
        if tag == "g":
            group_id = elem.attrib.get("id")

            if group_id in data:
                color = color_map[data[group_id]]

                for child in elem.iter():
                    child_tag = child.tag.split("}")[-1]
                    if child_tag == "path":
                        apply_color(child, color)

    tree.write(output_path)


# ---------------------------
# 📍 TELANGANA (DIRECT PATH)
# ---------------------------
def color_telangana(svg_path, output_path, data, color_map):
    tree = ET.parse(svg_path)
    root = tree.getroot()

    for elem in root.iter():
        tag = elem.tag.split("}")[-1]

        if tag != "path":
            continue

        region_id = elem.attrib.get("id")

        if region_id in data:
            apply_color(elem, color_map[data[region_id]])

    tree.write(output_path)


# ---------------------------
# RUN
# ---------------------------
with open("result.json") as f:
    full_data = json.load(f)

color_map = {
    1: "#ff0000",
    2: "#00ff00",
    3: "#0000ff",
    4: "#ffff00",
    5: "#ff00ff",
    6: "#00ffff",
}

color_australia(
    "images/Australia.svg",
    "Australia_out.svg",
    full_data["aus"],
    color_map
)

color_telangana(
    "images/Telangana.svg",
    "Telangana_out.svg",
    full_data["tel"],
    color_map
)
