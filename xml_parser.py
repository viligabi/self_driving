import glob, os
import xml.etree.ElementTree as ET

classes_name = ["car", "pedestrian", "cyclist", "motor"]
classes_num = {
    "car": 0,
    "pedestrian": 1,
    "cyclist": 2,
    "motor": 3
}

YOLO_ROOT = os.path.abspath('./')
DATA_PATH = os.path.join(YOLO_ROOT, 'data','frames')
OUTPUT_PATH = os.path.join(YOLO_ROOT, 'data','objects.txt')


def parse_xml(xml_file):
    """
    Parse xml file for classes and coordinates
    Args
        xml_file: str, location of xml file
    Returns
        image_path: str
        labels:     list of [xmin,ymin,xmax,ymax, class]
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()
    image_path = ''
    labels = []

    for item in root:
        if item.tag == 'filename':
            image_path = os.path.join(DATA_PATH, item.text)
        elif item.tag == 'object':
            obj_name = item[0].text
            obj_num = classes_num[obj_name]
            xmin = int(item[4][0].text)
            ymin = int(item[4][1].text)
            xmax = int(item[4][2].text)
            ymax = int(item[4][3].text)
            labels.append([xmin, ymin, xmax, ymax, obj_num])

    return image_path, labels


def convert_to_string(image_path, labels):
    """convert image_path, labels to string
    Returns:
      string
    """
    out_string = ''
    out_string += image_path
    for label in labels:
        for i in label:
            out_string += ' ' + str(i)
    out_string += '\n'
    return out_string


def main():
    out_file = open(OUTPUT_PATH, 'w')

    xml_list = glob.glob(os.path.join(DATA_PATH, "*.xml"))

    for xml in xml_list:
        try:
            image_path, labels = parse_xml(xml)
            record = convert_to_string(image_path, labels)
            out_file.write(record)
        except Exception:
            pass

    out_file.close()


if __name__ == '__main__':
    main()
