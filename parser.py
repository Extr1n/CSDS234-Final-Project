# This file parses the txt file into a json file

import json
import re

def parse_block(lines):
    """Parse one record block into a dict, capturing indented notes."""
    record = {}
    i = 0
    while i < len(lines):
        raw = lines[i]
        line = raw.strip()
        # Key: Value lines
        if ':' in line:
            key, rest = map(str.strip, line.split(':', 1))
            # Scalar fields
            if key in ('Id', 'ASIN', 'title', 'group', 'salesrank'):
                record[key] = int(rest) if key in ('Id', 'salesrank') else rest
                i += 1

            # similar: count + list
            elif key == 'similar':
                parts = rest.split()
                record['similar'] = parts[1:]
                i += 1

            # categories: N lines follow
            elif key == 'categories':
                num = int(rest)
                cats = []
                for j in range(1, num+1):
                    parts = lines[i+j].strip().lstrip('|').split('|')
                    cats.append(parts)
                record['categories'] = cats
                i += num + 1

            # reviews: header + N review‐lines
            elif key == 'reviews':
                header_parts = re.split(r'\s{2,}', rest)
                hdr = {}
                for part in header_parts:
                    k,v = map(str.strip, part.split(':',1))
                    hdr[k.replace(' ', '_')] = int(v)
                record['reviews_summary'] = hdr

                total = hdr.get('total', 0)
                revs = []
                for j in range(1, total+1):
                    fields = re.split(r'\s{2,}', lines[i+j].strip())
                    r = {'date': fields[0]}
                    for f in fields[1:]:
                        kk,vv = map(str.strip, f.split(':',1))
                        if vv != "":
                            r[kk] = int(vv) if kk in ('rating','votes','helpful') else vv
                        else:
                            r[kk] = vv
                    revs.append(r)
                record['reviews'] = revs
                i += total + 1

            else:
                # unknown key → raw
                record[key] = rest
                i += 1

        # Indented lines with no “Key:” → treat as a note
        elif raw.startswith('  ') and ':' not in line:
            record.setdefault('notes', []).append(line)
            i += 1

        else:
            # skip anything else
            i += 1

    return record

def parse_file_to_json(in_path, out_path):
    with open(in_path, 'r', encoding='utf-8') as f:
        text = f.read().strip()
    blocks = [b.splitlines() for b in re.split(r'\n\s*\n', text)]
    records = [parse_block(b) for b in blocks if b]
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(records, f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    parse_file_to_json('data/amazon-meta.txt', 'output.json')
    print("Wrote parsed JSON to output.json")

