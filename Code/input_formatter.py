import json

def format_input():
    assigned_to_file_json_root_key = 'assigned_to'
    component_file_json_root_key = 'component'
    short_desc_file_json_root_key = 'short_desc'

    # Open files with proper encoding
    with open('../Dataset/JSON/assigned_to.json', 'r', encoding='utf-8') as assigned_to_file:
        assigned_to = json.load(assigned_to_file)[assigned_to_file_json_root_key]

    with open('../Dataset/JSON/component.json', 'r', encoding='utf-8') as component_file:
        component = json.load(component_file)[component_file_json_root_key]

    with open('../Dataset/JSON/short_desc.json', 'r', encoding='utf-8') as short_desc_file:
        short_desc = json.load(short_desc_file)[short_desc_file_json_root_key]

    with open("OutputFiles/formatted_input", "a", encoding='utf-8') as output_file:
        count = 1
        for bug_id, assignments in assigned_to.items():
            assignments_len = len(assignments)
            components_len = len(component[bug_id])
            short_desc_len = len(short_desc[bug_id])
            for i in range(assignments_len):
                for j in range(components_len):
                    for k in range(short_desc_len):
                        if (assignments[i]["when"] == component[bug_id][j]["when"] == short_desc[bug_id][k]["when"]
                            and assignments[i]["what"] is not None
                            and component[bug_id][j]["what"] in ("UI", "Core", "Text", "Debug", "APT", 'Doc')):
                            count += 1
                            val = (short_desc[bug_id][k]["what"] + "  " + component[bug_id][j]["what"] + " , " + assignments[i]["what"] + "\n")
                            output_file.write(val)

    # No need to manually close files when using 'with' statement

if __name__ == '__main__':
    format_input()
