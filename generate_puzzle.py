import json
import math

CHROMATIC_SOLFEGE = ['DO', 'DI', 'RE', 'RI', 'MI', 'FA', 'FI', 'SOL', 'SI', 'LA', 'LI', 'TI']
CHROMATIC_SCALE = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
MELODIC_INTERVALS = ['P1', 'm2', 'M2', 'm3', 'M3', 'P4', 'A4', 'P5', 'm6', 'M6', 'm7', 'M7',
                     'P8', 'm9', 'M9', 'm10', 'M10', 'P11', 'A11', 'P12', 'm13', 'M13', 'm14', 'M14', 'P15']

KEYS = []
NUM_KEYS = 88
for i in range(1, NUM_KEYS + 1):
    octave = (i + 8) // 12
    note = (i + 8) % 12
    eng_notation = CHROMATIC_SCALE[note] + str(octave)
    KEYS.append(eng_notation)


def transpose(theme, first_note):
    base_tone = 0
    if "'" in first_note:
        first_note = first_note[:-1]
        base_tone = 12
    assert first_note in CHROMATIC_SOLFEGE
    base_tone += CHROMATIC_SOLFEGE.index(first_note)
    semitone_shift_counts = [(KEYS.index(tone) - KEYS.index(theme[0])) for tone in theme]
    #semitone_intervals = [KEYS.index(melody[j + 1]) - KEYS.index(melody[j]) for j in range(len(melody) - 1)]
    #interval_notations = [f'+{MELODIC_INTERVALS[x]}' if x >= 0 else f'-{MELODIC_INTERVALS[abs(x)]}' for x in semitone_intervals]
    #print(" ".join(interval_notations))
    transposed = []
    for shift_count in semitone_shift_counts:
        solfege_index = base_tone + shift_count
        octave_modifier = ""
        while solfege_index < 0:
            octave_modifier += ","
            solfege_index += len(CHROMATIC_SCALE)
        while solfege_index >= len(CHROMATIC_SCALE):
            octave_modifier += "'"
            solfege_index -= len(CHROMATIC_SCALE)
        transposed.append(f'{CHROMATIC_SOLFEGE[solfege_index]}{octave_modifier}')
    return transposed


def simulate_turing_machines(tm_defs, dedication_to_variation):
    parsed_tms = [
        [line.strip().split('\t') for line in tm]
        for tm in tm_defs
    ]
    outputs = []

    for tm in parsed_tms:
        dedication = tm[0][0]
        tape = list(dedication)
        state, pos = '0', 0

        while state != '*':
            char = tape[pos]
            char_index = list(sorted(set(dedication))).index(char)
            instruction = tm[char_index + 1][int(state) + 1]
            state, write, direction = instruction.split(',')
            tape[pos] = write
            if direction == '>':
                pos += 1
            elif direction == '<':
                pos -= 1

        tape_extract = "".join(tape).replace("_", "")
        solfege_length = 3 if dedication_to_variation[dedication] == 'III' else 2
        slice_l = math.floor((len(tape_extract)-solfege_length)/2)
        slice_u = math.ceil((len(tape_extract)-solfege_length)/2)
        composer = tape_extract[0:slice_l] + tape_extract[len(tape_extract)-slice_u:]
        solfege_key = tape_extract[slice_l:len(tape_extract)-slice_u]
        print(dedication, "".join(tape), tape_extract, composer, solfege_key)
        outputs.append({
            "TM": tm.copy(),
            "Composer": composer,
            "Dedication": dedication,
            "SolfegeKey": solfege_key,
        })

    return outputs


def generate_puzzle(tm_defs, clues_data, dedications):
    dedication_to_variation = {v: k for (k, v) in dedications.items()}
    assert len(dedication_to_variation.items()) == 12

    outputs = simulate_turing_machines(tm_defs, dedication_to_variation)
    outputs = sorted(outputs, key=lambda x: "".join(list(sorted(set(x["Dedication"])))))
    variation_to_solfege = {}

    tables_html = []
    for output in outputs:
        solfege_key = output["SolfegeKey"]
        assert solfege_key in CHROMATIC_SOLFEGE
        dedication = output["Dedication"]
        tm_def = output["TM"]
        variation_to_solfege[dedication_to_variation[dedication]] = solfege_key
        tables_html.append(f'''<table>
                <thead>
                    <tr>
                        <th>&nbsp;</th>
                        {
                            "".join([
                                "".join(["<th>", c, "</th>"])
                                for c in tm_def[0][1:]
                            ])
                        }
                    </tr>
                </thead>
                <tbody>
                    {
                        "".join([
                            "".join(["<tr>"] + ["".join(["<td>", c, "</td>"]) for c in row] + ["</tr>"])
                            for row in tm_def[1:]
                        ])
                    }
                </tbody>
            </table>''')

    for t in tables_html:
        print(t)

    solfege_to_variation = {v: k for (k, v) in variation_to_solfege.items()}
    assert set(solfege_to_variation.keys()) == set(CHROMATIC_SOLFEGE)
    assert set(solfege_to_variation.values()) == set(dedications.keys())

    clues_html = []
    extraction_html = []

    clues_data = sorted(
        clues_data,
        key=lambda x: x['Dedication'].split(' ')[1] + x['Composer'].split(' ')[-1]
    )
    for (i, clue_item) in enumerate(clues_data):
        variations = []
        notes_html = ''
        for _note in clue_item['TransposedTheme']:
            suffix = ''
            while _note[-1] == "," or _note[-1] == "'":
                suffix += _note[-1]
                _note = _note[0:-1]
            variations.append(f'{solfege_to_variation[_note]}{suffix}')
            notes_html = "".join([f'<td class=n><div>{v}</div></td>' for v in variations])

        dedication = clue_item['Dedication']
        enumeration = list(dedication)
        index = clue_item.get("Index", dedication.index(clue_item['Extract']))
        for (j, c) in enumerate(enumeration):
            if c != ' ':
                enumeration[j] = '<span>&nbsp;_&nbsp;</span>'
            else:
                enumeration[j] = '<span>&nbsp;&nbsp;</span>'
            if j == index:
                enumeration[j] = '<span class=e>&nbsp;_&nbsp;</span>'

        clues_html.append(f'<tr>{notes_html}</tr>')
        extraction_html.append(f'<tr><td>{"".join(enumeration)}</td></tr>')

    print(f'<table class=a><tbody>{"".join(clues_html)}</tbody></table>')
    print(f'<table class=b><tbody>{"".join(extraction_html)}</tbody></table>')


if __name__ == '__main__':
    with open('_spoilers.json', 'r') as f:
        theme_data = json.loads(f.read())

    tm_data = []
    for i in range(0, 12):
        j = str(i+1)
        if len(j) == 1:
            j = f'0{j}'
        with open(f'tms/tm{j}.txt', 'r') as f:
            tm_data.append(f.readlines())

    for (i, clue) in enumerate(theme_data['clued_themes']):
        clue['TransposedTheme'] = transpose(theme=clue['Theme'], first_note=theme_data['hidden_theme'][i])
        print("-".join(clue['TransposedTheme']))

    generate_puzzle(
        tm_defs=tm_data,
        clues_data=theme_data['clued_themes'],
        dedications=theme_data['enigma_dedications']
    )
