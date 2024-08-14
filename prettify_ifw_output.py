#!/usr/bin/env python3
import csv
import click
import math
import sys
import json
from typing import List, Dict




def convert_to_timestamp(seconds):
    import math
    hours = math.floor(seconds / 3600)
    minutes = math.floor((seconds % 3600) / 60)
    remaining_seconds = seconds % 60
    timestamp = "{:02}:{:02}:{:04.1f}".format(hours, minutes, remaining_seconds)
    return timestamp



def parse_json(txt:str) -> Dict:
    try:
        # Parse the JSON
        json_data = json.loads(txt)
    except json.JSONDecodeError as e:
        click.echo(f"Error: Invalid JSON input. {str(e)}", err=True)
        sys.exit(1)

    return json_data


def collate(indata:Dict) -> List[dict]:
    outdata = []
    speakers = indata['speakers']
    for s in speakers:
        timestamps = s['timestamp']
        d = {'rowid': None, 'word_count': 0}
        d['duration'] = round(timestamps[1] - timestamps[0], 2)
        d['speaker'] = s['speaker']
        d['time_begin'], d['time_end'] = (convert_to_timestamp(t) for t in timestamps)
        d['text'] = s['text']
        d['start_abs_time'] = timestamps[0]
        outdata.append(d)

    return outdata




def wrangle(indata:List[dict]) -> List[dict]:

    def squeeze_segments(segments:List[dict]):
        if not segments:
            return []

        squeezes = []
        cx = segments[0]
        _ix = 0

        for i in range(1, segments.__len__()):
            if segments[i]['speaker'] == cx['speaker']:
                if cx['text'][-1] == '.':  # end of sentence
                    dw = '\n'
                else:
                    dw = ' '
                nextword = segments[i]['text'].strip()
                cx['text'] += dw + nextword
                cx['word_count'] += 1               
                cx['duration'] = round(cx['duration'] + segments[i]['duration'], 1)
                cx['time_end'] = segments[i]['time_end']
            else:
                _ix += 1
                cx['rowid'] = _ix
                squeezes.append(cx)
                cx = segments[i]

        # Append the last accumulated dict
        squeezes.append(cx)

        return squeezes

    return squeeze_segments(indata)


def produce_csv(outdata:List[dict], outfile:click.File) -> None:
    wcsv = csv.DictWriter(outfile, fieldnames=outdata[0].keys())
    wcsv.writeheader()
    wcsv.writerows(outdata)

@click.command()
@click.option('--input-file', '-i', type=click.File('r'), default='-', help="Input text file in JSON format. Reads from stdin if not provided.")
@click.option('--output-file', '-o', type=click.File('w'), default='-', help="Output file to write prettified JSON. Defaults to stdout.")
def cli_parse(input_file, output_file):
    """Process the input file or stdin and output the result to stdout."""

    input_text = input_file.read()
    data = parse_json(input_text)
    data = collate(data)
    data = wrangle(data)
    produce_csv(data, output_file)

    # # Prettify the JSON output
    # prettified_json = json.dumps(data, indent=4)




if __name__ == "__main__":
    cli_parse()







# def main():
#     data = json.loads(READ_PATH.read_text())
#     segments = []

#     for row in data['segments']:

#         d = {'rowid': None}
#         d['speaker'] = row.get('speaker') if row.get('speaker') else 'N/A'
#         d['start_time'] = convert_to_timestamp(row['start'])
#         d['duration'] = round(row['end'] - row['start'], 1)
#         d['text'] = row['text'].strip()
#         d['end_time'] =  convert_to_timestamp(row['end'])
#         words = row['words']
#         if words:
#             wscores = [w.get('score') for w in words  if w.get('score') ]
#             d['word_count'] = len(words)
#             d['avg_score'] = round(sum(wscores) / len(wscores), 3) if wscores else None
#             d['min_score'] = min(wscores) if wscores else None
#         else:
#             d['word_count'] = 0
#             d['avg_score'] = d['min_score'] = None

#         d['start_time_in_absolute_seconds'] = row['start']
#         segments.append(d)


#     print("List of segments:", len(segments))
#     # outdata = compress_speaker_texts(segments)

#     outdata = []
#     stats = {}
#     _i = 0
#     for i, d in enumerate(segments, 1):
#         d['rowid'] = i
#         if d['speaker'] == 'SPEAKER_01':
#             d['speaker'] = 'Trump'
#         elif d['speaker'] == 'SPEAKER_00':
#             d['speaker'] = 'Elon'

#         if d['speaker'] != 'N/A':
#             _i += 1
#             d['rowid'] = _i
#             outdata.append(d)

#             p = d['speaker']
#             if not stats.get(p):
#                 stats[p] = {'segments': 0, 'words': 0, 'duration': 0}
#             stats[p]['segments'] += 1
#             stats[p]['words'] += len(d['text'].split())
#             stats[p]['duration'] += round(d['duration'])


#     print("Compressed list of segments:", len(outdata))
#     print(stats)

#     with open(WRIT_PATH, 'w') as w:
#         wcsv = csv.DictWriter(w, fieldnames=outdata[0].keys())
#         wcsv.writeheader()
#         wcsv.writerows(outdata)




