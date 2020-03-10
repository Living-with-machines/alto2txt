import argparse
from pathlib import Path

from tqdm import tqdm

from extract_text import xml_to_text_entry

"""
def remove_service(in_dir):
    for f in Path(in_dir).rglob('*.xml'):
        p = Path(f).absolute()
        xml_dir = p.parents[0]
        check for sub directories in folder containing xml
       # if len([f for f in xml_dir.iterdir() if f.is_dir()]) != 0:
       #     raise Exception()
        parent_dir = p.parents[1]
        # check for non 'service' directories
        if not xml_dir.name == 'service':
            print xml_dir.absolute()
            raise Exception('Unexpected folder structure')
         
        else:
            p.rename(parent_dir / p.name)
   for f in Path(in_dir).rglob('service'):
        try:
            f.rmdir()
            """


def remove_service(in_dir):
    for d in Path(in_dir).rglob('service'):
        for f in Path(d).rglob('*.xml'):
            p = Path(f).absolute()
            xml_dir = p.parents[0]
            parent_dir = p.parents[1]
            p.rename(parent_dir / p.name)
    # remove service directory
    for f in Path(in_dir).rglob('service'):
            f.rmdir()

def main():
    parser = argparse.ArgumentParser(description='Process JISC data')
    parser.add_argument('xml_in_dir',
                        type=str,
                        help='Input directory with XML publications')
    parser.add_argument('out_dir', type=str, help='output_dir')
    args = parser.parse_args()
    xml_in_dir = args.xml_in_dir
    out_dir = args.out_dir
    if not Path(xml_in_dir).is_dir():
        raise ValueError("""You didn't provide a valid input directory""")
    remove_service(xml_in_dir)
    issue_paths = []
    #issue_paths = set()
    for d in Path(xml_in_dir).rglob('18??'):
        issue_path = str(Path(d).parents[0])
        issue_paths.append(issue_path)
      #  issue_paths.update(issue_path)
    issue_paths = set(issue_paths)
    for issue_path in issue_paths:
        print('converting...')
        print(issue_path)
        xml_to_text_entry.xml_publications_to_text(issue_path, out_dir, 
        process_type='multi',)


if __name__ == "__main__":
    main()