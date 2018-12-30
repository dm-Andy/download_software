import json
import argparse
import os
import sys
from const import DATA_PATH


def main():

    parse = argparse.ArgumentParser(description=__doc__)

    parse.add_argument('name', help='要删除的name')

    params = parse.parse_args()

    try:
        if not os.path.exists(DATA_PATH):
            print('data.json 不存在，请先添加数据源')
            sys.exit(1)
        else:
            with open(DATA_PATH, 'r', encoding='utf-8') as f:
                local_data = json.loads(f.read())
                
                [local_data.remove(x) for x in local_data if x['name'].upper() == params.name.upper()]

            with open(DATA_PATH, 'w', encoding='utf-8') as f:
                f.write(json.dumps(local_data, indent=4, separators=(',', ':')))
        
    except Exception as ex:
        print('发生异常：%s' % ex)


if __name__ == "__main__":
    main()

