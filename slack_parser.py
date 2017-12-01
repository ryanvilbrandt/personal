import json, glob, pyperclip

input_dir = "inputs/channels"

for filename in glob.glob(input_dir + "/*.json"):
# for filename in ['channels\\2017-09-15.json']:
    with open(filename) as f:
        data = json.load(f)
        name = data['channel_info']['name_normalized']
        purpose = data['channel_info']['purpose']['value']
        topic = data['channel_info']['topic']['value']
        sorted_messages = sorted(data['messages'], key=lambda x: float(x['ts']))

        copied_string = ""
        if topic:
            copied_string += "Topic: " + topic + "\n"
        if purpose:
            copied_string += "Purpose: " + purpose + "\n"
        if topic or purpose:
            copied_string += "\n"
        for m in sorted_messages:
            if not "subtype" in m.keys():
                copied_string += m['text'] + "\n\n"
        copied_string = copied_string.strip("\n")

        print(name)
        print("Topic: " + topic)
        print("Purpose: " + purpose)
        names = ["Jason", "Amber", "Barry", "Astrid", "Varia", "Ephum", "Henry", "Nora"]
        print("Names found: " + ", ".join([name for name in names if name.lower() in copied_string.lower()]))
        pyperclip.copy(copied_string)
        print("Log has been copied to the clipboard.")
        print("Hit Enter to continue to the next log.")
        input()
        print("")
        print("")




